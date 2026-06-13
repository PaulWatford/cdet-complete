"""cdet_gui.py (v184) -- a thin visual front-end over the cdet CLI.

`cdet gui` starts a small stdlib http server and opens a single-page console. Every card is a real `cdet` subcommand;
its controls are that subcommand's actual flags (a slider for a number, a dropdown for a choice). Pressing Run executes
the real command -- `python3 cdet.py <subcommand> <flags>` -- and shows its real output. The GUI computes NOTHING itself:
it is exactly what you would type at the terminal, with sliders instead of typing numbers. Same math, same commands, same
results; only the input is friendlier. No new dependencies (Python stdlib). Frozen reference engine untouched.
"""
import json
import os
import re
import subprocess
import sys
import urllib.parse
from http.server import BaseHTTPRequestHandler, HTTPServer

ROOT = None  # the package root (where cdet.py lives); set by serve()

# ----------------------------------------------------------------------------------------------------------------------
# allow-list: subcommand -> {flag: caster}. The GUI may only invoke these, with these flags. argv is built as a list
# (never a shell string), and every value is cast/validated, so there is no shell and no injection. This mirrors the CLI
# one-to-one; the GUI adds no parameters the command line does not already have.
# ----------------------------------------------------------------------------------------------------------------------
_NUM = {int, float}
_TARGETS = {"addition-pole", "eos", "double-occ", "self-energy", "connected-det"}
_VARS = {"L", "mu", "U", "beta", "N"}
_FORMATS = {"csv", "json", "hdf5"}

ALLOW = {
    "validate": {}, "converge": {}, "connected": {}, "crosscheck": {}, "info": {}, "bench": {},
    "eos": {"--N": int, "--U": float, "--K": int},
    "docc": {"--N": int, "--U": float, "--K": int},
    "chi": {"--N": int, "--U": float},
    "resum": {"--N": int, "--U": float, "--K": int},
    "wall": {"--beta": float, "--mu": float},
    "tide": {"--beta": float, "--mu": float},
    "primes": {"--beta": float, "--mu": float},
    "twist": {"--beta": float, "--mu": float},
    "trueradius": {"--beta": float, "--mu": float},
    "run": {"--L": int, "--beta": float, "--beta-hi": float, "--bstep": float, "--K": int, "--NT": int},
    "sweep": {"--target": str, "--var": str, "--values": str},
    "export": {"--format": str},
    "diagmc": {"--system": str, "--beta": float, "--mu": float, "--U": float, "--nmax": int, "--samples": int},
}
_ANSI = re.compile(r"\x1b\[[0-9;]*m")


def run_cmd(cmd, params, timeout=300):
    """Run `cdet <cmd> <flags>` exactly as the CLI would, and return its real output."""
    spec = ALLOW.get(cmd)
    if spec is None:
        return {"error": f"unknown command: {cmd}"}
    argv = [sys.executable, "cdet.py", cmd]
    for flag, cast in spec.items():
        key = flag.lstrip("-")
        if key not in params or params[key] == "":
            continue
        val = params[key]
        if cast in _NUM:
            try:
                num = float(val); num = int(num) if cast is int else num
            except ValueError:
                return {"error": f"{flag} expects a number"}
            argv += [flag, str(num)]
        elif flag == "--values":                      # space/comma list of numbers
            nums = [x for x in re.split(r"[ ,]+", str(val)) if x]
            try:
                [float(x) for x in nums]
            except ValueError:
                return {"error": "values must be numbers, e.g. 6 12 24"}
            if nums:
                argv += [flag] + nums
        elif flag == "--target" and val in _TARGETS:
            argv += [flag, val]
        elif flag == "--var" and val in _VARS:
            argv += [flag, val]
        elif flag == "--format" and val in _FORMATS:
            argv += [flag, val]
        elif flag == "--system" and val in ("atom", "2site"):
            argv += [flag, val]
        # unknown string values are simply ignored (cannot inject)
    pretty = "cdet " + " ".join(argv[2:])
    try:
        r = subprocess.run(argv, cwd=ROOT, capture_output=True, text=True, timeout=timeout)
    except subprocess.TimeoutExpired:
        return {"command": pretty, "output": f"(still running after {timeout}s -- try smaller settings)", "ok": False}
    out = _ANSI.sub("", r.stdout or "")
    if r.returncode != 0 and r.stderr:
        out += "\n" + _ANSI.sub("", r.stderr)
    return {"command": pretty, "output": out.strip() or "(no output)", "ok": r.returncode == 0}


# ----- a small in-session memory of explicit runs ---------------------------------------------------------------------
_RECENT = []


def _record(cmd, params, data):
    rec = {"card": cmd, "params": {k: v for k, v in params.items()}, "command": data.get("command", "cdet " + cmd),
           "ok": data.get("ok", True)}
    if _RECENT and _RECENT[0]["command"] == rec["command"]:
        _RECENT[0] = rec
        return
    _RECENT.insert(0, rec)
    del _RECENT[8:]


# ----------------------------------------------------------------------------------------------------------------------
PAGE = r"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>cdet console</title>
<style>
:root{
  --bg:#0e1318;--panel:#161e27;--panel2:#1d2733;--line:#28333f;--ink:#e6edf3;--muted:#8593a2;
  --teal:#4fd1c5;--teal-dim:#2b6f69;--amber:#e8a44c;--amber-dim:#7a5a2c;
  --mono:ui-monospace,"JetBrains Mono","SF Mono",Menlo,Consolas,monospace;
  --ui:system-ui,-apple-system,"Segoe UI",Roboto,sans-serif;}
*{box-sizing:border-box}html,body{margin:0}
body{background:var(--bg);color:var(--ink);font-family:var(--ui);font-size:14px;line-height:1.45}
header{display:flex;align-items:baseline;gap:14px;padding:18px 22px;border-bottom:1px solid var(--line)}
header h1{font-family:var(--mono);font-size:15px;font-weight:600;letter-spacing:.06em;margin:0}
header h1 .d{color:var(--teal)} header .sub{color:var(--muted);font-size:12.5px}
header .stat{margin-left:18px;font-family:var(--mono);font-size:12px;color:var(--muted)}
.ask{margin-left:auto;font-family:var(--mono);font-size:12px;color:var(--teal);background:transparent;
  border:1px solid var(--teal-dim);border-radius:6px;padding:6px 14px;cursor:pointer}
.ask:hover{background:var(--teal-dim);color:var(--ink)} .ask.on{background:var(--teal);color:var(--bg)}
.assistant{position:fixed;top:0;right:0;width:360px;max-width:88vw;height:100vh;background:var(--panel);
  border-left:1px solid var(--line);display:flex;flex-direction:column;z-index:50;box-shadow:-12px 0 30px rgba(0,0,0,.35)}
.assistant[hidden]{display:none}
.ahead{display:flex;align-items:center;justify-content:space-between;padding:16px 18px;border-bottom:1px solid var(--line);
  font-family:var(--mono);font-size:12px;letter-spacing:.12em;text-transform:uppercase;color:var(--muted)}
.aclose{background:transparent;border:none;color:var(--muted);font-size:20px;cursor:pointer;line-height:1}
.aclose:hover{color:var(--ink)}
.amsgs{flex:1;overflow-y:auto;padding:16px 16px 8px;display:flex;flex-direction:column;gap:12px}
.msg{font-size:13px;line-height:1.5;max-width:92%}
.msg.user{align-self:flex-end;background:var(--teal-dim);color:var(--ink);border-radius:10px 10px 2px 10px;padding:8px 12px}
.msg.bot{align-self:flex-start;color:var(--ink)}
.msg.bot .body{background:var(--panel2);border:1px solid var(--line);border-radius:10px 10px 10px 2px;padding:10px 13px;white-space:pre-wrap}
.msg.bot .body strong{color:var(--teal)} .msg.bot code{font-family:var(--mono)}
.msg .cmds{display:flex;flex-wrap:wrap;gap:6px;margin-top:8px}
.msg .cmds button{font-family:var(--mono);font-size:11px;color:var(--muted);background:var(--panel);
  border:1px solid var(--line);border-radius:14px;padding:4px 10px;cursor:pointer}
.msg .cmds button:hover{color:var(--ink);border-color:var(--teal-dim)}
.msg .sugg{display:flex;flex-wrap:wrap;gap:6px;margin-top:8px}
.msg .sugg button{font-family:var(--ui);font-size:11.5px;color:var(--teal);background:transparent;
  border:1px solid var(--teal-dim);border-radius:14px;padding:4px 11px;cursor:pointer}
.msg .sugg button:hover{background:var(--teal-dim);color:var(--ink)}
.ain{display:flex;gap:8px;padding:12px 14px;border-top:1px solid var(--line)}
.ain input{flex:1;background:var(--panel2);color:var(--ink);border:1px solid var(--line);border-radius:7px;
  padding:9px 12px;font-family:var(--ui);font-size:13px;outline:none}
.ain input:focus{border-color:var(--teal-dim)}
.ain button{font-family:var(--mono);font-size:12px;color:var(--bg);background:var(--teal);border:none;border-radius:7px;padding:9px 14px;cursor:pointer}
.main{padding:18px 22px 40px}
.note{color:var(--muted);font-size:12.5px;margin:0 0 16px;max-width:70ch}
.note code{font-family:var(--mono);color:var(--ink)}
.recent{display:flex;align-items:center;gap:8px;margin:0 0 16px;overflow-x:auto;padding-bottom:4px}
.recent .lab{font-family:var(--mono);font-size:10px;letter-spacing:.14em;text-transform:uppercase;color:var(--muted);flex-shrink:0}
.chip{flex-shrink:0;display:flex;align-items:baseline;gap:7px;background:var(--panel);border:1px solid var(--line);
  border-radius:20px;padding:5px 12px;cursor:pointer;font-family:var(--mono);font-size:11px;color:var(--muted);white-space:nowrap}
.chip:hover{border-color:var(--teal-dim);color:var(--ink)} .chip.bad{border-color:var(--amber-dim)}
.recent .clr{margin-left:auto;flex-shrink:0;background:transparent;border:none;color:var(--muted);font-family:var(--mono);font-size:11px;cursor:pointer;text-decoration:underline}
.recent .clr:hover{color:var(--ink)}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(330px,1fr));gap:14px}
.card{background:var(--panel);border:1px solid var(--line);border-radius:9px;padding:15px 16px 14px;display:flex;flex-direction:column}
.card .top{display:flex;align-items:baseline;justify-content:space-between;gap:8px;margin-bottom:4px}
.card h3{margin:0;font-size:13.5px;font-weight:600}
.card .cmd{font-family:var(--mono);font-size:10.5px;color:var(--muted)}
.controls{display:flex;flex-direction:column;gap:9px;margin:10px 0 4px}
.ctl{display:grid;grid-template-columns:64px 1fr 54px;align-items:center;gap:10px}
.ctl label{font-family:var(--mono);font-size:11.5px;color:var(--muted)}
.ctl .v{font-family:var(--mono);font-size:12.5px;color:var(--teal);text-align:right}
.card.threshold .ctl .v{color:var(--amber)}
.ctl input[type=range]{-webkit-appearance:none;width:100%;height:3px;background:var(--line);border-radius:2px;outline:none}
.ctl input[type=range]::-webkit-slider-thumb{-webkit-appearance:none;width:13px;height:13px;border-radius:50%;background:var(--teal);border:2px solid var(--bg);cursor:pointer}
.ctl input[type=range]::-moz-range-thumb{width:13px;height:13px;border-radius:50%;background:var(--teal);border:2px solid var(--bg);cursor:pointer}
.card.threshold .ctl input[type=range]::-webkit-slider-thumb{background:var(--amber)}
.ctl select,.ctl input[type=text]{grid-column:2/4;background:var(--panel2);color:var(--ink);border:1px solid var(--line);
  border-radius:5px;padding:5px 8px;font-family:var(--mono);font-size:12px}
.actions{display:flex;gap:8px;align-items:center;margin-top:12px}
.run{font-family:var(--mono);font-size:12px;color:var(--bg);background:var(--teal);border:none;border-radius:6px;
  padding:7px 16px;cursor:pointer;letter-spacing:.03em}
.run:hover{filter:brightness(1.08)} .run.busy{background:var(--teal-dim);color:var(--ink)}
.card.threshold .run{background:var(--amber)} .card.threshold .run.busy{background:var(--amber-dim)}
.copy{font-family:var(--mono);font-size:10.5px;color:var(--muted);background:transparent;border:1px solid var(--line);border-radius:5px;padding:6px 10px;cursor:pointer}
.copy:hover{color:var(--ink)} .copy.ok{color:var(--teal);border-color:var(--teal-dim)}
.cli{font-family:var(--mono);font-size:11px;color:var(--muted);margin-top:10px;overflow-x:auto;white-space:nowrap}
.out{font-family:var(--mono);font-size:11.5px;color:var(--ink);background:#0b1014;border:1px solid var(--line);
  border-radius:6px;margin-top:11px;padding:10px 12px;max-height:300px;overflow:auto;white-space:pre;line-height:1.35;display:none}
.out.show{display:block} .out.bad{border-color:var(--amber-dim)}
@media(max-width:560px){.ctl{grid-template-columns:56px 1fr 48px}}
</style></head><body>
<header><h1><span class="d">cdet</span> console</h1>
  <span class="sub">every card runs the real CLI command &mdash; sliders just fill in the numbers</span>
  <button class="ask" id="askToggle">assistant</button>
  <span class="stat" id="stat">ready</span></header>
<aside class="assistant" id="assistant" hidden>
  <div class="ahead"><span>assistant</span><button class="aclose" id="askClose">&times;</button></div>
  <div class="amsgs" id="amsgs"></div>
  <div class="ain"><input type="text" id="aq" placeholder="ask: how do I start? what is the wall?" autocomplete="off">
    <button id="asend">send</button></div>
</aside>
<div class="main">
  <p class="note">This is a front-end over the command line. Each card runs <code>cdet &lt;command&gt;</code> with the
  flags you set and shows its actual output &mdash; identical to typing it in a terminal. Move a slider to choose a number
  (lattice size, &beta;, U&hellip;), pick from a dropdown for a choice, then Run. The <code>copy</code> button gives you
  the exact command.</p>
  <div class="recent" id="recent" hidden></div>
  <div class="grid" id="grid"></div>
</div>
<script>
const R=(f,min,max,step,def,lab)=>({f,lab:lab||f,t:"range",min,max,step,def});
const SEL=(f,opts,def,lab)=>({f,lab:lab||f,t:"select",opts,def});
const TXT=(f,def,lab)=>({f,lab:lab||f,t:"text",def});
const CARDS=[
 {id:"validate",  title:"Validate (5 gates)",      cmd:"validate",  ctrls:[]},
 {id:"converge",  title:"Converge (TD limit)",     cmd:"converge",  ctrls:[]},
 {id:"connected", title:"Connected determinant",   cmd:"connected", ctrls:[]},
 {id:"crosscheck",title:"Cross-check models",      cmd:"crosscheck",ctrls:[]},
 {id:"bench",     title:"Benchmark suite",         cmd:"bench",     ctrls:[]},
 {id:"diagmc",    title:"DiagMC sampler (sign wall)",cmd:"diagmc",thr:true,ctrls:[SEL("system",["atom","2site"],"atom"),R("beta",0.5,8,0.5,2),R("mu",-3,3,0.1,0.5),R("U",0,3,0.1,1),R("nmax",2,6,1,4),R("samples",2000,30000,2000,10000)]},
 {id:"eos",       title:"Equation of state",       cmd:"eos",   ctrls:[R("N",2,8,1,4),R("U",0,4,0.1,1),R("K",4,14,1,10)]},
 {id:"docc",      title:"Double occupancy",        cmd:"docc",  ctrls:[R("N",2,8,1,2),R("U",0,4,0.1,1),R("K",4,14,1,10)]},
 {id:"chi",       title:"Susceptibilities",        cmd:"chi",   ctrls:[R("N",2,8,1,2),R("U",0,4,0.1,1)]},
 {id:"resum",     title:"Resummation",             cmd:"resum", ctrls:[R("N",2,8,1,4),R("U",0,4,0.1,1),R("K",4,14,1,10)]},
 {id:"wall",      title:"Convergence wall",        cmd:"wall",  thr:true, ctrls:[R("beta",0.5,10,0.5,5),R("mu",-3,3,0.1,0)]},
 {id:"tide",      title:"Wall tide",               cmd:"tide",  ctrls:[R("beta",0.5,10,0.5,5),R("mu",-3,3,0.1,0)]},
 {id:"primes",    title:"Prime sieve",             cmd:"primes",ctrls:[R("beta",0.5,10,0.5,5),R("mu",-3,3,0.1,-0.6)]},
 {id:"twist",     title:"Twist / supercells",      cmd:"twist", ctrls:[R("beta",0.5,10,0.5,5),R("mu",-3,3,0.1,-0.6)]},
 {id:"trueradius",title:"True radius",             cmd:"trueradius",thr:true,ctrls:[R("beta",0.5,10,0.5,2),R("mu",-3,3,0.1,0.5)]},
 {id:"run",       title:"Hybrid grid run",         cmd:"run",   ctrls:[R("L",4,64,2,6,"L"),R("beta",1,40,1,30,"beta"),R("beta-hi",1,50,1,36,"beta-hi"),R("bstep",1,10,1,6),R("K",2,8,1,4),R("NT",100,3000,100,800)]},
 {id:"sweep",     title:"Parameter sweep",         cmd:"sweep", ctrls:[SEL("target",["addition-pole","eos","double-occ","self-energy","connected-det"],"addition-pole"),SEL("var",["L","mu","U","beta","N"],"L"),TXT("values","6 12 24")]},
 {id:"export",    title:"Export data",             cmd:"export",ctrls:[SEL("format",["csv","json","hdf5"],"csv")]},
];
const CMAP=Object.fromEntries(CARDS.map(c=>[c.id,c]));
function vals(c){const o={};c.ctrls.forEach(ct=>{const el=document.getElementById(`ctl-${c.id}-${ct.f}`);if(el)o[ct.f]=el.value;});return o;}
function cmdline(c){const v=vals(c);let s="cdet "+c.cmd;c.ctrls.forEach(ct=>{if(v[ct.f]!==undefined&&v[ct.f]!=="")s+=` --${ct.f} ${v[ct.f]}`;});return s;}
function render(){
  const g=document.getElementById("grid");
  CARDS.forEach(c=>{
    const el=document.createElement("div");el.className="card"+(c.thr?" threshold":"");
    let ctrls=c.ctrls.map(ct=>{
      if(ct.t==="range")return `<div class="ctl"><label>${ct.lab}</label><input type="range" id="ctl-${c.id}-${ct.f}" min="${ct.min}" max="${ct.max}" step="${ct.step}" value="${ct.def}"><span class="v" id="val-${c.id}-${ct.f}">${ct.def}</span></div>`;
      if(ct.t==="select")return `<div class="ctl"><label>${ct.lab}</label><select id="ctl-${c.id}-${ct.f}">${ct.opts.map(o=>`<option${o===ct.def?" selected":""}>${o}</option>`).join("")}</select></div>`;
      return `<div class="ctl"><label>${ct.lab}</label><input type="text" id="ctl-${c.id}-${ct.f}" value="${ct.def}"></div>`;
    }).join("");
    el.innerHTML=`<div class="top"><h3>${c.title}</h3><span class="cmd">${c.cmd}</span></div>
      ${ctrls?`<div class="controls">${ctrls}</div>`:""}
      <div class="actions"><button class="run" id="bt-${c.id}">Run</button>
        <button class="copy" id="cp-${c.id}">copy</button></div>
      <div class="cli" id="cl-${c.id}"></div>
      <pre class="out" id="out-${c.id}"></pre>`;
    g.appendChild(el);
    c.ctrls.forEach(ct=>{const el2=document.getElementById(`ctl-${c.id}-${ct.f}`);
      if(ct.t==="range")el2.addEventListener("input",()=>{document.getElementById(`val-${c.id}-${ct.f}`).textContent=el2.value;sync(c);});
      else el2.addEventListener("input",()=>sync(c));});
    document.getElementById("bt-"+c.id).addEventListener("click",()=>runCard(c));
    document.getElementById("cp-"+c.id).addEventListener("click",()=>copyCli(c));
    sync(c);
  });
}
function sync(c){document.getElementById("cl-"+c.id).textContent=cmdline(c);}
async function copyCli(c){const cmd=cmdline(c),b=document.getElementById("cp-"+c.id);
  try{await navigator.clipboard.writeText(cmd);}catch(e){const t=document.createElement("textarea");t.value=cmd;document.body.appendChild(t);t.select();try{document.execCommand("copy");}catch(_){}t.remove();}
  const o=b.textContent;b.textContent="copied";b.classList.add("ok");setTimeout(()=>{b.textContent=o;b.classList.remove("ok");},1100);}
async function runCard(c){
  const bt=document.getElementById("bt-"+c.id);bt.classList.add("busy");bt.textContent="\u2026";
  document.getElementById("stat").textContent="running  "+cmdline(c);
  const out=document.getElementById("out-"+c.id);
  try{
    const qs=new URLSearchParams(Object.assign({cmd:c.cmd,log:"1"},vals(c))).toString();
    const r=await fetch("/api/run?"+qs);const d=await r.json();
    out.classList.add("show");out.classList.toggle("bad",d.ok===false);
    out.textContent=d.error?("error: "+d.error):(d.output||"(no output)");
    refreshRecent();
  }catch(e){out.classList.add("show","bad");out.textContent="error: "+e;}
  bt.classList.remove("busy");bt.textContent="Run";document.getElementById("stat").textContent="ready";
}
async function refreshRecent(){try{const r=await fetch("/api/_recent");renderRecent(await r.json());}catch(e){}}
function renderRecent(list){
  const box=document.getElementById("recent");
  if(!list||!list.length){box.hidden=true;box.innerHTML="";return;}
  box.hidden=false;let html=`<span class="lab">recent</span>`;
  list.forEach((rec,i)=>{html+=`<button class="chip${rec.ok===false?" bad":""}" data-i="${i}">${rec.command}</button>`;});
  html+=`<button class="clr" id="clrRecent">clear</button>`;box.innerHTML=html;
  list.forEach((rec,i)=>box.querySelector(`[data-i="${i}"]`).addEventListener("click",()=>restore(rec)));
  document.getElementById("clrRecent").addEventListener("click",async()=>{await fetch("/api/_clear");refreshRecent();});
}
function restore(rec){
  const c=CMAP[rec.card];if(!c)return;
  Object.entries(rec.params||{}).forEach(([f,v])=>{const el=document.getElementById(`ctl-${c.id}-${f}`);
    if(el){el.value=v;const lab=document.getElementById(`val-${c.id}-${f}`);if(lab)lab.textContent=v;}});
  sync(c);runCard(c);
}
function mdToHtml(t){const esc=t.replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;");
  return esc.replace(/\*\*(.+?)\*\*/g,"<strong>$1</strong>");}
function addMsg(role,text,cmds,suggestions){
  const m=document.getElementById("amsgs");const d=document.createElement("div");d.className="msg "+role;
  if(role==="bot"){
    d.innerHTML='<div class="body">'+mdToHtml(text)+'</div>';
    if(cmds&&cmds.length){const cd=document.createElement("div");cd.className="cmds";
      cmds.forEach(c=>{const b=document.createElement("button");b.textContent=c;
        b.addEventListener("click",async()=>{try{await navigator.clipboard.writeText(c);}catch(e){}
          const o=b.textContent;b.textContent="copied";setTimeout(()=>b.textContent=o,900);});
        cd.appendChild(b);});d.appendChild(cd);}
    if(suggestions&&suggestions.length){const sd=document.createElement("div");sd.className="sugg";
      suggestions.forEach(s=>{const b=document.createElement("button");b.textContent=s;
        b.addEventListener("click",()=>ask(s));sd.appendChild(b);});d.appendChild(sd);}
  }else{d.textContent=text;}
  m.appendChild(d);m.scrollTop=m.scrollHeight;
}
let _lastTopic=null;
async function ask(q){if(!q.trim())return;addMsg("user",q);
  try{const u="/api/assist?q="+encodeURIComponent(q)+(_lastTopic?"&ctx="+encodeURIComponent(_lastTopic):"");
    const r=await fetch(u);const d=await r.json();_lastTopic=d.topic||null;
    addMsg("bot",d.reply||"(no answer)",d.commands||[],d.suggestions||[]);}
  catch(e){addMsg("bot","(couldn't reach the assistant)");}}
const _panel=document.getElementById("assistant"),_tgl=document.getElementById("askToggle");
function toggleAsk(open){const show=open===undefined?_panel.hidden:open;_panel.hidden=!show;_tgl.classList.toggle("on",show);
  if(show&&!document.getElementById("amsgs").children.length){
    addMsg("bot","Hi! I'm the cdet assistant \u2014 offline and rule-based. Ask what a command does, what a concept means, or an intent like \u201chow do I start?\u201d or \u201cstudy the wall\u201d. I work alongside the docs; I won't run anything for you.",["cdet validate","cdet info"],["how do I start?","what is the sign problem?","study the wall"]);}
  if(show)document.getElementById("aq").focus();}
_tgl.addEventListener("click",()=>toggleAsk());
document.getElementById("askClose").addEventListener("click",()=>toggleAsk(false));
document.getElementById("asend").addEventListener("click",()=>{const q=document.getElementById("aq");ask(q.value);q.value="";});
document.getElementById("aq").addEventListener("keydown",e=>{if(e.key==="Enter"){const q=document.getElementById("aq");ask(q.value);q.value="";}});
render();refreshRecent();
</script></body></html>"""


class _Handler(BaseHTTPRequestHandler):
    def _send(self, code, body, ctype):
        b = body.encode() if isinstance(body, str) else body
        self.send_response(code); self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(b))); self.end_headers(); self.wfile.write(b)

    def do_GET(self):
        u = urllib.parse.urlparse(self.path)
        if u.path in ("/", "/index.html"):
            return self._send(200, PAGE, "text/html; charset=utf-8")
        if u.path == "/api/_recent":
            return self._send(200, json.dumps(_RECENT), "application/json")
        if u.path == "/api/_clear":
            _RECENT.clear(); return self._send(200, json.dumps(_RECENT), "application/json")
        if u.path == "/api/assist":
            q = {k: v[0] for k, v in urllib.parse.parse_qs(u.query).items()}
            try:
                import cdet_assistant
                return self._send(200, json.dumps(cdet_assistant.respond(q.get("q", ""), q.get("ctx") or None)), "application/json")
            except Exception as e:
                return self._send(200, json.dumps({"reply": f"(assistant error: {e})", "commands": []}), "application/json")
        if u.path == "/api/run":
            q = {k: v[0] for k, v in urllib.parse.parse_qs(u.query).items()}
            cmd = q.pop("cmd", ""); log = q.pop("log", None)
            try:
                data = run_cmd(cmd, q)
                if log and not data.get("error"):
                    _record(cmd, q, data)
                return self._send(200, json.dumps(data), "application/json")
            except Exception as e:
                return self._send(200, json.dumps({"error": str(e)}), "application/json")
        return self._send(404, "not found", "text/plain")

    def log_message(self, *a):
        pass


def serve(root, port=8765, open_browser=True):
    global ROOT
    ROOT = root
    requested, httpd = port, None
    for p in range(requested, requested + 10):           # the old server may still be bound; find the next free port
        try:
            httpd = HTTPServer(("127.0.0.1", p), _Handler); port = p; break
        except OSError:
            continue
    if httpd is None:
        print(f"could not start: ports {requested}-{requested + 9} are all in use. The cdet console may already be "
              f"running at http://127.0.0.1:{requested}/ -- open that, or rerun with `cdet gui --port <N>`.")
        return
    if port != requested:
        print(f"port {requested} was busy (the console may already be running there); using port {port} instead.")
    url = f"http://127.0.0.1:{port}/"
    print(f"cdet console at {url}   (Ctrl-C to stop)")
    if open_browser:
        try:
            import webbrowser, threading
            threading.Timer(0.6, lambda: webbrowser.open(url)).start()
        except Exception:
            pass
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nstopped."); httpd.server_close()


if __name__ == "__main__":
    serve(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), open_browser=False)

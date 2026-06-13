# CROSSCHECK_v185 — an optional, self-contained help assistant

**Claims.** (1) cdet_assistant.py is a rule-based knowledge graph (21 commands, 9 concepts, 6 workflows), NOT an LLM:
offline, no downloads, instant. (2) toggle-on panel in the GUI, hidden by default; /api/assist endpoint. (3) answers
intents/commands/concepts with clickable command chips; complements the docs; runs nothing. (4) GUI still a pure wrapper;
no physics in the assistant. Frozen engine untouched.

**Reproduce.**
```
cd 08_2d_interacting && PYTHONPATH=. python3 cdet_assistant.py     # 10-query self-test
python3 ../cdet.py gui --no-browser
curl "http://127.0.0.1:8765/api/assist?q=how+do+I+start"           # -> getting-started steps + chips
```

**Frozen engine.** Untouched: `cd engine && make CC=gcc test` → 194/194; constants bit-identical
(−0.5082750022348369  0.44040518398732875).

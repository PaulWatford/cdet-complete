/* cdet_stable_engine.c (v109) -- the STABLE C deep-beta engine: the frozen-occupancy connected
 * determinant with the log-domain propagator (cdet_stable G0), so deep-beta measurements that took
 * ~90 s/point in Python run in ~1 s/point in C. Reads the exact L=6 spectrum (spectrum_l6.bin,
 * dumped from cube_hopping) so it matches the Python stable engine to machine precision. Validated
 * against stable_cdet.StableFrozen.C_V on reference configs (mode 'val'); runs the A(beta)/c1(beta)
 * median-of-means grid (mode 'grid'). Frozen engine (engine/) untouched.
 *   build: gcc -O2 -Wall -Werror -std=c11 -o cse cdet_stable_engine.c -lm
 *   build (float64):     gcc -O2 -Wall -Werror -std=c11 -o cse    cdet_stable_engine.c -lm
 *   build (long double):  gcc -O2 -Wall -Werror -std=c11 -DUSE_LD -o cse_ld cdet_stable_engine.c -lm
 *   usage: cse  val  < refs.txt           (validate C_V vs Python at beta=36)
 *          cse  valb < cfgs.txt           (per-beta C_V check: lines 'beta s c0 c1 c2 t0 t1 t2 ref')
 *          cse  grid beta_lo beta_hi beta_step K NT seed delta mode(0=v99,1=delta1) [probe=2] [s0 s1 s2] [mu=1.845]
 *             v116: optional sites s0,s1,s2 (args 11-13); v118: optional mu (arg 14); both leave z(inf)=2.
 *            (optional 10th arg PROBE = the level frozen to s; default 2 = the Fermi-surface level.
 *             v114: probe!=2 is ill-defined -- e.g. probe=3 makes c1 diverge as exp(+2.7 beta), a
 *             population inversion (level 3 occupied while level 2 empty) forbidden by Fermi statistics.)
 * v110 PRECISION NOTE: the FROZEN connected determinant is well-conditioned (freezing the deep
 * occupied levels removes the ill-conditioned occupied-far physical amplitudes), so float64 is
 * reliable to ~beta=80; at beta>=96 the tiny determinant residual underflows to NaN in float64 --
 * use -DUSE_LD (x87 80-bit, +3.3 digits) to reach beta=120. (The PHYSICAL engine, by contrast,
 * hits a determinant-level wall already at beta~56 -- the freeze is also a numerical regulator.) */
#define _POSIX_C_SOURCE 199309L
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <stdint.h>
#ifdef USE_LD
typedef long double REAL;
#define EXP expl
#define LOG1P log1pl
#define FABS fabsl
#else
typedef double REAL;
#define EXP exp
#define LOG1P log1p
#define FABS fabs
#endif

static int N;
static double *EV, *U;          /* EV[N], U[N*N] row-major (U[i*N+k]) */
static double TO=0.7, TI=0.2;

static int load_spectrum(const char *path){
    FILE *f=fopen(path,"rb"); if(!f){perror("spectrum");return 1;}
    if(fread(&N,sizeof(int),1,f)!=1){return 1;}
    EV=malloc(sizeof(double)*N); U=malloc(sizeof(double)*N*N);
    if(fread(EV,sizeof(double),N,f)!=(size_t)N){return 1;}
    if(fread(U,sizeof(double),(size_t)N*N,f)!=(size_t)N*N){return 1;}
    fclose(f); return 0;
}
static REAL softplus(REAL x){ return x>0.0 ? x+LOG1P(EXP(-x)) : LOG1P(EXP(x)); }

/* per-level occupancy setup for the freeze (occ=1, probe=PROBE): frozen value or marks physical */
static double OCC[512]; static int FROZ[512];
static int PROBE = 2;   /* the level frozen to s (the s-direction); default 2 (the v99 window) */
static void set_freeze(double s, int mode){
    for(int k=0;k<N;k++){
        long lev=lround(EV[k]); FROZ[k]=1;
        if(lev<=1) OCC[k]=1.0;
        else if(lev>=2 && lev<=3) OCC[k] = (lev==PROBE) ? s : 0.0;  /* window level: probe->s, other->0 */
        else FROZ[k]=0;                 /* lev>=4 physical */
        if(mode==1 && lev==1) FROZ[k]=0; /* delta1: level 1 physical */
    }
}
/* stable g0 with frozen occupancies; beta passed for the physical softplus */
static REAL g0(int i,int j,REAL tau,REAL mu,REAL beta){
    REAL tt=tau;
    while(tt>beta) tt-=2*beta;
    while(tt<=-beta) tt+=2*beta;
    REAL out=0.0;
    const double *Ui=U+(size_t)i*N, *Uj=U+(size_t)j*N;
    for(int k=0;k<N;k++){
        REAL xi=(REAL)EV[k]-mu, val;
        if(FROZ[k]){
            REAL o=(REAL)OCC[k];
            if(tt>0) val=-(1.0-o)*EXP(-xi*tt);
            else if(tt<0) val=o*EXP(-xi*tt);
            else val=o;
        } else {                         /* physical, log-domain stable */
            if(tt>0) val=-EXP(-xi*tt - softplus(-beta*xi));
            else if(tt<0) val=EXP(-xi*tt - softplus(beta*xi));
            else val=EXP(-softplus(beta*xi));
        }
        out+=(REAL)Ui[k]*(REAL)Uj[k]*val;
    }
    return out;
}
/* LU determinant (destroys A) */
static REAL det_lu(REAL*A,int m){
    REAL d=1.0;
    for(int c=0;c<m;c++){
        int p=c; for(int r=c+1;r<m;r++) if(fabs(A[r*m+c])>fabs(A[p*m+c])) p=r;
        if(A[p*m+c]==0.0) return 0.0;
        if(p!=c){ for(int k=0;k<m;k++){REAL t=A[c*m+k];A[c*m+k]=A[p*m+k];A[p*m+k]=t;} d=-d; }
        d*=A[c*m+c];
        for(int r=c+1;r<m;r++){ REAL fct=A[r*m+c]/A[c*m+c]; for(int k=c;k<m;k++) A[r*m+k]-=fct*A[c*m+k]; }
    }
    return d;
}
/* bdet: det of M[a][b] = g0(rs[a], cs[b], rt[a]-ct[b], mu) */
static REAL bdet(const int*rs,const REAL*rt,const int*cs,const REAL*ct,int m,REAL mu,REAL beta){
    if(m==0) return 1.0;
    REAL M[16];
    for(int a=0;a<m;a++) for(int b=0;b<m;b++) M[a*m+b]=g0(rs[a],cs[b],rt[a]-ct[b],mu,beta);
    return det_lu(M,m);
}
/* Dcorr / Dvac for a subset given by sites[], taus[], cnt */
static REAL Dcorr(const int*sites,const REAL*taus,int cnt,REAL mu,REAL beta){
    int rs[4],cs[4]; REAL rt[4],ct[4];
    rs[0]=0; rt[0]=TO; cs[0]=0; ct[0]=TI;
    for(int i=0;i<cnt;i++){rs[i+1]=sites[i];rt[i+1]=taus[i];cs[i+1]=sites[i];ct[i+1]=taus[i];}
    REAL du=bdet(rs,rt,cs,ct,cnt+1,mu,beta), dd=1.0;
    if(cnt>0) dd=bdet(sites,taus,sites,taus,cnt,mu,beta);
    REAL sgn=(cnt&1)?-1.0:1.0;
    return sgn*du*dd;
}
static REAL Dvac(const int*sites,const REAL*taus,int cnt,REAL mu,REAL beta){
    if(cnt==0) return 1.0;
    REAL dA=bdet(sites,taus,sites,taus,cnt,mu,beta);
    REAL sgn=(cnt&1)?-1.0:1.0;
    return sgn*dA*dA;
}
/* connected determinant C_V for n vertices (Rossi recursion) */
static REAL C_V(const int*S,const REAL*T,int n,REAL mu,REAL beta){
    int NS=1<<n; REAL Dv[256], C[256];
    for(int mask=0;mask<NS;mask++){
        int s[4]; REAL t[4]; int cnt=0;
        for(int i=0;i<n;i++) if(mask&(1<<i)){s[cnt]=S[i];t[cnt]=T[i];cnt++;}
        Dv[mask]=Dvac(s,t,cnt,mu,beta);
    }
    for(int k=0;k<=n;k++) for(int mask=0;mask<NS;mask++){
        if(__builtin_popcount(mask)!=k) continue;
        int s[4]; REAL t[4]; int cnt=0;
        for(int i=0;i<n;i++) if(mask&(1<<i)){s[cnt]=S[i];t[cnt]=T[i];cnt++;}
        REAL val=Dcorr(s,t,cnt,mu,beta);
        int sm=(mask-1)&mask;
        while(1){ if(sm!=mask) val-=C[sm]*Dv[mask^sm]; if(sm==0) break; sm=(sm-1)&mask; }
        C[mask]=val;
    }
    return C[NS-1];
}

static uint64_t st_;
static inline uint64_t xs(void){uint64_t x=st_;x^=x>>12;x^=x<<25;x^=x>>27;st_=x;return x*0x2545F4914F6CDD1DULL;}
static inline double ur(void){return (double)(xs()>>11)*(1.0/9007199254740992.0);}
static int cmp_d(const void*a,const void*b){double x=*(const double*)a,y=*(const double*)b;return x<y?-1:x>y?1:0;}

int main(int argc,char**argv){
    if(load_spectrum("spectrum_l6.bin")){fprintf(stderr,"need spectrum_l6.bin\n");return 1;}
    double mu=1.845;
    if(argc>=2 && strcmp(argv[1],"valb")==0){
        double bb,s,t0,t1,t2,ref; int c0,c1,c2; double worst=0; int nn=0;
        while(scanf("%lf %lf %d %d %d %lf %lf %lf %lf",&bb,&s,&c0,&c1,&c2,&t0,&t1,&t2,&ref)==9){
            set_freeze(s,0); int S[3]={c0,c1,c2}; REAL T[3]={t0,t1,t2};
            double vd=(double)C_V(S,T,3,(REAL)1.845,(REAL)bb);
            double rel=fabs(vd-ref)/(fabs(ref)+1e-30);
            printf("%.1f %.6e %.6e %.2e\n",bb,vd,ref,rel);
            if(rel>worst)worst=rel;
            nn++;
        }
        fprintf(stderr,"worst rel %.2e over %d\n",worst,nn); return 0;
    }
    if(argc>=2 && strcmp(argv[1],"val")==0){
        /* validate against Python refs from stdin: s c0 c1 c2 t0 t1 t2 cvref */
        double s,t0,t1,t2,ref; int c0,c1,c2; double worst=0; int n=0;
        while(scanf("%lf %d %d %d %lf %lf %lf %lf",&s,&c0,&c1,&c2,&t0,&t1,&t2,&ref)==8){
            set_freeze(s,0);
            int S[3]={c0,c1,c2}; REAL T[3]={t0,t1,t2};
            REAL v=C_V(S,T,3,(REAL)mu,(REAL)36.0); double vd=(double)v;
            double rel=fabs(vd-ref)/(fabs(ref)+1e-30);
            double ad=fabs(vd-ref);
            if(ad>=1e-13 && rel>worst)worst=rel;   /* ignore configs at the 1e-13 cancellation floor */
            n++;
            printf("  s=%.3f cfg=(%d,%d,%d): C=%.6e ref=%.6e rel=%.2e\n",s,c0,c1,c2,vd,ref,rel);
        }
        printf("VALIDATION: %d refs, worst significant rel dev %.2e (above the 1e-13 floor) -> %s\n",n,worst,worst<1e-6?"PASS":"FAIL");
        return worst<1e-6?0:1;
    }
    if(argc>=10 && strcmp(argv[1],"grid")==0){
        double blo=atof(argv[2]),bhi=atof(argv[3]),bstep=atof(argv[4]);
        int K=atoi(argv[5]),NT=atoi(argv[6]); uint64_t seed=strtoull(argv[7],0,10);
        double delta=atof(argv[8]); int mode=atoi(argv[9]);
        if(argc>=11) PROBE=atoi(argv[10]);   /* optional probe level (default 2) */
        int S[3]={1,2,4};                     /* fixed vertex config (default the v99 window) */
        if(argc>=14){ S[0]=atoi(argv[11]); S[1]=atoi(argv[12]); S[2]=atoi(argv[13]); }  /* optional sites */
        if(argc>=15) mu=atof(argv[14]);       /* optional chemical potential (default 1.845) */
        double strip=exp(0.5*(mu-2.0)); st_=seed?seed:88172645463325252ULL;
        const double LAM=0.8;
        printf("# beta  A  A_err  c1  c1_err   (stable C engine, sites (%d,%d,%d) probe=%d, cluster IS, MoM K=%d NT=%d)\n",S[0],S[1],S[2],PROBE,K,NT);
        for(double beta=blo;beta<=bhi+1e-9;beta+=bstep){
            double *Abm=malloc(sizeof(double)*K), *Cbm=malloc(sizeof(double)*K);
            for(int b=0;b<K;b++){
                double Asum=0,Csum=0;
                for(int it=0;it<NT;it++){
                    /* cluster IS proposal over the 3-tau box at fixed sites (matches draw_batch) */
                    double T[3]; int pick = ur()<0.5;
                    double t1=ur()*beta; T[0]=t1;
                    double Z=1.0-0.5*(exp(-LAM*t1)+exp(-LAM*(beta-t1)));
                    for(int j=1;j<3;j++){
                        if(pick){ T[j]=ur()*beta; }
                        else {
                            double r=ur()*Z, Fl=0.5*(1-exp(-LAM*t1));
                            if(r<Fl) T[j]=t1+log(1-2*(Fl-r))/LAM;
                            else     T[j]=t1-log(1-2*(r-Fl))/LAM;
                        }
                    }
                    /* mixture weight w = (1/beta^3)/q */
                    double lap2=(LAM/2)*exp(-LAM*fabs(T[1]-t1))/Z;
                    double lap3=(LAM/2)*exp(-LAM*fabs(T[2]-t1))/Z;
                    double q=0.5*(1.0/(beta*beta*beta))+0.5*(1.0/beta)*lap2*lap3;
                    double w=(1.0/(beta*beta*beta))/q;
                    set_freeze(0.0,mode);   REAL TT[3]={T[0],T[1],T[2]}; double a0=(double)C_V(S,TT,3,(REAL)mu,(REAL)beta);
                    set_freeze(delta,mode); double ad=(double)C_V(S,TT,3,(REAL)mu,(REAL)beta);
                    Asum+=a0*w; Csum+=((ad-a0)/delta)*w;
                }
                Abm[b]=Asum/NT/strip; Cbm[b]=Csum/NT/strip;
            }
            qsort(Abm,K,sizeof(double),cmp_d); qsort(Cbm,K,sizeof(double),cmp_d);
            double Amed=Abm[K/2], Cmed=Cbm[K/2];
            /* simple inter-batch spread / sqrt(K) as error */
            double Av=0,Cv=0,Am=0,Cm=0;
            for(int b=0;b<K;b++){Am+=Abm[b];Cm+=Cbm[b];} Am/=K;Cm/=K;
            for(int b=0;b<K;b++){Av+=(Abm[b]-Am)*(Abm[b]-Am);Cv+=(Cbm[b]-Cm)*(Cbm[b]-Cm);}
            double Ae=sqrt(Av/K/(K-1)), Ce=sqrt(Cv/K/(K-1));
            printf("%.1f %.6e %.6e %.6e %.6e\n",beta,Amed*1e9,Ae*1e9,Cmed*1e9,Ce*1e9);
            fflush(stdout); free(Abm); free(Cbm);
        }
        return 0;
    }
    fprintf(stderr,"usage: cse val | cse grid blo bhi bstep K NT seed delta mode\n"); return 1;
}

/* subset_conv_poc.c (v29) -- the connected-determinant recursion's killer step,
 * sum_{sm subset mask} C[sm]*Dv[mask\sm], is a SUBSET CONVOLUTION. Naive: O(3^n), scattered gather.
 * Fast (Bjorklund et al., STOC 2007): O(2^n n^2) via the zeta/Mobius (Yates/butterfly) transform,
 * whose passes touch only CONTIGUOUS strided memory -- no scatter/gather.
 *
 * This POC, in RAM (no disk), measures: (a) the in-RAM wall-time crossover, and (b) whether the
 * butterfly's accuracy loss is a fixed bias or recoverable rounding.
 *
 * MEASURED (random data): in-RAM crossover at n=19 (n=20: 1.74x, n=21: 2.70x, growing). The error is
 * NOT a fixed ratio -- it grows with n (Mobius alternating +/- cancellation) and SHRINKS with
 * precision: long double cuts max-rel 4-14x (n=14: 1.6e-11 -> 1.2e-12; n=16: 3.1e-9 -> 7.9e-10),
 * proving it is recoverable rounding, not systematic bias. Tradeoff: the fast form needs ~(n+1)/2x
 * more RAM (popcount ranks), so its RAM wall is a few orders earlier than the naive 2*2^n engine.
 *
 * Build: gcc -O2 subset_conv_poc.c -lm -o poc
 * Run:   ./poc <n>           # naive vs fast (double), in-RAM timing + accuracy
 *        ./poc <n> prec      # also run the long-double Mobius, report precision recovery
 */
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <time.h>
static double now(void){struct timespec ts;clock_gettime(CLOCK_MONOTONIC,&ts);return ts.tv_sec+ts.tv_nsec*1e-9;}
static int popc(unsigned x){int c=0;while(x){c+=x&1;x>>=1;}return c;}
static void naive(const double*f,const double*g,double*h,int n){int N=1<<n;
  for(int S=0;S<N;S++){double a=0;int T=S;for(;;){a+=f[T]*g[S^T];if(T==0)break;T=(T-1)&S;}h[S]=a;}}
static void zeta(double*a,int n){int N=1<<n;for(int i=0;i<n;i++)for(int m=0;m<N;m++)if(m&(1<<i))a[m]+=a[m^(1<<i)];}
static void mob(double*a,int n){int N=1<<n;for(int i=0;i<n;i++)for(int m=0;m<N;m++)if(m&(1<<i))a[m]-=a[m^(1<<i)];}
static void fast(const double*f,const double*g,double*h,int n){int N=1<<n;
  double**fz=malloc((n+1)*sizeof(void*)),**gz=malloc((n+1)*sizeof(void*)),**hz=malloc((n+1)*sizeof(void*));
  for(int k=0;k<=n;k++){fz[k]=calloc(N,8);gz[k]=calloc(N,8);hz[k]=calloc(N,8);}
  for(int m=0;m<N;m++){int p=popc(m);fz[p][m]=f[m];gz[p][m]=g[m];}
  for(int k=0;k<=n;k++){zeta(fz[k],n);zeta(gz[k],n);}
  for(int k=0;k<=n;k++)for(int j=0;j<=k;j++)for(int m=0;m<N;m++)hz[k][m]+=fz[j][m]*gz[k-j][m];
  for(int k=0;k<=n;k++)mob(hz[k],n);
  for(int m=0;m<N;m++)h[m]=hz[popc(m)][m];
  for(int k=0;k<=n;k++){free(fz[k]);free(gz[k]);free(hz[k]);}free(fz);free(gz);free(hz);}
/* long-double Mobius path -- to test precision recovery */
static void zetaL(long double*a,int n){int N=1<<n;for(int i=0;i<n;i++)for(int m=0;m<N;m++)if(m&(1<<i))a[m]+=a[m^(1<<i)];}
static void mobL(long double*a,int n){int N=1<<n;for(int i=0;i<n;i++)for(int m=0;m<N;m++)if(m&(1<<i))a[m]-=a[m^(1<<i)];}
static void fastL(const double*f,const double*g,double*h,int n){int N=1<<n;
  long double**fz=malloc((n+1)*sizeof(void*)),**gz=malloc((n+1)*sizeof(void*)),**hz=malloc((n+1)*sizeof(void*));
  for(int k=0;k<=n;k++){fz[k]=calloc(N,sizeof(long double));gz[k]=calloc(N,sizeof(long double));hz[k]=calloc(N,sizeof(long double));}
  for(int m=0;m<N;m++){int p=popc(m);fz[p][m]=f[m];gz[p][m]=g[m];}
  for(int k=0;k<=n;k++){zetaL(fz[k],n);zetaL(gz[k],n);}
  for(int k=0;k<=n;k++)for(int j=0;j<=k;j++)for(int m=0;m<N;m++)hz[k][m]+=fz[j][m]*gz[k-j][m];
  for(int k=0;k<=n;k++)mobL(hz[k],n);
  for(int m=0;m<N;m++)h[m]=(double)hz[popc(m)][m];
  for(int k=0;k<=n;k++){free(fz[k]);free(gz[k]);free(hz[k]);}free(fz);free(gz);free(hz);}
int main(int argc,char**argv){
  int n=argc>1?atoi(argv[1]):16; int N=1<<n; int prec=(argc>2);
  double*f=malloc(N*8),*g=malloc(N*8),*h0=malloc(N*8),*h1=malloc(N*8),*h2=malloc(N*8);
  srand(12345);for(int m=0;m<N;m++){f[m]=(rand()/(double)RAND_MAX)-0.5;g[m]=(rand()/(double)RAND_MAX)-0.5;}
  double t0=now();naive(f,g,h0,n);double tn=now()-t0;
  t0=now();fast(f,g,h1,n);double tf=now()-t0;
  double e1=0;for(int m=0;m<N;m++){double r=fabs(h0[m]-h1[m])/(fabs(h0[m])+1e-300);if(r>e1)e1=r;}
  if(!prec) printf("n=%2d  naive(3^n)=%8.3g s  fast(2^n n^2)=%8.3g s  speedup=%5.2fx  maxrel(double)=%.2g\n",n,tn,tf,tn/tf,e1);
  else{ fastL(f,g,h2,n); double e2=0;for(int m=0;m<N;m++){double r=fabs(h0[m]-h2[m])/(fabs(h0[m])+1e-300);if(r>e2)e2=r;}
    printf("n=%2d  maxrel double=%.2g  maxrel long-double=%.2g  recovered=%.0fx  (=> rounding, not fixed bias)\n",n,e1,e2,e1/(e2+1e-300)); }
  free(f);free(g);free(h0);free(h1);free(h2); return 0;}

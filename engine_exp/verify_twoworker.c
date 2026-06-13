#define _USE_MATH_DEFINES
#ifndef M_PI
#define M_PI 3.14159265358979323846
#endif
#include "qss_det.h"
#include "qss_parallel.h"
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <string.h>
#include <pthread.h>
#include <time.h>

/* Build a batch of B independent same-site qss determinant problems. */
static void make_batch(int B, int L, double beta, double mu, double t,
 double **A, double **Bu, double **Bl, int *n){
 for(int b=0;b<B;b++){
 int nn = 8 + (b%24); /* varied sizes 8..31 */
 n[b]=nn;
 double tau[64]; for(int a=0;a<nn;a++) tau[a]=0.05 + (beta-0.1)*a/nn;
 A[b]=malloc(sizeof(double)*nn*L); Bu[b]=malloc(sizeof(double)*nn*L); Bl[b]=malloc(sizeof(double)*nn*L);
 qss_build_ring(L,beta,mu,t,tau,nn,A[b],Bu[b],Bl[b]);
 }
}

/* a "worker" computes dets for a contiguous slice [lo,hi) of the batch */
typedef struct { double **A,**Bu,**Bl; int *n; int L,lo,hi; double *out; } Work;
static void* worker(void *arg){
 Work *w=arg;
 for(int b=w->lo;b<w->hi;b++) w->out[b]=qss_det(w->A[b],w->Bu[b],w->Bl[b],w->n[b],w->L);
 return NULL;
}

int main(void){
 const int B=2000, L=6; const double beta=20,mu=0.3,t=1;
 double **A=malloc(sizeof(double*)*B),**Bu=malloc(sizeof(double*)*B),**Bl=malloc(sizeof(double*)*B);
 int *n=malloc(sizeof(int)*B);
 make_batch(B,L,beta,mu,t,A,Bu,Bl,n);

 /* (1) SERIAL reference */
 double *serial=malloc(sizeof(double)*B);
 for(int b=0;b<B;b++) serial[b]=qss_det(A[b],Bu[b],Bl[b],n[b],L);

 /* (2) TWO WORKERS (real pthreads), batch split into two independent halves */
 double *par=malloc(sizeof(double)*B);
 pthread_t th[2]; Work w[2];
 int mid=B/2;
 w[0]=(Work){A,Bu,Bl,n,L,0,mid,par};
 w[1]=(Work){A,Bu,Bl,n,L,mid,B,par};
 pthread_create(&th[0],NULL,worker,&w[0]);
 pthread_create(&th[1],NULL,worker,&w[1]);
 pthread_join(th[0],NULL); pthread_join(th[1],NULL);

 /* CORRECTNESS: do the two-worker results match serial exactly? */
 double maxe=0; for(int b=0;b<B;b++){ double e=fabs(par[b]-serial[b]); if(e>maxe)maxe=e; }
 printf("Two independent workers vs serial, over %d determinants:\n",B);
 printf(" max |two-worker - serial| = %.2e -> %s\n", maxe, maxe==0.0?"BIT-IDENTICAL":(maxe<1e-12?"match to round-off":"MISMATCH"));

 /* also via the OpenMP batch (may be 1 thread here) */
 double *bat=malloc(sizeof(double)*B);
 qss_det_batch((const double*const*)A,(const double*const*)Bu,(const double*const*)Bl,n,L,B,bat);
 double maxe2=0; for(int b=0;b<B;b++){ double e=fabs(bat[b]-serial[b]); if(e>maxe2)maxe2=e; }
 printf(" OpenMP batch vs serial: max diff %.2e (threads=%d)\n", maxe2, qss_parallel_threads());
 return 0;
}

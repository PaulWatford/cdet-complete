/* test_eigen.c; verify the optional Eigen dense path against the engine's own
 * det_lu / jacobi_eigh to round-off, and benchmark Eigen vs plain LU on large
 * dense matrices. Built by `make eigen`. */
#include "dense_eigen.h"
#include "cdet_engine.h"
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <time.h>

/* plain heap LU (same as the engine's det_lu, duplicated to time independently) */
static double plain_det(double *a, int m) {
 double det = 1.0;
 for (int col = 0; col < m; col++) {
 int piv = col; double best = fabs(a[col*m+col]);
 for (int r = col+1; r < m; r++)
 if (fabs(a[r*m+col]) > best) { best = fabs(a[r*m+col]); piv = r; }
 if (best == 0.0) return 0.0;
 if (piv != col) { for (int k=0;k<m;k++){double t=a[col*m+k];a[col*m+k]=a[piv*m+k];a[piv*m+k]=t;} det=-det; }
 double d = a[col*m+col]; det *= d;
 for (int r = col+1; r < m; r++) { double f=a[r*m+col]/d; for (int k=col;k<m;k++) a[r*m+k]-=f*a[col*m+k]; }
 }
 return det;
}

static unsigned long s = 12345;
static double rnd(void){ s = s*6364136223846793005ULL + 1; return (double)(s>>11)/9007199254740992.0*2-1; }

int main(void) {
 printf("=====================================================================\n");
 printf(" Optional Eigen dense path; verification + benchmark\n");
 printf("=====================================================================\n");

 /* 1) correctness: det vs the engine's det_lu on small + medium matrices */
 printf("\n [correctness] eigen_det vs engine det_lu:\n");
 for (int n = 3; n <= 64; n *= 2) {
 double *M = malloc(sizeof(double)*n*n);
 for (int i=0;i<n*n;i++) M[i]=rnd();
 double de = eigen_det(M, n);
 double dl = det_lu(M, n); /* engine's (heap) LU */
 double denom = fabs(dl) > 1e-12 ? fabs(dl) : 1.0;
 printf(" n=%3d: eigen=% .6e det_lu=% .6e rel.err=%.1e\n",
 n, de, dl, fabs(de-dl)/denom);
 free(M);
 }

 /* 2) correctness: symmetric eigensolver vs jacobi_eigh (n<=8) */
 printf("\n [correctness] eigen_eigh vs jacobi_eigh (eigenvalue sets):\n");
 for (int n = 2; n <= 6; n++) {
 double *A = malloc(sizeof(double)*n*n);
 for (int i=0;i<n;i++) for (int j=i;j<n;j++){ double v=rnd(); A[i*n+j]=v; A[j*n+i]=v; }
 double *eve=malloc(sizeof(double)*n*n), *evj=malloc(sizeof(double)*n*n);
 double we[8], wj[8];
 eigen_eigh(A, n, we, eve);
 jacobi_eigh(A, n, wj, evj);
 /* jacobi evals unsorted; sort both ascending for comparison */
 for (int a=0;a<n;a++) for (int b=a+1;b<n;b++){ if(wj[b]<wj[a]){double t=wj[a];wj[a]=wj[b];wj[b]=t;} }
 double mx=0; for(int i=0;i<n;i++){double e=fabs(we[i]-wj[i]); if(e>mx)mx=e;}
 printf(" n=%d: max |eigenvalue diff| = %.1e\n", n, mx);
 free(A); free(eve); free(evj);
 }

 /* 3) benchmark: eigen_det vs plain LU on LARGE dense matrices */
 printf("\n [benchmark] eigen_det vs plain LU (large dense):\n");
 printf(" n eigen(ms) plainLU(ms) speedup\n");
 for (int idx=0; idx<4; idx++) {
 int n = (int[]){128,256,512,1024}[idx];
 double *M = malloc(sizeof(double)*n*n);
 for (int i=0;i<n*n;i++) M[i]=rnd();
 double *Mc = malloc(sizeof(double)*n*n);
 int reps = n<=256?20:5;
 clock_t c0=clock();
 for(int r=0;r<reps;r++){ volatile double d=eigen_det(M,n); (void)d; }
 double te=(double)(clock()-c0)/CLOCKS_PER_SEC/reps*1e3;
 c0=clock();
 for(int r=0;r<reps;r++){ for(int i=0;i<n*n;i++)Mc[i]=M[i]; volatile double d=plain_det(Mc,n); (void)d; }
 double tp=(double)(clock()-c0)/CLOCKS_PER_SEC/reps*1e3;
 printf(" %4d %9.2f %10.2f %5.2fx\n", n, te, tp, tp/te);
 free(M); free(Mc);
 }
 printf("\n Eigen is the tuned dense path for large blocks; for tiny Wick\n");
 printf(" matrices the engine's inlined det_lu remains preferable.\n");
 return 0;
}

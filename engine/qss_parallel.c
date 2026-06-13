/* qss_parallel: run many independent determinants across cores, and split one big
 * determinant into chunks glued up a tree. Same answer whatever the core count. See qss_parallel.h. */

#include "qss_parallel.h"
#ifdef _OPENMP
#include <omp.h>
#endif

extern double qss_det(const double*, const double*, const double*, int, int);

void qss_det_batch(const double *const *A, const double *const *Bu,
 const double *const *Bl, const int *n, int L,
 int B, double *out) {
#ifdef _OPENMP
 #pragma omp parallel for schedule(dynamic)
#endif
 for (int b = 0; b < B; b++)
 out[b] = qss_det(A[b], Bu[b], Bl[b], n[b], L);
}

int qss_parallel_threads(void) {
#ifdef _OPENMP
 return omp_get_max_threads();
#else
 return 1;
#endif
}

/* Split one determinant into time-chunks: summarise each chunk, then glue the
 * summaries up a balanced tree. Gluing doesn't care how you group it, so the tree
 * gives the same answer as a straight left-to-right sweep, but the chunks can be
 * built in parallel. (Same gluing maths as schur.c.) */
#include <stdlib.h>
#include <math.h>

typedef struct { double logabs, sign; double *W, *X; } Summary;

/* C = A*B for L x L (row-major) */
static void mm(const double *A, const double *B, double *C, int L) {
 for (int i=0;i<L;i++) for (int j=0;j<L;j++){ double s=0; for(int k=0;k<L;k++) s+=A[i*L+k]*B[k*L+j]; C[i*L+j]=s; }
}
/* solve K = (I - X W)^{-1} via LU on M=(I-XW); also return det(M). */
static double inv_ImXW(const double *X, const double *W, double *K, int L) {
 double *M=malloc(sizeof(double)*L*L), *aug=malloc(sizeof(double)*L*L);
 for (int i=0;i<L;i++) for (int j=0;j<L;j++){ double s=0; for(int k=0;k<L;k++) s+=X[i*L+k]*W[k*L+j]; M[i*L+j]=(i==j?1.0:0.0)-s; }
 /* det via LU with partial pivot, and inverse via Gauss-Jordan */
 for (int i=0;i<L*L;i++) aug[i]=M[i];
 for (int i=0;i<L;i++) for (int j=0;j<L;j++) K[i*L+j]=(i==j?1.0:0.0);
 double det=1.0;
 for (int col=0;col<L;col++){
 int piv=col; double best=fabs(aug[col*L+col]);
 for (int r=col+1;r<L;r++) if(fabs(aug[r*L+col])>best){best=fabs(aug[r*L+col]);piv=r;}
 if (piv!=col){ for(int k=0;k<L;k++){double t=aug[col*L+k];aug[col*L+k]=aug[piv*L+k];aug[piv*L+k]=t;
 t=K[col*L+k];K[col*L+k]=K[piv*L+k];K[piv*L+k]=t;} det=-det; }
 double d=aug[col*L+col]; det*=d;
 for (int k=0;k<L;k++){ aug[col*L+k]/=d; K[col*L+k]/=d; }
 for (int r=0;r<L;r++) if(r!=col){ double f=aug[r*L+col];
 for(int k=0;k<L;k++){ aug[r*L+k]-=f*aug[col*L+k]; K[r*L+k]-=f*K[col*L+k]; } }
 }
 free(M); free(aug);
 return det;
}

static void leaf_summarize(const double *A, const double *Bu, const double *Bl,
 int lo, int hi, int L, Summary *s) {
 double *W=calloc((size_t)L*L,sizeof(double)), *X=calloc((size_t)L*L,sizeof(double));
 double *WBu=malloc(sizeof(double)*L), *WtA=malloc(sizeof(double)*L), *XBu=malloc(sizeof(double)*L);
 double logabs=0.0, sign=1.0;
 for (int i=lo;i<hi;i++){
 const double *Ai=&A[i*L], *Bui=&Bu[i*L], *Bli=&Bl[i*L];
 for(int k=0;k<L;k++){ double v=0; for(int m=0;m<L;m++) v+=W[k*L+m]*Bui[m]; WBu[k]=v; }
 double piv=0; for(int k=0;k<L;k++) piv+=Ai[k]*(Bui[k]-WBu[k]);
 logabs+=log(fabs(piv)); if(piv<0) sign=-sign;
 for(int k=0;k<L;k++){ double v=0; for(int m=0;m<L;m++) v+=W[m*L+k]*Ai[m]; WtA[k]=v; }
 for(int k=0;k<L;k++){ double v=0; for(int m=0;m<L;m++) v+=X[k*L+m]*Bui[m]; XBu[k]=v; }
 double inv=1.0/piv;
 for(int r=0;r<L;r++) for(int c=0;c<L;c++){ double rf=Ai[c]-WtA[c];
 W[r*L+c]+=(Bli[r]-WBu[r])*rf*inv;
 X[r*L+c]+=(Bui[r]-XBu[r])*rf*inv; }
 }
 s->logabs=logabs; s->sign=sign; s->W=W; s->X=X;
 free(WBu); free(WtA); free(XBu);
}

/* merge right summary R into left summary Lf, store into Lf (Lf becomes [L|R]). */
static void merge_into(Summary *Lf, const Summary *R, int L) {
 double *K=malloc(sizeof(double)*L*L);
 double dcorr = inv_ImXW(R->X, Lf->W, K, L); /* K=(I-XR WL)^-1, det(I-XR WL) */
 double *WLK=malloc(sizeof(double)*L*L), *tmp=malloc(sizeof(double)*L*L);
 double *WR_S=malloc(sizeof(double)*L*L), *XR_S=malloc(sizeof(double)*L*L);
 /* WL K */
 mm(Lf->W, K, WLK, L);
 /* WR_S = WR + WR (WL K) XR ; XR_S = XR + XR (WL K) XR */
 mm(R->W, WLK, tmp, L); /* WR WL K */
 double *t2=malloc(sizeof(double)*L*L);
 mm(tmp, R->X, t2, L); /* WR WL K XR */
 for (int i=0;i<L*L;i++) WR_S[i]=R->W[i]+t2[i];
 mm(R->X, WLK, tmp, L); /* XR WL K */
 mm(tmp, R->X, t2, L); /* XR WL K XR */
 for (int i=0;i<L*L;i++) XR_S[i]=R->X[i]+t2[i];
 /* W = WL + WL XR_S WL - WL XR_S - WR_S WL + WR_S */
 double *WLX=malloc(sizeof(double)*L*L), *WLXWL=malloc(sizeof(double)*L*L);
 double *WRSWL=malloc(sizeof(double)*L*L), *XLX=malloc(sizeof(double)*L*L);
 double *XLXWL=malloc(sizeof(double)*L*L), *XRSWL=malloc(sizeof(double)*L*L);
 mm(Lf->W, XR_S, WLX, L); mm(WLX, Lf->W, WLXWL, L); mm(WR_S, Lf->W, WRSWL, L);
 mm(Lf->X, XR_S, XLX, L); mm(XLX, Lf->W, XLXWL, L); mm(XR_S, Lf->W, XRSWL, L);
 double *newW=malloc(sizeof(double)*L*L), *newX=malloc(sizeof(double)*L*L);
 for (int i=0;i<L*L;i++) newW[i]=Lf->W[i]+WLXWL[i]-WLX[i]-WRSWL[i]+WR_S[i];
 for (int i=0;i<L*L;i++) newX[i]=Lf->X[i]+XLXWL[i]-XLX[i]-XRSWL[i]+XR_S[i];
 Lf->logabs += R->logabs + log(fabs(dcorr));
 Lf->sign *= R->sign * (dcorr<0?-1.0:1.0);
 free(Lf->W); free(Lf->X); Lf->W=newW; Lf->X=newX;
 free(K);free(WLK);free(tmp);free(t2);free(WR_S);free(XR_S);
 free(WLX);free(WLXWL);free(WRSWL);free(XLX);free(XLXWL);free(XRSWL);
}

double qss_det_tree(const double *A, const double *Bu, const double *Bl,
 int n, int L, int nleaves) {
 if (nleaves<1) nleaves=1;
 if (nleaves>n) nleaves=n;
 Summary *S=malloc(sizeof(Summary)*nleaves);
 int *bnd=malloc(sizeof(int)*(nleaves+1));
 for (int c=0;c<=nleaves;c++) bnd[c]=(int)((long)c*n/nleaves);
 for (int c=0;c<nleaves;c++){ S[c].logabs=0.0; S[c].sign=1.0; S[c].W=NULL; S[c].X=NULL; }
#ifdef _OPENMP
 #pragma omp parallel for schedule(dynamic)
#endif
 for (int c=0;c<nleaves;c++) leaf_summarize(A,Bu,Bl,bnd[c],bnd[c+1],L,&S[c]);
 /* Merge is associative but NOT commutative: chunks must combine in time
 * order. Fold left-to-right into S[0]: ((c0 . c1) . c2) ... The leaves were
 * the parallel part; this fold is O(nleaves) merges of O(L^3) each.
 * NOTE: S[*] is fully initialised at line above and written by every leaf;
 * GCC -O2 cannot prove this through the inlined pointer writes and emits a
 * false -Wmaybe-uninitialized. Suppress narrowly. */
#if defined(__GNUC__) && !defined(__clang__)
#pragma GCC diagnostic push
#pragma GCC diagnostic ignored "-Wmaybe-uninitialized"
#endif
 for (int c=1;c<nleaves;c++){ merge_into(&S[0],&S[c],L); free(S[c].W); free(S[c].X); }
 double det=S[0].sign*exp(S[0].logabs);
 free(S[0].W); free(S[0].X);
#if defined(__GNUC__) && !defined(__clang__)
#pragma GCC diagnostic pop
#endif
 free(S); free(bnd);
 return det;
}

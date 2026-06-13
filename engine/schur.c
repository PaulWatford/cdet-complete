/* schur: the glue that joins two time-chunk summaries into one. See schur.h. */

#include "schur.h"
#include <stdlib.h>
#include <math.h>

static double *zeros(int L){ return (double*)calloc((size_t)L*L, sizeof(double)); }

/* C = A*B for L x L row-major */
static void mm(const double *A, const double *B, double *C, int L){
 for (int i=0;i<L;i++) for (int j=0;j<L;j++){ double s=0; for(int k=0;k<L;k++) s+=A[i*L+k]*B[k*L+j]; C[i*L+j]=s; }
}
/* K = (I - X W)^{-1} via Gauss-Jordan; returns det(I - X W). */
static double inv_ImXW(const double *X, const double *W, double *K, int L){
 double *aug=(double*)malloc(sizeof(double)*L*L);
 for (int i=0;i<L;i++) for (int j=0;j<L;j++){ double s=0; for(int k=0;k<L;k++) s+=X[i*L+k]*W[k*L+j]; aug[i*L+j]=(i==j?1.0:0.0)-s; }
 for (int i=0;i<L;i++) for (int j=0;j<L;j++) K[i*L+j]=(i==j?1.0:0.0);
 double det=1.0;
 for (int col=0;col<L;col++){
 int piv=col; double best=fabs(aug[col*L+col]);
 for (int r=col+1;r<L;r++) if(fabs(aug[r*L+col])>best){best=fabs(aug[r*L+col]);piv=r;}
 if (piv!=col){ for(int k=0;k<L;k++){double tmp=aug[col*L+k];aug[col*L+k]=aug[piv*L+k];aug[piv*L+k]=tmp;
 tmp=K[col*L+k];K[col*L+k]=K[piv*L+k];K[piv*L+k]=tmp;} det=-det; }
 double d=aug[col*L+col]; det*=d;
 for (int k=0;k<L;k++){ aug[col*L+k]/=d; K[col*L+k]/=d; }
 for (int r=0;r<L;r++) if(r!=col){ double f=aug[r*L+col];
 for(int k=0;k<L;k++){ aug[r*L+k]-=f*aug[col*L+k]; K[r*L+k]-=f*K[col*L+k]; } }
 }
 free(aug);
 return det;
}

Summary schur_identity(int L){
 Summary s; s.logabs=0.0; s.sign=1.0; s.W=zeros(L); s.X=zeros(L); return s;
}

Summary schur_leaf(const double *Ar, const double *Bur, const double *Blr, int L){
 Summary s; s.W=zeros(L); s.X=zeros(L);
 double *WBu=(double*)malloc(sizeof(double)*L), *WtA=(double*)malloc(sizeof(double)*L), *XBu=(double*)malloc(sizeof(double)*L);
 for(int k=0;k<L;k++) WBu[k]=0; /* W=0 initially -> W Bu = 0 */
 double piv=0; for(int k=0;k<L;k++) piv+=Ar[k]*(Bur[k]-WBu[k]);
 s.logabs=log(fabs(piv)); s.sign=(piv<0)?-1.0:1.0;
 for(int k=0;k<L;k++) WtA[k]=0; /* W^T A = 0 */
 for(int k=0;k<L;k++) XBu[k]=0; /* X=0 -> X Bu = 0 */
 double inv=1.0/piv;
 for(int r=0;r<L;r++) for(int c=0;c<L;c++){ double rf=Ar[c]-WtA[c];
 s.W[r*L+c]=(Blr[r]-WBu[r])*rf*inv;
 s.X[r*L+c]=(Bur[r]-XBu[r])*rf*inv; }
 free(WBu); free(WtA); free(XBu);
 return s;
}

Summary schur_chunk(const double *A, const double *Bu, const double *Bl, int n, int L){
 Summary acc=schur_identity(L);
 for (int i=0;i<n;i++){
 Summary lf=schur_leaf(&A[i*L],&Bu[i*L],&Bl[i*L],L);
 Summary m=schur_merge(&acc,&lf,L);
 schur_free(&acc); schur_free(&lf); acc=m;
 }
 return acc;
}

Summary schur_merge(const Summary *Lf, const Summary *R, int L){
 const double *WL=Lf->W, *XL=Lf->X, *WR=R->W, *XR=R->X;
 size_t LL=(size_t)L*L;
 double *K=(double*)calloc(LL,sizeof(double));
 double dcorr=inv_ImXW(XR, WL, K, L);
 double *WLK=(double*)calloc(LL,sizeof(double)), *tmp=(double*)calloc(LL,sizeof(double)), *t2=(double*)calloc(LL,sizeof(double));
 double *WR_S=(double*)calloc(LL,sizeof(double)), *XR_S=(double*)calloc(LL,sizeof(double));
 mm(WL,K,WLK,L);
 mm(WR,WLK,tmp,L); mm(tmp,XR,t2,L); for(size_t i=0;i<LL;i++) WR_S[i]=WR[i]+t2[i];
 mm(XR,WLK,tmp,L); mm(tmp,XR,t2,L); for(size_t i=0;i<LL;i++) XR_S[i]=XR[i]+t2[i];
 double *WLX=(double*)calloc(LL,sizeof(double)), *WLXWL=(double*)calloc(LL,sizeof(double)), *WRSWL=(double*)calloc(LL,sizeof(double));
 double *XLX=(double*)calloc(LL,sizeof(double)), *XLXWL=(double*)calloc(LL,sizeof(double)), *XRSWL=(double*)calloc(LL,sizeof(double));
 mm(WL,XR_S,WLX,L); mm(WLX,WL,WLXWL,L); mm(WR_S,WL,WRSWL,L);
 mm(XL,XR_S,XLX,L); mm(XLX,WL,XLXWL,L); mm(XR_S,WL,XRSWL,L);
 Summary out; out.W=(double*)calloc(LL,sizeof(double)); out.X=(double*)calloc(LL,sizeof(double));
 for(size_t i=0;i<LL;i++) out.W[i]=WL[i]+WLXWL[i]-WLX[i]-WRSWL[i]+WR_S[i];
 for(size_t i=0;i<LL;i++) out.X[i]=XL[i]+XLXWL[i]-XLX[i]-XRSWL[i]+XR_S[i];
 out.logabs=Lf->logabs+R->logabs+log(fabs(dcorr));
 out.sign=Lf->sign*R->sign*((dcorr<0)?-1.0:1.0);
 free(K);free(WLK);free(tmp);free(t2);free(WR_S);free(XR_S);
 free(WLX);free(WLXWL);free(WRSWL);free(XLX);free(XLXWL);free(XRSWL);
 return out;
}

Summary schur_copy(const Summary *s, int L){
 Summary c; c.logabs=s->logabs; c.sign=s->sign;
 c.W=(double*)malloc(sizeof(double)*L*L); c.X=(double*)malloc(sizeof(double)*L*L);
 for(int i=0;i<L*L;i++){ c.W[i]=s->W[i]; c.X[i]=s->X[i]; } return c;
}
void schur_free(Summary *s){ if(s->W){free(s->W);s->W=NULL;} if(s->X){free(s->X);s->X=NULL;} }
double schur_det(const Summary *s){ return s->sign*exp(s->logabs); }

/* dyndet: a time-sorted balanced tree where each branch remembers a summary of
 * everything below it, so changing one vertex only redoes its branch. See dyndet.h. */

#include "dyndet.h"
#include "schur.h"
#include <stdlib.h>
#include <stdint.h>
#include <math.h>
#ifndef M_PI
#define M_PI 3.14159265358979323846
#endif

typedef struct Node {
 double tau; uint64_t pri;
 struct Node *l, *r;
 Summary leaf; /* this vertex alone */
 Summary sub; /* whole subtree, in time order */
} Node;

struct DynDet {
 int L; double beta, mu, t;
 Node *root; int n;
 uint64_t rng; /* xorshift state for priorities */
};

static uint64_t xrand(DynDet *d){
 uint64_t x=d->rng; x^=x<<13; x^=x>>7; x^=x<<17; d->rng=x; return x;
}

/* build leaf generators for a single same-site ring vertex at time tau */
static void gen_row(const DynDet *d, double tau, double *Ar, double *Bur, double *Blr){
 int L=d->L; double s=1.0/sqrt((double)L);
 for (int k=0;k<L;k++){
 double eps=-2.0*d->t*cos(2.0*M_PI*(double)k/(double)L);
 double xi=eps-d->mu, bx=d->beta*xi, nF;
 if (bx>0){ double e=exp(-bx); nF=e/(1.0+e);} else nF=1.0/(1.0+exp(bx));
 Ar[k]=s*exp(-xi*tau);
 Bur[k]=s*exp(xi*tau)*nF;
 Blr[k]=s*exp(xi*tau)*(-(1.0-nF));
 }
}

/* recompute nd->sub = merge(merge(sub(l), leaf), sub(r)) */
static void pull(Node *nd, int L){
 /* left part */
 Summary lid; int left_is_id = (nd->l==NULL);
 Summary ls = left_is_id ? (lid=schur_identity(L), lid) : nd->l->sub;
 Summary m1 = schur_merge(&ls, &nd->leaf, L);
 if (left_is_id) schur_free(&ls);
 Summary rid; int right_is_id = (nd->r==NULL);
 Summary rs = right_is_id ? (rid=schur_identity(L), rid) : nd->r->sub;
 Summary m2 = schur_merge(&m1, &rs, L);
 if (right_is_id) schur_free(&rs);
 schur_free(&m1);
 schur_free(&nd->sub);
 nd->sub = m2;
}

static Node *rotr(Node *p, int L){ Node *q=p->l; p->l=q->r; q->r=p; pull(p,L); pull(q,L); return q; }
static Node *rotl(Node *p, int L){ Node *q=p->r; p->r=q->l; q->l=p; pull(p,L); pull(q,L); return q; }

static Node *node_new(DynDet *d, double tau){
 Node *nd=(Node*)malloc(sizeof(Node));
 nd->tau=tau; nd->pri=xrand(d); nd->l=nd->r=NULL;
 int L=d->L; double *Ar=malloc(sizeof(double)*L),*Bur=malloc(sizeof(double)*L),*Blr=malloc(sizeof(double)*L);
 gen_row(d,tau,Ar,Bur,Blr);
 nd->leaf=schur_leaf(Ar,Bur,Blr,L);
 nd->sub=schur_copy(&nd->leaf,L);
 free(Ar);free(Bur);free(Blr);
 return nd;
}

static Node *ins(DynDet *d, Node *nd, double tau, Node *fresh){
 int L=d->L;
 if (nd==NULL) return fresh;
 if (tau < nd->tau){
 nd->l=ins(d,nd->l,tau,fresh); pull(nd,L);
 if (nd->l->pri < nd->pri) nd=rotr(nd,L);
 } else {
 nd->r=ins(d,nd->r,tau,fresh); pull(nd,L);
 if (nd->r->pri < nd->pri) nd=rotl(nd,L);
 }
 return nd;
}

/* remove the node whose tau is closest to the query (assumes one exists). */
static Node *rem(DynDet *d, Node *nd, double tau, int *removed){
 int L=d->L;
 if (nd==NULL){ *removed=0; return NULL; }
 /* find by descending toward the nearest; we match on exact-ish equality but
 * route by comparison; to remove "nearest" we first locate it by a separate
 * search, here we assume tau equals a stored key within tol. */
 if (fabs(tau-nd->tau) < 1e-12){
 if (nd->l==NULL && nd->r==NULL){ schur_free(&nd->leaf); schur_free(&nd->sub); free(nd); *removed=1; return NULL; }
 if (nd->l==NULL){ Node *r=nd->r; schur_free(&nd->leaf); schur_free(&nd->sub); free(nd); *removed=1; return r; }
 if (nd->r==NULL){ Node *l=nd->l; schur_free(&nd->leaf); schur_free(&nd->sub); free(nd); *removed=1; return l; }
 if (nd->l->pri < nd->r->pri){ nd=rotr(nd,L); nd->r=rem(d,nd->r,tau,removed); }
 else { nd=rotl(nd,L); nd->l=rem(d,nd->l,tau,removed); }
 pull(nd,L); return nd;
 } else if (tau < nd->tau){ nd->l=rem(d,nd->l,tau,removed); }
 else { nd->r=rem(d,nd->r,tau,removed); }
 if (nd) pull(nd,L);
 return nd;
}

/* find the stored tau closest to a query (for remove-nearest semantics). */
static void nearest(const Node *nd, double tau, double *best, double *bestd){
 if (!nd) return;
 double dd=fabs(nd->tau-tau);
 if (dd<*bestd){ *bestd=dd; *best=nd->tau; }
 if (tau<nd->tau) nearest(nd->l,tau,best,bestd); else nearest(nd->r,tau,best,bestd);
 /* also check the other side within range (simple full check for safety) */
 nearest(tau<nd->tau?nd->r:nd->l, tau, best, bestd);
}

DynDet *dyndet_create(int L, double beta, double mu, double t){
 DynDet *d=(DynDet*)malloc(sizeof(DynDet));
 d->L=L; d->beta=beta; d->mu=mu; d->t=t; d->root=NULL; d->n=0; d->rng=88172645463325252ULL;
 return d;
}
static void free_node(Node *nd){ if(!nd) return; free_node(nd->l); free_node(nd->r);
 schur_free(&nd->leaf); schur_free(&nd->sub); free(nd); }
void dyndet_free(DynDet *d){ if(!d) return; free_node(d->root); free(d); }

void dyndet_insert(DynDet *d, double tau){
 Node *fresh=node_new(d,tau);
 d->root=ins(d,d->root,tau,fresh); d->n++;
}
void dyndet_remove(DynDet *d, double tau){
 double best=tau, bestd=1e300; nearest(d->root,tau,&best,&bestd);
 int removed=0; d->root=rem(d,d->root,best,&removed); if (removed) d->n--;
}
double dyndet_value(const DynDet *d){
 if (d->root==NULL) return 1.0; /* empty product */
 return schur_det(&d->root->sub);
}
int dyndet_size(const DynDet *d){ return d->n; }

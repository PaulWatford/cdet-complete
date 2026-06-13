#!/usr/bin/env python3
"""
hubbard_pattern.py  --  the interference pattern of many electrons on a lattice.

Exact diagonalization of a finite Hubbard ring. Computes the spin and charge
correlations and their structure factors, shows how the free-fermion ripple
stiffens into a correlated standing wave as the interaction U is turned on, and
how doping shifts the dominant wavevector between 2k_F and 4k_F.

This is the EXACT reference pattern. It is the validation target the cdet
connected-determinant engine must reproduce at sizes ED cannot reach.

Usage:
  python3 hubbard_pattern.py              # static figures + printed validation
  python3 hubbard_pattern.py --anim       # also write the animated GIF
  python3 hubbard_pattern.py --L 10 --filling 1.0 --Umax 8
"""
import argparse, numpy as np, scipy.sparse as sp
from scipy.sparse.linalg import eigsh

def states(L, N):
    return [s for s in range(1 << L) if bin(s).count('1') == N]

def hop_matrix(S, idx, L, t=1.0):
    rows, cols, val = [], [], []
    for n, s in enumerate(S):
        for a in range(L):
            b = (a + 1) % L
            for (i, j) in ((a, b), (b, a)):          # c^dag_i c_j
                if (s >> j & 1) and not (s >> i & 1):
                    lo, hi = min(i, j), max(i, j)
                    mask = ((1 << hi) - 1) ^ ((1 << (lo + 1)) - 1)   # bits strictly between
                    sign = -1.0 if bin(s & mask).count('1') & 1 else 1.0
                    s2 = (s & ~(1 << j)) | (1 << i)
                    rows.append(idx[s2]); cols.append(n); val.append(-t * sign)
    return sp.csr_matrix((val, (rows, cols)), shape=(len(S), len(S)))

class HubbardRing:
    def __init__(self, L, Nup, Ndn, t=1.0):
        self.L, self.Nup, self.Ndn, self.t = L, Nup, Ndn, t
        self.US = states(L, Nup); self.DS = states(L, Ndn)
        self.nu, self.nd = len(self.US), len(self.DS)
        uidx = {s: i for i, s in enumerate(self.US)}
        didx = {s: i for i, s in enumerate(self.DS)}
        self.Tu = hop_matrix(self.US, uidx, L, t)
        self.Td = hop_matrix(self.DS, didx, L, t)
        self.Iu = sp.identity(self.nu); self.Id = sp.identity(self.nd)
        self.ub = np.array([[(s >> i) & 1 for i in range(L)] for s in self.US])
        self.db = np.array([[(s >> i) & 1 for i in range(L)] for s in self.DS])
        self.docc = np.array([[bin(u & d).count('1') for d in self.DS]
                              for u in self.US]).ravel()

    def ground_state(self, U):
        H = sp.kron(self.Tu, self.Id) + sp.kron(self.Iu, self.Td) + sp.diags(U * self.docc)
        w, v = eigsh(H.tocsr(), k=1, which='SA')
        return float(w[0]), v[:, 0]

    def correlations(self, psi):
        """Return (spin <Sz0 Szr>, charge connected <n0 nr>_c) for r=0..L-1."""
        L = self.L; P = (psi ** 2).reshape(self.nu, self.nd)
        nup_i = self.ub; ndn_j = self.db
        # site densities weighted by |psi|^2
        spin = np.zeros(L); chg = np.zeros(L)
        ni = np.zeros(L)
        for i in range(L):
            ni[i] = np.sum(P * (nup_i[:, i][:, None] + ndn_j[:, i][None, :]))
        for r in range(L):
            su0 = nup_i[:, 0][:, None] - ndn_j[:, 0][None, :]
            sur = nup_i[:, r][:, None] - ndn_j[:, r][None, :]
            spin[r] = np.sum(P * su0 * sur) / 4.0
            n0 = nup_i[:, 0][:, None] + ndn_j[:, 0][None, :]
            nr = nup_i[:, r][:, None] + ndn_j[:, r][None, :]
            chg[r] = np.sum(P * n0 * nr) - ni[0] * ni[r]      # connected
        return spin, chg

    def structure_factor(self, corr):
        L = self.L; q = 2 * np.pi * np.arange(L) / L
        Sq = np.array([np.real(np.sum(corr * np.exp(-1j * q[m] * np.arange(L)))) for m in range(L)])
        return q, Sq

def free_check(L, N):
    """Free-fermion <Sz0 Szr> = -|rho(r)|^2/2. Returns (corr, closed_shell).
    Exact only for a closed-shell (non-degenerate) Fermi sea; open shells have a
    degenerate free ground state and no unique reference."""
    Nup = N // 2
    k = 2 * np.pi * np.arange(L) / L; k = np.where(k > np.pi, k - 2 * np.pi, k)
    eps = -2 * np.cos(k)
    order = np.argsort(eps); es = np.sort(eps)
    closed = not (0 < Nup < L and abs(es[Nup - 1] - es[Nup]) < 1e-9)
    occ = np.zeros(L); occ[order[:Nup]] = 1.0
    rho = np.array([np.real(np.sum(occ * np.exp(1j * k * r)) / L) for r in range(L)])
    return -rho ** 2 / 2, closed

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--L', type=int, default=10)
    ap.add_argument('--filling', type=float, default=1.0, help='electrons per site (1.0 = half)')
    ap.add_argument('--Umax', type=float, default=8.0)
    ap.add_argument('--anim', action='store_true', help='also write the animated GIF')
    ap.add_argument('--out', default='.')
    args = ap.parse_args()

    L = args.L; N = int(round(args.filling * L)); Nup = N // 2; Ndn = N - Nup
    kF = np.pi * (N / L) / 2
    print('Hubbard ring  L=%d  N=%d (Nup=%d,Ndn=%d)  filling n=%.2f' % (L, N, Nup, Ndn, N / L))
    print('  k_F=%.4f  2k_F=%.4f  4k_F=%.4f' % (kF, 2 * kF, 4 * kF))
    H = HubbardRing(L, Nup, Ndn)

    Us = [0.0, 2.0, 4.0, 8.0]
    spin, chg = {}, {}
    for U in Us:
        E0, psi = H.ground_state(U)
        spin[U], chg[U] = H.correlations(psi)
        print('  U=%4.1f  E0=%.5f  <Sz0 Szr> r=0..%d: %s'
              % (U, E0, L // 2, np.round(spin[U][:L // 2 + 1], 4)))
    # validation against free fermions at U=0 (only meaningful for a closed shell)
    fc, closed = free_check(L, N)
    if closed:
        err = np.max(np.abs(fc[1:L // 2 + 1] - spin[0.0][1:L // 2 + 1]))
        print('  U=0 vs free-fermion -|rho|^2/2 : max|diff| = %.2e  (exact check)' % err)
    else:
        print('  U=0 free check skipped: open-shell (degenerate Fermi sea) at L=%d,N=%d; '
              'use a closed-shell size, e.g. L=10 n=1.' % (L, N))

    import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
    BG = '#0b1220'; cols = {0.0: '#5ad1e6', 2.0: '#7ee0a0', 4.0: '#ffd166', 8.0: '#ff7a8a'}

    # ---- static figure 1: spin correlation vs U ----
    fig, ax = plt.subplots(figsize=(10, 5)); fig.patch.set_facecolor(BG); ax.set_facecolor(BG)
    r = np.arange(L // 2 + 1)
    for U in Us:
        ax.plot(r, spin[U][:L // 2 + 1], '-o', color=cols[U], ms=4, lw=1.6, label='U/t = %g' % U)
    ax.axhline(0, color='#5a6b85', lw=0.8)
    ax.set_title('Spin correlation stiffening with interaction (Hubbard ring, ED, L=%d, n=%.2f)' % (L, N / L),
                 color='#e8eef6', fontsize=11.5)
    ax.set_xlabel('separation r (sites)', color='#93a4bd'); ax.set_ylabel(r'$\langle S^z_0 S^z_r\rangle$', color='#93a4bd')
    ax.tick_params(colors='#5a6b85'); ax.legend(facecolor='#111c30', edgecolor='#23344f', labelcolor='#cfe0f5', fontsize=9)
    for s in ax.spines.values(): s.set_color('#23344f')
    plt.tight_layout(); plt.savefig('%s/hubbard_spin_vs_U.png' % args.out, dpi=150, facecolor=BG); plt.close()

    # ---- static figure 2: charge structure factor (2k_F vs 4k_F) ----
    fig, ax = plt.subplots(figsize=(10, 5)); fig.patch.set_facecolor(BG); ax.set_facecolor(BG)
    for U in Us:
        q, Nq = H.structure_factor(chg[U])
        o = np.argsort(q)
        ax.plot(q[o], Nq[o], '-o', color=cols[U], ms=4, lw=1.6, label='U/t = %g' % U)
    for qv, lab in ((2 * kF, '2k_F'), (4 * kF, '4k_F')):
        if qv < 2 * np.pi:
            ax.axvline(qv, color='#5a6b85', ls='--', lw=0.9); ax.text(qv, ax.get_ylim()[1], lab, color='#93a4bd', fontsize=9)
    ax.set_title('Charge structure factor N(q): 2k_F vs 4k_F (L=%d, n=%.2f)' % (L, N / L), color='#e8eef6', fontsize=11.5)
    ax.set_xlabel('q', color='#93a4bd'); ax.set_ylabel('N(q)', color='#93a4bd')
    ax.tick_params(colors='#5a6b85'); ax.legend(facecolor='#111c30', edgecolor='#23344f', labelcolor='#cfe0f5', fontsize=9)
    for s in ax.spines.values(): s.set_color('#23344f')
    plt.tight_layout(); plt.savefig('%s/hubbard_structure_factor.png' % args.out, dpi=150, facecolor=BG); plt.close()
    print('  wrote hubbard_spin_vs_U.png, hubbard_structure_factor.png')

    if args.anim:
        from matplotlib.animation import FuncAnimation, PillowWriter
        Ugrid = np.linspace(0.0, args.Umax, 25)
        data = []
        for U in Ugrid:
            _, psi = H.ground_state(U); sp_, ch_ = H.correlations(psi); data.append((sp_, ch_))
        fig, (axL, axR) = plt.subplots(1, 2, figsize=(12, 5)); fig.patch.set_facecolor(BG)
        for a in (axL, axR):
            a.set_facecolor(BG); a.tick_params(colors='#5a6b85')
            for s in a.spines.values(): s.set_color('#23344f')
        rr = np.arange(L // 2 + 1)
        lineL, = axL.plot([], [], '-o', color='#5ad1e6', ms=5, lw=2)
        axL.axhline(0, color='#5a6b85', lw=0.8); axL.set_xlim(0, L // 2); axL.set_ylim(-0.16, 0.26)
        axL.set_xlabel('separation r', color='#93a4bd'); axL.set_ylabel(r'$\langle S^z_0 S^z_r\rangle$', color='#93a4bd')
        q, _ = H.structure_factor(data[0][1]); o = np.argsort(q)
        lineR, = axR.plot([], [], '-o', color='#ffd166', ms=5, lw=2)
        nqmax = max(np.max(H.structure_factor(d[1])[1]) for d in data)
        axR.set_xlim(0, 2 * np.pi); axR.set_ylim(0, nqmax * 1.15)
        axR.set_xlabel('q', color='#93a4bd'); axR.set_ylabel('N(q)', color='#93a4bd')
        for qv, lab in ((2 * kF, '2k_F'), (4 * kF, '4k_F')):
            if qv < 2 * np.pi: axR.axvline(qv, color='#5a6b85', ls='--', lw=0.9); axR.text(qv, nqmax * 1.05, lab, color='#93a4bd', fontsize=9)
        sup = fig.suptitle('', color='#e8eef6', fontsize=13)

        def upd(f):
            sp_, ch_ = data[f]
            lineL.set_data(rr, sp_[:L // 2 + 1])
            q2, Nq = H.structure_factor(ch_); oo = np.argsort(q2)
            lineR.set_data(q2[oo], Nq[oo])
            sup.set_text('Many electrons on a lattice  |  U/t = %.2f  (n=%.2f)   spin standing wave  +  charge 2k_F/4k_F' % (Ugrid[f], N / L))
            return lineL, lineR, sup
        anim = FuncAnimation(fig, upd, frames=len(Ugrid), blit=False)
        anim.save('%s/hubbard_pattern.gif' % args.out, writer=PillowWriter(fps=8), dpi=110, savefig_kwargs={'facecolor': BG})
        plt.close()
        print('  wrote hubbard_pattern.gif')

if __name__ == '__main__':
    main()

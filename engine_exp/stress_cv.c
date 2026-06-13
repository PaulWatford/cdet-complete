/* stress_cv.c  (v26)  --  crash-safe stress of the (now buffer-free) C_V connected recursion.
 *
 * Drives C_V up in expansion order n until a wall, measuring real RAM (the recursion's 2*2^n
 * doubles) and wall-time per call. engine_exp's C_V has had all fixed order-buffers removed (VLAs +
 * OOM-safe malloc, v26), so the only wall is RAM (2*2^n*8 bytes) or time (~3^n).
 *
 * CRASH SAFETY (default, no flags needed):
 *   - every completed row is written to a log file AND flushed immediately, so the data survives a
 *     Ctrl-C, a kill, or a crash mid-run -- whatever completed is already on disk;
 *   - a RAM-budget guard stops gracefully BEFORE an allocation would exceed available RAM (so the
 *     run never actually OOMs); C_V itself is OOM-safe (returns NaN) as a backstop;
 *   - SIGINT (Ctrl-C) / SIGTERM print the log path (all completed rows are there) and exit cleanly.
 *
 * Build (against either engine):
 *   gcc -O2 -Iengine_exp stress_cv.c engine_exp/cdet_engine.c engine_exp/lattices.c \
 *       engine_exp/quad.c engine_exp/schur.c engine_exp/rankone.c engine_exp/symmetry.c -lm
 * Run:  ./a.out [nmax] [time_budget_s] [logpath]
 */
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <time.h>
#include <signal.h>
#include <unistd.h>
#include <string.h>
#include "cdet_engine.h"
#include "lattices.h"

static FILE *g_log = NULL;
static char g_logpath[512] = "stress_cv_log.txt";

/* async-signal-safe handler: the log already holds every completed row (flushed per row),
 * so we just point the user at it and exit. */
static void on_signal(int sig) {
    (void)sig;
    const char *m = "\n[interrupted] partial data already saved to: ";
    ssize_t w = write(2, m, strlen(m)); (void)w;
    w = write(2, g_logpath, strlen(g_logpath));
    w = write(2, "\n", 1);
    _exit(130);
}

static double now_s(void) {
    struct timespec ts; clock_gettime(CLOCK_MONOTONIC, &ts);
    return ts.tv_sec + ts.tv_nsec * 1e-9;
}

static double avail_ram_bytes(void) {
    long pages = sysconf(_SC_AVPHYS_PAGES), ps = sysconf(_SC_PAGE_SIZE);
    if (pages <= 0 || ps <= 0) return 2e9;
    return (double)pages * (double)ps;
}

int main(int argc, char **argv) {
    int nmax = argc > 1 ? atoi(argv[1]) : 40;
    double tbudget = argc > 2 ? atof(argv[2]) : 120.0;
    if (argc > 3) { strncpy(g_logpath, argv[3], sizeof(g_logpath) - 1); }

    struct sigaction sa; memset(&sa, 0, sizeof(sa)); sa.sa_handler = on_signal;
    sigaction(SIGINT, &sa, NULL); sigaction(SIGTERM, &sa, NULL);

    g_log = fopen(g_logpath, "w");
    double beta = 4.0; LatticeCtx c; hexring_init(&c, beta, 0.7, 1.0);
    double avail = avail_ram_bytes();

    printf("# C_V stress (buffer-free). available RAM ~ %.2f GB ; time budget %.0f s ; log: %s\n",
           avail / 1e9, tbudget, g_logpath);
    printf("#  n | C_V RAM (2*2^n*8) | wall-time/call | 3^n\n");
    if (g_log) {
        fprintf(g_log, "# n  ram_bytes  ram_MB  time_s  3^n  status   (avail %.2f GB, budget %.0f s)\n",
                avail / 1e9, tbudget);
        fflush(g_log);
    }

    Vertex *V = (Vertex *)malloc((size_t)(nmax + 1) * sizeof(Vertex));  /* dynamic, no fixed cap */
    if (!V) { fprintf(stderr, "vertex alloc failed\n"); return 1; }

    for (int n = 1; n <= nmax; n++) {
        double ram = 2.0 * ldexp(1.0, n) * 8.0;
        if (ram > 0.90 * avail) {
            printf("-> RAM wall at n=%d (needs %.2f GB of %.2f GB) -- stopping gracefully\n",
                   n, ram / 1e9, avail / 1e9);
            if (g_log) { fprintf(g_log, "# RAM wall at n=%d (needs %.2f GB of %.2f GB)\n",
                                  n, ram / 1e9, avail / 1e9); fflush(g_log); }
            break;
        }
        for (int k = 0; k < n; k++) { V[k].site = k % 6; V[k].tau = beta * (k + 0.5) / n; }
        double t0 = now_s();
        double r = C_V(V, n, 0, 1.5, 0, 0.5, lattice_G0, &c);
        double dt = now_s() - t0;
        int ok = (r == r);  /* NaN -> allocation failed inside C_V */
        printf("  %2d | %8.3g B (%8.3g MB) | %10.4g s | %.3g %s\n",
               n, ram, ram / 1e6, dt, pow(3.0, n), ok ? "" : "[ALLOC-FAILED]");
        fflush(stdout);
        if (g_log) {
            fprintf(g_log, "%d %.0f %.6g %.6g %.6g %s\n",
                    n, ram, ram / 1e6, dt, pow(3.0, n), ok ? "ok" : "alloc-failed");
            fflush(g_log);   /* persist this row NOW -- survives Ctrl-C / kill / crash */
        }
        if (!ok) { printf("-> C_V allocation failed at n=%d (OOM-safe)\n", n); break; }
        if (dt > tbudget) {
            printf("-> time wall (>%.0f s/call) at n=%d\n", tbudget, n);
            if (g_log) { fprintf(g_log, "# time wall at n=%d\n", n); fflush(g_log); }
            break;
        }
    }
    free(V);
    if (g_log) { fprintf(g_log, "# done\n"); fclose(g_log); }
    printf("# full log saved: %s\n", g_logpath);
    return 0;
}

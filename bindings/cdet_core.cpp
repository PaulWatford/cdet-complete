// cdet_core -- native pybind11 bindings to the FROZEN reference engine (read-only; engine source untouched).
// Lets Python call the frozen C physics primitives directly, eliminating subprocess overhead for programmatic use.
// Because these are literally the frozen functions compiled in, results are bit-identical to the 194/194 engine.
#include <pybind11/pybind11.h>
extern "C" {
#include "cdet_engine.h"
#include "lattices.h"
}
namespace py = pybind11;

// 2D plane-wave free propagator (builds the O(L) context, then evaluates one entry)
static double square2d_g0(int L, double beta, double mu, double t, int i, int j, double tau) {
    Square2DPW c;
    square2d_pw_init(&c, L, beta, mu, t);
    return square2d_G0_pw(i, j, tau, &c);
}

PYBIND11_MODULE(cdet_core, m) {
    m.doc() = "native bindings to the frozen CDet reference engine (no subprocess; bit-identical to 194/194)";
    m.def("G0_atom", &G0_atom, "frozen band propagator G0_atom(tau, beta, mu)",
          py::arg("tau"), py::arg("beta"), py::arg("mu"));
    m.def("G_exact_atom", &G_exact_atom, "exact atom Green's function G_exact_atom(tau, beta, mu, U)",
          py::arg("tau"), py::arg("beta"), py::arg("mu"), py::arg("U"));
    m.def("density_exact", &density_exact, "exact atom density density_exact(beta, mu, U)",
          py::arg("beta"), py::arg("mu"), py::arg("U"));
    m.def("n_F", &n_F, "Fermi function n_F(xi, beta)", py::arg("xi"), py::arg("beta"));
    m.def("square2d_g0", &square2d_g0, "2D plane-wave free propagator (frozen-engine band function)",
          py::arg("L"), py::arg("beta"), py::arg("mu"), py::arg("t"), py::arg("i"), py::arg("j"), py::arg("tau"));
}

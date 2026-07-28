# Limitations and deviations

The paper provides neither Figure 3's numeric coordinates nor its values of
`L,h,K,Nw,prec`, so an exact coordinate comparison is impossible. This
reproduction fixes and reports those values and measures grid/quadrature
convergence.

The formal workload has uncertain runtime and uses multiprocessing. It is
therefore routed to Hugging Face `cpu-upgrade`, never to local CPU or GPU.

Numerical evidence validates the accountant over the declared suite; it does
not replace the composition theorem. Tightness follows from computing the
composed PRV's hockey-stick divergence rather than a relaxation, with
discretization error diagnosed separately.

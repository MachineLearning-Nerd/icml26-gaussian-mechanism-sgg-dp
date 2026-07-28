# Claim C5 method

The verifier implements Algorithm 7 directly:

1. transform `t=beta*r^p`, for which `t` is Gamma distributed;
2. evaluate Lemma D.1 with generalized Gauss-Laguerre quadrature;
3. invert the monotone angular privacy-loss map on a dense lookup grid;
4. form bin masses from CDF differences;
5. compute linear FFT convolutions, cropping to the declared support after
   multiplication;
6. integrate `(1-exp(epsilon-Z))_+` against the composed PRV.

The exact Figure 3 regime is calibrated by independent root searches, not by
using formula-derived sample counts. The broader sweep covers six SGG shapes,
three common dimensionless sensitivities `beta^(1/p)*s`, and four composition
counts. Coarse/fine convergence is checked for all 72 cases. An independent
160-node quadrature is compared with an adaptive radial integral at 45 l2 CDF
points, and direct polynomial convolution checks the FFT result.

Controls deliberately use circular FFT without zero-padding, omit Gamma
normalization, and reverse the privacy-loss sign. Each must be rejected.

# Claim C1 method

This route replaces the rejected single-anisotropic-Gaussian spot check with an
independently reconstructed symbolic derivation:

1. `M^T M=I` gives `||Mx||^2=||x||^2` pointwise, hence equality of expectations.
2. Haar left invariance gives `QMX =_d MX` for every orthogonal `Q`, which is the
   definition of spherical symmetry.
3. Joint convexity of hockey-stick divergence under mixtures follows from
   convexity of the positive-part function.
4. Conditioning on `M`, applying the bijection `M^T`, and using
   `||M^Tv||=||v||` bounds every symmetrized shift by the original
   worst-direction supremum.

The verifier checks the dependency DAG, exact symbolic isometry algebra, the
two exhaustive sign cases for positive-part convexity, and three intentionally
invalid mutations.


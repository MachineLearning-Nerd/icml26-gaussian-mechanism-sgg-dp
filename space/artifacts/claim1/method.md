# Claim C0 method

The proof certificate reconstructs the complete implication:

1. Haar-symmetrize arbitrary noise without increasing privacy delta or changing
   MSE.
2. Represent the symmetrized noise as `R_T U_T`.
3. Verify the exact finite-`T` algebra of the paper's threshold test
   `S_T`.
4. Use the uniform CDF convergence of `sqrt(T) U_{T,1}` to a standard normal
   to obtain `delta_T >= E[g(R_T^2/T)] + o(1)`.
5. Verify the supporting-line Jensen identity and the eventual-convexity /
   vanishing-intercept argument that creates a non-vacuous `delta_star`.
6. Combine with `E[R_T^2/T]=u0` and the Haar privacy order to obtain the
   theorem's limit inferior.

An independent checker evaluates the exact spherical-coordinate beta CDF for
dimensions 2 through 65,536, four epsilon values, and four radial-law families,
including a `T`-dependent rare-spike law. These data only calibrate the
asymptotic step.

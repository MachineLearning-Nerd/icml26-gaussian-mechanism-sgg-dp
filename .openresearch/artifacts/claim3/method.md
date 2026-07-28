# Claim C2 method

The normalization check applies the independent substitution
`t = beta * r^p`, reducing the integral to `Gamma(k)/Gamma(k)` with
`k=(alpha+1)/p`. The two special cases use the exact generalized-gamma second
moment `E[R^2] = beta^(-2/p) Gamma((alpha+3)/p)/Gamma((alpha+1)/p)`.

The code checks three admissible non-special parameter tuples and the two
closed-form mechanisms. This is an identity check rather than a stochastic
estimate.


# Paper Claim 5 method

The independent checker uses the analytic first derivative of the Gaussian
privacy curve. Tangent dominance is checked on 12,000 left-grid points and
convexity by monotonicity of the analytic derivative on 12,000 right-grid
points. This differs from the retained central-second-difference checker.
An out-of-regime mutation at `epsilon=1,delta=0.9` must fail.

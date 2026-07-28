# Paper Claim 4 method

Eight independently scrambled Sobol replicates of 32,768 points calibrate
each of the three displayed SGG configurations. The report gives a
replicate-based 95% half-width. The exact Gaussian special case is a negative
control: replacing `p>2` by `p=2,alpha=T-1` has exactly zero MSE reduction.

The original judged 15.0%, 12.6%, and 10.5% values remain preserved. The
independent QMC checker tests magnitude and trend without claiming identical
unpublished optimizer coordinates.

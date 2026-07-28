# Claim C5 / paper Claim 6 source audit

Source: arXiv:2606.08681v1, Section 4.4, Lemma D.1, Algorithm 7
(`alg7`), Figure 3, and Appendix D. Retrieved 2026-07-28 from ar5iv with
an explicit reproduction User-Agent. Saved HTML SHA-256:
`a02952f28208ebacabb7e555436985040f909dd881786f74d71cd4aee7841a38`.

Algorithm 7 takes `T,s,(alpha,beta,p),k,epsilon`, truncation `L`, grid step
`h`, radial quadrature size `K`, angular grid `Nw`, and precision. It
discretizes the exact Lemma D.1 PRV CDF, performs `k`-fold FFT convolution
with cropping after multiplication, and evaluates the hockey-stick payoff.

Figure 3 fixes `T=10`, `alpha=9`, `p=1`, total
`(epsilon,delta)=(1,1e-5)`, and `k in {2,4,8,16,32}`. It compares the
minimal per-invocation MSE under sequential allocation
`(epsilon/k,delta/k)` against Algorithm 7 and claims a clear, growing gap.
The paper does not publish the plotted coordinates or numerical settings.

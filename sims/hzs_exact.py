# High-resolution uniform quantizer: given S, Z = S/Δ - E, E = sum of K iid U(-1/2,1/2) rounding errors.
# P(Z=z | S) ∝ f_K(t - z), t = frac offset of S/Δ. H(Z|S) = average over t of entropy of that pmf.
import math
from fractions import Fraction
def irwin_hall_pdf(x,K):  # sum of K U(0,1)
    if x<0 or x>K: return 0.0
    return sum((-1)**j*math.comb(K,j)*(x-j)**(K-1) for j in range(int(math.floor(x))+1))/math.factorial(K-1)
def f(x,K):  # centered: sum of K U(-1/2,1/2)
    return irwin_hall_pdf(x+K/2,K)
def H_given_t(t,K):
    zs=range(-K-2,K+3); p=[f(t-z,K) for z in zs]; s=sum(p)
    return -sum(q/s*math.log2(q/s) for q in p if q>0)
for K in [2,4,8,16]:  # K>=32는 부동소수점 상쇄로 계산 불가
    T=200; h=sum(H_given_t((i+0.5)/T,K) for i in range(T))/T
    print(f"K={K:3d}  H(Z|S)={h:.3f}  ½log2(2πeK/12)={0.5*math.log2(2*math.pi*math.e*K/12):.3f}  ½log2K={0.5*math.log2(K):.3f}")

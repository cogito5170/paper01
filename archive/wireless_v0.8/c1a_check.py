"""정리 C1-a(SPEC 6.3) 수치 검증. 표준 라이브러리만 사용.

설정: 이진 가설, 단말 K개, 관측 X_k ∈ {0,1}, P0(X=1)=p0, P1(X=1)=p1.
우도비 상한 L = max(p1/p0, (1-p0)/(1-p1)).
채널 사용 m=1. 서버가 보는 것은 Y = Σ h_k x_k + Z.

비교하는 경우
  (A) Rayleigh, CSI 없음  : |Y|^2 ~ Exp(평균 N0 + S),  S = Σ|x_k|^2   (정리 C1-a의 대상)
  (B) 동일 채널(h_k = 1) : Y = √a·N + Z, 복소 가우시안 Z            (코히런트 결합 기준점)

설계
  on/off  : X_k=1이면 진폭 √a로 송신 (a = P)
  sparse  : X_k=1이고 사적 난수 U_k < q(=λ/K)이면 진폭 √(P/q)로 송신 (드물고 큰 진폭)
두 설계 모두 송신 단말 수 N ~ Bin(K, θ·p_H)이고 S = a·N 이다.

각 K에 대해 최적(Bayes, 사전확률 1/2) 오류 P_e = ½∫min(q0, q1)를 수치 적분으로 정확히 계산하고,
정리의 하한 c(L, m) = ¼ (2L)^(-4m) β(2L)^(2m),  β(r) = 2√r/(1+r) 과 비교한다.
"""

import math


def binom_pmf(K, p):
    """Bin(K, p)의 pmf 리스트 (로그 공간에서 계산)."""
    if p <= 0.0:
        return [1.0] + [0.0] * K
    if p >= 1.0:
        return [0.0] * K + [1.0]
    lp, lq = math.log(p), math.log1p(-p)
    lg = math.lgamma
    return [math.exp(lg(K + 1) - lg(n + 1) - lg(K - n + 1) + n * lp + (K - n) * lq)
            for n in range(K + 1)]


def trim(pmf, tol=1e-15):
    """무시할 만한 질량을 버리고 (n, w) 쌍만 남긴다."""
    return [(n, w) for n, w in enumerate(pmf) if w > tol]


def pe_rayleigh_nocsi(K, p0, p1, theta, a, N0=1.0, grid=4000):
    """(A) |Y|^2 = (N0 + aN)·E, E ~ Exp(1). t = log|Y|^2 위에서 적분."""
    w0 = trim(binom_pmf(K, theta * p0))
    w1 = trim(binom_pmf(K, theta * p1))
    smax = N0 + a * max(n for n, _ in w0 + w1)
    lo, hi = math.log(N0) - 25.0, math.log(smax) + 4.0
    dt = (hi - lo) / grid

    def dens(t, w):  # t = log y 의 밀도: Σ w_n · (y/s) e^{-y/s}
        y = math.exp(t)
        tot = 0.0
        for n, wn in w:
            s = N0 + a * n
            u = y / s
            if u < 700:
                tot += wn * u * math.exp(-u)
        return tot

    acc = 0.0
    for i in range(grid):
        t = lo + (i + 0.5) * dt
        acc += min(dens(t, w0), dens(t, w1))
    return 0.5 * acc * dt


def pe_equal_channel(K, p0, p1, theta, a, N0=1.0, grid=6000):
    """(B) Y = √a·N + Z, Z ~ CN(0, N0). 허수부는 정보가 없으므로 실수부만 적분 (분산 N0/2)."""
    w0 = trim(binom_pmf(K, theta * p0))
    w1 = trim(binom_pmf(K, theta * p1))
    sd = math.sqrt(N0 / 2)
    ra = math.sqrt(a)
    lo = -8 * sd
    hi = ra * max(n for n, _ in w0 + w1) + 8 * sd
    dx = (hi - lo) / grid
    c = 1.0 / (sd * math.sqrt(2 * math.pi))

    def dens(x, w):
        tot = 0.0
        for n, wn in w:
            z = (x - ra * n) / sd
            if abs(z) < 38:
                tot += wn * math.exp(-0.5 * z * z)
        return c * tot

    acc = 0.0
    for i in range(grid):
        x = lo + (i + 0.5) * dx
        acc += min(dens(x, w0), dens(x, w1))
    return 0.5 * acc * dx


def c1a_bound(L, m=1):
    beta = 2 * math.sqrt(2 * L) / (1 + 2 * L)
    return 0.25 * (2 * L) ** (-4 * m) * beta ** (2 * m)


def coupling_check(K, m, L_target=2.0, trials=4000, seed=0):
    """보조정리 4의 커플링을 직접 구성해 P(E0 ∩ E1)을 몬테카를로로 추정.

    단말 k의 에너지 벡터 A_k ∈ R_+^m 은 유한 집합 위의 분포 p0_k, p1_k를 따른다 (단말마다 다름,
    꼬리가 두꺼운 값 포함). 공통 질량 c = min(p0, p1)으로 B_k ~ Bern(γ_k)를 만들고
    B_k=1이면 A^0_k = A^1_k ~ c/γ_k, 아니면 각자 잔여분포에서 독립 추출.
    E_H = {∀j: N0 + S^H_j ≤ 2L (N0 + W_j)},  W_j = Σ_k B_k A^0_kj.
    증명이 주는 하한은 (2L)^(-2m).
    """
    import random
    rng = random.Random(seed)
    N0 = 1.0
    terms = []
    for _ in range(K):
        n_sup = 4
        support = [tuple(rng.choice([0.0, 0.0, 1e-3, 1.0, 50.0, 1e4]) for _ in range(m))
                   for _ in range(n_sup)]
        base = [rng.random() + 0.05 for _ in range(n_sup)]
        z = sum(base)
        p0 = [b / z for b in base]
        tilt = [rng.uniform(1 / L_target, L_target) for _ in range(n_sup)]
        z1 = sum(p * t for p, t in zip(p0, tilt))
        p1 = [p * t / z1 for p, t in zip(p0, tilt)]
        c = [min(a, b) for a, b in zip(p0, p1)]
        g = sum(c)
        r0 = [(a - x) / (1 - g) if g < 1 else 0 for a, x in zip(p0, c)]
        r1 = [(b - x) / (1 - g) if g < 1 else 0 for b, x in zip(p1, c)]
        terms.append((support, g, c, r0, r1, p0, p1))
    L = max(max(max(a / b, b / a) for a, b in zip(t[5], t[6])) for t in terms)

    def draw(support, weights):
        return support[rng.choices(range(len(support)), weights=weights)[0]]

    hit = 0
    for _ in range(trials):
        S0, S1, W = [0.0] * m, [0.0] * m, [0.0] * m
        for support, g, c, r0, r1, _, _ in terms:
            if rng.random() < g:
                a = draw(support, c)
                a0 = a1 = a
                for j in range(m):
                    W[j] += a[j]
            else:
                a0, a1 = draw(support, r0), draw(support, r1)
            for j in range(m):
                S0[j] += a0[j]
                S1[j] += a1[j]
        if all(N0 + S0[j] <= 2 * L * (N0 + W[j]) and N0 + S1[j] <= 2 * L * (N0 + W[j])
               for j in range(m)):
            hit += 1
    return L, hit / trials, (2 * L) ** (-2 * m)


def main():
    print("[1] 보조정리 4 커플링: P(E0∩E1) 추정 vs 증명 하한 (2L)^(-2m)")
    for K, m in [(10, 1), (200, 1), (10, 2), (200, 2), (1000, 3)]:
        L, est, lb = coupling_check(K, m, trials=1500 if K >= 1000 else 4000)
        print(f"  K={K:>5}, m={m}: L={L:.2f}, 추정 {est:.3f} ≥ 하한 {lb:.2e} : {est >= lb}")
    print()
    print("[2] 최적 Bayes 오류 P_e (정확한 수치 적분)")
    p0, p1 = 1 / 3, 2 / 3
    L = max(p1 / p0, (1 - p0) / (1 - p1))
    P, N0, lam = 1.0, 1.0, 1.0
    print(f"p0={p0:.3f}, p1={p1:.3f}, L={L:.1f}, P/N0={P / N0}, m=1")
    print(f"정리 C1-a 하한 c(L,1) = {c1a_bound(L):.3e}\n")
    print(f"{'K':>6} | {'(A) on/off':>12} {'(A) sparse':>12} | {'(B) on/off':>12}")
    print("-" * 52)
    for K in [1, 2, 5, 10, 20, 50, 100, 200, 500, 1000]:
        q = min(1.0, lam / K)
        a_on = pe_rayleigh_nocsi(K, p0, p1, 1.0, P, N0)
        a_sp = pe_rayleigh_nocsi(K, p0, p1, q, P / q, N0)
        b_on = pe_equal_channel(K, p0, p1, 1.0, P, N0) if K <= 200 else float("nan")
        print(f"{K:>6} | {a_on:>12.4e} {a_sp:>12.4e} | {b_on:>12.4e}")


if __name__ == "__main__":
    main()

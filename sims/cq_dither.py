# 합 오차 분산 비율(독립 디더 = 1 기준): 감산 디더 균일 양자화, 가우시안 입력
import random, math
random.seed(0)
def run(N,sigma,corr,T=6000,D=1.0):
    acc=0.0
    for _ in range(T):
        if corr:
            V=random.random(); p=list(range(N)); random.shuffle(p)
            u=[D*(p[i]+V)/N for i in range(N)]
        else:
            u=[D*random.random() for _ in range(N)]
        e=0.0
        for i in range(N):
            x=random.gauss(0,sigma)
            e+=D*round((x+u[i])/D)-u[i]-x
        acc+=e*e
    return acc/T/(N*D*D/12)
for s in [0.01,0.1,0.3,1.0,10.0]:
    print(f"sigma/Delta={s:5}", "  ".join(f"N={N}: indep {run(N,s,False):.2f} corr {run(N,s,True):.3f}" for N in [4,64]))

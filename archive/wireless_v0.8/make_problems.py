"""Generate one HTML page per research problem; PDFs are printed afterwards with headless Chrome."""
import os, sys

OUT = sys.argv[1]
os.makedirs(OUT, exist_ok=True)
TOTAL = 6

CSS = r"""
@page { size: A4; margin: 16mm 15mm 16mm 15mm; }
* { box-sizing: border-box; }
body { margin: 0; color: #141414; background: #fff;
  font-family: "Gowun Batang", "Batang", serif; font-size: 10.6pt; line-height: 1.72; }
.mast { display: grid; grid-template-columns: 1fr 34mm; border: 1.6pt solid #111; }
.mast .l { padding: 3.2mm 6mm; display: grid; gap: 0.6mm; text-align: center; }
.mast .org { font-family: "Black Han Sans", sans-serif; font-size: 13pt; letter-spacing: 0.14em; }
.mast .ttl { font-family: "Black Han Sans", sans-serif; font-size: 19pt; letter-spacing: 0.04em; }
.mast .r { border-left: 1.6pt solid #111; display: grid; grid-template-rows: auto 1fr; text-align: center; }
.mast .r span { font-family: "Black Han Sans", sans-serif; font-size: 11pt; letter-spacing: 0.3em;
  border-bottom: 1.6pt solid #111; padding: 0.8mm 0; }
.mast .r b { font-family: Georgia, serif; font-size: 34pt; display: grid; place-items: center; line-height: 1; }
.status { margin-top: 3mm; display: flex; gap: 2.5mm; flex-wrap: wrap; font-family: "IBM Plex Sans KR", sans-serif; font-size: 8.8pt; }
.status span { border: 0.8pt solid #111; padding: 0.2mm 2.2mm; }
.status .warn { border-color: #8a1f1f; color: #8a1f1f; font-weight: 600; }
h2 { font-family: "IBM Plex Sans KR", sans-serif; font-size: 10.6pt; font-weight: 600; margin: 5mm 0 1.6mm;
  padding-bottom: 0.8mm; border-bottom: 0.8pt solid #111; letter-spacing: 0.02em; }
p { margin: 0 0 1.6mm; }
.box { border: 0.9pt solid #111; padding: 3mm 4.5mm; background: #f6f6f2; }
.task { border: 1.4pt solid #111; padding: 3.2mm 4.5mm; }
.task .head { font-weight: 700; margin-bottom: 1.2mm; }
.pts { font-family: "IBM Plex Sans KR", sans-serif; font-size: 8.8pt; color: #555; }
ol.sub { list-style: none; padding: 0; margin: 0; display: grid; gap: 1.6mm; }
ol.sub li { display: grid; grid-template-columns: 7mm 1fr; }
ul.facts { margin: 0; padding-left: 5mm; display: grid; gap: 1mm; }
ol.dir { margin: 0; padding-left: 5.5mm; display: grid; gap: 1.6mm; }
.note { font-size: 9.6pt; color: #3d3d3d; }
.dep { font-family: "IBM Plex Sans KR", sans-serif; font-size: 8.8pt; color: #333; }
.work { margin-top: 5mm; border: 0.9pt solid #111; min-height: 70mm; padding: 2mm 3mm;
  font-family: "IBM Plex Sans KR", sans-serif; font-size: 8.8pt; color: #555; break-inside: avoid; }
.foot { margin-top: 4mm; text-align: center; font-family: "IBM Plex Sans KR", sans-serif; font-size: 8.5pt; color: #555; }
mjx-container[display="true"] { margin: 1.4mm 0 !important; }
"""

HEAD = r"""<!doctype html><html lang="ko"><head><meta charset="utf-8"><title>{title}</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Black+Han+Sans&family=Gowun+Batang:wght@400;700&family=IBM+Plex+Sans+KR:wght@400;600&display=swap">
<script>window.MathJax={{tex:{{inlineMath:[['\\(','\\)']],displayMath:[['\\[','\\]']]}},svg:{{fontCache:'global'}}}};</script>
<script src="https://cdn.jsdelivr.net/npm/mathjax@3.2.2/es5/tex-svg.js"></script>
<style>{css}</style></head><body>"""


def page(n, title, status, setting, task_head, task_items, facts, directions, dep, note=""):
    items = "".join((f"<li><span>({k})</span><span>{v}</span></li>" if k else f"<li style=\"display:block\">{v}</li>") for k, v in task_items)
    fact_html = "".join(f"<li>{f}</li>" for f in facts) if facts else "<li>없음</li>"
    dir_html = "".join(f"<li>{d}</li>" for d in directions)
    stat = "".join(f'<span class="{c}">{t}</span>' for c, t in status)
    html = HEAD.format(title=title, css=CSS) + f"""
<div class="mast"><div class="l"><div class="org">연구 문제지 · 확률론</div><div class="ttl">{title}</div></div>
<div class="r"><span>문제</span><b>{n}</b></div></div>
<div class="status">{stat}</div>
<h2>설정</h2><div class="box">{setting}</div>
<h2>증명할 명제 (서술형)</h2>
<div class="task"><p class="head">{task_head}</p><ol class="sub">{items}</ol></div>
{f'<p class="note" style="margin-top:2mm">{note}</p>' if note else ''}
<h2>인용 가능한 알려진 사실 (증명하지 않아도 됨)</h2><ul class="facts">{fact_html}</ul>
<h2>추천 방향</h2><ol class="dir">{dir_html}</ol>
<h2>다른 문제와의 관계</h2><p class="dep">{dep}</p>
<div class="work">풀이</div>
<div class="foot">문제 {n} / {TOTAL}</div>
</body></html>"""
    with open(os.path.join(OUT, f"problem{n}.html"), "w", encoding="utf-8") as f:
        f.write(html)


UNVERIFIED = [("warn", "미검증: 증명 초안은 있으나 사람이 확인하지 않음"), ("", "답안 없음")]

COMMON_DEF = r"""<p><b>기호.</b> 평균이 \(a>0\)인 지수분포 \(\mathrm{Exp}(a)\)의 밀도는 \(\tfrac1a e^{-x/a}\;(x>0)\). <b>표준 복소 가우시안</b>은 실수부·허수부가 독립이고 각각 \(N(0,\tfrac12)\)인 복소 확률변수이며, \(\mathcal{CN}(0,\sigma^2)\)은 그것에 \(\sigma\)를 곱한 분포이다.
두 확률밀도 \(p,q\)에 대하여 \(P_e(p,q)=\tfrac12\int\min(p,q)\)(사전확률 \(\tfrac12\)씩일 때의 최소 오류 확률), \(\rho(p,q)=\int\sqrt{pq}\)(Bhattacharyya 계수), \(\beta(r)=\dfrac{2\sqrt r}{1+r}\).</p>"""

LR_DEF = r"""<p><b>우도비 조건.</b> 실수 \(L\ge1\)에 대하여 두 확률측도 \(P^0,P^1\)이 서로 절대연속이고 \(\tfrac1L\le \tfrac{dP^1}{dP^0}\le L\)일 때 ‘\((P^0,P^1)\)이 우도비 조건 \(L\)을 만족한다’고 한다. 측도론이 낯설면 유한집합 값의 경우 \(\tfrac1L\le P^1(x)/P^0(x)\le L\)로 읽어도 된다.</p>"""

MAIN_SETTING = r"""<p>양의 정수 \(m,K\), 실수 \(L\ge1\). 각 \(k=1,\dots,K\)에 대하여 \([0,\infty)^m\) 위의 두 확률측도 \(P_k^0,P_k^1\)이 우도비 조건 \(L\)을 만족한다(\(k\)마다 달라도 됨). <b>가설 \(i\in\{0,1\}\) 아래에서</b> \(A_1,\dots,A_K\)는 서로 독립, \(A_k\sim P_k^i\)이고 \(S=\sum_k A_k\in[0,\infty)^m\).</p>"""

# ---------------- Problem 1 ----------------
page(1, "수신 신호의 구조", UNVERIFIED,
     COMMON_DEF + r"""
<p>복소수 \(x_{kj}\) \((k=1,\dots,K,\ j=1,\dots,m)\)에 대하여, 서로 독립인 표준 복소 가우시안 \(h_{kj}, Z_j\)로
\[ Y_j=\sum_{k=1}^K h_{kj}\,x_{kj}+Z_j,\qquad S_j=\sum_{k=1}^K |x_{kj}|^2 \]
라 하자. 이어서 \(x=(x_{kj})\)가 \((h,Z)\)와 독립인 확률변수이고, 두 가설 \(i\in\{0,1\}\)에서 \(x\)의 분포만 다르다고 하자(\(h,Z\)의 분포는 같음). 가설 \(i\) 아래 \(Y=(Y_1,\dots,Y_m)\)의 분포를 \(Q_i^Y\), \(W=(|Y_1|^2,\dots,|Y_m|^2)\)의 분포를 \(Q_i^W\)라 한다.</p>""",
     "다음을 증명하시오.",
     [("가", r"\(x\)가 상수이면 \(Y_1,\dots,Y_m\)은 서로 독립이고 \(Y_j\sim\mathcal{CN}(0,1+S_j)\)."),
      ("나", r"\(x\)가 확률변수이면, \(Y\)의 분포는 \(x\)를 통해 \(S=(S_1,\dots,S_m)\)에만 의존한다. 또 \(S\)가 주어지면 \(W_j=(1+S_j)E_j\)로 쓸 수 있다. 여기서 \(E_1,\dots,E_m\)은 \(S\)와 독립인 i.i.d. \(\mathrm{Exp}(1)\)."),
      ("다", r"\(P_e(Q_0^Y,Q_1^Y)=P_e(Q_0^W,Q_1^W)\). 즉 \(Y\) 대신 \(W\)만 봐도 두 가설을 구분하는 최소 오류 확률은 같다.")],
     [r"독립인 가우시안 벡터의 선형 결합은 가우시안이다.",
      r"\(\mathcal{CN}(0,\sigma^2)\)의 제곱 크기는 \(\mathrm{Exp}(\sigma^2)\)를 따르고, 위상은 크기와 독립이며 균등분포이다.",
      r"충분통계량이면 최소 오류 확률이 보존된다(Fisher–Neyman 분해 정리)."],
     [r"(가): 복소 확률변수를 실수 2차원 벡터로 보고, 각 \(j\)마다 \(Y_j\)의 실수부·허수부의 공분산 행렬을 계산한다. 서로 다른 \(j\)는 서로 다른 \(h_{kj}, Z_j\)를 쓴다는 점에 주목한다.",
      r"(나): \(x\)로 조건부를 걸면 (가)가 그대로 적용된다. 조건부 밀도 \(\prod_j \frac{1}{\pi(1+S_j)}e^{-|y_j|^2/(1+S_j)}\)를 써 본다.",
      r"(다): 위 밀도를 \(S\)에 대해 평균한 \(Q_i^Y\)의 밀도가 \(y\)에 \(|y_j|^2\)들을 통해서만 의존함을 보이면, \(W\)가 두 가설 모두에 대해 충분통계량이 된다. 극좌표 변환의 야코비안이 두 가설에 공통이라는 점을 확인한다."],
     r"문제 3이 서버의 관측을 \(W\)로 바꿔 쓸 때 이 결과를 쓴다. 통신에서는 '채널 이득이 랜덤이고 아무도 모르면 서버가 보는 것은 단말 에너지 합 \(S\)의 잡음 섞인 사본뿐'이라는 뜻이다.")

# ---------------- Problem 2 ----------------
page(2, "곱셈 비교 보조정리", UNVERIFIED + [("warn", "핵심 문제")],
     LR_DEF + MAIN_SETTING + r"""
<p class="note">왜 어려운가: \(S\) 자체의 두 분포는 \(K\)가 커지면 완전히 갈라질 수 있다. 예를 들어 \(m=1\), \(A_k\in\{0,1\}\), \(P_k^0(1)=\tfrac13,\ P_k^1(1)=\tfrac23\)이면 \(S/K\)가 \(\tfrac13\)과 \(\tfrac23\)으로 따로 모인다. 두 합의 우도비는 \(L^K\)까지 커지므로 우도비를 직접 다루는 논법은 쓸 수 없다. 그러나 비율 \((1+S^0)/(1+S^1)\)은 위 예에서 2 근처에 머문다.</p>""",
     r"하나의 확률공간 위에 두 확률벡터 \((S^0,S^1)\)이 존재하여, \(S^0\)은 가설 0 아래 \(S\)의 분포를, \(S^1\)은 가설 1 아래 \(S\)의 분포를 따르고 다음이 성립함을 증명하시오.",
     [("", r"\[ P\!\left(\text{모든 } j \text{에 대해 } \frac{1}{2L}\le\frac{1+S^0_j}{1+S^1_j}\le 2L\right)\;\ge\;(2L)^{-2m}. \] 하한은 \(K\)에도, \(P_k^i\)의 모양에도 의존하지 않아야 한다.")],
     [r"<b>해리스(Harris) 부등식.</b> \(B=(B_1,\dots,B_K)\)가 서로 독립인 베르누이 변수이고 \(f,g\)가 \(\{0,1\}^K\) 위에서 각 좌표에 대해 증가하는 함수이면 \(E[f(B)g(B)]\ge E[f(B)]\,E[g(B)]\). 특히 증가 사건들의 교집합 확률은 각 확률의 곱 이상이다.",
      r"\([0,1]\) 값 확률변수 \(Z\)와 \(t\in[0,1]\)에 대하여 \(E[Z]\le t+P(Z\ge t)\)."],
     [r"<b>공통 질량으로 결합한다.</b> \(p_k^0,p_k^1\)을 밀도, \(c_k=\min(p_k^0,p_k^1)\), \(\gamma_k=\int c_k\)로 두면 우도비 조건에서 \(\gamma_k\ge 1/L\)이다. \(B_k\sim\mathrm{Bern}(\gamma_k)\)를 뽑아 \(B_k=1\)이면 두 가설에 같은 값 \(A_k^0=A_k^1\sim c_k/\gamma_k\)를, \(B_k=0\)이면 남은 질량 \((p_k^i-c_k)/(1-\gamma_k)\)에서 서로 독립으로 뽑는다. 이를 \(k\)마다 독립으로 한다. 확인할 것: 주변분포가 맞는가? \(A^0=(A_k^0)_k\)가 주어질 때 \(B_k\)들이 독립이고 \(P(B_k=1\mid A^0)=c_k(A_k^0)/p_k^0(A_k^0)\ge 1/L\)인가?",
      r"<b>두 합을 직접 비교하지 말고 공통 부분합과 비교한다.</b> \(T_j=\sum_k B_kA^0_{kj}\)로 두면 \(T_j\le S^0_j\), \(T_j\le S^1_j\)이다.",
      r"<b>한 방향.</b> \(E_0=\{\text{모든 } j:\ S^0_j\le 2L\,T_j\}\)에 대하여 \(A^0\)의 모든 값에서 \(P(E_0\mid A^0)\ge(2L)^{-m}\)을 노린다. \(Z_j=T_j/S^0_j\)의 조건부 기댓값을 구해 위의 \([0,1]\) 부등식을 \(t=\tfrac1{2L}\)로 쓰고, 각 사건이 \(B\)에 대해 증가함을 이용해 해리스 부등식으로 \(j\)들을 묶는다. \(E_1=\{\text{모든 } j:\ S^1_j\le 2L\,T_j\}\)도 대칭적으로 다룬다.",
      r"<b>두 방향 동시.</b> \(A^0\)를 고정하면 \(1_{E_0}\)은 \(B\)의 증가 함수이다. \(f_1(B)=P(E_1\mid A^0,B)\)도 증가 함수인지 확인한다(\(B_k\)를 0에서 1로 바꾸면 \(E_1\)의 부등식 양변이 각각 어떻게 변하는가?). 해리스 부등식을 조건부로 적용한 뒤 \(A^0\)에 대해 평균한다. 앞 단계의 하한이 \(A^0\)에 대해 <b>점별로</b> 성립해야 이 단계가 작동한다.",
      r"<b>비율로 옮긴다.</b> \(E_0\cap E_1\) 위에서 \(S^0_j\le 2L\,T_j\le 2L\,S^1_j\)이고 \(2L\ge1\)임을 쓴다.",
      r"<b>의심할 곳.</b> 첫째 방향의 조건부 표현(결합밀도 계산)과 넷째 방향의 증가성. 이 두 곳이 틀리면 전체가 무너진다."],
     r"문제 3(정리 C1-a)의 핵심 재료이다. 문제 4·6은 문제 3을 거쳐 이 결과에 의존한다. 확률론 문헌에서 같은 형태의 결과는 아직 찾지 못했다.")

# ---------------- Problem 3 ----------------
page(3, "오류 확률의 하한 (정리 C1-a)", UNVERIFIED,
     COMMON_DEF + LR_DEF + r"""
<p><b>관측과 송신.</b> 가설 \(i\in\{0,1\}\) 아래에서 \(X_1,\dots,X_K\)는 서로 독립이고, 각 \(k\)에 대해 \(X_k\)의 두 분포 \((P_{X_k}^0,P_{X_k}^1)\)는 우도비 조건 \(L\)을 만족한다. 확률변수 \(V\)(공통 난수)와 \(U_1,\dots,U_K\)(개별 난수)는 서로 독립이고, \(X\)들과도 독립이며, 두 가설에서 분포가 같다. 임의의 가측함수 \(f_k\)로
\[ A_k=f_k(X_k,U_k,V)\in[0,\infty)^m,\qquad S=\sum_k A_k,\qquad W_j=(1+S_j)E_j \]
라 하자. 여기서 \(E_j\)는 다른 모든 것과 독립인 i.i.d. \(\mathrm{Exp}(1)\)이다. 가설 \(i\) 아래 \(W\)의 분포를 \(Q_i\)라 한다.</p>""",
     r"다음을 증명하시오. 하한은 \(K\)와 \(f_k\), \(U\), \(V\)의 선택에 무관해야 한다.",
     [("가", r"\(V=v\)를 고정하면 \(A_1,\dots,A_K\)는 각 가설 아래 독립이고, 각 \(k\)에 대해 \(A_k\)의 두 분포가 우도비 조건 \(L\)을 만족한다."),
      ("나", r"\(V\)가 상수일 때 \(\displaystyle P_e(Q_0,Q_1)\ \ge\ c(L,m)=\tfrac14\,(2L)^{-4m}\,\beta(2L)^{2m}\)."),
      ("다", r"\(V\)가 일반 확률변수일 때도 같은 하한이 성립한다.")],
     [r"\(P_e(p,q)\ge\tfrac14\rho(p,q)^2\) (Le Cam).",
      r"\(\rho\)는 곱 분포에서 곱이 된다: \(\rho(\bigotimes_j p_j,\bigotimes_j q_j)=\prod_j\rho(p_j,q_j)\).",
      r"\(\rho(\mathrm{Exp}(a),\mathrm{Exp}(b))=\beta(a/b)\). \(\beta(r)\)는 \(|\log r|\)에 대해 감소한다.",
      r"결합 오목성: 쌍 \((s,t)\) 위의 확률측도 \(\pi\)에 대해 \(p=\int p_s\,d\pi\), \(q=\int q_t\,d\pi\)이면 \(\rho(p,q)\ge\int\rho(p_s,q_t)\,d\pi\).",
      r"문제 2의 결과(곱셈 비교 보조정리). 단 문제 2는 미검증이므로, 문제 3의 증명은 '문제 2가 참이면'이라는 조건부 증명이 된다."],
     [r"(가): 가측함수에 의한 상(push-forward)이 우도비의 범위를 보존함을 보인다. 사건 \(B\)에 대해 \(P^1(A_k\in B)=\int 1_B(f_k(x,u,v))\,dP_{X_k}^1(x)\,dP_U(u)\)로 쓰고 \(dP^1_{X_k}\le L\,dP^0_{X_k}\)을 적분 안에 넣는다.",
      r"(나): \(S=s\)가 주어지면 \(W\)의 분포는 \(\bigotimes_j\mathrm{Exp}(1+s_j)\)이다. 문제 2의 결합 \(\pi\)를 결합 오목성의 \(\pi\)로 쓰고, 문제 2의 사건 위에서는 곱 성질과 \(\beta\)의 단조성으로, 사건 밖에서는 \(\rho\ge0\)으로 아래로 누른 뒤 Le Cam 부등식을 쓴다.",
      r"(다): \(Q_i=\int Q_i^{v}\,dP_V(v)\)로 쓰고 결합 오목성을 대각선 결합(\(s=t=v\))으로 적용한다.",
      r"검산: \(L=2,\ m=1\)이면 \(c=\tfrac1{1600}\). 수치 실험에서 실제 오류 확률은 약 \(0.375\)였으므로 하한은 느슨하지만 모순은 없다."],
     r"문제 1과 결합하면 통신 문제의 정리 C1-a가 된다: 채널 이득이 랜덤이고 아무도 모르면, 단말 수 \(K\)를 아무리 늘려도 판별 오류가 \(c(L,m)\) 아래로 내려가지 않는다. 문제 4·6이 이 결과를 쓴다.")

# ---------------- Problem 4 ----------------
page(4, "대역폭을 늘릴 때의 지수 상한", UNVERIFIED + [("warn", "문제 3에 의존")],
     COMMON_DEF + r"""
<p>문제 3의 설정에서 채널 사용 횟수 \(m\)이 \(K\)에 따라 정해진다고 하자: \(m=m_K\), \(\lim_{K\to\infty} m_K/K=b>0\). \(P_e^{(K)}\)를 \(K\)번째 설정에서 모든 \(f_k,U,V\)와 모든 판정 규칙에 대한 최소 오류 확률이라 한다.</p>
<p>비교 기준: 관측 \(X_k\)들이 i.i.d.이고 잡음 없이 전부 모일 때의 오류 지수는 \(E_{\mathrm{cent}}=-\min_{0\le\lambda\le1}\log\int (dP^0_X)^{\lambda}(dP^1_X)^{1-\lambda}\) (체르노프 정보)이다.</p>""",
     r"다음을 증명하시오.",
     [("가", r"문제 3의 하한 \(c(L,m)\)이 \(m\)이 \(K\)와 함께 커지는 경우에도 그대로 성립한다. 즉 증명의 어느 단계에도 \(K\)나 \(m\)에 대한 숨은 가정이 없다."),
      ("나", r"\(\displaystyle \limsup_{K\to\infty}\Bigl(-\tfrac1K\log P_e^{(K)}\Bigr)\ \le\ b\cdot c_1(L),\qquad c_1(L)=4\log(2L)+2\log\frac{1}{\beta(2L)}.\)"),
      ("다", r"\(X_k\in\{0,1\}\), \(P_X^0(1)=\tfrac13\), \(P_X^1(1)=\tfrac23\)인 경우 \(c_1\)과 \(E_{\mathrm{cent}}\)를 계산하고, (나)의 상한이 \(E_{\mathrm{cent}}\)보다 작아지는 \(b\)의 범위를 구하시오.")],
     [r"문제 3의 결과(미검증이므로 조건부)."],
     [r"(가): 문제 2와 문제 3의 증명을 다시 읽으며 \(K\), \(m\)이 들어가는 곳을 모두 표시한다. 상수가 \((2L)^{-2m}\)처럼 \(m\)에 대해 지수형으로만 나빠지고 \(K\)는 전혀 들어가지 않는지 확인한다.",
      r"(나): \(-\log P_e\le -\log c(L,m)\)을 \(m=m_K\)에 대해 쓰고 \(K\)로 나눈다.",
      r"(다): 대칭인 경우 체르노프 정보의 최소점은 \(\lambda=\tfrac12\)이다. \(L=2\)이다.",
      r"<b>남는 질문(열린 부분).</b> (다)에서 상한이 의미 있는 \(b\)의 범위가 매우 좁게 나올 것이다. 상수 \(c_1\)을 채널 사용 1회당 친화도를 더 정밀하게 계산해서 줄일 수 있는지, 그리고 문제 5의 하한과의 격차가 얼마인지가 다음 연구 과제이다."],
     r"통신에서는 '대역폭을 단말 수에 비례해 늘려야만 오류가 지수적으로 줄고, 그 지수는 대역폭 비율 \(b\)에 비례하는 이상을 넘지 못한다'는 뜻이다(추측 C2의 상한 쪽). 문제 5가 반대 방향(달성)이다.")

# ---------------- Problem 5 ----------------
page(5, "그룹 시간 슬롯 방식의 지수", UNVERIFIED,
     COMMON_DEF + r"""
<p>가설 \(i\) 아래 \(X_1,\dots,X_K\)는 i.i.d. \(\sim P_X^i\). 양의 정수 \(g\)에 대하여 \(K=g\,m\)이라 하고, 단말을 크기 \(g\)인 그룹 \(G_1,\dots,G_m\)으로 나눈다. 집합 \(D\)와 진폭 \(\alpha>0\)을 고정하고, 단말 \(k\in G_\ell\)은 슬롯 \(\ell\)에서만 \(x_{k\ell}=\sqrt\alpha\cdot 1\{X_k\in D\}\)를 보내고 다른 슬롯에서는 0을 보낸다. 서버는 문제 1처럼 \(W_\ell=|Y_\ell|^2\) \((\ell=1,\dots,m)\)를 본다. \(\pi_i=P_X^i(D)\)로 둔다.</p>""",
     r"다음을 증명하시오. (방식 하나에 대한 분석이므로, 모든 설계에 대한 명제인 문제 3·4와 방향이 반대이다.)",
     [("가", r"각 가설 아래 \(W_1,\dots,W_m\)은 i.i.d.이고 밀도는 \[ r_i(w)=\sum_{n=0}^{g}\binom gn\pi_i^{\,n}(1-\pi_i)^{g-n}\,\frac{1}{1+\alpha n}\,e^{-w/(1+\alpha n)}\quad(w>0). \]"),
      ("나", r"이 방식에서 최적 판정의 오류 확률 \(P_e\)는 \(\displaystyle\lim_{K\to\infty}\Bigl(-\tfrac1K\log P_e\Bigr)=\tfrac1g\,C(r_0,r_1)\)를 만족한다. 여기서 \(C\)는 체르노프 정보."),
      ("다", r"\(\pi_0\ne\pi_1\)이면 \(C(r_0,r_1)>0\)이다. 따라서 \(b=1/g\)일 때 최적 지수는 \(b\cdot\sup_{D,\alpha}C(r_0,r_1)\) 이상이다.")],
     [r"<b>체르노프 정리.</b> i.i.d. 표본 \(n\)개로 두 분포 \(r_0,r_1\)을 구분하는 최적 Bayes 오류는 \(-\tfrac1n\log P_e\to C(r_0,r_1)=-\min_{0\le\lambda\le1}\log\int r_0^{\lambda}r_1^{1-\lambda}\)를 만족한다.",
      r"문제 1의 결과(미검증이므로 조건부)."],
     [r"(가): 슬롯 \(\ell\)에서 \(S_\ell=\alpha N_\ell\), \(N_\ell=\#\{k\in G_\ell: X_k\in D\}\sim\mathrm{Bin}(g,\pi_i)\). 그룹들이 서로 다른 단말과 서로 다른 채널을 쓰므로 슬롯들이 독립이다. 문제 1의 (나)를 \(N_\ell\)에 대한 혼합으로 쓴다.",
      r"(나): 표본 수가 \(m=K/g\)이므로 체르노프 정리를 \(n=m\)으로 쓰고 지수를 \(K\) 기준으로 바꾼다.",
      r"(다): \(\int r_0^{\lambda}r_1^{1-\lambda}=1\)이 되려면 \(r_0=r_1\)이어야 한다(횔더 부등식의 등호 조건). \(\pi\mapsto r\)이 일대일인지 확인한다. 지수분포 혼합의 성분 평균 \(1+\alpha n\)이 서로 다르다는 점이 열쇠이다.",
      r"<b>수치 과제(증명 아님).</b> \(P_X^i\)가 \(\mathrm{Bern}(\tfrac13)\), \(\mathrm{Bern}(\tfrac23)\)일 때 \(g,\alpha,D\)를 바꿔 가며 \(C(r_0,r_1)\)을 계산하고, 문제 4의 \(c_1\)과 비교한다. \(g=1\)이 직교 접속(TDMA)에 해당한다."],
     r"문제 4(상한)와 합치면 \(b\cdot C\le E^{*}\le b\cdot c_1\)이 되어 추측 C2의 양쪽이 생긴다. 이 방식은 Li, Evans, Dey (IEEE TSP 2011)의 결론부 제안을 정식화한 것이다.")

# ---------------- Problem 6 ----------------
page(6, "추정 오차의 하한", UNVERIFIED + [("warn", "문제 3에 의존")],
     COMMON_DEF + LR_DEF + r"""
<p>모수 \(\theta\in\Theta\subset\mathbb R\). \(\theta\)가 주어지면 \(X_1,\dots,X_K\)는 서로 독립이고 \(X_k\sim P^{(k)}_\theta\). 송신과 관측 \(W\)는 문제 3과 같다(\(A_k=f_k(X_k,U_k,V)\), \(W_j=(1+S_j)E_j\)). 추정량 \(\hat\theta=\hat\theta(W)\)는 임의의 가측함수이다. 두 점 \(\theta_0\ne\theta_1\)에 대하여 모든 \(k\)에서 \((P^{(k)}_{\theta_0},P^{(k)}_{\theta_1})\)이 우도비 조건 \(L\)을 만족한다고 하자.</p>""",
     r"다음을 증명하시오.",
     [("가", r"모든 \(K\), 모든 \(f_k,U,V\), 모든 추정량에 대하여 \[ \max_{i\in\{0,1\}}E_{\theta_i}\bigl[(\hat\theta-\theta_i)^2\bigr]\ \ge\ \frac{(\theta_1-\theta_0)^2}{4}\,c(L,m). \]"),
      ("나", r"\(X_k\in\{0,1\}\), \(P_\theta(X_k=1)=\theta\), \(\Theta=[\tfrac14,\tfrac34]\)일 때 (가)를 적용해 \(\sup_{\theta\in\Theta}E_\theta[(\hat\theta-\theta)^2]\)의 \(K\)에 무관한 양의 하한을 구하시오."),
      ("다", r"관측이 \(X_k=\theta+N(0,1)\)이면 (가)를 그대로 쓸 수 없는 이유를 설명하시오.")],
     [r"문제 3의 결과(미검증이므로 조건부).",
      r"Le Cam의 두 점 방법: 추정량에서 판정 규칙 \(\psi=\arg\min_i|\hat\theta-\theta_i|\)를 만들 수 있다."],
     [r"(가): \(\psi\)가 틀리면 \(|\hat\theta-\theta_i|\ge|\theta_1-\theta_0|/2\)임을 보이고, 마르코프 부등식과 '최대값 \(\ge\) 평균'을 써서 \(\psi\)의 Bayes 오류(문제 3에 의해 \(\ge c(L,m)\))와 연결한다.",
      r"(나): \(\theta_0=\tfrac14,\ \theta_1=\tfrac34\)이면 우도비의 범위가 얼마인지 계산한다.",
      r"(다): 가우시안 평균 이동 모형에서 \(dP_{\theta_1}/dP_{\theta_0}\)가 유계인지 본다.",
      r"<b>남는 질문(열린 문제).</b> 가우시안 관측처럼 우도비가 유계가 아닐 때도 추정 오차가 0으로 가지 않는가? 이것은 문제 3에서 우도비 조건을 없애는 문제와 같다."],
     r"학위논문의 과업 범위를 '검정 + 추정'으로 정했으므로 필요한 따름정리이다. 통신에서는 '채널 정보가 없으면 단말을 늘려도 추정 오차가 0으로 가지 않는다'는 뜻이다.")

print("written", TOTAL, "pages to", OUT)

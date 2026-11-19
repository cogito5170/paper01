# 선행조사: 부가 정보의 지배성, 엔트로피 기반 도구, 꼬리 모델 (2026-11-19)

사용자 지시(2026-11-19)에 따른 두 가지 선행조사와 꼬리 모델 확인. 웹 검색과 초록 확인이 대부분이며, 본문을 읽은 것은 [A1]뿐이다.

## 조사 A. 공간 부가 정보와 시간 부가 정보 중 어느 쪽이 지배적인가

**결론.** 둘을 같은 조건에서 직접 비교해 "어느 쪽이 지배적"이라고 정량화한 연구는 찾지 못했다. 간접 증거는 **시간 쪽이 더 견고**하다는 방향이다. 단, 시간 상관의 이득은 "잡음의 상관"이 아니라 "평균 그래디언트가 천천히 움직이는 것(드리프트)"에서 나온다는 반론이 있다. 데이터 병렬 학습에서 공간 상관의 크기는 "공통 성분(참 그래디언트) 대 작업자별 잡음"의 비율이며, 이 비율은 배치 크기에 따라 정해진다.

| # | 문헌 | 내용 | 본 연구와의 관계 | 확인 수준 |
|---|---|---|---|---|
| A1 | Jhunjhunwala, Mallick, Gadhikar, Kadhe, Joshi, "Leveraging Spatial and Temporal Correlations in Sparsified Mean Estimation," NeurIPS 2021, [arXiv:2110.07751](https://arxiv.org/abs/2110.07751) | Rand-k 희소화에서 서버 복호만 바꿔 공간·시간 상관을 활용. 실험: 시간 추정기는 3개 과제 모두에서, 공간 추정기는 2/3에서 기준보다 좋음. 비-IID CIFAR-10 로지스틱 회귀에서는 공간 추정기가 실패하고, 저자들은 "비-IID 분할이 공간 상관을 줄였을 가능성"을 언급 | 둘을 함께 다룬 가장 가까운 연구. 단 PCA·K-평균·로지스틱 회귀뿐이고 심층망·스위치 집계는 없음. 상관의 크기를 직접 측정하지 않음 | 본문 확인 |
| A2 | M. Kim, "Information-Theoretic Lower Bounds for Bit-Constrained Stochastic Optimization via a Reduction to Compressed Gaussian Mean Estimation," [arXiv:2606.00703](https://arxiv.org/abs/2606.00703) (2026, 단독 저자 프리프린트) | 단일 장치, 순차 레이트-왜곡. AR(1) 잡음 상관 ρ는 하한을 (1+ρ)/(1−ρ)배 **키운다**. 필요한 비트를 줄이는 것은 "최적점 궤적의 예측 가능성(느린 드리프트)"이라고 결론 | **시간 부가 정보의 이득이 어디서 오는지**에 대한 직접적 주장. 다중 작업자·공간 상관 없음, 실측 없음, 동료 검토 전 | 초록·본문 일부 |
| A3 | "Wyner-Ziv Gradient Compression for Federated Learning," [arXiv:2111.08277](https://arxiv.org/abs/2111.08277) (저자 미확인) | 이전 라운드 그래디언트를 부가 정보로 사용(시간) | 시간 부가 정보의 실용 방식 | 초록 |
| A4 | Mayekar, Jha, Tyagi, "Wyner-Ziv compression is (almost) optimal for distributed optimization," ISIT 2022; [arXiv:2011.12160](https://arxiv.org/abs/2011.12160) | 작업자들의 그래디언트 추정이 서로 가까우면(공간) 수렴 속도가 개선됨. 절반의 작업자가 부가 정보를 만들고 나머지를 압축 | 공간 부가 정보의 이론 결과 | 초록 |
| A5 | Abrahamyan 등, "Learned Gradient Compression for Distributed Deep Learning," [arXiv:2103.08870](https://arxiv.org/abs/2103.08870); "Neural Distributed Source Coding," [arXiv:2106.02797](https://arxiv.org/abs/2106.02797) | 작업자 간 그래디언트 상관을 오토인코더·분산 소스 부호화로 활용 | 공간 상관이 심층망에서도 존재한다는 실용 근거 | 초록 |
| A6 | Edin, Chen, Kieffer, Johansson, "Temporal Predictive Coding for Gradient Compression in Distributed Learning," [arXiv:2410.02478](https://arxiv.org/abs/2410.02478) (2024) | 과거 그래디언트의 최소제곱 선형 예측 + 잔차 압축 | SPEC T6(예측 부호화)와 직접 겹침 → T6 신규성 점검 대상 | 초록 |
| A7 | McCandlish, Kaplan, Amodei 등, "An Empirical Model of Large-Batch Training" (2018, arXiv:1812.06162, **기억에 의존, 서지 확인 필요**) | "그래디언트 잡음 척도" B_noise = tr(Σ)/‖G‖²를 여러 과제에서 측정. 학습이 진행될수록 커짐 | 공통 성분 모델 X_k = U + N_k에서 **공통 성분 대 작업자 잡음 비율 = b/B_noise**(b: 작업자당 배치). 즉 공간 상관의 크기를 재는 기존 지표가 이미 있음 | 기억 |

**본 연구에 주는 함의 (판단, 검증 전)**
1. 데이터 병렬 학습에서는 작업자 데이터가 같은 분포라서 비-IID 문제는 작고, 공간 상관의 크기는 b/B_noise로 정해질 것으로 본다. B_noise가 작업자당 배치보다 크면(흔한 경우) 작업자별 잡음이 지배하고, 공통 성분을 써도 ½log₂K 대가는 크게 줄지 않는다.
2. 시간 부가 정보는 잡음 상관이 아니라 평균의 드리프트를 통해서만 이득이 있을 수 있다(A2). 측정할 양은 "합의 반복 간 상관"이 아니라 "이전 합으로 예측한 뒤의 조건부 분산 Var(S_t | S_{t−1})"이다.
3. 두 부가 정보의 지배성은 실측(S2)으로 정한다. 비교 지표는 Var(S | 부가 정보)를 같은 단위로 맞춘 것이어야 한다.

## 조사 B. 그래디언트를 엔트로피 기반 도구로 다룰 수 있는가

**결론.** 다룰 수 있다고 보고 실제로 다룬 논문들이 있다. 대부분 가우시안(i.i.d.) 가정이며, 실제 그래디언트 통계로 파라미터를 맞춘 것은 [B1] 하나다. **합 호환(스위치가 복호 없이 군 덧셈만 함) 제약을 넣은 레이트-왜곡 분석은 찾지 못했다.**

| # | 문헌 | 내용 | 본 연구와의 관계 | 확인 수준 |
|---|---|---|---|---|
| B1 | N. Zhang, M. Tao, J. Wang, F. Xu, "Fundamental Limits of Communication Efficiency for Model Aggregation in Distributed Learning: A Rate-Distortion Approach," [arXiv:2206.13984](https://arxiv.org/abs/2206.13984) (학회판 ISIT 2021, 저널판 IEEE TCOM 2022로 보고됨) | 모델 집계를 **벡터 가우시안 CEO 문제**로 정식화하고 합 전송률-왜곡 함수 유도. 실제 데이터셋의 그래디언트 통계 사용. "작업자 간 상관 활용의 이득이 SignSGD에서 크다" | **가장 가까운 선행연구.** 상관이 있는 작업자들의 집계를 레이트-왜곡으로 다룸. 합 호환 제약 없음(서버가 각 메시지를 받음) | 초록 |
| B2 | T. Adikari, "Rate distortion comparison of a few gradient quantizers," [arXiv:2108.09899](https://arxiv.org/abs/2108.09899) (2021) | Scaled-sign, Top-K를 가우시안 성분 가정 아래 섀넌 R(D)와 비교 | "i.i.d.가 아니면 R(D) 하한이 그대로 적용되지 않는다"는 단서가 있음 | 초록 |
| B3 | Safaryan, Shulgin, Richtárik, "Uncertainty Principle for Communication Compression in Distributed and Federated Learning and the Search for an Optimal Compressor," [arXiv:2002.08958](https://arxiv.org/abs/2002.08958) | 비트 수와 분산의 불확정성 원리. 레이트-왜곡으로도 같은 한계가 나온다고 언급 | 단일 벡터 압축의 기본 한계 | 초록 |
| B4 | Kim 2026 (A2와 같음) | 순차 레이트-왜곡으로 시간 상관 그래디언트 분석 | 시간 축의 엔트로피 기반 분석 | 초록·본문 일부 |

**새로운 분석법의 단서 (제안, 검증 전)**
- B1의 **CEO 문제** 틀에 본 연구의 **합 호환 제약**을 넣으면 "융합 센터가 메시지들의 군 합(mod M)만 보는 CEO 문제"가 된다. 문헌에서 이 조합은 찾지 못했다. Körner–Marton(모듈로 합 계산)과 CEO 문제를 잇는 형태라 SPEC의 "외면받은 20세기 이론" 정체성과도 맞는다.
- 공통 성분 모델 X_k = U + N_k는 CEO 문제의 표준 모델(공통 소스 + 독립 관측 잡음)과 같은 구조다. 정리 A(독립)와 돌파(상관)를 한 틀에서 다룰 수 있다.

## 꼬리 모델: 가우시안인가, 두꺼운 꼬리인가

**결론.** 논쟁 중이며, **무엇을 재느냐**에 따라 답이 갈린다. 본 연구의 모델에서 중요한 것은 "같은 좌표에서 작업자마다 달라지는 부분(미니배치 잡음)"의 분포다.

| # | 문헌 | 주장 |
|---|---|---|
| C1 | Şimşekli, Sagun, Gürbüzbalaban, "A Tail-Index Analysis of Stochastic Gradient Noise in Deep Neural Networks," ICML 2019, [arXiv:1901.06053](https://arxiv.org/abs/1901.06053) | 그래디언트 잡음은 α-안정 분포의 두꺼운 꼬리 |
| C2 | Panigrahi 등, "Non-Gaussianity of Stochastic Gradient Noise," [arXiv:1910.09626](https://arxiv.org/abs/1910.09626) | 배치 256 이상, 학습 초기에는 가우시안. 배치 32나 학습 후반에는 비가우시안 |
| C3 | "On the Overlooked Structure of Stochastic Gradients," NeurIPS 2023, [arXiv:2212.02083](https://arxiv.org/abs/2212.02083) | **좌표 방향**(한 시점의 좌표들)은 비등방성 때문에 거듭제곱 꼬리, **반복 방향의 진짜 미니배치 잡음**은 대체로 가우시안에 가까운 가벼운 꼬리 |

**함의 (판단, 검증 전).** 작업자 간 차이(미니배치 잡음)는 가우시안에 가까울 수 있고(C2, C3), 좌표 간 크기 차이는 두꺼운 꼬리다. THC처럼 무작위 하다마드 변환(RHT)을 먼저 하면 좌표들이 섞여 좌표별 분포가 가우시안 쪽으로 간다. 따라서 실측에서는 **RHT 전후**와 **좌표 방향 대 작업자 방향**을 나눠 재야 한다.

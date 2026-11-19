SPEC: 외면받은 20세기 이론으로 푸는 AI 데이터센터 집단 통신의 근본 한계 (박사 연구 명세)
상태: v1.0 (방향 전환판). 작성 기준일: 2026-11-18
v1.0 변경: 응용을 무선 다중 단말 공중 계산 → AI 데이터센터 집단 통신(All-Reduce) 으로 전환. 이론 핵심(과업 지향 × 함수 계산)은 유지.
이전 무선 버전(v0.1~v0.6)은 지우지 않고 archive/SPEC_v0.6_wireless.md에 그대로 보관. 요약은 부록 A.
⚠ 이 문서의 정리·추측·수치는 대부분 검증 전이다. 특히 5장의 정리 A와 9장의 신규성 위험을 먼저 확인할 것.
0. 인터뷰 기록 (요구사항 출처)
항목	사용자 답변
목표	박사 연구 주제 정하기. 해결되지 못한 통신 문제를 해결하고 싶음
근거	1900년대(~1999) IEEE 논문 30편
방법	1900년대에 외면받은 개념을 써서 현재 통신 문제를 해결
방법론 범위	정보이론·수학, 신호처리, 알고리즘, 딥러닝을 모두 포함
검증 방식	시뮬레이션만 사용, 하드웨어 실험 없음. 그만큼 파격적인 이론 시도
응용 분야	AI 네이티브 통신 → (v1.0) AI 데이터센터 통신, 그중 집단 통신의 근본 한계
결과물 규모	박사 학위논문
파격성 수위	증명 가능한 파격
연구 정체성	한계 중심: 근본 한계를 규명하고, 방식은 그 한계에 도달 가능함을 보이는 증거
시뮬레이션 환경	Python + PyTorch
계산 자원	GPU 1~2장
방향 전환 경위. 무선 공중 계산 노선(v0.1~v0.6)을 검토하면서 두 가지가 드러났다. (1) "채널 중첩이 충분통계량을 계산한다"는 핵심 아이디어는 이미 증명된 선행연구가 있었다(TBMA, LBMA 등). (2) 무선에서는 영평균 페이딩 때문에 중첩 계산 자체가 막힐 가능성이 크다(추측 C1-a). 반면 유선 데이터센터에는 페이딩이 없고 스위치가 정확히 더해 주므로, 같은 수학이 실제로 절실하게 쓰이는 환경이다.
1. 연구의 한 줄 요약
"합을 압축된 채로 더할 수 있게 만드는 대가는 얼마인가?" AI 학습의 집단 통신(All-Reduce)에서 압축 기법이 실제로 쓰이려면 네트워크 안에서 압축된 상태 그대로 합산(합 호환)될 수 있어야 한다. 본 연구는 1950~90년대에 정립되었으나 통신 시스템에서 주변으로 밀려났던 함수 계산 이론(Körner–Marton, Yamamoto), 격자·디더 양자화(Schuchman, Ziv, Zamir–Feder), 예측 부호화와 잡음 성형(Elias, Inose, Spang–Schultheiss) 을 이용해, 합 호환 압축의 근본 한계(역 한계) 를 규명하고 그 한계에 도달하는 부호를 제시한다.
2. 서론: 왜 이 연구가 필요한가
학위논문 1장의 뼈대. 2.1은 논증 골격, 2.2는 산문 초안. [n]은 11장 근거 논문 번호. [출처 필요]는 수치 확보가 필요한 자리.
2.1 논증 구조
단계	주장	근거	이 고리가 무너지면
P1. 병목의 이동	AI 데이터센터의 병목이 연산에서 통신으로 옮겨가고 있다	업계 분석 (Yole Group 2026, Lightmatter Computex 2026 발표). 학습 트래픽의 대부분은 All-Reduce·All-to-All 집단 통신 (Ultra Ethernet 규격 1.0, 2025)	연구 동기 약화
P2. 기존 설계	손실 없는 All-Reduce는 이미 대역폭 최적이다 (링 All-Reduce의 단말당 전송량 2(N−1)/N · d). 더 줄이려면 압축이 필요하다	링 All-Reduce 분석, 네트워크 함수 계산 용량 (Appuswamy 등 2011: 합은 최소 절단이 정확)	(사실 기술)
P3. 압축의 조건	압축이 실제로 쓸모 있으려면 압축된 채로 더할 수 있어야 한다. top-k, sign, 일반 양자화 대부분은 이게 안 되어 단말 수 N에 비례하는 All-Gather로 빠진다	MLSys 2022 실증 연구 ("On the Utility of Gradient Compression")	합 호환 제약이 실무상 중요하지 않다는 결론
P4. 함수만 필요함	학습에 필요한 것은 개별 그래디언트가 아니라 그 합이고, 손실 압축도 허용된다 (SGD는 잡음에 강함)	함수 계산 이론 [5][7][9], 간접 레이트-왜곡 [11][12][14], 압축 SGD 수렴 이론	개별 복원 문제로 환원
P5. 공백	손실 없는 합 계산(망 전체)과 별형 손실 압축(분산 평균 추정)은 풀렸지만, "합 호환" 제약 아래 손실 압축의 역 한계는 비어 있는 것으로 보인다	9장의 선행연구 점검	신규성 상실
P6. 왜 지금인가	네트워크 내 집단 연산이 표준화 중이고(UEC), 스위치가 정수 덧셈을 지원한다. 그래디언트 벡터는 차원이 수백만~수십억이라 정보이론의 긴 블록 가정이 실제로 성립하는 드문 통신 환경이다	UEC 규격 문서, 모델 규모	"왜 예전엔 안 했나"에 답하지 못함
결론	합 호환 압축의 근본 한계와 그 달성 방식이 필요하다	P1~P6	
논증의 성격. "새 정보이론이 필요하다"는 주장이 아니다. 분산 압축 이론에서 오래전에 정립된 도구로, 현실 시스템이 부과하는 새 제약(합 호환)의 대가를 정확히 계산하자는 주장이다.
2.2 서론 초안
1.1 배경: 통신이 AI의 새 병목이다
대규모 AI 모델 학습은 수천~수만 개의 가속기가 매 반복마다 그래디언트를 교환하는 분산 계산이다. 업계 분석은 AI 데이터센터의 병목이 연산에서 통신으로 옮겨가고 있다고 진단한다(Yole Group, 2026). 학습 트래픽의 대부분은 모든 가속기가 자신의 그래디언트를 더해 같은 합을 나눠 갖는 All-Reduce와, 전원이 전원과 교환하는 All-to-All이라는 집단 통신이다. [출처 필요: 학습 시간 중 통신 비중 수치]
1.2 문제: 압축은 "더할 수 있어야" 쓸모가 있다
손실 없는 All-Reduce는 이미 대역폭 최적이다. 링 구조에서 각 가속기는 d차원 벡터에 대해 약 2(N−1)/N · d개의 값만 보내면 된다. 전송량을 더 줄이려면 압축이 필요하지만, 실증 연구에 따르면 압축 기법의 상당수는 실제 시스템에서 이득이 작다. 이유는 단순하다. All-Reduce는 중간 노드가 받은 값을 더해서 넘기는 구조인데, 대부분의 압축 표현은 압축된 채로 더할 수 없다. 그래서 개별 압축값을 모두 모으는 All-Gather로 빠지고, 전송량은 가속기 수 N에 비례해 늘어난다.
1.3 왜 근본 한계가 필요한가
압축된 채로 더할 수 있는 표현(합 호환 표현)을 쓰면 네트워크 안에서 합산이 가능하다. 하지만 그 대가가 있다. 예를 들어 스위치의 정수 누산기는 N개 값을 더할 때 넘침을 막기 위해 비트 폭을 늘려야 한다. 이 대가가 피할 수 없는 근본적인 것인지, 더 나은 부호로 줄일 수 있는 것인지는 알려져 있지 않다. 이를 모르면 압축 설계는 시행착오에 머문다.
1.4 기존 연구의 공백
네트워크 함수 계산 이론은 손실 없는 합 계산의 용량을 망 전체에서 결정했다(Appuswamy 등, 2011). 그러나 손실 압축은 다루지 않는다.
분산 평균 추정 연구는 별형 구조에서 통신량 대 오차의 한계를 정밀하게 제시했다(Zhang·Duchi·Jordan·Wainwright 2013, Braverman 등 2016, Davies 등). 그러나 대부분 서버가 각 메시지를 따로 복호한 뒤 더하는 구조를 가정한다.
그래디언트 압축 이론은 단일 그래디언트에 필요한 최소 비트 수를 밝혔다(Mayekar & Tyagi, 2020). 그러나 다중 단말의 합과 네트워크 내 집계는 다루지 않는다.
시스템 연구는 네트워크 내 집계(SwitchML)와 합 호환 압축(GradiVeQ, THC 등)을 구현했지만, 그 압축이 근본 한계에서 얼마나 떨어져 있는지는 답하지 않는다.
결과적으로 "합 호환" 제약 아래 손실 압축의 근본 한계는 확립되지 않은 것으로 보인다. [⚠ 9장 신규성 점검 후 확정]
1.5 왜 지금인가: 외면받았던 이론의 귀환
필요한 도구는 이미 반세기 전에 나와 있었다. 함수만 계산하면 될 때는 선형 부호가 오히려 유리하다는 Körner–Marton(1979)의 결과, 부가 정보가 있을 때의 함수 계산(Yamamoto 1982), 양자화 잡음을 신호와 독립으로 만드는 디더(Schuchman 1964)와 보편 양자화(Ziv 1985, Zamir–Feder 1992), 그리고 양자화 오차를 다음 단계로 넘겨 성형하는 예측 부호화(Elias 1955)와 시그마-델타 변조(Inose 1962)다.
이 이론들이 통신 시스템의 주류에서 밀려난 이유는 결함이 아니라 쓰일 곳이 없었기 때문이다. 무선 통신은 짧은 패킷과 페이딩 때문에 긴 블록과 정확한 덧셈이라는 가정이 맞지 않았다. AI 데이터센터는 정반대다. 그래디언트 벡터의 차원은 수백만 이상이어서 긴 블록 가정이 실제로 성립하고, 스위치는 정수를 정확히 더하며, 매 반복의 합은 이전 반복의 합과 강하게 상관되어 있다. 반세기 전의 이론이 처음으로 제자리를 찾은 환경이다.
1.6 연구 목표와 기여
본 논문은 집단 통신의 손실 압축에 대해 (1) 합 호환 제약 아래 근본 한계를 세우고, (2) 그 한계에 도달하는 격자 기반 부호를 제시한다.
합 호환 손실의 크기: 네트워크 내 집계를 허용하는 대가가 링크당 좌표당 약 ½ log₂ N 비트인지, 그것이 근본적인지를 규명한다. (학위논문 3장, 정리 A)
시스템 수준 상충: 이 로그 비용과 All-Gather의 선형 비용을 비교해, 어떤 조건에서 어느 쪽이 유리한지 경계를 제시한다. (3장)
다단 집계: 링과 다단 스위치 트리에서 중간 재양자화가 만드는 오차 누적의 하한과 달성 방식을 제시한다. (4장)
시간 상관의 활용: 압축 SGD의 오차 피드백을 예측 부호화와 잡음 성형 이론으로 재해석하고, 이전 반복의 합을 부가 정보로 쓰는 부호의 한계를 제시한다. (5장)
과업 기준 한계: 합의 MSE가 아니라 학습 수렴 속도를 기준으로 필요한 통신량을 제시하고, 시뮬레이션으로 검증한다. (6장)
1.7 범위 한정
본 논문은 네트워크 혼잡 제어, 스케줄링, 하드웨어 구현을 다루지 않는다. 결과는 시뮬레이션과 증명으로 제시하며, 실제 스위치 하드웨어에서의 검증은 범위 밖이다.
3. 연구 문제 정의
3.1 기본 모델 (1단 스위치 집계)
작업자: n = 1, …, N. 작업자 n은 벡터 g_n ∈ ℝ^d를 가짐 (한 반복의 그래디언트)
목표: 모든 작업자가 합 S = Σ_n g_n 또는 평균 S/N의 추정을 얻음 (정규화된 왜곡에서는 두 목표가 같은 문제)
통계 모델 (기본, 2026-11-18 확정): 독립 가우시안 벡터. g_n ~ N(0, σ_ξ² I_d) (사용자 표기: X_k ~ N(0, σ² I_d), k = 1, …, K), 작업자 사이와 좌표 사이 모두 독립. Var(S) = N σ_ξ² (좌표당)
부가 정보: 기본 모델에는 없음. 이전 반복의 예측 S′은 시간 상관 확장(3.3)에서 다룸
망: 작업자 → 스위치 → 작업자. 링크마다 좌표당 R비트 (블록 길이 = 차원 d, d → ∞)
왜곡: 좌표당 MSE, D = (1/d) E‖Ŝ − S‖². 정규화 왜곡 D̄ = D / Var(S) (기본 모델에서 Var(S) = Nσ_ξ²). 평균을 목표로 해도 D̄는 같음. D̄로 쓰면 A-2는 ½log₂(1/D̄), A-3은 ½log₂(N/D̄)가 되어 대가 ½log₂N이 바로 보임
3.2 합 호환 제약 (핵심)
모든 작업자가 같은 유한 아벨 군 G (예: (ℤ_{2^b})^d, 즉 스위치의 b비트 정수 덧셈) 위의 메시지를 보냄. |G| = 2^{dR}
인코더 E_n: ℝ^d → G. 공유 난수(공통 시드에 의한 디더)는 허용 (데이터센터에서 현실적)
스위치는 군 덧셈만 수행: Z = E_1(g_1) ⊕ ⋯ ⊕ E_N(g_N). 복호나 재부호화는 하지 않음
복호기: Ŝ = D(Z, 공유 난수) (부가 정보가 있는 확장에서는 D(Z, S′, 공유 난수))
비교 대상 (제약 없음). 스위치가 각 메시지를 따로 복호하고 임의로 처리할 수 있는 경우. 같은 링크 전송률에서의 최적 왜곡을 기준으로 삼는다.
3.3 확장 모델
확장	내용	대응 장
상관 가우시안 (공통 성분, 2단계)	g_n = θ + ξ_n (사용자 표기: X_k = U + N_k, 목표 합 KU + Σ_k N_k), θ ~ N(0, σ_θ² I_d) (모든 작업자에 공통), ξ_n ~ N(0, σ_ξ² I_d) (작업자별, 서로 독립). σ_θ = 0이면 기본 모델	3장
링 All-Reduce	축소-분산 + 전체-수집 단계. 중간 노드가 군 덧셈 후 전달	4장
다단 스위치 트리	깊이 h의 트리. 중간 스위치의 누산기 비트 폭 제한 시 재양자화	4장
시간 상관	반복 t의 합이 t−1의 합과 상관. 오차 피드백 포함	5장
두꺼운 꼬리 (3단계: 두 가우시안 단계 뒤, 2026-11-18)	그래디언트의 꼬리가 가우시안보다 두꺼움. 분포 부류(예: 거듭제곱 꼬리)는 미정, 신규성 점검 후 확정. 유계 입력(최악 경우)은 기존 결과(Chen 2022 Cor 5.4)라 인용만 함	3장, 4장
과업 기준	왜곡 대신 SGD 수렴 속도	6장
3.4 연구 질문 (RQ)
RQ	내용	방법론
RQ1	합 호환 제약의 대가 Δ_compat(N, D) = R_compat(D) − R*(D)는 얼마이며, 근본적인가?	정보이론, 격자 이론, 유한 아벨 군 위의 조화해석
RQ2	이 대가와 All-Gather의 선형 비용 사이의 시스템 수준 경계는?	분석 + 시뮬레이션
RQ3	다단 집계에서 재양자화 오차의 누적 하한은 망 깊이와 어떻게 관계되는가?	정보이론
RQ4	오차 피드백은 정보이론적으로 무엇이며, 시간 상관을 최적으로 쓰는 부호는?	예측 부호화, 잡음 성형, 부가 정보 이론
RQ5	학습 수렴 기준으로 필요한 통신량은?	최적화 이론 + 딥러닝 시뮬레이션
4. 증명 목표 (모두 검증 전 가설)
번호	성격	목표	근거 논문	난이도
T1	역 한계 (제약 없음)	3.1 모델에서 제약 없는 최적 전송률 R*(D)의 하한. 작업자별 성분이 독립이면 각 작업자는 해상도 약 D/N이 필요하므로 R* ≳ ½ log₂(N σ_eff² / D) 꼴	[4][6][10][13]	중
T2	달성 (합 호환)	디더를 쓴 중첩 격자(nested lattice)와 모듈로 덧셈으로 R_compat(D) ≤ ½ log₂(N (Var(S|S′) + D) / D) + ε. 스칼라 격자에서 ε ≈ ½ log₂(2πe/12) ≈ 0.254비트	[5][7][16][21][22][23]	중
⭐ T3	역 한계 (합 호환)	단일 라운드 합 호환 부호는 모두 R_compat(D) ≥ ½ log₂(N Var(S|S′) / D) − c를 만족. 즉 Δ_compat ≈ ½ log₂(Var(S|S′)/σ_eff²)이고, 작업자별 성분이 지배하면 ≈ ½ log₂ N	[5][9] + 아벨 군 조화해석, 엔트로피 합집합 부등식	상. 핵심
T4	격차·경계	링 All-Reduce에서 합 호환 방식(좌표당 약 2(R* + ½ log₂ N)비트)과 All-Gather 방식(좌표당 약 (N−1)R*비트)의 경계	T1~T3	하
T5	역 한계 (다단)	깊이 h 트리에서 누산기 폭이 b비트로 제한되면 재양자화 오차가 누적되는 하한	[9][15][19]	상
T6	해석 + 한계	오차 피드백 = 잡음 성형(Spang–Schultheiss 1962, Inose 1962)임을 정식화하고, 이전 합을 부가 정보로 쓰는 합 호환 부호의 한계를 Yamamoto(1982) 틀로 제시	[7][24]~[28]	중상
T7	과업 기준	다중 작업자 합과 네트워크 내 집계에서 표준 SGD 수렴 속도를 유지하는 최소 비트 수	[11]~[14] + Mayekar–Tyagi	중상
T2와 T3의 직관. 합 호환 부호의 최종 오차는 N개 작업자의 양자화 오차의 합이므로, 각 작업자는 해상도 D/N이 필요하다. 동시에 모듈로 덧셈의 범위(거친 격자)는 합 전체의 불확실성을 덮어야 한다. 작업자별 성분이 독립이면 그 분산은 N σ_ξ²로 N배 커진다. 제약이 없으면 각 메시지를 따로 풀 때 범위가 σ_ξ²면 충분하다. 이 차이가 ½ log₂ N이다. 스위치 누산기 폭을 log₂ N비트 늘리는 공학적 관행의 정보이론적 버전이며, T3는 이것이 어떤 부호로도 피할 수 없음을 보이려는 것이다.
5. 첫 번째 증명 목표: 정리 A (합 호환 손실의 크기)
⚠ v1.0에서 새로 전개한 가설이며 검증 전. 착수 전 9장의 문헌 확인이 먼저.
5.1 정리 A 진술 (가설)
3.1~3.2의 기본 모델(독립 가우시안, 부가 정보 없음, Var(S) = N σ_ξ²)에서:
부분	주장	상태
A-1 (달성)	합 호환 부호: R_compat(D) ≤ ½ log₂(N² σ_ξ² / D) + ε	구성이 명확함. 증명 난이도 하
A-2 (제약 없는 역 한계)	모든 부호: R*(D) ≥ ½ log₂(N σ_ξ² / D) − c₁	⚠ 선행 있음 (2026-11-18): Yang–Grover–Kar arXiv 1601.06224 Thm 2(트리 망, 독립 가우시안, 임의 부호의 바깥 한계). 특수화해 인용. 신규 아님
A-3 (합 호환 역 한계)	모든 단일 라운드 합 호환 부호: R_compat(D) ≥ ½ log₂(N² σ_ξ² / D) − c₂	미증명. 핵심. ⚠ (2026-11-18) 유계 입력(최악 경우) 버전은 Chen 등 arXiv 2203.03761 Cor 5.4의 개수 논증으로 사실상 나옴 → 가우시안 버전만 신규 후보. 반례 위험: 상관 양자화(Suresh 등 arXiv 2203.04925)
결론	Δ_compat = ½ log₂ N ± O(1) 비트/좌표/링크	A-1~A-3이 모두 성립할 때
해석. 네트워크 내 집계의 대가는 로그(½ log₂ N)이고, 그것을 피하려고 All-Gather를 쓰면 대가는 선형(N배 전송량)이다. 예를 들어 N = 1024이면 대가는 좌표당 약 5비트다. 4비트 압축을 쓰는 상황이라면 무시할 수 없는 크기다.
5.2 A-3 증명의 어려움과 후보 도구
어려운 점: 복호기가 보는 것은 군 위의 합 Z 하나뿐이다. "각 작업자의 해상도가 D/N이어야 한다"와 "Z의 범위가 합의 불확실성을 덮어야 한다"를 모든 부호(비선형, 비균일 포함)에 대해 동시에 보여야 한다.
단순한 정보량 논증으로는 부족함: H(Z) ≤ dR만 쓰면 Wyner–Ziv형 하한 ½ log₂(Var(S|S′)/D)만 나오고, N에 대한 의존성이 사라진다.
후보 도구:
유한 아벨 군 위의 푸리에 해석 (지표 이용)
군 값 확률변수 합의 엔트로피 부등식: Tao(2010)의 엔트로피 합집합 이론, Madiman–Kontoyiannis의 엔트로피 합집합 부등식 (가산 조합론과 정보이론의 접점)
아벨 군 부호에 의한 분산 부호화 (Krithivasan–Pradhan)
반례 가능성: 다중 라운드나 작업자별로 다른 디더 구조가 ½ log₂ N을 줄일 수 있는지 먼저 확인해야 한다. 단순한 다중 라운드는 오히려 나빠짐을 계산으로 확인했다(라운드마다 N배 범위가 다시 생김). 그러나 일반적인 경우는 미확인.
5.3 후속 순서
순서	목표
1	A-1 (구성 + 오차 분석) → A-2 (표준 역 한계)
2	A-3 (핵심)
3	두꺼운 꼬리 버전: 범위가 √N이 아니라 N으로 커지면 대가가 log₂ N이 되는지
4	T4 시스템 경계, T5 다단 트리, T6 시간 상관
6. 시뮬레이션 계획
ID	시나리오	목적
S1	가우시안 합성 데이터 (3.1 모델)	정리 A의 수치 확인. 달성 곡선과 역 한계 비교
S2	실제 그래디언트 기록 (소형 모델: ResNet-18 on CIFAR-10, 소형 트랜스포머)	공통·작업자별 성분 비율, 꼬리 두께, 반복 간 상관 측정 → 모델 가정 검증
S3	링·트리 All-Reduce 모사 (정수 누산기 폭, 넘침 포함)	T4·T5 검증
S4	압축 SGD 학습 (작업자 수 N을 모사)	T7 검증. 같은 전송 바이트에서 최종 정확도·손실
비교 대상: 무압축 / QSGD류 확률적 반올림 / top-k + All-Gather / SwitchML식 고정소수점 / THC류 합 호환 압축 / DRIVE·EDEN류 공유 난수 회전 양자화 / 제안 격자 부호
성능 지표: 좌표당 링크당 비트, 합의 MSE, 역 한계 대비 격차(비트), 같은 바이트에서의 학습 정확도, 넘침 발생률
구현: Python + PyTorch. 작업자는 단일 GPU에서 텐서로 모사(N개 그래디언트를 배치로 생성). GPU 1~2장으로 충분.
7. 필요 수학 배경
분야	쓰이는 곳	교재·자료
측도론 기반 확률론	전반	Durrett, Probability: Theory and Examples
정보이론 (분산 부호화, 레이트-왜곡)	T1~T3, T6	Cover & Thomas / El Gamal & Kim, Network Information Theory / Csiszár & Körner
격자 이론과 양자화	T2, T5	Zamir, Lattice Coding for Signals and Networks / Conway & Sloane, Sphere Packings, Lattices and Groups / Gray & Neuhoff, "Quantization" (IEEE TIT 1998)
유한 아벨 군 위의 조화해석, 가산 조합론	T3 (핵심)	Tao & Vu, Additive Combinatorics / Tao (2010) 엔트로피 합집합 이론
예측 부호화와 잡음 성형	T6	Jayant & Noll, Digital Coding of Waveforms
확률적 최적화	T7	Bottou·Curtis·Nocedal (2018) 서베이, Mayekar–Tyagi 논문
MSC 2020: 94A15·94A29(소스 부호화)·94A34(레이트-왜곡), 94A05(통신 이론), 11H06(격자), 11B30(가산 조합론), 43A70(유한 아벨 군 위의 해석), 90C15(확률적 최적화)
권장 학습 순서: 확률론 → El Gamal & Kim의 분산 부호화 장 → Zamir 격자 책 → 가산 조합론(T3 착수 시)
8. 대전제 점검 및 타당성 위협
8.1 대전제 점검
전제	판정	근거·위험	본 연구의 입장
P-A. 통신이 학습의 병목이다	⚠ 조건부	랙 내부(NVLink 등 scale-up)는 대역폭이 커서 압축 이득이 작을 수 있음. 랙 간·데이터센터 간에서는 병목	결과를 통신이 병목인 체계(scale-out, scale-across)로 한정
P-B. 압축은 실제로 쓸모가 있다	⚠ 논쟁 중	MLSys 2022는 압축의 실익이 생각보다 작다고 보고. 그 주된 이유가 바로 합 비호환	그 이유 자체를 연구 대상으로 삼음
P-C. 학습은 손실 압축을 견딘다	✅ 견고	압축 SGD 수렴 이론, 오차 피드백	채택
P-D. 네트워크 내 집계가 보급된다	⚠ 진행 중	UEC에서 표준화 진행 중. SwitchML류 시스템 존재	링 All-Reduce(스위치 없이도 합 호환이 중요)를 함께 다뤄 위험 분산
P-E. 정보이론의 긴 블록 가정이 성립한다	✅ 견고	그래디언트 차원 d가 수백만 이상	채택 (무선과의 핵심 차이)
8.2 유형별 타당성 위협
유형	위협	대응
구성	합의 MSE가 학습 성능을 대표하지 못함	T7과 S4로 과업 기준 검증
구성	가우시안 모델이 실제 그래디언트와 다름	S2에서 꼬리·상관을 실측하고 두꺼운 꼬리 버전도 증명
내적	모사한 네트워크와 실제 네트워크의 차이 (지연, 혼잡)	결과를 "전송 비트" 기준으로 한정하고, 시간 지표는 보조로만 사용
외적	소형 모델·소규모 N에서만 검증	이론 결과가 N에 대한 스케일링을 주므로 외삽 근거로 사용. 대규모 일반화 주장은 하지 않음
결론	학습 결과의 분산	시드 5개 이상, 신뢰구간 보고
8.3 반증 조건
관찰	판단
A-3이 거짓 (½ log₂ N보다 작은 대가로 합 호환 부호가 가능)	그 부호를 찾는 것이 새 기여가 됨. "근본 한계" 서술을 "개선된 부호"로 전환
실제 그래디언트에서 작업자별 성분이 무시할 만큼 작음	대가가 상수로 줄어듦. 주장을 "작업자별 성분 비율에 따른 대가"로 일반화
강한 기존 기법(THC, DRIVE/EDEN)이 이미 한계에 근접	기여를 "기존 기법이 최적임을 증명"으로 재정의 (한계 중심 정체성과 일치)
9. 신규성 위험과 대응
선행연구	겹칠 수 있는 지점	확인 상태	대응
Davies, Gurunathan, Moshrefi, Ashkboos, Alistarh (arXiv 2002.09268)	격자 양자화 + 수신자 자신의 벡터를 부가 정보로 쓰는 모듈로 복호. 별형·트리형 알고리즘과 하한	본문 확인 (2026-11-18): 별형·트리형 모두 리더·내부 노드가 메시지를 개별 복호 후 재부호화(Alg. 3 p.14, Alg. 4 pp.15-16). 하한(Thm 6~8, 38)은 공유 난수 아래 '수신 비트 수' 기준 부피 논증이며 합 호환 제약 없음. A-1 부분 중복(격자+mod q+부가 정보 복호), A-2 약한 형태(균등 공 분포, 큰 상수), A-3 없음	차별점은 "스위치가 복호 없이 군 덧셈만 한다"는 제약과 그 역 한계
arXiv 2609.23898 (2026, 링 기반 부호화 근사 All-Reduce)	근사 All-Reduce의 정규화 통신률	본문 확인 (2026-11-18): Munim–Ramamoorthy. 양자화 없는 실수 선형 부호화, 통신률 = 전송 실수 개수/d. 유일한 하한은 '선형 프로토콜은 통신률 ≥ 1'(부록 V-A). 비트·군·log N 없음. A-1~A-3, T4 모두 없음	관련 연구로 인용 (저자 스스로 양자화는 직교 방향, 정보이론적 관점은 열려 있다고 씀 p.2)
THC (텐서 준동형 압축, arXiv 2302.08545, NSDI '24 추정) + 후속 HotNets '24 (arXiv 2407.01378)	합 호환 압축의 시스템 구현	본문 확인 (2026-11-18): 동형 압축(정의 1), 스위치가 정수 인덱스 덧셈. 하행 비트 ⌈log₂(gN)⌉로 log N 증가를 서술·실험으로만 인정(Fig. 15). 후속은 포화 덧셈, '작업자가 늘면 b > q 필요'를 경험적으로 서술. 정리·하한 없음. A-1~A-3 없음	이론 한계와의 격차 측정 대상으로 활용
DRIVE (arXiv 2105.08339), EDEN (arXiv 2108.08842)	공유 난수 회전 + 양자화의 최적 분산 평균 추정	본문 확인 (2026-11-18): 둘 다 비동형(작업자마다 다른 회전, 경로 내 집계 불가라고 명시). DRIVE 하한은 단일 벡터 1비트 추정(Safaryan 등 인용), EDEN은 단일 가우시안 D(R)=σ²2^{-2R} 한 줄. A-1~A-3 없음	비교 대상
GradiVeQ (2018)	합과 교환 가능한 벡터 양자화	초록 확인	비교 대상
SwitchML (2021)	스위치 고정소수점 집계, 넘침 처리	초록 확인	정리 A의 공학적 대응물
Appuswamy 등 (2011), Krithivasan–Pradhan (2009)	손실 없는 망 함수 계산 / 가우시안 선형 함수 분산 부호화	초록 확인	기반 이론으로 인용
Mayekar–Tyagi (2020)	그래디언트 압축 최소 비트	초록 확인	T7의 출발점
10. 학위논문 구성과 일정
10.1 장 구성
장	내용	대응 목표	예상 산출
1	서론 (2장 논증)		
2	배경: 분산 부호화·격자·예측 부호화의 반세기		튜토리얼 (선택)
3	합 호환 손실의 근본 한계 (정리 A)	T1~T4	IEEE Trans. Inf. Theory / ISIT
4	링·다단 트리와 재양자화	T5	IEEE Trans. Inf. Theory / JSAC
5	시간 상관과 오차 피드백의 정보이론	T6	IEEE Trans. Signal Process. / ISIT
6	과업 기준 한계와 학습 실험	T7, S4	NeurIPS / ICML / MLSys
7	결론. 부록: 무선 공중 계산의 불가능성 (부록 A의 C1-a)		
10.2 일정 (4~5년)
기간	마일스톤	완료 기준
1년차 상반기	신규성 점검(9장), S2로 실제 그래디언트 통계 측정, A-1·A-2	문헌 노트, 측정 보고서
1년차 하반기	A-3 착수, T4	ISIT 투고 1편
2년차	A-3 완성, 두꺼운 꼬리 버전	저널 1편
3년차	T5, T6	저널 1편 + 학회 1편
4년차	T7, S4 학습 실험	ML 학회 1편
5년차	학위논문	제출
11. 근거 논문 30편 (1900년대 IEEE/IRE)
서지는 기억에 기반한 것이 많다. 모두 IEEE Xplore로 확인할 것. ⚠는 저자·쪽수 확신이 특히 낮은 항목.
A. 분산 부호화와 함수 계산 (핵심)
#	서지	개념	쓰이는 곳
1	D. Slepian & J. K. Wolf, "Noiseless coding of correlated information sources," IEEE Trans. Inf. Theory, vol. 19, no. 4, pp. 471–480, 1973	분산 무손실 압축	기준
2	A. D. Wyner, "On source coding with side information at the decoder," IEEE Trans. Inf. Theory, vol. 21, no. 3, pp. 294–300, 1975	부가 정보 하 부호화	T6
3	R. Ahlswede & J. Körner, "Source coding with side information and a converse for degraded broadcast channels," IEEE Trans. Inf. Theory, vol. 21, no. 6, pp. 629–637, 1975	다중 단말 역 한계 기법	T1, T3
4	A. D. Wyner & J. Ziv, "The rate-distortion function for source coding with side information at the decoder," IEEE Trans. Inf. Theory, vol. 22, no. 1, pp. 1–10, 1976	Wyner–Ziv 레이트-왜곡	T1, T6
5	J. Körner & K. Marton, "How to encode the modulo-two sum of binary sources," IEEE Trans. Inf. Theory, vol. 25, no. 2, pp. 219–221, 1979	합만 계산하면 선형 부호가 유리	T2, T3
6	T. M. Cover, A. El Gamal, M. Salehi, "Multiple access channels with arbitrarily correlated sources," IEEE Trans. Inf. Theory, vol. 26, no. 6, pp. 648–657, 1980	다중 단말에서 분리 붕괴	서론
7	H. Yamamoto, "Wyner–Ziv theory for a general function of the correlated sources," IEEE Trans. Inf. Theory, vol. 28, no. 5, pp. 803–807, 1982	부가 정보 하 함수 계산	T2, T6
8	T. S. Han & K. Kobayashi, "A dichotomy of functions F(X,Y) of correlated sources (X,Y) from the viewpoint of the achievable rate region," IEEE Trans. Inf. Theory, vol. 33, no. 1, pp. 69–76, 1987 ⚠	어떤 함수가 계산 이득을 갖는가	T3
9	R. G. Gallager, "Finding parity in a simple broadcast network," IEEE Trans. Inf. Theory, vol. 34, no. 2, pp. 176–180, 1988	망 안에서의 함수 계산 비용	T3, T5
10	T. Berger, Z. Zhang, H. Viswanathan, "The CEO problem," IEEE Trans. Inf. Theory, vol. 42, no. 3, pp. 887–902, 1996	다수 관측자의 원격 추정	T1
B. 간접(과업 지향) 레이트-왜곡
#	서지	개념	쓰이는 곳
11	R. L. Dobrushin & B. S. Tsybakov, "Information transmission with additional noise," IRE Trans. Inf. Theory, vol. 8, no. 5, pp. 293–304, 1962 ⚠	간접 레이트-왜곡의 원조	T7
12	J. K. Wolf & J. Ziv, "Transmission of noisy information to a noisy receiver with minimum distortion," IEEE Trans. Inf. Theory, vol. 16, no. 4, pp. 406–411, 1970	간접 MSE 분해	T7
13	J. Ziv & M. Zakai, "On functionals satisfying a data-processing theorem," IEEE Trans. Inf. Theory, vol. 19, no. 3, pp. 275–283, 1973	일반화된 정보 범함수	T1
14	H. S. Witsenhausen, "Indirect rate distortion problems," IEEE Trans. Inf. Theory, vol. 26, no. 5, pp. 518–521, 1980	간접 문제의 환원	T7
C. 양자화, 디더, 격자 (합 호환 부호의 재료)
#	서지	개념	쓰이는 곳
15	J. Max, "Quantizing for minimum distortion," IRE Trans. Inf. Theory, vol. 6, no. 1, pp. 7–12, 1960	최적 스칼라 양자화	T5
16	L. Schuchman, "Dither signals and their effect on quantization noise," IEEE Trans. Commun. Technol., vol. COM-12, no. 4, pp. 162–165, Dec. 1964 (DOI 10.1109/TCOM.1964.1088973)	디더 = 확률적 반올림의 원조	T2
17	H. Gish & J. N. Pierce, "Asymptotically efficient quantizing," IEEE Trans. Inf. Theory, vol. 14, no. 5, pp. 676–683, 1968 ⚠	엔트로피 부호 균일 양자화 (1.53 dB)	T2
18	A. Gersho, "Asymptotically optimal block quantization," IEEE Trans. Inf. Theory, vol. 25, no. 4, pp. 373–380, 1979 ⚠	고해상도 벡터 양자화	T2
19	S. P. Lloyd, "Least squares quantization in PCM," IEEE Trans. Inf. Theory, vol. 28, no. 2, pp. 129–137, 1982 (1957년 내부 보고서가 25년 뒤 출판)	외면받았다 출판된 대표 사례	T5
20	J. H. Conway & N. J. A. Sloane, "Fast quantizing and decoding algorithms for lattice quantizers and codes," IEEE Trans. Inf. Theory, vol. 28, no. 2, pp. 227–232, 1982 ⚠	격자 양자화 알고리즘	T2, 구현
21	J. Ziv, "On universal quantization," IEEE Trans. Inf. Theory, vol. 31, no. 3, pp. 344–347, 1985 ⚠	디더 균일 양자화의 보편성	T2
22	G. D. Forney, "Coset codes—Part I: Introduction and geometrical classification," IEEE Trans. Inf. Theory, vol. 34, no. 5, pp. 1123–1151, 1988	격자·잉여류와 모듈로 구조	T2, T3
23	R. Zamir & M. Feder, "On universal quantization by randomized uniform/lattice quantizers," IEEE Trans. Inf. Theory, vol. 38, no. 2, pp. 428–436, 1992 ⚠	디더 격자 양자화	T2
D. 예측 부호화와 잡음 성형 (오차 피드백의 원조)
#	서지	개념	쓰이는 곳
24	P. Elias, "Predictive coding—Part I, II," IRE Trans. Inf. Theory, vol. 1, no. 1, pp. 16–33, 1955	예측 부호화	T6
25	H. Inose, Y. Yasuda, J. Murakami, "A telemetering system by code modulation—Δ-Σ modulation," IRE Trans. Space Electron. Telem., vol. 8, pp. 204–209, 1962 ⚠	시그마-델타 변조	T6
26	H. A. Spang & P. M. Schultheiss, "Reduction of quantizing noise by use of feedback," IRE Trans. Commun. Syst., vol. 10, no. 4, pp. 373–380, 1962 ⚠	양자화 오차 피드백 (잡음 성형)	T6
27	N. S. Jayant, "Digital coding of speech waveforms: PCM, DPCM, and DM quantizers," Proc. IEEE, vol. 62, no. 5, pp. 611–632, 1974	예측 양자화 종합	T6
28	R. M. Gray, "Oversampled sigma-delta modulation," IEEE Trans. Commun., vol. 35, no. 5, pp. 481–489, 1987 ⚠	시그마-델타의 해석	T6
E. 분산 최적화와 모듈로 연산
#	서지	개념	쓰이는 곳
29	J. N. Tsitsiklis, D. P. Bertsekas, M. Athans, "Distributed asynchronous deterministic and stochastic gradient optimization algorithms," IEEE Trans. Autom. Control, vol. 31, no. 9, pp. 803–812, 1986	분산 SGD의 원조 (1986)	T7
30	H. Harashima & H. Miyakawa, "Matched-transmission technique for channels with intersymbol interference," IEEE Trans. Commun., vol. 20, no. 4, pp. 774–780, 1972 ⚠	모듈로 프리코딩 (넘침 처리의 원리)	T2, T5
보조 문헌 (2000년 이후 또는 IEEE 아님)
이론: Appuswamy·Franceschetti·Karamchandani·Zeger, IEEE TIT 2011 (망 함수 계산 용량) / Krithivasan & Pradhan, IEEE TIT 2009 (격자 분산 부호화, 선형 함수) / Nazer & Gastpar 2007, 2011 (공중 계산, compute-and-forward) / Zhang·Duchi·Jordan·Wainwright, NeurIPS 2013 / Braverman 등, STOC 2016 / Davies 등, arXiv 2002.09268 / Acharya·Canonne·Tyagi 등, arXiv 2010.06562 / Mayekar & Tyagi, AISTATS 2020, arXiv 2001.09032 / Tao 2010 (엔트로피 합집합 이론) / Zamir, Lattice Coding for Signals and Networks (2014)
압축 SGD: QSGD (Alistarh 등 2017) / 1-bit SGD (Seide 등 2014) / 오차 피드백 (Karimireddy 등 2019) / DRIVE, EDEN, THC (기억 기반, 확인 필요)
시스템: SwitchML (arXiv 1903.06701) / GradiVeQ (arXiv 1811.03617) / MLSys 2022 압축 실효성 연구 / arXiv 2609.23898 (2026) / arXiv 2606.25759 (2026)
업계: Ultra Ethernet 규격 1.0 (2025) / Yole Group (2026) / Lightmatter Computex 2026 / OIF 448G 워크숍 (2025)
12. 결정이 필요한 항목
 (완료 2026-11-18, 9장 표) 1차 신규성 점검: Davies·CERAR·THC(+후속)·DRIVE·EDEN 본문에 A-3 없음. 남은 점검: Yang–Grover–Kar(arXiv 1601.06224, 망 내 손실 선형 함수 계산의 율-왜곡), Krithivasan–Pradhan 본문, GradiVeQ·SwitchML 본문
 arxiv.org 등 논문 호스트를 세션 네트워크 허용 목록에 추가할지 (현재 본문 접근 차단)
 S2로 실제 그래디언트에서 공통·작업자별 성분 비율과 반복 간 상관 측정 (3.1 모델 가정의 타당성)
 (완료 2026-11-18) 정리 A의 기준 모델: 독립 가우시안 벡터가 기본, 공통 성분이 있는 상관 가우시안으로 확장, 두꺼운 꼬리를 함께 사용 (interview Q16)
 두꺼운 꼬리의 분포 부류 확정과 신규성 점검
 근거 논문 30편 서지 확인 (⚠ 항목 우선)
 학위논문 7장에 무선 노선(C1-a)을 부록으로 넣을지
 지도교수 연구실의 기존 연구와 맞는지
부록 A. 이전 노선: 무선 공중 계산 (v0.1~v0.6) 요약
전체 내용: archive/SPEC_v0.6_wireless.md. 수학 문제 문서: lemma4_problem.tex
항목	내용
주제	다중 단말 과업 지향 공중 계산 (무선 MAC의 신호 중첩으로 추론)
시도한 조합	D1(과업 지향) × D3(함수 계산), 대안으로 D2 × D4, D1 × D2
확인된 선행연구	"채널 중첩이 충분통계량을 계산한다"는 이미 증명됨 (TBMA: Mergen & Tong 2006·2007, SSBMA 2008, LBMA: Cohen & Leshem 2013, Goldenbaum 등 2013). 페이딩에서는 LLR 공중 전송이 중앙 집중 지수에 못 미침 (Cohen & Leshem 2013)
체계 지도	점근 체계·전력·대역폭·페이딩·채널 정보·안테나 6개 축으로 R1~R8 정리
추측 C1-a	Rayleigh 페이딩, 송수신단 채널 정보 없음, 단일 안테나, 채널 사용 횟수 고정이면 어떤 설계로도 오류 확률이 0으로 가지 않음. 핵심 보조정리 4 (유계 우도비 아래 독립합의 곱셈적 결합)
전환 이유	(1) 핵심 아이디어의 선행연구 존재 (2) 무선에서는 페이딩 때문에 중첩 계산이 근본적으로 막힐 가능성 (3) 유선 데이터센터가 같은 수학이 실제로 쓰이는 환경
남은 가치	C1-a는 "무선 공중 계산의 이득에는 송신단 채널 정보, 직접파, 다중 안테나 중 하나가 필요하다" 는 독립된 결과가 될 수 있음. 학위논문 부록이나 별도 학회 논문 후보
교훈	아이디어를 기여로 주장하기 전에 신규성 점검을 먼저 한다 (v0.3에서 확인된 문제)

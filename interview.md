# 논문 제안서 인터뷰 기록

- 목적: 논문 제안서(proposal.md) 작성. 사용자의 질문·주장마다 근거를 단다.
- 근거 기준: `papers/` 의 원문을 직접 인용한다(파일명 + 원문 문장). `papers/` 에 없는 근거는 "근거 없음"으로 표시한다.
- 형식: 질문 번호마다 [사용자] 원문, [답변 요지], [근거], [미확인·위험], [제안서 반영 위치].

---

## Q1. 이 논문을 쓰는 이유가 무엇인가? (2026-11-18)

**[사용자]** "1. 이 논문을 쓰는 이유가 무엇인가 ?"

**[답변 요지]** 그래디언트 압축이 실제 데이터센터에서 효과가 없는 주된 이유는 압축값을 네트워크 안에서 더할 수 없기 때문이다. 더할 수 있게 만든 시스템(THC 등)은 작업자 수 N에 따라 비트가 늘어나는 대가를 경험적으로만 보고했다. 이 대가가 근본적인지 증명한 이론은 없다. 그래서 대가의 크기를 증명하고 그 한계에 도달하는 부호를 제시하려고 이 논문을 쓴다.

**[근거]**

| 주장 | 출처 (papers/) | 원문 |
|---|---|---|
| R1. 통신은 분산 학습의 병목이다 | modern/SwitchML_NSDI21.pdf §2 | "At 10 Gbps, all but three workloads spend more than 50% of their time in communication" / "even so communication remains a significant share (at least 17%) of batch processing time for half of the workloads" |
| | modern/UtilityGradComp2022.pdf §1 | "millions to billions of parameters are communicated among nodes [6], which has been shown to lead to communication bottlenecks" |
| R2. 압축은 실제로 거의 효과가 없다 | modern/UtilityGradComp2022.pdf 초록 | "only in 6 cases out of more than 200, gradient compression methods provide speedup over optimized synchronous data-parallel training in the typical data-center setting" |
| R3. 그 주된 원인은 압축값을 더할 수 없다는 점이다 | modern/UtilityGradComp2022.pdf §4 | "For an operation to be compatible with all-reduce it must be associative ... In these cases, to perform gradient aggregation, the workers need to perform an all-gather operation. This can lead to high communication costs, leading to poor scalability" |
| | 같은 논문 §1 | "signSGD, which is not compatible with all-reduce, takes 1042ms ... while PowerSGD, which is compatible with all-reduce, takes only 470ms" |
| | modern/GradiVeQ.pdf 초록 | "these techniques could perform poorly when used together with ... ring all-reduce (RAR), mainly due to their inability to directly aggregate compressed gradients" |
| | modern/DRIVE2021.pdf 한계 절 | "DRIVE will not allow for efficient in-path aggregation without decoding the vectors" |
| R4. 스위치는 정수 덧셈만 할 수 있다 (합 호환 제약의 물리적 근거) | modern/SwitchML_NSDI21.pdf | "Floating-point operations exceed the computational power of today's switches. We instead convert floating-point values to 32-bit integers" |
| R5. 합 호환 압축에는 N에 따른 대가가 있다고 관찰됐지만 증명은 없다 | modern/THC2024.pdf 평가 절(Scalability) | "the maximum aggregated result is m = g × (# of workers) and the number of bits needed to send this value downstream is ⌈log2 m⌉. If we keep the number of bits sent downstream constant, we must decrease the granularity for a larger number of workers to prevent overflow, which increases the error." |
| | 같은 곳 | "we cannot increase the number of workers to an arbitrary large size without incurring costs to accuracy" |
| | modern/THC_followup2024.pdf | "As the number of workers n increases, our saturation-based aggregation has to allocate more communication bits b > q to upper-bound the probability of overflows." |
| R6. 이론 연구는 이 구조(복호 없이 더하기만 하는 중간 노드)를 다루지 않는다 | modern/Davies2021_DME_lattice.pdf Alg. 3 (p.14) | "Machine v decodes (using xv ) and averages all received inputs" (중간 노드가 메시지마다 복호함) |
| | modern/CERAR2026_ring_allreduce.pdf §1 | "From an information-theoretic perspective, one can consider the problem of recovering the sum with arbitrarily small (but nonzero) error; the lower bound of [3] does not apply in this case." |
| | modern/EDEN2022.pdf 결론 | "It is also interesting to explore if EDEN can be adapted to all-reduce techniques" |
| R7. 필요한 도구는 1970년대에 이미 있다: 합만 필요하면 선형 부호가 유리하다 | classic/05_Koerner-Marton1979.pdf | "This result may be surprising since it disproves a natural conjecture concerning the general solution of the two-help-one problem." / "The proof of Theorem 1 is based upon a suitable interpretation of Elias' theorem on linear codes" (대상: "modulo-two adder source network") |
| | modern/Appuswamy_netcomp.pdf | "work ... on computing the sum (over a finite field) of source messages" (손실 없는 합 계산만 다룸) |

**[미확인·위험]**
- SPEC 2.1의 P1 근거(Yole Group 2026, Lightmatter 2026, Ultra Ethernet 1.0)는 papers/에 없다 → **근거 없음**. 제안서에서는 R1(SwitchML, Agarwal 등)로 대체했다.
- "대가 = ½log₂N 비트"는 **가설**(SPEC 정리 A)이며 증명 전이다. 제안서에서는 "규명한다"로 쓰고 수치는 가설로 표시한다.
- R6 "이론이 다루지 않는다"는 6편(Davies, CERAR, THC+후속, DRIVE, EDEN) 본문 점검까지만 확인됐다. **modern/YangGroverKar_innetwork_RD.pdf** 는 트리 망의 손실 선형 함수 계산의 율-왜곡 한계를 다룬다("fundamental limits on network computation rate as a function of incremental distortions"). 가장 가까운 선행연구이므로 본문 점검이 필요하다. Krithivasan–Pradhan, GradiVeQ, SwitchML 본문도 하한 유무를 점검해야 한다.
- R2의 Agarwal 등 결과는 2021년 하드웨어(V100, 최대 96 GPU) 기준이다.

**[제안서 반영]** proposal.md §1 연구 필요성.

---

## Q2. 압축이 필요한 이유 / "더할 수 있게 만든 시스템"의 뜻 / 루트 PDF 3편의 개념 (2026-11-18)

**[사용자]** "그래디언트 압축이 네트워크에서 필요한 이유는 무엇인가? 더할 수 있게 만든 시스템은 구체적으로 무엇을 의미하는가? 1301.6467v5.pdf, 1701.06416v2.pdf, Source_coding_with_side_information_at_the_decoder_revisited.pdf 세 논문이 주는 개념은 무엇인가?"

### Q2-a. 그래디언트 압축이 네트워크에서 필요한 이유

**[답변 요지]** 집계 알고리즘 쪽에서는 더 줄일 여지가 없다. 손실 없는 링 All-Reduce는 작업자 수와 상관없이 작업자당 약 2d개의 값을 보내며, 정확한 합 복원 기준으로 최적이다. 그런데도 통신 시간이 학습 시간의 큰 몫을 차지한다. 남은 수단은 값 하나에 쓰는 비트를 줄이는 것, 즉 압축이다. 다만 압축이 늘 이득은 아니고, 대역폭이 낮을 때 효과가 크다.

| 주장 | 출처 | 원문 |
|---|---|---|
| 통신이 학습 시간의 큰 몫이다 | modern/SwitchML_NSDI21.pdf §2 | "At 10 Gbps, all but three workloads spend more than 50% of their time in communication" / "DeepLight at 10 Gbps spends 97% of its batch time in communication" |
| GPU가 빨라질수록 통신 비중이 커진다 | 같은 곳 | "Faster GPUs would reduce the computation time, increasing the relative communication fraction." |
| 손실 없는 링 All-Reduce는 이미 최적이다 → 알고리즘으로는 더 못 줄인다 | modern/CERAR2026_ring_allreduce.pdf §1 | "each worker transmits and receives a total of 2(N − 1)d/N real values. For large N , the load normalized by d approaches 2" / "The basic Ring All-Reduce algorithm is nominally considered to be optimal from the point of view of recovering the sum ... exactly [3]." |
| 정확한 복원을 포기하면 그 최적성이 더는 성립하지 않는다 | 같은 곳 | "one can consider the problem of recovering the sum with arbitrarily small (but nonzero) error; the lower bound of [3] does not apply in this case. We note that approximate recovery often suffices in scenarios such as distributed parameter training" |
| 압축은 대역폭이 낮을 때 이득이 크다 (조건부 필요성) | modern/UtilityGradComp2022.pdf §1 | "at lower bandwidths gradient compression can provide significant benefits" |

**[미확인·위험]** 반대 근거도 같은 논문에 있다. 데이터센터 기본 설정에서는 200개 이상 설정 중 6개만 이득이었다(Q1 R2). 따라서 "압축이 필요하다"보다 "압축이 이득을 내려면 합 호환이어야 한다"가 정확한 주장이다.

### Q2-b. "더할 수 있게 만든 시스템"의 구체적 의미

**[정의]** 작업자들의 압축값 C(g₁), …, C(g_N)을 중간 노드(스위치·링의 이웃 노드)가 **복원하지 않고 그대로 더해도**, 그 합에서 원래 합 Σg_n의 추정을 얻을 수 있는 압축. 수식으로는 Decomp(Σ C(g_n)) ≈ Σ g_n이다. 논문마다 이름이 다르다: "compatible with all-reduce"(결합 법칙), "commutable with the gradient aggregation"(GradiVeQ), "homomorphic"(THC, Li 등). 이 연구의 용어로는 **합 호환(sum-compatible)** 이다.

| 시스템 | 무엇을 더하나 | 출처·원문 |
|---|---|---|
| 조건 정의 | 결합 법칙을 만족해야 All-Reduce에 쓸 수 있다 | UtilityGradComp2022: "For an operation to be compatible with all-reduce it must be associative, i.e., the order of operations should not matter." |
| GradiVeQ (2018) | PCA 선형 압축. 압축과 합의 순서를 바꿔도 같다 | GradiVeQ.pdf: "the compression function should be commutable with the gradient aggregation ... Σ Q(g_n) = Q(Σ g_n)" (식 (1)) |
| SwitchML (NSDI '21) | 압축이라기보다 32비트 고정소수점 정수. 스위치가 정수를 더한다 | SwitchML_NSDI21.pdf: "We instead convert floating-point values to 32-bit integers" / "using a per-packet scaling factor f" |
| THC (NSDI '24) | 4비트 정도의 격자 인덱스 → 표를 거쳐 정수로 바꾼 값을 더한다 | THC2024.pdf: "the PS only performs table lookups and summation without decompressing the vectors and without additional processing and re-compression that increases the error" |
| Li 등 (2024) 무손실 동형 압축 | Count Sketch(선형) + 비트맵 색인(OR) | LosslessHomomorphic2024.pdf: "Count Sketch, satisfying Y(ΣX)=ΣY(X), and a compact indexing structure B, satisfying B(ΣX)=∨B(X)" |
| 반례: signSGD, Top-k | 다수결·희소 선택은 결합 법칙이 없어 All-Gather로 빠진다 | UtilityGradComp2022: "Majority vote operation is not associative thus requiring use of all-gather." |

**[이 연구와의 연결]** 위 시스템들이 공통으로 내는 대가는 THC의 ⌈log₂(g·N)⌉ 비트다(Q1 R5). SPEC 3.2의 수학 모델(같은 유한 아벨 군 G 위의 메시지, 스위치는 군 덧셈만 함)은 이 시스템들을 추상화한 것이다. SwitchML(32비트 정수 = ℤ_{2^32})과 THC(정수 인덱스 합)가 직접 대응한다.

### Q2-c. 루트 PDF 3편이 주는 개념

공통 배경: 세 편 모두 **부가 정보가 있는 분산 소스 부호화**를 다룬다. 즉 복호기가 원하는 것은 소스 하나(또는 그 함수)이고, 다른 단말의 정보는 돕는 역할만 한다. 이 연구의 구조와 같다. 복호기는 합 S만 원하고, 이전 반복의 예측 S′이 부가 정보다.

**(1) Watanabe–Kuzuoka–Tan, "Non-Asymptotic and Second-Order Achievability Bounds for Coding With Side-Information" (arXiv 1301.6467, IEEE Trans. IT)**
- 개념: **유한 블록 길이(finite blocklength) 분석과 2차 부호화율(second-order coding rate)**. 블록 길이 n이 유한할 때 필요한 여분 전송률이 대략 S(V,ε)/√n 꼴임을 WAK·WZ·GP 세 문제에서 보였다. 증명 도구는 채널 해상도(channel resolvability)와 우도 부호기(likelihood encoder)다.
- 원문: "for a fixed test channel PU|Y, the redundancy at blocklength n in order to achieve an error probability ε > 0 is governed by the term S(V,ε)/√n"
- 원문: "our non-asymptotic achievability bound for the WZ problem, when suitably specialized, yields the correct dispersion for lossy source coding"
- 이 연구에 주는 것: SPEC은 d → ∞ 를 가정한다. 그러나 실제 All-Reduce는 그래디언트를 버킷 단위로 나눠 보낸다(UtilityGradComp2022: "create fixed size buckets"). 실제 블록 길이는 버킷 크기이므로, ½log₂N 대가에 √(1/n) 보정이 얼마나 붙는지 계산할 틀이 된다. WZ = 복호기 쪽 부가 정보(S′) 문제다.
- 차이: 오차 척도가 평균제곱오차(MSE)가 아니라 초과 왜곡 확률("Pr(d(X, X̂) > D)")이다. 달성 한계만 있고 역 한계는 없다. 합 호환 제약도 없다.

**(2) Wolf–González–Dörpinghaus–Santos Filho–Fettweis, "On The Binary Lossless Many-Help-One Problem with Independently Degraded Helpers" (arXiv 1701.06416)**
- 개념: **다수 조력자-단일 복원(many-help-one) 문제**. 복호기는 주 소스 X₀ 하나만 원하고, L개의 조력자가 각자 압축해 돕는다. 일반해는 있지만 보조 확률변수(auxiliary random variable)에 대한 최적화로 주어져 계산이 어렵다. 저자들은 이진 대칭 경우에서 계산 가능한 내부 한계를 구했다(Theorem 2, 3).
- 원문: "its solution is given in terms of a convex closure over a set of auxiliary random variables ... Providing the solution is surprisingly difficult even for an example as basic as binary sources."
- 원문: "Körner and Marton [3] addressed a two-help-one problem where the primary source is a modulo-two sum of correlated binary auxiliary sources."
- 이 연구에 주는 것: (i) 우리 문제는 "N-help-one"에서 원하는 것이 **합**인 경우다. Körner–Marton이 그 2개짜리 이진 원형이다. (ii) 보조 확률변수 형태의 일반해는 구체적인 N 의존성(½log₂N)을 알려 주지 않는다. 그래서 격자처럼 구조가 있는 부호와 명시적 한계가 필요하다는 동기가 된다.
- 차이: 무손실, 이진 소스, 주 소스 X₀도 직접 부호화됨, 합 호환 제약 없음.

**(3) Uyematsu–Matsuta, "Source Coding with Side Information at the Decoder Revisited" (ISIT 2015)**
- 개념: **일반 소스(general source)에 대한 단일 시행(one-shot) 역 정리**. WAK 시스템에서 오류 확률 ε을 허용할 때의 전송률 영역을 평활 최대 엔트로피(smooth max-entropy)와 평활 최대 Rényi 발산(smooth max Rényi divergence)으로 정확히 구했다. i.i.d.·정상성 가정이 없다.
- 원문: "we show a new one-shot converse theorem for the WAK coding system, and a one-shot covering lemma which is a refined version of Warsi's result"
- 이 연구에 주는 것: 핵심 정리 A-3는 "단일 라운드" 부호 전체에 대한 역 한계다. 실제 그래디언트는 i.i.d.가 아니다. one-shot 역 정리 기법은 i.i.d. 가정 없이 역 한계를 세우는 후보 도구다.
- 차이: 무손실(ε-오류), 유한·가산 알파벳, 두 단말뿐, 합 호환 제약 없음.

**[미확인·위험]**
- 세 편 모두 합 호환 제약이나 네트워크 내 계산을 다루지 않는다. 신규성을 위협하지는 않고, **도구와 배경**으로 쓴다.
- 세 편은 papers/ 로 옮기지 않았다(루트에 그대로 있음). README 목록에도 없다.

**[제안서 반영]** proposal.md §1.1 보강, §2 핵심 개념 정의, §3 관련 연구(부가 정보 소스 부호화).

---

## Q3. 통신을 모르는 사람을 위한 배경 설명 (2026-11-18)

**[사용자]** "통신을 전혀 모르는 사람이다. 집계 알고리즘은 무엇인가? 뭐를 압축하는 것인가? 배경을 구체적인 예시로 설명해라. 노드는 뭐고 압축값은 무엇인지 설명해라. 분산 소스 부호화는 뭐고 복호기는 무엇인가?"

**[답변 방식]** 용어마다 쉬운 정의 → 숫자 예시 → 원문 근거 순서로 쓴다. 숫자 예시는 설명용으로 만든 것이며, 원문 수치가 아니다.

### 용어와 근거

| 용어 | 쉬운 정의 | 원문 근거 |
|---|---|---|
| 그래디언트(gradient, 기울기) | AI 모델의 손잡이(매개변수)마다 "어느 쪽으로 얼마나 돌리면 오답이 줄어드는가"를 적은 숫자 목록. 손잡이 수만큼 숫자가 있다 | UtilityGradComp2022: "During the computation phase the gradient of the model is typically computed using backpropagation." / "millions to billions of parameters are communicated among nodes" |
| 작업자(worker) = 노드(node) | 계산을 나눠 맡은 컴퓨터(GPU) 한 대. 망에서 데이터를 주고받는 지점이면 모두 노드다(스위치도 노드) | GradiVeQ: "RAR places all nodes in a logical ring" / SwitchML: "workers compute model updates and send them to parameter servers" |
| 집계(aggregation) | 모든 작업자의 그래디언트를 더해 합을 모두가 나눠 갖는 단계 | UtilityGradComp2022: "an aggregation phase, where gradients are synchronously averaged among all participating nodes" |
| 집계 알고리즘 | 누가 누구에게 무엇을 어떤 순서로 보내 합을 만드는지 정한 절차. 대표적으로 중앙 서버 방식(파라미터 서버), 링 All-Reduce, 스위치 내 집계가 있다 | SwitchML: "Today's ML toolkits implement this communication phase in one of two ways: The parameter server (PS) approach ... The all-reduce approach" / GradiVeQ: "Upon the reception of a segment, a node will add to it the same segment of its own, and then send the sum to the next node in the ring." |
| 스위치(switch) | 컴퓨터들을 잇는 망의 중계기. 최근 것은 프로그래밍이 가능해 정수 덧셈을 할 수 있다 | SwitchML: "uses a programmable switch dataplane to execute a key step of the training process" / "the computing units inside a programmable switch operate on integer values" |
| 압축 대상 | 각 작업자가 보내는 그래디언트 숫자 목록. 숫자 하나는 보통 32비트 | SwitchML: 모델 크기 "in 100s-of-MB or GB range ... today's largest models exceed 32 GB" / UtilityGradComp2022: signSGD는 "1 bit is sent for each float (32 bit) leading to 32× compression" |
| 압축값 | 압축한 결과로 실제로 보내는 짧은 비트열. 예: 0.3을 "3"이라는 4비트 정수로 보냄 | GradiVeQ: "number of bits used to describe the gradients. Popular methods include gradient scalar quantization (lossy) ... and sparsity coding (lossless)" |
| 부호기(encoder) / 복호기(decoder) | 부호기는 숫자를 짧은 비트열로 바꾸는 쪽(압축), 복호기는 비트열을 다시 숫자로 되돌리는 쪽(압축 해제). zip과 unzip에 해당한다 | Slepian–Wolf 1973: "The decoder then produces the messageblock X* as its estimate of X." |
| 분산 소스 부호화(distributed source coding) | 서로 관련 있는 정보를 가진 여러 단말이 **서로 상의하지 않고 각자** 압축하고, 복호기 하나가 그것들을 모아 푸는 문제 | Slepian–Wolf 1973: "The encoder of each source is constrained to operate without knowledge of the other source, while the decoder has available both encoded binary messagestreams." |
| 넘침(overflow) | 더한 값이 정해진 비트 칸에 안 들어가는 현상 | GradiVeQ: "summing two scalar quantized gradients will incur overflow due to limited quantization levels" |

### 숫자 예시 (설명용으로 만든 값)
- 작업자 4대, 손잡이 3개. g₁=(0.3, −0.2, 0.1), g₂=(0.2, −0.1, 0.0), g₃=(0.4, −0.3, 0.2), g₄=(0.1, −0.2, 0.1). 필요한 것은 합 (1.0, −0.8, 0.4).
- 압축: 0.1 단위로 반올림한 정수를 보낸다. g₁ → (3, −2, 1). 4비트 부호 있는 정수는 −8~7을 담는다. 원래 32비트였으므로 8배 압축이다.
- 스위치가 정수를 더한다: (3+2+4+1, −2−1−3−2, 1+0+2+1) = (10, −8, 4). 10은 4비트 칸(최대 7)을 넘친다.
- 작업자가 4배 많으면 합의 범위도 최대 4배이므로 2비트(= log₂4)가 더 필요하다. 작업자별 값이 서로 독립적으로 흔들리면 합의 흔들림은 √N배로 커지므로 ½log₂N비트가 더 필요하다. 이것이 SPEC 정리 A의 가설이다(증명 전). THC의 "⌈log2 m⌉, m = g × (# of workers)"(Q1 R5)가 같은 현상이다.

### 이 연구에서 분산 소스 부호화와 복호기의 대응
- 소스 = 각 작업자의 그래디언트. 작업자들은 서로의 값을 모르고 각자 압축한다(분산).
- 복호기 = 스위치가 더한 결과 Z를 받아 합의 추정값으로 되돌리는 단계. 각 작업자 안에서 돌아간다.
- 보통의 분산 소스 부호화와 다른 점: 복호기가 각 압축값을 따로 받지 못하고 **더해진 것 하나만** 받는다. 이것이 합 호환 제약이다.

**[미확인·위험]** 숫자 예시는 설명용이며, 실제 4비트 압축(THC)은 회전·표 변환 등을 더 쓴다.

**[제안서 반영]** proposal.md 부록 A "배경 설명(비전공자용)".

---

## Q4. 논문은 무엇을 해결하고자 하는가 (2026-11-18)

**[사용자]** "논문은 무엇을 해결하고자 하는 것인가?"

**[답변 요지]** 해결하려는 문제는 하나다. **스위치가 압축값을 풀지 않고 더하기만 하도록 허용하면, 각 작업자는 비트를 최소 몇 개 더 보내야 하는가? 그 추가 비트는 어떤 압축 방식으로도 피할 수 없는가?** 이를 위해 (i) 그 최소 추가 비트의 하한을 증명하고(역 한계, converse), (ii) 하한에 도달하는 압축 방식을 제시하고(달성, achievability), (iii) 그 결과로 "스위치에서 더하기"와 "모두 모아서 따로 풀기(All-Gather)" 중 언제 무엇이 유리한지 경계를 준다.

### 근거: 문제가 실재한다
| 주장 | 출처 | 원문 |
|---|---|---|
| 추가 비트 현상은 실제 시스템에서 관찰된다 | THC2024 §평가 'Scalability' | "the number of bits needed to send this value downstream is ⌈log2 m⌉. If we keep the number of bits sent downstream constant, we must decrease the granularity for a larger number of workers to prevent overflow, which increases the error." |
| 그 대가 때문에 작업자 수를 마음대로 늘릴 수 없다 | 같은 곳 | "we cannot increase the number of workers to an arbitrary large size without incurring costs to accuracy" |
| 후속 연구도 경험적으로만 다룬다 | THC_followup2024 | "As the number of workers n increases, our saturation-based aggregation has to allocate more communication bits b > q to upper-bound the probability of overflows." |
| 더할 수 없는 압축의 대안(All-Gather)은 N에 비례해 비싸다 | UtilityGradComp2022 | "the workers need to perform an all-gather operation. This can lead to high communication costs, leading to poor scalability as we increase the number of processors." |

### 근거: 아직 풀리지 않았다 (6+1편 본문 점검)
| 선행연구 | 무엇을 했나 | 빠진 것 | 원문 |
|---|---|---|---|
| Yang–Grover–Kar 2017 (YangGroverKar_innetwork_RD) | 트리 망, 독립 가우시안 소스의 가중합. **임의의 부호화 방식**에 대한 율-왜곡 바깥 한계(Thm 2)와 오차 누적(Thm 1) | 달성 방식에서 중간 노드가 복호→합→재부호화. 군 덧셈만 하는 제약 없음 | 모델: "The only assumption that we make about the encoding mappings is that each mapping gt outputs a binary sequence of a finite length." / 달성: "decodes these description indices, computes the sum of these descriptions ... and re-encodes" / 향후 과제: "investigate compression algorithms, e.g., lattice codes [18], [39], that achieve the outer bound" |
| Davies 2021 | 격자 + mod q, 부가 정보 복호 | 리더가 메시지를 하나씩 복호 | "Machine v decodes (using xv ) and averages all received inputs" |
| CERAR 2026 | 실수 선형 부호화 링 All-Reduce | 비트·양자화 없음. 정보이론적 근사 합 문제를 열린 문제로 둠 | "the lower bound of [3] does not apply in this case" |
| THC, DRIVE, EDEN | 시스템·알고리즘 | 정리·하한 없음 | (Q1 R5, 9장 표) |

**[중요 수정, 2026-11-18]** Yang–Grover–Kar Thm 2는 제약 없는 부호의 하한이다. 따라서 **정리 A-2(제약 없는 역 한계)는 신규 기여가 아니다.** 이 논문의 결과를 인용하거나 특수화(깊이 1 트리 = 스위치 1단, 합의 문제 = 모든 작업자가 합을 받음)해서 쓴다. 신규 기여 후보는 **A-3(합 호환 역 한계)와, 그것과 A-2의 차이인 Δ_compat**다. 차이: 우리 모델에는 공통 성분 θ와 부가 정보 S′이 있고 그들의 모델에는 없다. 그러나 작업자별 성분이 지배하는 경우에는 이 차이가 사라진다.

### 해결하는 것 / 해결하지 않는 것
- 해결: (1) 합 호환 대가 Δ_compat의 크기와 불가피성(핵심, 가설 ½log₂N 비트/좌표/링크). (2) 대가에 도달하는 격자 부호. (3) 스위치 내 집계 대 All-Gather의 경계. 확장: 다단 트리, 시간 상관(오차 피드백), 학습 수렴 기준.
- 해결하지 않음: 혼잡 제어, 스케줄링, 하드웨어 구현 (SPEC 1.7).

**[미확인·위험]**
- Yang–Grover–Kar의 합의(consensus) 절(Section V)과 Thm 2를 스위치 1단 별형에 특수화했을 때 정확히 ½log₂(Nσ²/D) 꼴이 나오는지는 아직 계산하지 않았다.
- 남은 점검: Krithivasan–Pradhan, GradiVeQ, SwitchML 본문.

**[제안서 반영]** proposal.md §4 "연구 문제와 목표". §1.4에 Yang–Grover–Kar 추가.

---

## Q5. 수학적으로 새로운 개념은 아닌가? (2026-11-18)

**[사용자]** "수학적으로 새로운 개념은 아닌가?"

**[답변 요지]** 개념(문제 틀)은 새롭지 않다. "여러 단말이 각자 압축하고, 복호기는 유한 군 위의 합만 본다"는 틀은 Körner–Marton(1979)과 보안 집계(secure aggregation) 정보이론 문헌에 이미 있다. 도구(격자로 합을 직접 계산하기)도 이미 있다. 새로울 수 있는 것은 **정리 하나**다. 가우시안(평균적 경우) 모델에서 "합만 보는 복호기"에 대한 역 한계, 그리고 그것을 증명하는 기법이다. **최악 경우(유계 입력) 버전은 단순한 개수 논증으로 이미 나와 있다** [Chen2022].

### 이미 있는 것
| 구성 요소 | 출처 | 원문 |
|---|---|---|
| 합만 원하는 분산 압축, 선형 부호가 유리 | 05_Koerner-Marton1979 | "This result may be surprising since it disproves a natural conjecture" (모듈로-2 합, Theorem 1) |
| 격자로 가우시안 소스의 선형 함수를 직접 복원 | KrithivasanPradhan_lattice_DSC | "A portion of this inner bound is achieved by a scheme that reconstructs the linear function directly rather than reconstructing the individual components" / "Our coding scheme relies on lattice coding techniques" |
| 중첩 격자에서 정수 결합(합)을 바로 복호 | NazerGastpar_CF | "nested lattices whose algebraic structure ensures that integer combinations of codewords can be decoded reliably" |
| 서버가 유한 군 위의 합만 본다 | Chen2022_SecAgg_price §2 | "SecAgg is achieved via additive masking over a finite group" |
| **그 틀에서의 통신 하한 (최악 경우)** | Chen2022_SecAgg_price §5, Thm 5.3·Cor 5.4 | "under SecAgg, the individual communication budget each client has is equal to the total number of bits the server can observe ... even if each client sends a b-bit message (so the total information transmitted is n · b bits), the server still can only observe b bits information." / Cor 5.4: "For any encoding function Aenc(·) with output space Z, if the ℓ2 estimation error E‖µ̂ − µ‖² ≤ ξ for all possible x1, ..., xn ∈ Bd(c), then it must hold that log|Z| = Ω(d log(c²/ξ))" |
| 같은 틀, 근사 복원 (평균적 경우) | Chen2023_SecAgg_freq Lemma 3.2 | "Under the β-approximate recovery criterion (C1′) and the security constraints (S1) and (S2), it holds that H(Yi) ≥ R(β)" (R(β) = 합의 율-왜곡 함수) |
| 제약 없는 부호의 하한 (트리 망) | YangGroverKar_innetwork_RD Thm 2 | (Q4) |

### 왜 최악 경우 버전은 이미 있는 셈인가 (계산)
Chen2022 Cor 5.4를 합의 언어로 옮긴다. 입력 ‖x_i‖ ≤ c, 평균 μ의 오차 ξ ⇔ 합 S = nμ의 오차 D = n²ξ. 그러면 log|Z| ≳ d·log(c²/ξ) = d·log(n²c²/D). 정리 A-3의 N² 항이 그대로 나온다. 최악 경우에는 모든 입력이 같은 방향으로 정렬될 수 있어서, 합의 범위가 실제로 N배이기 때문이다. 증명은 "서버가 보는 것은 |Z|개 중 하나"라는 개수 논증뿐이다. (이 환산과 상수는 본 세션의 계산이며 원문에 그대로 있는 식은 아니다.)

### 왜 가우시안 버전은 아직 비어 있는가
- 가우시안 모델에서는 작업자별 성분이 독립이므로 합의 전형적 범위가 √N·σ_ξ다. 위의 개수·엔트로피 논증을 쓰면 H(Z) ≥ R_S(D) = ½log₂(Nσ_ξ²/D)만 나온다. Chen2023 Lemma 3.2도 이 꼴이다. 이것은 **제약 없는 하한(A-2)과 같다** → Δ_compat에 대해 아무것도 말하지 못한다.
- A-3가 주장하는 것은 그보다 ½log₂N 큰 ½log₂(N²σ_ξ²/D)다. 복호기가 보는 Z의 **엔트로피**는 작아도 되지만, 각 작업자가 **해상도** D/N을 가져야 한다는 것을 모든 부호에 대해 보여야 한다. 기존 논증으로는 나오지 않는다(SPEC 5.2와 같은 진단).
- 신규성은 개념이 아니라 이 증명 기법에 있다.

### 새로 드러난 위험: 상관 양자화
| 출처 | 원문 | 의미 |
|---|---|---|
| Suresh2022_correlated_quant Thm 2 | "the proposed estimator OneDimOneBitCQ is unbiased and the mean squared error is upper bounded by (3/n)·σmd(r − l) + 12(r − l)²/n²" | 공유 난수로 작업자들의 양자화 오차를 서로 상쇄시키면, 평균의 오차가 (r−l)²/n이 아니라 σmd(r−l)/n + (r−l)²/n²로 준다. 출력은 격자 위의 값이라 더할 수 있다(합 호환). |
- "각 작업자는 해상도 D/N이 필요하다"는 A-3의 직관은 **오차가 독립일 때만** 맞다. 공유 난수로 오차를 음의 상관으로 만들면 깨질 수 있다.
- 거친 추정(본 세션 계산): 작업자별 성분이 지배하면 σmd ~ r−l이므로 이득이 상수배에 그칠 가능성이 크다. 그러나 증명 전이다. A-3 증명은 이런 부호를 반드시 포함해야 한다.

**[수정 사항]**
- Q1·Q4의 "A-3는 점검한 문헌에 없음"을 고친다 → **최악 경우 A-3는 Chen2022 Cor 5.4에 사실상 있음. 가우시안 A-3는 없음.**
- SPEC 12장 "정리 A의 기준 모델: 가우시안 / 유계 입력" → 권고: 가우시안(평균적 경우)을 주 정리로. 유계 입력 버전은 Chen2022로 인용. (사용자 결정 필요)

**[제안서 반영]** proposal.md §4.2 표 수정, §4.4 "수학적 신규성의 위치" 추가.

---

## Q6. 새로운 발견을 해야 한다 (2026-11-18)

**[사용자]** "새로운 발견을 해야한다."

**[답변 요지]** 목표로 할 새 발견을 하나로 좁힌다.
> **합 호환 대가 ½log₂N의 정체는 "독립 이산 확률변수의 합은 엔트로피가 최소 ½비트씩 자란다"는 이산 엔트로피 거듭제곱 부등식(entropy power inequality)이다. 스위치의 정수 덧셈(ℤ_{2^b})에서는 이 부등식이 깨지는데, 깨지는 경우는 정확히 넘침(wrap-around)이 정보를 지우는 경우다.**

이것이 증명되면 (i) 가우시안 A-3가 처음으로 증명되고, (ii) 가산 조합론(additive combinatorics)의 결과가 네트워크 압축 한계로 처음 연결되며, (iii) ℤ_{2^b} 위의 새 엔트로피 부등식이 수학 쪽 기여가 된다.

### 근거 1: ½비트 상수가 정확히 ½log₂N을 준다
| 출처 | 원문 |
|---|---|
| HighEntropy_sums2026 (Wang), 초록 | "independent discrete random variables X, Y with finite Shannon entropies in bits satisfy H(X + Y) ≥ (H(X) + H(Y))/2 + 1/2 − o(1) in every torsion-free abelian group as max{H(X), H(Y)} → ∞. The same conclusion holds in the prime cyclic group Fp when both max{H(X), H(Y)} and log2 p − max{H(X), H(Y)} tend to infinity." |
| 같은 논문 | "Binomial distributions show that the constant 1/2 is optimal." |
| Tao_sumset_entropy, 초록 | "When G is torsion-free, we also establish the sharp lower bound H(X+X) ≥ H(X) + ½ log 2 − o(1)" (자연로그 기준 ½ln2 = ½비트) |

- 계산(본 세션): 작업자 메시지 E_n의 엔트로피가 각각 h 이상이면, 둘씩 짝지어 더할 때마다 ½비트가 늘어난다. N = 2^k이면 H(Z) ≥ h + ½log₂N − (오차 누적). 공유 난수가 있어도 시드를 고정하면 메시지들은 조건부 독립이므로 적용 가능하다.
- 그러면 log₂|G| ≥ H(Z) ≥ h + ½log₂N. h ≈ ½log₂(Nσ²/D)(해상도 조건)를 넣으면 A-3의 ½log₂(N²σ²/D)가 나온다.

### 근거 2: 이 연결은 (모은 문헌 안에서는) 아직 없다
- 집계·보안 집계·분산 평균 추정 논문 9편(Chen2022, Chen2023, YangGroverKar, Davies2021, SecAgg_capacity2026, Kairouz_DDG, NazerGastpar, THC2024 등)에서 "entropy power"와 "sumset"은 0회 나온다. KrithivasanPradhan은 1회다. ⚠ 모은 문헌 안에서만 확인한 것이다. 외부 검색은 하지 않았다.
- Madiman_prime_cyclic은 이산 EPI가 통신 문제에 쓰일 수 있다고만 언급한다: "in discrete groups would have direct applications to communication and control problems"

### 근거 3: 스위치 군 ℤ_{2^b}는 기존 정리 밖이다 → 수학적 새 질문
- Wang의 정리는 비틀림 없는 군(torsion-free)과 소수 순환군 F_p에서만 성립한다(Cor 1.2: "If they take values in a torsion-free abelian group, or in Fp with H(X) ≤ log2 p − Kε").
- ℤ_{2^b}에는 부분군이 있다. 반례(본 세션): X, Y가 같은 부분군 위에서 균등하면 X+Y도 그 부분군 위에서 균등하다 → H(X+Y) = H(X)이고 엔트로피가 자라지 않는다. Tao의 역 정리도 같은 구조를 말한다: 엔트로피가 거의 안 자라는 변수는 "factorise as X = U + Z where U is uniformly distributed on a coset progression of bounded rank".
- 해석: 엔트로피가 안 자라는 경우는 합이 부분군 안에서 돌아 넘치는 경우다. 따라서 증명해야 할 새 정리는 **"ℤ_{2^b}에서 엔트로피가 ½비트 자라거나, 아니면 넘침 때문에 합에 대한 정보가 사라진다"**는 양자택일이다.

### 근거 4: 상관 양자화는 고해상도에서 반례가 아니다 (시뮬레이션)
`sims/cq_dither.py`. 감산 디더 균일 양자화, 가우시안 입력, 합 오차 분산 ÷ (독립 디더의 값 NΔ²/12). 시행 6000회.

| σ/Δ | N=4 독립 | N=4 상관 | N=64 독립 | N=64 상관 |
|---|---|---|---|---|
| 0.01 | 1.02 | 0.255 | 1.01 | 0.066 |
| 0.1 | 1.00 | 0.565 | 0.98 | 0.557 |
| 0.3 | 1.01 | 0.999 | 1.00 | 0.983 |
| 1.0 | 0.99 | 1.005 | 0.96 | 1.002 |
| 10.0 | 1.01 | 1.019 | 1.02 | 1.048 |

- 고해상도(σ ≥ 0.3Δ)에서는 상관 디더의 이득이 없다 → 해상도 조건 h ≈ ½log₂(Nσ²/D)가 이 영역에서는 유지된다.
- 저해상도(σ ≤ 0.1Δ, 좌표당 1비트 미만)에서는 합 오차가 크게 준다. 이 영역에서는 합 호환 대가가 다를 수 있다 → 두 번째 발견 후보.

### 새 발견 후보 (우선순위)
1. **(주) 가우시안 A-3 = ℤ_{2^b} 위의 이산 EPI + 넘침 양자택일.** 필요한 단계: (a) 해상도 보조정리: 각 메시지 엔트로피 ≥ ½log₂(Nσ²/D) − c. (b) ℤ_{2^b}^d 위의 "½비트 성장 또는 부분군 집중" 정리(Wang + Tao 역 정리의 확장). (c) 부분군 집중 ⇒ 왜곡 하한. (d) 결합.
2. **(부) 저전송률 상전이.** 좌표당 1비트 근처에서는 공유 난수로 오차를 상쇄할 수 있어 대가가 줄거나 사라질 수 있다. 실무 압축(1~4비트)과 맞닿는 영역이다. 근거는 위 시뮬레이션과 Suresh2022 Thm 2뿐이다.

**[미확인·위험]**
- (a) 해상도 보조정리는 미증명이다. 시뮬레이션은 균일 감산 디더만 확인했다. 비균일·비격자 부호는 확인하지 않았다.
- 반복 적용 시 o(1) 오차가 log₂N단계에 걸쳐 누적된다. 균일한 오차 한계가 필요하다(Wang은 명시적 오차 한계를 준다고 씀: "We give explicit error bounds in both settings").
- 신규성은 모은 문헌 안에서만 확인했다. 외부 검색이 필요하다(예: 이산 EPI를 분산 압축·계산과 연결한 문헌).

**[제안서 반영]** proposal.md §4.5 "목표로 하는 새 발견".

---

## Q7. 외부 문헌 검색 (2026-11-18)

**[사용자]** "외부 문헌 검색해라."

**[검색 범위]** 웹 검색 11회. 주제: (1) 이산 군의 엔트로피 거듭제곱 부등식(EPI)을 분산 부호화·합 계산의 역 한계에 쓴 문헌, (2) 보안 집계·네트워크 내 집계의 비트 폭 하한, (3) 가우시안 소스 합의 손실 분산 압축 역 한계, (4) 디지털 공중 계산(over-the-air computation)의 모듈로 합 하한.

### 결정적 발견: Jog–Anantharam (2014)이 Q6 계획의 2단계를 반증한다
- 서지: V. Jog, V. Anantharam, "The Entropy Power Inequality and Mrs. Gerber's Lemma for Groups of Order 2^n", IEEE Trans. IT 60(7):3773–3786, 2014. arXiv 1207.6355. 원문 저장: papers/modern/JogAnantharam2014_EPI_2n.pdf
- Theorem 4.1 (ℤ_{2^n}, 원문): "f2n(x, y) = f2(x − k log 2, y − k log 2) + k log 2, if k log 2 ≤ x, y ≤ (k + 1) log 2; max(x, y) otherwise." 여기서 f2n(x,y) = min_{H(X)=x, H(Y)=y} H(X+Y).
- 최소화하는 분포 (원문): "the random variables X and Y should be supported on the smallest possible subgroup of G (or cosets of the same)"
- k개 합 (§6.2, 원문): "H(X1 + X2 + ... + Xk) = H(X1 + X2 + ... + Xr) = fG,2(x1, fG,2(x2, (...(fG,2(xr−1, xr)))..))" — 부분군 H1(크기 2^{m+1})과 그 부분군 H2 위의 분포로 하한이 달성된다.
- **의미 (본 세션 해석):** x = y = k비트(정수)이면 f2(0,0) = 0이므로 H(X+Y) = k = H(X)다. 즉 ℤ_{2^b}에서는 N개를 더해도 엔트로피가 **전혀 자라지 않을 수 있다**. Q6에서 "반례"라고 쓴 것은 이미 2014년에 정확한 정리로 나와 있다. 따라서 **"엔트로피가 ½비트씩 자란다 → log|G| ≥ h + ½log₂N"이라는 순수 엔트로피 논증은 스위치 군에서 성립하지 않는다.** Wang 2026의 ½비트 결과는 비틀림 없는 군과 F_p(넘침에서 먼 경우)에서만 쓸 수 있다.

### 그래도 남는 공백 (검색으로 찾지 못한 것)
| 찾은 것 | 출처 | 빠진 것 |
|---|---|---|
| 정수 값 변수의 EPI, "used as a key ingredient to prove converse results" | Haghighatshoar–Abbe–Telatar, arXiv 1301.4185 | 합 계산·집계 응용 없음 |
| F_p 조건부 엔트로피 합집합 부등식 (극 부호용) | Guruswami–Velingker, CCC 2015 | 합 호환 역 한계 없음 |
| 선형 부호 전형 합집합, Tao·Madiman과 Nazer–Gastpar를 함께 인용 | Zhu–Gastpar 계열, arXiv 1511.08435 | 손실·가우시안 역 한계 없음 |
| 보안 집계 모듈로 합: "the small sub-optimality gap is due to the modular arithmetic used by SecAgg" (log n 인자) | Chen 등, arXiv 2211.10041 §5.1 | 그 log n이 근본적인지 증명하지 않음 → **우리 질문과 같은 공백을 저자들이 언급** |
| 2개 소스 가우시안 선형 함수의 바깥 한계 | Wagner 2011 "On Distributed Compression of Linear Functions" | N개 소스, N 의존성 없음 |
| 이진 모듈로 합에서 구조적 부호가 이기는 조건 | Tsujino–Watanabe, arXiv 2606.25570 (2026) | 2개 소스, 무손실 |
| 디지털 공중 계산의 모듈로 합 부호 | SumComp arXiv 2310.20504 | 달성만 있고 역 한계 없음 |
| 비트 제약 SGD 하한 (가우시안 평균 추정으로 환원) | Kim, arXiv 2606.00703 (2026) | 단일 단말, 합 호환 없음 |

**검색 결론:** "합 호환(군 덧셈만) 제약 아래 손실 압축의 역 한계가 작업자 수 N에 따라 커진다"를 증명한 문헌은 찾지 못했다. 가장 가까운 언급은 Chen 등 2211.10041의 "log n 차이는 모듈로 연산 때문"이라는 문장이다(증명 없음).

### 계획 수정
- 폐기: Q6 계획 (b) "ℤ_{2^b}에서 ½비트 성장" → Jog–Anantharam Thm 4.1로 거짓임이 확정됐다.
- 대체 (새 핵심 보조정리): **엔트로피 단독이 아니라 복원 조건과 결합한 양자택일.** Jog–Anantharam이 보인 "엔트로피가 안 자라는 분포"는 부분군(의 잉여류) 위에 몰린 분포다. 이때 각 작업자 메시지의 상위 비트가 사실상 버려지므로(합이 부분군 안에서 돈다), 해상도 조건과 범위 조건을 동시에 만족할 수 없음을 보여야 한다. 즉 "엔트로피가 자라지 않는다 ⇒ 메시지가 부분군에 집중된다(Jog–Anantharam 등호 조건, Tao 역 정리) ⇒ 합의 범위 정보가 사라져 왜곡이 크다."
- 이 보조정리는 검색에서 찾지 못했다 → 신규 후보로 유지.
- ℤ_{2^b}의 최소 엔트로피 함수가 정확히 알려져 있다는 점은 오히려 도구가 된다(등호 조건이 명시적).

**[미확인·위험]**
- 검색은 웹 검색 결과와 초록 수준이다. Jog–Anantharam만 원문 PDF로 확인했다.
- 검색어에 걸리지 않는 문헌(특히 2025~2026 보안 집계 정보이론 논문들)이 남아 있을 수 있다.

**[제안서 반영]** proposal.md §4.4 수정 (Jog–Anantharam 반영).

---

## Q8. 근거 문헌 원문 확보 (2026-11-18)

**[사용자]** "[목표] 근거 문헌들을 원문 수준으로 확보한다. 필요시에 사용자에게 논문명을 제공해라."

**[결과]**
- 새로 받은 원문 12편 (첫 쪽 제목 대조 완료): papers/README.md "추가" 표.
- 직접 받아야 할 유료 문헌 18편: papers/TO_DOWNLOAD.md (우선순위 A 3편 / B 8편 / C 7편).

**[정정]** Q7 답변에서 [arXiv cs/0511103](https://arxiv.org/abs/cs/0511103)을 "Wagner–Anantharam, An Improved Outer Bound for Multiterminal Source Coding"로 표기했다. 실제 arXiv 제목은 "An Infeasibility Result for the Multiterminal Source-Coding Problem"(2005)이다. 초록이 "We prove a new outer bound on the rate-distortion region for the multiterminal source-coding problem"로 시작하므로 같은 연구의 초기판으로 보인다. 학술지판(IEEE TIT 54(5), 2008)은 Berkeley 사본으로 따로 받았다.

**[남은 원문 공백]**
- SPEC 11장의 업계 근거(Ultra Ethernet 1.0, Yole 2026, Lightmatter, OIF)는 원문이 없다. 제안서는 이것들 대신 SwitchML 측정을 쓰므로 제안서 근거로는 필요 없다.
- Wagner 2011 "On distributed compression of linear functions"는 arXiv 판이 없다 → TO_DOWNLOAD 우선순위 A.

**[정정 2, 2026-11-18]** Wagner 2011 "On distributed compression of linear functions"는 처음부터 papers/classic/S1_Wagner2011.pdf로 있었다. 확인할 때 번호가 붙은 파일만 대조하고 S1·S2 파일을 빠뜨려서, TO_DOWNLOAD 우선순위 A에 잘못 올렸다. 사용자가 받은 사본(루트 "On_Distributed_Compression_of_Linear_Functions (1).pdf")은 IEEE 다운로드 시각 워터마크(10:29 대 11:41 UTC)만 다른 동일 문서다. Wyner 1975 → classic/02_Wyner1975.pdf, Schuchman 1964 → classic/16_Schuchman1964.pdf로 정리했다.

---

## Q9. 새 발견을 위해 자료를 더 모은 것 아닌가? (2026-11-18)

**[사용자]** "새로운 발견을 위해서 추가로 자료를 모은 것인 아니가?"

**[답변 요지]** 맞다. 일부는 새 발견을 위해 모았다. 하지만 **모아만 두고 본문은 거의 읽지 않았다.** 그리고 계획이 Q7에서 바뀐 뒤, 바뀐 계획에 꼭 필요한 도구는 아직 모으지 않았다.

### 모은 자료의 용도별 구분 (papers/modern 46편, classic 20편)
| 묶음 | 용도 | 본문을 읽었나 |
|---|---|---|
| 1차 점검 7편 (YangGroverKar, Chen2022, Chen2023, Suresh2022 등) | 신규성 확인 (Q4·Q5) | 읽음 |
| Q6 도구 4편: Tao_sumset_entropy, KontoyiannisMadiman_sumset, Madiman_prime_cyclic, HighEntropy_sums2026 | **새 발견용** (½비트 성장) | 초록·주정리만 인용 |
| Q7 검색 7편: JogAnantharam2014, HaghighatshoarAbbeTelatar2014, GuruswamiVelingker2015, ZhuGastpar, TsujinoWatanabe2026, SumComp2023, Kim2026 | **새 발견용** + 신규성 | JogAnantharam만 정리 본문 확인. 나머지는 초록 수준 |
| Q8 원문 확보 (Wyner 1975, Schuchman 1964, WagnerAnantharam 2008 등) | 제안서 인용 근거 | 서지 대조만 함 |

### 새 핵심 보조정리에 비추어 본 공백
Q7 이후 핵심 보조정리는 "ℤ_{2^b}에서 엔트로피가 자라거나, 아니면 메시지가 부분군에 몰려 왜곡이 커진다"이다. 이것을 증명하려면 **안정성(stability) 형태의 역 정리**가 필요하다. 엔트로피가 *거의* 안 자라면 분포가 부분군 위 균등에 *정량적으로* 가깝다는 정리다. 모은 문헌은 그 도구를 주지 않는다.

| 문헌 | 주는 것 | 부족한 점 | 원문 |
|---|---|---|---|
| Tao_sumset_entropy | 일반 아벨 군의 역 정리 | 상수가 O(1)이라 정성적이다. ½비트 수준의 정량을 주지 않는다 | "H(X1 +X2 ) = H(X)+ O(1) ... factorise as X = U + Z where U is uniformly distributed on a coset progression of bounded rank, and H(Z) = O(1)" |
| GuruswamiVelingker2015 | 조건부 엔트로피 증가의 정량 하한 | 소수 q에서만 성립하고, 합성수에는 부분군 반례가 있음을 명시한다 | "The assumption of q being prime is necessary: for X supported uniformly on a proper subgroup of Zq we have H(X + X) = H(X)." |
| JogAnantharam2014 | ℤ_{2^n}의 최소 엔트로피 함수와 최소화 분포 (정확한 값) | 등호 조건만 준다. "거의 최소면 거의 부분군"이라는 안정성 결과는 없다 (본문에서 stabil·robust·approximate 검색 결과, 관련 문장 0건) | "supported on the smallest possible subgroup of G (or cosets of the same)" |

- 보조정리의 두 번째 고리("부분군 집중 ⇒ 왜곡 하한")에 대한 문헌은 아직 하나도 모으지 않았다.

**[다음에 모을 것 (미확보·미확인)]**
- Gowers–Green–Manners–Tao의 엔트로피판 다항 Freiman–Ruzsa(PFR) 정리. F_2^n판(2023)과 유계 비틀림 군(bounded torsion)판(2024)이 있다. 엔트로피 Ruzsa 거리가 작으면 부분군 위 균등과 가깝다는 *다항 정량* 정리로, 우리에게 필요한 안정성 도구에 가장 가깝다. ⚠ 기억에 근거한 서지다. 원문으로 확인하지 않았다. ℤ_{2^b}의 비틀림 2^b는 b와 함께 커지므로 상수가 b에 어떻게 의존하는지가 관건이다.
- ℤ_{2^n} 또는 유한 아벨 군에서 엔트로피 거듭제곱 부등식(EPI)의 안정성 결과 (검색 필요).

**[미확인·위험]** 위 공백 판단은 모은 문헌 안에서 내린 것이다. Tao 논문 본문(정량판 정리가 있는지)은 아직 정독하지 않았다.

---

## Q10. 안정성 도구 문헌 수집과 Tao 논문 정독 (2026-11-18)

**[사용자]** "안정성 도구 문헌을 찾아 받고, Tao 논문 본문에서 수치로 된 정리가 있는지 정독해라"

**[답변 요지]**
1. Tao 논문에서 정량적인 것은 균등화 정리(Thm 4.1)뿐이다. 핵심인 역 정리(Thm 1.11)와 ½비트 정리(Thm 1.13)는 상수가 명시되지 않았거나 수렴 속도가 없다.
2. **새로 드러난 문제 (차원):** Tao·Wang의 ½비트는 합 하나당 *전체* 증가량이다. 좌표 d개짜리 블록 부호에서는 합마다 d/2비트(좌표당 ½비트)가 늘어야 A-3가 나온다. Q6의 계산은 사실상 d = 1(좌표별 스칼라 부호)만 다뤘다.
3. 새로 받은 문헌 7편 중 ℤ_{2^b}에 바로 쓸 수 있는 정량 안정성 정리는 없다. 가장 가까운 것은 GGMT 2024이며, 상수가 m³ = 2^{3b}으로 b에 지수적으로 커진다.

### Tao_sumset_entropy 정독 결과
| 정리 | 내용 | 정량성 | 원문 |
|---|---|---|---|
| Thm 1.11 (역 정리) | σ[X] ≤ K이면 X는 계수 O_K(1)인 잉여류 진행(coset progression) H+P 위 균등 분포와 수송 거리(transport distance) O_K(1) 이내에 있다 | ✗ 상수가 K에 삼중 지수적이고 명시되지 않음 | "The implied constants in Theorem 1.11 can be explicitly computed from the proof, but are rather poor (being triple exponential in K). We will not attempt to optimise these constants here." |
| Thm 1.13 (½비트) | 비틀림 없는 군에서 σ(X) ≥ √2 − ε | ✗ "H(X)가 충분히 크면"이며 속도가 없음 | "provided H(X) is sufficiently large depending on ε" |
| Thm 4.1 (균등화) | 유한 군에서 H(p) ≥ log|G| − log K이면 수송 거리 disttr(p, U_G) ≪ log K | ✓ 절대상수이고 군의 크기·비틀림과 무관 | "Then disttr (p, pU ) ≪ log K. ... with significantly better dependence on the constants." |
| Cor 4.6 | 계수 d인 고유(proper) 잉여류 진행 위에서 같은 결과, ≪ log K + d | ✓ | (37) |
| Lemma 5.3 (합 엔트로피 증가 공식) | H(X+Y) − H(X)를 log₊ 합으로 표현 | ✗ 덧셈 오차 O(1). ½비트 규모에서는 쓸 수 없음 | "= H(X + Y ) − H(X) + O(1)" |
| Thm 1.10 (16)(17) | Ruzsa 삼각부등식, 합·차 부등식 | ✓ 상수 1, 3 | "distR (X, −Y ) ≤ 3 distR (X, Y )" |

**증명 구조에서 얻은 것 (본 세션 해석):** Thm 1.13의 증명은 (1) 역 정리로 X ≈ U + Z(U는 H+P 위 균등)로 쓰고, (2) 비틀림이 없으므로 유한 부분군 H가 자명해지며 ("Since G is torsion-free, the H component of the coset progression is trivial"), (3) P를 ℤ^d의 상자로 Freiman 동형 사상해 연속 EPI로 넘어간다. ℤ_{2^b}에서는 (2)가 깨지며, 깨질 때 남는 H가 정확히 Jog–Anantharam의 최소화 분포다. 따라서 "H가 자명하면 ½비트 성장, 아니면 부분군 집중"이라는 우리 양자택일은 Tao 증명의 분기와 같은 모양이다. 다만 이 경로를 그대로 쓰면 상수가 정성적(O_K(1))이다.

### 새로 받은 문헌 7편 (papers/README.md "추가 2")
| 파일 | 핵심 정리 (원문, PDF 대조) | ℤ_{2^b}에 쓸 수 있나 |
|---|---|---|
| GGMT2024_Marton_boundedtorsion (arXiv 2404.02244) | Thm 1.3: "Suppose that G is an abelian group of torsion m. ... Then there exists a subgroup H ⩽ G such that d[X; UH ], d[Y ; UH ] ≪ m3 d[X; Y ]." | 구조는 맞다. 그러나 m = 2^b이므로 상수가 2^{3b}. 저자도 "can probably be improved"라고 씀 (⚠ 이 문장은 에이전트 인용, 미대조) |
| GGMT2023_Marton_F2n (arXiv 2311.05762) | Thm 1.8: F_2^n에서 d[X;U_H] ≤ 6 d[X;Y] (⚠ 에이전트 인용, 미대조) | ✗ 비틀림이 2인 군만 해당 |
| Karam2024_Marton_type_entropy (arXiv 2406.10872) | Thm 1.5: "if ǫ ∈ (0, exp(−2)), G is an abelian group, and A ⊂ G is a non-empty finite distributional ǫ-approximate group, then \|A∆(H + {x})\|/\|H\| ≤ (240 log(ǫ−1 \|A\|))ǫ" | 상수가 비틀림과 무관하다. 그러나 집합의 균등 분포만 다룬다. 일반 분포로 확장하는 것이 유망한 경로 |
| GavalakisKontoyiannis2026_EPI_compact_groups (arXiv 2608.22534) | 진부분군이 없는 군에서 KL 안정성. "If G has proper open subgroups, then there is no hope of having stability results in relative entropy." | ✗ 직접은 안 됨. 장애물이 부분군 집중뿐임을 확인해 줌 |
| FradeliziGavalakisRapaport2024_discrete_entropy_Zd (arXiv 2401.15462) | Thm 3: ℤ^d, 부류 C(c1,c2,c3)(로그오목 계열)에서 "H(X1 + · · · + Xn+1 ) ≥ H(X1 + · · · + Xn ) + (d/2) log((n+1)/n) − o(1)" | **차원 비례 이득이 있는 유일한 결과**. 그러나 로그오목 계열만 해당하고, 유한 군에는 쓸 수 없다 |
| GreenMannersTao2023_sumsets_entropy_revisited (arXiv 2306.13403) | 엔트로피 doubling 이론 | ⚠ 본문 미확인 |
| MadimanKontoyiannis2015_Ruzsa_divergence (arXiv 1508.04089) | Ruzsa 발산 삼각부등식 | 보조 도구. ⚠ 정리문 미대조 |

### 찾지 못한 것
- 일반 분포에서 ℤ^d나 ℤ_{2^b}^d 위 차원 비례(exp(2H/d) 꼴) 이산 EPI.
- b에 다항 이하로 의존하는 ℤ_{2^b} 안정성 정리.
- Jog–Anantharam 극값의 안정성(근사 극값) 결과.
- "부분군 집중 ⇒ 왜곡 하한"을 잇는 문헌 (검색하지 않음).
- ⚠ arXiv 2512.04433 (단독 저자, 미심사)은 ℤ/Nℤ에서 다항 PFR을 주장한다. 받지 않았다. 검증이 필요하다.

### 계획에 주는 의미
- **차원 문제가 가장 크다.** 좌표당 ½비트를 보장하려면 메시지가 d개 방향 모두로 퍼져 있다는 조건을 써야 한다. 일반 분포의 최소화 예는 사실상 1차원 분포라 전체 ½비트만 준다. 우리 문제에서는 해상도 조건(왜곡 D/N)이 모든 좌표로 퍼짐을 강제하므로, 이를 이용하는 것이 길이다. 이 부분이 신규성의 핵심이자 가장 어려운 부분이 된다.
- 단순히 균등 잡음을 더해 연속 EPI로 넘기는 방법은 실패한다 (본 세션 계산). H(ΣX_n) ≥ h(Σ(X_n+U_n)) − h(ΣU_n)로 바꾸면 EPI가 주는 (d/2)log₂N 이득을 h(ΣU_n) ≈ (d/2)log₂(2πeN/12)가 그대로 지운다. 고해상도에서 짧은 방향으로만 평활화하는 Tao 6장의 방식이 필요하다.
- 넘침 쪽: Tao Thm 4.1(절대상수)은 "합의 엔트로피가 log|G|에 가까우면 합은 사실상 균등이라 정보가 없다"를 정량적으로 준다. 양자택일의 (c) 단계에 쓸 수 있는 후보다.
- 이 차원 문제는 단일 문자(d = 1, 좌표별 양자화) 부호에는 해당하지 않는다. 실제 시스템(THC, SwitchML)은 좌표별 양자화를 쓴다. 따라서 **좌표별 부호로 한정한 A-3을 먼저 증명하는 것**이 현실적인 1단계다.

**[미확인·위험]** 차원 문제와 평활화 실패는 본 세션의 계산이며 검증하지 않았다. GMT 2023, Madiman–Kontoyiannis 2015의 본문은 읽지 않았다.

**[제안서 반영]** proposal.md §4.4: 차원 문제와 Tao 역 정리가 정성적이라는 점을 추가했다.

---

## Q11. 주 정리를 가우시안 모델로 하지 않으면 무엇이 있는가? (2026-11-18)

**[사용자]** "주 정리를 가우시안 모델로 하지 않으면 뭐가 있는가?"

**[답변 요지]** 대안은 다섯 가지다. 그중 소스 모델을 바꾸는 것은 1·3·4, 부호의 범위를 좁히는 것은 2, 영역을 바꾸는 것은 5다. 새 결과가 확실히 될 수 있는 것은 가우시안뿐이고, 증명 가능성이 가장 높은 것은 2다.

| # | 대안 | 신규성 | 증명 난이도 | 근거 |
|---|---|---|---|---|
| 1 | 유계 입력 (최악 경우) | ✗ 기존 결과에서 바로 나옴 | 하 | SPEC A-3: Chen 등 arXiv 2203.03761 Cor 5.4의 개수 논증 (Q5) |
| 2 | 소스는 가우시안 그대로, 부호를 좌표별·격자·디더 양자화로 한정 | △ "모든 부호"가 아니라 약한 정리 | 중하 | 실제 시스템이 쓰는 부류 (THC2024, SwitchML). Q6 시뮬레이션은 이 부류만 확인함 |
| 3 | 두꺼운 꼬리 (범위가 √N이 아니라 N으로 커짐 → 대가 log₂N 가설) | ? 검색 안 함 | ? | SPEC 5.3 순서 3, SPEC 3.3. 가설만 있음 |
| 4 | 유한 알파벳 소스 (ℤ_q, 모듈로 합 계산) | △ 2소스 결과는 있음 | 중 | Körner–Marton 1979, TsujinoWatanabe2026 (2소스, 무손실). Jog–Anantharam을 바로 쓸 수 있다. 그러나 스위치의 넘침이 "대가"가 아니라 계산의 일부가 되어 문제의 뜻이 바뀐다 |
| 5 | 저전송률 상전이 (좌표당 1비트 근처) | ? | ? | Q6 시뮬레이션 (N = 64, σ = 0.01Δ에서 0.066배), Suresh2022 Thm 2뿐 |

### 판단 (본 세션)
- 1은 주 정리가 될 수 없다. 기존 결과의 특수화로 인용하는 데 그친다.
- 2는 가우시안을 버리는 대안이 아니라 **가우시안 증명의 1단계**로 쓸 수 있다. Q10의 차원 문제도 피한다(d = 1). 가우시안 일반 부호가 막혀도 2는 독립적인 기여로 남는다.
- 3은 실제 그래디언트에 가깝고 대가가 더 크다는(log₂N) 점에서 매력적이다. 그러나 선행 연구를 검색하지 않았다. 주 정리로 정하려면 먼저 신규성을 점검해야 한다.
- 4와 5는 부차 목표로 적당하다.

**권고:** 주 정리는 가우시안으로 하고, 증명은 2(좌표별 부호) → 가우시안 일반 부호 순서로 진행한다. 3은 신규성 점검 후 2년차 목표(SPEC 184행)로 둔다.

**[미확인·위험]** 3과 5의 신규성과 난이도는 확인하지 않았다. 2가 "약한 정리"라는 평가는 학계의 수용도에 대한 추정이다.

---

## Q12. 가우시안·두꺼운 꼬리·유한 알파벳 모듈로란 무엇이며, 내가 고를 수 있는가? (2026-11-18)

**[사용자]** "가우시안, 두꺼운 꼬리, 유한 알파벳 모듈 등등 이런 개념은 어떤 개념인가 ? 그리고 내가 선택할 수 있는 것인가 ?"

**[답변 요지]** 이것들은 모두 **소스 모델(source model)**, 즉 "작업자가 보내는 그래디언트 값이 어떻게 생겼다고 가정하는가"에 대한 선택지다. 정리는 가정 위에서만 성립하므로, 가정이 달라지면 증명할 문장도 달라진다. 연구자가 고를 수 있다. 다만 아무것이나 고를 수는 없고 세 가지 기준이 있다.

### 각 모델의 뜻 (예시 수치는 설명용으로 만든 값)
| 모델 | 뜻 | 일상 비유 | 작업자 N = 1024일 때 합의 퍼짐 |
|---|---|---|---|
| 가우시안 (Gaussian, 정규분포) | 값 대부분이 평균 근처에 있고, 큰 값은 지수적으로 드물다 (종 모양 곡선) | 사람의 키 | 표준편차가 √N = 32배 → 대가 ½log₂N = 5비트 (가설 A-3) |
| 두꺼운 꼬리 (heavy tail) | 큰 값이 가우시안보다 훨씬 자주 나온다 (예: 거듭제곱 꼴로 줄어듦) | 재산 분포, 지진 규모 | 최악의 경우 N = 1024배 → 대가 log₂N = 10비트 (가설, SPEC 5.3 순서 3) |
| 유계 입력 (bounded, 최악 경우) | 분포는 가정하지 않고 "값이 어떤 범위 안에 있다"만 가정한다. 그 범위 안 최악의 값에 대해 보장한다 | 상자 크기만 알고 내용물은 모름 | 기존 결과로 이미 증명됨 (Chen 2022 Cor 5.4) |
| 유한 알파벳 모듈로 합 (finite alphabet, modulo sum) | 값이 0, 1, …, q−1 중 하나인 기호이고, 합이 q를 넘으면 시계처럼 0으로 돌아간다 | 시계: 10시 + 5시간 = 3시 | 넘침이 "오류"가 아니라 계산 규칙 자체가 된다 → 문제의 뜻이 바뀜 |

### 고를 수 있는가: 고를 수 있다. 다만 기준이 셋 있다
1. **현실성**: 실제 그래디언트와 닮아야 결론이 실무에 의미가 있다. SPEC 151행이 이 위험을 적고 있다("가우시안 모델이 실제 그래디언트와 다름 → S2에서 꼬리·상관을 실측"). 즉 실제 그래디언트를 측정해서 판단할 수 있다.
2. **신규성**: 이미 증명된 모델을 고르면 논문이 되지 않는다. 유계 입력은 여기서 탈락한다 (Q5).
3. **증명 가능성**: 가정이 강할수록(가우시안) 쓸 수 있는 도구가 많다. 정보이론에서 가우시안은 표준 기준 모델이다. 우리 문헌에서도 가장 가까운 선행 연구가 가우시안을 쓴다 (YangGroverKar: "independent gaussian", CEO 문제의 이차-가우시안 판본, Wyner–Ziv).

### 두꺼운 꼬리와 가우시안 중 어느 쪽이 현실에 가까운가
- ⚠ 확인 안 됨: SGD 그래디언트 잡음이 두꺼운 꼬리를 가진다는 실증 연구가 있다고 알고 있다(예: Şimşekli 등 2019). 원문을 확보하지 않았다.
- 본 세션 추론: 한 작업자의 그래디언트가 미니배치 여러 샘플의 평균이면 중심극한정리 때문에 가우시안 쪽으로 가까워진다. 반대로 미니배치가 작거나 소수 샘플이 지배하면 꼬리가 두꺼울 수 있다. 결국 실측이 답이다.

**권고:** 가우시안을 주 모델로 둔다(기준 모델, 신규, 도구 있음). 두꺼운 꼬리는 실측과 신규성 점검 뒤 확장으로 둔다. 실측은 sims/에서 작은 모델로 그래디언트 분포의 꼬리를 재면 된다.

**[미확인·위험]** 표의 "10비트"는 가설이며 증명되지 않았다. 그래디언트 꼬리에 대한 실증 문헌은 확보하지 않았다.

---

## Q13. 이 기술은 어디에 쓰이는가? (2026-11-18)

**[사용자]** "이 기술은 어디에 사용될 것인가 ?"

**[답변 요지]** 이 연구의 주 결과는 장치나 프로그램이 아니라 **한계 정리**다. "작업자 N명의 압축값을 스위치가 더하게 하려면, 어떤 방식을 써도 좌표당 비트가 최소 이만큼 더 든다"는 문장이다. 따라서 쓰임은 두 갈래다. (1) 시스템 설계자가 판단 기준으로 쓴다. (2) 달성 방식(격자 부호)은 실제 압축 기법으로 쓸 수 있다.

### 1. 주 응용: AI 데이터센터의 분산 학습
| 쓰임 | 설명 | 근거 |
|---|---|---|
| 네트워크 내 집계 스위치의 비트 폭 설계 | 스위치가 정수로 더하므로 작업자가 늘면 비트가 더 필요하다. 정리는 몇 비트가 *불가피한지* 알려준다 | SwitchML_NSDI21 (스위치는 부동소수점 연산을 못 해 정수로 더함), THC2024 ("the number of bits needed to send this value downstream is ⌈log2 m⌉") |
| "스위치에서 더하기" 대 "모두 모아 따로 풀기(All-Gather)"의 선택 | 앞쪽 대가는 ½log₂N(가설), 뒤쪽 대가는 N배 전송량. 어느 규모에서 무엇이 유리한지 경계를 준다 | UtilityGradComp2022 ("This can lead to high communication costs, leading to poor scalability") |
| 기존 압축 시스템의 평가 | THC 같은 시스템이 한계에서 몇 비트 떨어져 있는지 잰다. 더 개선할 여지가 있는지 판단한다 | proposal.md §1.6 |
| 새 압축 방식 | 한계에 도달하는 격자·디더 부호(A-1) | proposal.md §4.2 |

- 규모 감각 (SPEC 5.1의 예시): N = 1024이면 대가는 좌표당 약 5비트다. 4비트 압축을 쓰는 상황이라면 무시할 수 없다.

### 2. 같은 수학이 쓰이는 다른 분야
| 분야 | 왜 같은 문제인가 | 근거 |
|---|---|---|
| 연합 학습의 보안 집계 (secure aggregation) | 서버가 유한 군 위의 합만 본다. 같은 log n 차이가 관찰되지만 불가피한지는 증명되지 않았다 | Chen2023_SecAgg_freq §5.1: "the small sub-optimality gap is due to the modular arithmetic used by SecAgg" |
| 디지털 공중 계산 (over-the-air computation) | 무선 신호의 중첩으로 모듈로 합을 계산한다. 달성 방식만 있고 역 한계가 없다 | SumComp2023, Lattice_OTA_FL (Q7 표) |
| 센서망의 네트워크 내 계산·합의 | 중간 노드가 합을 전달한다 | YangGroverKar_innetwork_RD ("In-network Linear Function Computation and Consensus") |

**[미확인·위험]**
- 실제 시스템에 쓰이려면 가설 A-3이 증명되어야 하고, 실제 그래디언트가 모델과 닮아야 한다 (Q12).
- 5비트는 가설에서 계산한 값이며, 상수항(c₂)이 얼마인지는 모른다.
- 보안 집계와 공중 계산에 그대로 옮겨지는지는 각 분야의 모델(차분 프라이버시 잡음, 채널 잡음)을 반영해 따로 확인해야 한다.

---

## Q14. 목표는 한계가 아니라 새로운 발견이라고 하지 않았나? (2026-11-18)

**[사용자]** "우리의 목표는 한계가 아니라 새로운 발견이라고 하지 않았나?"

**[답변 요지]** 맞다. Q6의 목표는 새 발견이다 ("새로운 발견을 해야한다"). Q13에서 "주 결과는 한계 정리"라고만 쓴 것은 쓰임새 쪽에서 본 설명이었고, 목표를 흐리게 했다. 정정한다.

- 이 분야에서 한계 정리는 발견을 담는 *형식*이다. 발견은 그 *내용*이다. Shannon의 채널 용량도 형식은 한계 정리이지만, 내용은 "잡음이 있어도 오류 없이 보낼 수 있다"는 발견이다.
- 우리 발견의 내용은 Q6·Q7·Q10에서 좁힌 다음 세 가지다. 한계 정리는 이것들을 증명한 결과로 따라 나온다.

| # | 발견 (가설) | 무엇이 새로운가 | 상태 |
|---|---|---|---|
| D1 | **대가가 생기는 원리**: 스위치의 정수 덧셈에서 합은 "엔트로피가 자라거나, 부분군에 몰려 정보를 잃는다" 둘 중 하나다. ½log₂N은 이 양자택일에서 나온다 | 현상(THC가 관찰한 추가 비트)의 *원인*을 처음 밝힌다. 지금까지는 경험적 관찰뿐이다 (THC2024, THC_followup2024) | 미증명. Tao 증명의 분기와 같은 모양임을 확인 (Q10) |
| D2 | **ℤ_{2^b} 위 새 엔트로피 부등식**: 위 양자택일을 b에 지수적이지 않은 상수로 | 수학 쪽 발견. 지금 알려진 최선은 상수 2^{3b} (GGMT2024 Thm 1.3) | 미증명. 가장 어려움 |
| D3 | **저전송률 상전이**: 좌표당 1비트 근처에서는 공유 난수로 대가가 줄거나 사라질 수 있다 | 대가가 *항상* 있다는 통념을 뒤집을 수 있다. 실무 압축(1~4비트)과 맞닿는다 | 시뮬레이션 근거만 있음 (Q6 근거 4) |

- D3은 A-3과 반대 방향일 수 있다. A-3이 저전송률에서 깨진다면 그것 자체가 발견이다.

**[제안서 반영]** 가제가 "합 호환 압축의 근본 한계"로 한계를 앞세운다. 발견을 앞세우도록 가제와 §1.6의 수정을 제안한다 (사용자 승인 후 반영).

**[미확인·위험]** D1~D3 모두 가설이다. 신규성은 모은 문헌과 웹 검색(Q7, Q10) 범위에서만 확인했다.

---

## Q15. 제목을 단어별로 검증 (2026-11-18)

**[사용자]** "'합 호환 압축의 근본 한계: 링·트리 All-Reduce에서 압축된 상태로 집계할 때의 레이트-왜곡 역 한계와 이를 달성하는 격자 기반 부호' 라는 제목이 올바른지 단어 하나씩 매핑해서 검증해라"

**[답변 요지]** 단어 대부분은 정의와 맞는다. 문제는 셋이다. (1) "링·트리"는 확장 모델이고, 기본 모델(1단 스위치)이 빠졌다. (2) "근본 한계"와 "달성"은 지금 증명 계획보다 강한 주장이다. (3) 핵심 결과(½log₂N)와 발견(Q14)이 제목에 없다.

### 단어별 대조
| 제목의 단어 | 대응하는 정의·결과 | 판정 | 근거 |
|---|---|---|---|
| 합 호환 압축 | proposal §2.1: 중간 노드가 복원하지 않고 더해도 합을 추정할 수 있는 압축 | ✓ 다만 본 연구의 신조어다. 시스템 문헌은 "homomorphic compression"이라 부른다 | THC2024 (Tensor Homomorphic Compression), LosslessHomomorphic2024 |
| 근본 한계 | A-3: *모든* 단일 라운드 합 호환 부호에 대한 역 한계 | △ (a) Q14의 목표(발견)와 어긋난다. (b) 1단계를 좌표별 부호로 한정하면(Q10·Q11) "모든 부호"가 아니다. (c) 가우시안 모델에서만 성립한다 | SPEC 5.1 A-3, Q11 |
| 링·트리 All-Reduce | SPEC 3.1 기본 모델은 **1단 스위치 집계**(작업자 → 스위치 → 작업자). 링은 확장(3.3, 4장), 다단 트리도 확장(4장) | ✗ 확장 모델만 적고 기본 모델을 뺐다. 또한 링에서는 중간 노드가 GPU여서 복호할 수 있다. 합 호환 제약이 *강제*되는 곳은 정수 덧셈만 하는 스위치다 | SPEC 3.1·3.3, SwitchML_NSDI21 (스위치는 부동소수점 연산 불가) |
| 압축된 상태로 집계할 때 | SPEC 3.2: 스위치는 군 덧셈만 하고 복호·재부호화는 하지 않는다 | ✓ 단 "합 호환"과 같은 말이 겹친다 | SPEC 3.2 |
| 레이트-왜곡 | 좌표당 R비트, 왜곡 D(MSE)에서 R(D) | ✓ 문서 안 표기가 섞여 있다: proposal은 "율-왜곡", SPEC은 "레이트" 6회, "율-왜곡" 1회. 하나로 통일해야 한다 | SPEC 3.1 |
| 역 한계 | A-3 (가우시안, 미증명) | ✓ 제목의 역 한계가 A-3을 뜻하면 맞다. A-2는 신규가 아니다 (YangGroverKar Thm 2) | proposal §4.2 |
| 이를 달성하는 | A-1: R_compat ≤ ½log₂(N²σ²/D) + ε. A-3과는 상수(c₂ + ε)만큼 차이 난다 | △ 정보이론에서 "달성"은 보통 한계와 정확히 같음을 뜻한다. 우리는 "상수 차이 이내"(Δ = ½log₂N ± O(1))다 | proposal §4.2 결론 행 |
| 격자 기반 부호 | A-1: 디더를 쓴 중첩 격자 + 모듈로 덧셈 | ✓ 좌표별(d = 1) 단계에서는 격자 ℤ, 즉 균일 디더 양자화로 줄어든다 | proposal §4.2 |

### 본 세션 추론 (링·트리 관련)
- 모든 중간 노드가 같은 군 G에서 덧셈만 하면, 최종 복호기가 보는 것은 망 모양과 무관하게 Z = E₁ ⊕ ⋯ ⊕ E_N이다. 따라서 A-3 역 한계는 링·트리로 그대로 옮겨진다. "링·트리"가 틀린 것은 아니고, *기본 모델을 빼고 확장만 적은 것*이 문제다.
- 반대로 다단 트리에서 중간 스위치가 비트 폭 제한으로 재양자화하면(SPEC 3.3) 다른 문제가 된다.

### 제목에 없는 것
- 핵심 수치 ½log₂N (작업자 수에 따른 대가)
- 가우시안 모델
- 발견의 내용 D1 (엔트로피 성장 또는 부분군 집중, Q14)

### 수정안 (사용자 선택용)
- A (발견 앞세움): "스위치 내 집계의 ½log₂N 비트 대가: 정수 덧셈 아래 엔트로피 성장과 부분군 집중의 양자택일"
- B (원 제목을 최소 수정): "네트워크 내 집계를 위한 합 호환 압축의 율-왜곡: 가우시안 모델의 역 한계와 상수 차이로 이에 도달하는 격자 부호"
- C (절충): "합 호환 압축은 왜 비트를 더 쓰는가: 네트워크 내 집계의 ½log₂N 대가와 그 원리"

**[미확인·위험]** 링·트리로 옮겨진다는 것은 본 세션의 추론이며 증명하지 않았다. 링 All-Reduce에서 링크당 전송률을 어떻게 셀지(축소-분산 단계의 조각 크기)는 정하지 않았다.

---

## Q16. [결정] 소스 모델 확정 (2026-11-18)

**[사용자]** "독립 가우시안 벡터를 기본 모델로 두고, 공통 성분이 있는 상관 가우시안 모델로 확장한다. 가우시안 + 두꺼운 꼬리를 사용한다."

**[결정 내용]**
| 단계 | 모델 | 정의 |
|---|---|---|
| 기본 | 독립 가우시안 벡터 | g_n ~ N(0, σ_ξ² I_d), 작업자 사이·좌표 사이 독립. Var(S) = Nσ_ξ² |
| 확장 | 상관 가우시안 (공통 성분) | g_n = θ + ξ_n, θ ~ N(0, σ_θ² I_d) 공통, ξ_n ~ N(0, σ_ξ² I_d) 작업자별. σ_θ = 0이면 기본 |
| 함께 사용 | 두꺼운 꼬리 | 분포 부류는 미정 |

**[본 세션이 함께 정한 것 (사용자 확인 필요)]**
- 이전 반복의 예측 S′(부가 정보)은 기본 모델에서 뺐다. 독립 모델에는 예측할 공통 구조가 없기 때문이다. S′은 SPEC 3.3의 시간 상관 확장에서 다룬다. 그래서 기존 SPEC의 "작업자별 성분이 지배하는 경우 Var(S|S′) ≈ Nσ_ξ²"라는 근사 조건이 기본 모델에서는 등식 Var(S) = Nσ_ξ²가 된다.

**[이 결정의 의미]**
- 기본 모델은 YangGroverKar의 "independent gaussian"과 같아서, A-2를 특수화해 인용하기가 바로 된다.
- 공통 성분 확장에서는 합 S = Nθ + Σξ_n의 분산이 N²σ_θ² + Nσ_ξ²가 된다. 공통 성분은 모든 작업자에게 같으므로 합 호환 대가가 달라질 수 있다 (미분석).
- 두꺼운 꼬리는 Q11에서 신규성을 점검하지 않았다고 적었다. **주 모델로 쓰려면 신규성 점검과 분포 부류 확정이 먼저다.**

**[반영]** SPEC.md 3.1 (기본 모델), 3.3 (상관 가우시안 행 추가, 두꺼운 꼬리 행 수정), 5.1 (A-3 전제), 12장 (결정 완료 표시, 새 항목 추가). proposal.md §2.2 (소스 모델 3단계).

---

## Q17. [결정 보강] 기본 모델과 확장 모델의 정식화 (2026-11-18)

**[사용자]** 독립 가우시안 X_k ~ N(0, σ²I_d)를 기본으로, X_k = U + N_k를 확장으로 둔다. 목표는 합 또는 평균, 왜곡은 정규화된 평균제곱오차. 이유: "처음부터 실제 그래디언트의 복잡한 분포를 넣으면 한계 증명과 압축 알고리즘 중 무엇이 성능을 좌우하는지 분리하기 어렵습니다." 근거로 Zamir, Shamai & Erez "Lattices for Distributed Source Coding"과 Zhou et al. 2022를 제시.

**[반영]**
- 두꺼운 꼬리는 Q16의 "함께 사용"에서 **3단계(두 가우시안 단계 뒤)**로 옮겼다. 사용자가 제시한 이유와 맞추었다. ⚠ 사용자 확인 필요.
- 목표: 합 또는 평균. 정규화 왜곡 D̄ = D / Var(S)에서는 두 목표가 같은 문제다 (평균의 MSE는 합의 MSE의 1/K², 분산도 1/K²).
- 정규화의 이점 (본 세션 계산): 기본 모델에서 Var(S) = Kσ²이므로 A-2는 ½log₂(1/D̄), A-3(가설)은 ½log₂(K/D̄)가 된다. 대가 ½log₂K가 식에 그대로 드러난다.

### 제시 문헌 확인
| 사용자 인용 | 확인 결과 | 근거 |
|---|---|---|
| Zamir, Shamai & Erez, "Lattices for Distributed Source Coding" | ⚠ **저자와 제목이 섞였다.** "Lattices for Distributed Source Coding: Jointly Gaussian Sources and Reconstruction of a Linear Function"은 **Krithivasan & Pradhan** 논문이다 (이미 보유). Zamir·Shamai·Erez의 논문은 "Nested linear/lattice codes for structured multiterminal binning", IEEE TIT 48(6):1250–1276, 2002이다 (원문 미보유) | papers/modern/KrithivasanPradhan_lattice_DSC.pdf 첫 쪽: "Dinesh Krithivasan and S. Sandeep Pradhan". 서지는 KrithivasanPradhan2009_journal 참고문헌 [45] |
| Zhou et al., 2022 | 확인. "On Distributed Lossy Coding of Symmetrically Correlated Gaussian Sources", arXiv 2201.07784, IEEE Trans. Commun. 70(12), 2022. 원문 받음 (papers/modern/Zhou2022_symmetric_Gaussian_DSC.pdf) | 초록: "The decoder produces a joint reconstruction of target signals ... observed sources can be expressed as the sum of target signals and corruptive noises which are independently generated from two symmetric multivariate Gaussian distributions." |

**Zhou 2022와 우리 모델의 차이:**
| 항목 | Zhou 2022 | 우리 확장 모델 |
|---|---|---|
| 복원 대상 | 모든 목표 신호 (X̂₁, …, X̂_L) | 합 KU + Σ N_k 하나 |
| 관측 | 목표 + 잡음 (원격 소스) | X_k 자체를 관측 |
| 목표 신호의 상관 | 대칭 다변량 가우시안 | 공통 성분 U 하나 |
| 합 호환 제약 | 없음 | 있음 (군 덧셈만) |
- 가까운 고전 문제는 CEO 문제다 (Berger–Zhang–Viswanathan 1996, classic/10). 그러나 CEO 문제의 목표는 U이고, 우리 목표는 N_k까지 포함한 합이라서 같지 않다.

**[기호]** 사용자 표기(K, X_k, U, N_k)와 기존 문서 표기(N, g_n, θ, ξ_n)가 다르다. 특히 잡음 N_k와 작업자 수 N이 겹친다. SPEC 3.1과 proposal §2.2에는 대응표를 달았다. 문서 전체를 통일할지는 사용자 결정이 필요하다.

---

## Q18. 구체적 예시로 직관 만들기 (2026-11-18)

**[사용자]** "[목표] 직관적으로 이해하기. 아직 정확하고 명확하게 상황이 머릿속에 그려지지 않는다. '구체적인 예시'를 들어서 머리속에 이미지를 만들어라"

**[답변 요지]** GPU 4대, 숫자 하나(그래디언트의 한 좌표), 4비트 정수 덧셈 스위치로 전 과정을 손으로 계산한다. 수치는 모두 설명용으로 만든 값이며, 계산은 본 세션에서 했다.

### 설정
- 작업자 K = 4, 각자 값 x_k ~ N(0, 1) (σ = 1). 실제로는 좌표가 수백만 개지만 좌표마다 같은 일이 일어나므로 하나만 본다.
- 압축: 눈금 Δ = 0.25로 반올림해 정수로 보낸다. 4비트 부호 있는 정수는 −8~7이므로 한 작업자는 −2~1.75 범위(약 ±2σ)를 표현한다.
- 스위치: 받은 정수를 4비트 레지스터에서 더한다. 범위를 넘으면 16을 빼고 다시 돈다(시계와 같다).

### 장면 1: 잘 되는 반복
| GPU | 값 | ÷0.25 반올림 |
|---|---|---|
| 1 | +0.7 | 3 |
| 2 | −1.2 | −5 |
| 3 | +0.3 | 1 |
| 4 | +1.6 | 6 |
| 합 | 1.4 | 5 → 5×0.25 = 1.25 (오차 0.15) |

### 장면 2: 넘침 (모두 양수로 쏠린 반복)
| GPU | 값 | 정수 |
|---|---|---|
| 1 | 1.5 | 6 |
| 2 | 1.2 | 5 |
| 3 | 0.9 | 4 |
| 4 | 1.6 | 6 |
| 합 | 5.2 | 21 → 4비트에서 21 − 16 = 5 → 1.25로 복원 (오차 약 4) |
- 각 GPU의 값은 모두 자기 범위 안에 있었다. 문제는 **합**이 범위를 넘은 것이다.

### 왜 비트가 더 드는가
- 합의 표준편차는 √K·σ = 2다. 4비트 범위(±2)는 합의 ±1σ밖에 못 덮어서 약 3번에 1번 넘친다.
- 합 레지스터에 1비트를 더하면(5비트, ±4 = ±2σ) 넘침은 약 5%, 2비트를 더하면(±8 = ±4σ) 약 0.006%로 준다.
- 즉 추가 비트 = log₂(√K) = ½log₂K = 1비트 + 신뢰도를 위한 상수. 이것이 가설 A-3의 "½log₂K ± O(1)"이다.
- K = 1024이면 합의 퍼짐이 32배 → 5비트 + 상수.

### 다른 선택지와 비교
| 방법 | 4대의 경우 | 대가 |
|---|---|---|
| 합 레지스터에 비트 추가 | 4 + 1(~2)비트 | ½log₂K + 상수 |
| 비트는 4로 두고 눈금을 0.5로 키움 (THC가 보고한 절충) | 넘침은 줄지만 GPU마다 오차가 2배 | 정확도 손실 |
| All-Gather (각자 4비트를 모두에게, 받은 쪽이 따로 풀어 더함) | 4 × 4 = 16비트 | K에 비례 |

### 연구 질문을 이 그림으로
"반올림 대신 더 영리한 부호를 쓰면 추가 1비트를 없앨 수 있는가?"
- 속임수 시도: 모든 GPU가 **짝수만** 보낸다. 짝수끼리 더하면 짝수이므로 합이 쓰는 값의 가짓수가 늘지 않는다(엔트로피가 자라지 않음). 그러나 이것은 맨 아래 비트를 버린 것이고, 실제 눈금이 0.5로 거칠어진 것과 같다.
- 이것이 D1(Q14)의 그림이다. **합의 엔트로피가 자라서 비트가 더 들거나, 짝수 같은 부분군에 갇혀 해상도를 잃거나** 둘 중 하나다. Jog–Anantharam의 최소화 분포("the smallest possible subgroup")가 정확히 이 짝수 예다.
- 증명할 것: 어떤 부호도 이 둘을 동시에 피할 수 없다.

### 2단계 모델 (공통 성분)을 같은 그림으로
- 모든 GPU가 비슷한 방향을 본다: U = +1.0, 각자 차이 N_k가 ±0.2 정도. 값은 1.1, 0.9, 1.2, 0.8, 합은 4.0 ≈ 4U.
- 공통 성분은 서로 상쇄되지 않으므로 합에서 √K배가 아니라 **K배**로 커진다. 합 레지스터의 부담이 더 크다.
- 한편 모두가 비슷한 값을 가지므로 압축이 이를 이용할 여지도 있다. 대가가 어떻게 바뀌는지가 2단계 질문이다 (⚠ 미분석).

### 3단계 (두꺼운 꼬리)
- 대부분의 반복에서는 값이 ±2 안이지만, 가끔 한 GPU가 10을 낸다. 합의 범위는 이런 드문 큰 값이 정한다.

**[미확인·위험]** 넘침 확률(약 1/3, 5%, 0.006%)은 합이 정규분포 N(0, 4)라고 보고 계산한 근삿값이다. 반올림 오차와 작업자별 범위 초과는 무시했다.

---

## Q19. GPU에서 SerDes로 데이터가 전달되는가? + 장면 1·2 시각화 (2026-11-18)

**[사용자]** "gpu에서 serdes로 데이터가 전달되는 것인가 ?" / "장면 1과 장면 2가 표로만 그려져서 머릿속에 그려지지 않는다. 시각자료를 적극 활용하라"

**[답변 요지]** 그렇다. 칩 밖으로 나가는 모든 구간(GPU→NIC의 PCIe, NIC→케이블, 케이블→스위치 칩)에서 SerDes(직렬화기·역직렬화기)가 병렬 비트를 고속 직렬 신호로 바꾸고 받는 쪽에서 되돌린다. SerDes는 비트를 나르기만 한다. 덧셈은 스위치 칩 안에서 신호가 다시 병렬 비트로 풀린 뒤 정수 연산 회로가 한다. 우리 연구는 SerDes보다 위층의 문제다. SerDes 링크 속도는 고정되어 있고, 우리는 그 위로 보낼 비트 수를 줄인다.

| 근거 | 원문 |
|---|---|
| THC 실험 구성 | THC2024: "four GPU machines as workers, each with one NVIDIA A100 GPU and one NVIDIA MCX516A-CCAT ConnectX-5 100G dual-port NIC connecting to a Tofino2 switch" |
| 스위치는 정수로 더함 | SwitchML_NSDI21 (Q2·proposal §1.3) |
| 인피니밴드 스위치의 망 내 집계 | SwitchML_NSDI21: "Mellanox's Scalable Hierarchical Aggregation Protocol (SHARP) is a proprietary in-network aggregation scheme available in certain InfiniBand switches" |
- ⚠ SerDes의 위치와 역할은 일반적인 하드웨어 구조에 대한 설명이며, 모은 문헌에서 확인한 것은 아니다 (문헌 66편에 "SerDes" 언급 0건).
- 랙 안 GPU끼리는 NVLink(역시 SerDes 기반)로 연결되며, 이 구간은 대역폭이 커서 압축 이득이 작을 수 있다 (SPEC P-A ⚠, CERAR2026: "for GPU clusters with high-bandwidth NVLink interconnects, CERAR performs worse").

**[시각자료]** 해설 페이지: https://claude.ai/code/artifact/4e50c491-4173-4186-9549-fa6e8195ba7d
- 0: 데이터 경로 (GPU → SerDes → NIC → SerDes → 케이블 → SerDes → 스위치 정수 덧셈기)
- 1·2: 장면 1·2를 수직선 화살표(누적 합)와 16칸 시계판(레지스터)으로. 단계별 재생
- 3: K와 추가 비트를 바꾸며 합의 종 모양 곡선이 칸을 넘는 정도와 넘침 확률을 보는 계산기
- 4: 16칸 대 짝수 8칸 시계판 (부분군 속임수와 그 대가)

---

## Q20. 실제 논문에서 증명된 것은 무엇인가? (2026-11-18)

**[사용자]** "실제 논문에서 증명된 것은 어떤 것인가?"

**[답변 요지]** 예시(Q18·Q19 그림)의 주장을 하나씩 떼어 상태별로 나눈다. 핵심 결론: **"어떤 영리한 부호도 가우시안에서 ½log₂K 추가 비트를 피할 수 없다"는 어디에서도 증명되지 않았다.** 그 주변 조각(제약 없는 하한, 최악 경우 하한, 짝수 속임수의 엔트로피)은 증명되어 있다.

| 상태 | 주장 (예시 기준) | 출처 |
|---|---|---|
| 관찰됨 | 작업자가 늘면 하행 비트가 늘어난다 | THC2024, THC_followup2024 (실험) |
| 관찰됨 | 더할 수 없는 압축은 실제 이득이 거의 없다 | UtilityGradComp2022 (200여 설정 중 6개) |
| 증명됨 | 제약이 없을 때 최소 ½log₂(Kσ²/D) | YangGroverKar Thm 2 |
| 증명됨 | 최악 입력에서 합 호환 부호의 추가 비트 | Chen2022 Cor 5.4 |
| 증명됨 | 가우시안에서 엔트로피 개수 논증은 제약 없는 하한만 준다 | Chen2023 Lemma 3.2 |
| 증명됨 | 정수에서 합마다 엔트로피 ½비트 성장 (전체 기준) | Tao Thm 1.13, Wang 2026 |
| 증명됨 | ℤ_{2^n}에서 합의 엔트로피가 안 자랄 수 있고, 최소화 분포는 부분군 위 | JogAnantharam2014 Thm 4.1 |
| 증명됨 | 엔트로피가 거의 안 자라면 부분군 근처 (상수 m³) | GGMT2024 Thm 1.3 |
| 증명됨 | 상관 양자화는 저해상도에서 합 오차를 줄인다 | Suresh2022 Thm 2 |
| 증명됨 (보조) | 손실 없는 링 All-Reduce 전송량 최적성, 망 합 계산 용량, 모듈로-2 합에서 선형 부호의 이득, 격자로 가우시안 선형 함수 복원 | CERAR2026, Appuswamy, Körner–Marton 1979, Krithivasan–Pradhan |
| 우리 계산 | 1비트 추가로 넘침 1/3 → 5%, 고해상도에서 상관 디더 이득 없음 | Q18 근사, sims/cq_dither.py |
| 가설 | 가우시안 A-3 (½log₂K 불가피) | 미증명, 핵심 |
| 가설 | D1: 엔트로피 비성장 ⇒ 왜곡 증가 (뒤 절반) | 앞 절반만 Jog–Anantharam이 증명 |
| 가설 | A-1 격자 부호의 달성 | 구성은 단순, 오차 분석 미작성 |

**[시각자료]** 해설 페이지 5절 "어디까지 증명되었나"에 같은 지도를 추가했다 (같은 URL, 버전 2).

---

## Q21. 각 논문은 이 문제를 어떻게 다루는가? (2026-11-18)

**[사용자]** "이제 어떤 문제를 해결하려고 하는지 이해했다. 이제, 각 논문이 어떻게 위 문제를 해결하는 지 알고 싶다."

**[방법]** 시스템 논문 5편과 이론 논문 6편을 에이전트 둘이 본문까지 읽었다. 핵심 인용(THC 룩업 표, Davies Thm 7, Krithivasan–Pradhan Thm 3.1, Chen2022 Cor 5.4)은 본 세션에서 PDF와 대조했다.

**[답변 요지]** 넘침 앞에서 논문들은 다섯 길 중 하나를 택했다. 앞의 넷은 피하거나 견디고, 다섯째는 불가피함을 증명하려 한다. **가우시안에서 ½log₂K가 불가피한지 증명한 논문은 없다.**

| 길 | 논문 | 방법 | 4-GPU 예시 | 남긴 것 |
|---|---|---|---|---|
| ① 칸을 넓힌다 | SwitchML_NSDI21, THC2024 | SwitchML: 32비트 정수, 배율 "f is set to (2^31 − 1)/(n · 2^m)". THC: 4비트 번호 → 표 T로 0~g 정수로 확장 → 8비트 합 ("allows an efficient expansion of the indices to wider values that allow summation without overflows") | 21이 넓은 칸에 들어감. 대가는 합 칸의 폭 | 더 영리한 부호로 줄일 수 있는지 다루지 않음 |
| ② 중간에서 풀고 다시 묶는다 | Davies2021, YangGroverKar | Davies: mod q 격자 번호를 자기 값 근처로 풀기(Lemma 15), 중간 노드가 풀고 평균 내고 재압축(Alg. 3·4). YGK: 복호 → 합 → 재부호화 | 중간 노드가 21을 실수로 복원하므로 넘침 없음. 스위치는 못 함 | 더하기만 하는 중간 노드의 한계 없음 |
| ③ 접힘을 계산에 쓴다 | KrithivasanPradhan2009, Körner–Marton 1979 | 고운 격자로 반올림 → 굵은 격자로 접기 → 접은 것의 합 = 합을 접은 것 → 한 번 펴기. 굵은 격자가 합의 퍼짐을 덮어야 함 | 시계 둘레를 합의 퍼짐만큼 키우면 21도 풀림. 키우는 비용이 추가 비트 | 하한 없음 |
| ④ 오차를 맞물린다 | Suresh2022 | 공유 난수로 반올림 기준을 GPU마다 다르게(비복원 추출) | 둘은 올리고 둘은 내려 합 오차 상쇄 | 칸 폭·넘침은 다루지 않음 |
| ⑤ 불가피함을 증명 | Chen2022, Chen2023, Appuswamy | Chen2022: 칸 수 세기(공 덮기, Cor 5.4, 최악 입력). Chen2023: 엔트로피 세기(Lemma 3.2). Appuswamy: 손실 없는 cut-set | 최악 입력(넷이 모두 같은 값)이면 합 0~60, 약 6비트. 가우시안이면 세기 논증이 A-2만 줌 | **가우시안 ½log₂K 불가피성.** 두 세기 논증 모두 접힘을 쓰지 않음 |

### 새로 확인한 것
- **Krithivasan–Pradhan Thm 3.1이 K = 2에서 A-3 값을 달성한다 (본 세션 검산).** Thm 3.1: (2^{−2R₁} + 2^{−2R₂})⁻¹ ≥ σ_Z²/D가 달성 가능. 독립 가우시안 두 개의 합이면 σ_Z² = 2σ², 대칭 R₁ = R₂ = R에서 R = ½log₂(2σ_Z²/D) = ½log₂(4σ²/D) = A-3의 K = 2 값 ½log₂(K²σ²/D). 제약 없는 값 ½log₂(2σ²/D)보다 정확히 ½log₂2 = ½비트 많다. → A-1(달성)은 K = 2에서 이미 있다. K > 2는 Thm 4.1로 계산해야 한다 (미계산).
- **Davies2021 Thm 7**: 분산 감소(참 평균 추정) 문제에서 "to achieve any variance reduction at all ... at least one machine must receive Ω(d log n) bits". 제약 없는 프로토콜의 log n 하한이다. 목표가 표본 합이 아니라 참 평균 ∇이라서 우리 A-2·A-3과 직접 비교되지 않는다. ⚠ 관계를 정밀하게 따져야 한다 (예: 참 평균 추정으로 환원하면 다른 하한이 나오는지).
- Chen2022 Cor 5.4의 K² 항은 입력이 모두 같은 방향으로 정렬된 최악 경우에서 나온다. 가우시안 독립 입력에서는 합이 √K배만 퍼져 같은 세기가 A-2를 준다 (에이전트 해석, 본 세션 동의).

**[미확인·위험]**
- SwitchML Thm 2의 정확한 분자, Suresh Thm 2의 계수는 PDF 추출이 깨져 원문 수식 확인이 필요하다.
- LosslessHomomorphic2024는 희소성 이용 방식이며 칸 폭 문제를 다루지 않는다 (본문 "overflow" 0회). 위 다섯 길에서 뺐다.

**[시각자료]** 해설 페이지 6절 "넘침 앞에서 논문들이 고른 다섯 가지 길" (같은 URL, 버전 3).

**[제안서 반영 후보]** proposal §4.2 A-1 행에 "K = 2에서 Krithivasan–Pradhan Thm 3.1이 달성"을 추가. (사용자 승인 후)

---

## Q22. 왜 수학적 증명이 이렇게 많은가? (2026-11-19)

**[사용자]** "수학적인 증명이 엄청 많은데 왜 그런것인가 ?"

**[답변 요지]** 우리가 하려는 말이 **"어떤 부호로도 안 된다"**이기 때문이다. 실험은 시도해 본 부호에 대해서만 말할 수 있고, 증명만이 아직 아무도 생각하지 못한 부호까지 포함해 모든 부호를 한꺼번에 다룰 수 있다.

### 부호가 얼마나 많은가 (설명용 계산)
- 4-GPU 예시에서 GPU 하나의 부호는 "입력값 → 16칸 중 하나"로 가는 규칙이다.
- 입력을 100구간으로만 나눠도 규칙의 수는 16^100 ≈ 10^120개다. GPU 4대가 서로 다른 규칙을 쓰면 그 4제곱이다. 공유 난수와 복호기까지 넣으면 더 많다.
- 1초에 10억 개를 시험해도 우주 나이(약 4×10^17초)로는 10^27개도 못 본다. 실험으로 "모든 부호"를 확인하는 것은 불가능하다.
- 짝수 속임수(Q18)처럼 반올림이 아닌 영리한 부호가 실제로 존재한다. 그래서 "반올림으로 해 보니 1비트 더 들었다"는 결론이 되지 못한다.

### 달성과 역 한계의 비대칭
| | 달성 (A-1) | 역 한계 (A-3) |
|---|---|---|
| 주장 | "이 부호 하나로 된다" | "어떤 부호로도 안 된다" |
| 확인 방법 | 부호 하나를 만들어 시뮬레이션으로도 확인 가능 | 증명만 가능 |
| 예 | THC·SwitchML(실험), Krithivasan–Pradhan(구성) | Chen2022 Cor 5.4, YangGroverKar Thm 2 |

### 분야의 관행
- 시스템 논문(SwitchML, THC, UtilityGradComp)은 측정으로 말한다. 정보이론 논문(Shannon 이래)은 정리로 말한다. 이번 연구는 둘 사이에 있다. 현상은 시스템 쪽에서 관찰되었고(THC), 불가피성은 정보이론 쪽에서 증명해야 한다.

### 우리 논문에 필요한 증명의 수
- 많아 보이는 것은 문헌의 정리들(재료)이다. 우리가 새로 증명할 것은 핵심 정리 하나(가우시안 A-3)와 그것을 받치는 보조정리 몇 개다 (Q6: 해상도 보조정리, 성장 또는 집중, 집중 ⇒ 왜곡, 결합). A-2는 YangGroverKar 인용, A-1은 K = 2에서 Krithivasan–Pradhan 인용.
- 실험(시뮬레이션)도 쓴다. 증명할 부호가 실제로 어떻게 동작하는지 보고(sims/cq_dither.py), 증명 방향이 맞는지 미리 점검하는 용도다.

---

## Q23. 수학적 논리 전개 (스칼라 부호, 1단계) (2026-11-19)

**[사용자]** "수학적으로 논리 전개를 해볼래?"

**[범위]** 좌표별(스칼라, d = 1) 단일 라운드 합 호환 부호 (Q11 권고의 1단계). 각 단계에 [엄밀] / [계산] / [미증명]을 붙인다. 모두 본 세션의 전개이며 검토받지 않았다.

### 설정
- X_1, …, X_K ~ N(0, σ²) 독립, S = Σ X_k (Var S = Kσ²).
- 공유 난수 W (X와 독립). 인코더 Q_k = f_k(X_k, W) ∈ ℤ_M, M = 2^R.
- 스위치: Z = Q_1 + ⋯ + Q_K (mod M). 복호기 Ŝ = g(Z, W), E(S − Ŝ)² ≤ D.
- 목표 (A-3 스칼라판): R ≥ ½log₂(K²σ²/D) − c.

### 1단계 [엄밀] 레지스터 비트의 분해
R = log₂M ≥ H(Z | W) = I(S; Z | W) + H(Z | S, W).
- 첫 부등호: Z는 M가지 값. 등식: 엔트로피의 연쇄 법칙.

### 2단계 [엄밀] 첫 항 = 제약 없는 하한
S ⊥ W이므로 I(S; Z | W) = I(S; Z, W) ≥ I(S; Ŝ) ≥ ½log₂(Kσ²/D).
- 마지막 부등식: 가우시안 율-왜곡 함수. MSE ≤ D인 어떤 추정량도 I(S; Ŝ) ≥ ½log₂(Var S / D).
- 결과: **R ≥ ½log₂(Kσ²/D) + H(Z | S, W).** 첫 항이 A-2 값이다.

### 따라서 A-3은 다음 보조정리와 같다
> **보조정리 L (가설):** 왜곡 D를 만족하는 모든 스칼라 합 호환 부호에서 H(Z | S, W) ≥ ½log₂K − c.

**뜻:** 합 S를 이미 알아도 Z에 남는 불확실성이다. 각 작업자의 반올림 흔적이 더해진 "찌꺼기"로, 복호기에는 필요 없지만 스위치 레지스터는 이것까지 실어 날라야 한다. 찌꺼기 K개의 합은 √K배로 퍼지므로 ½log₂K비트가 든다.

**왜 기존 엔트로피 논증이 A-2에서 멈췄는가 (본 세션 해석):** Chen2023 Lemma 3.2는 H(Y_i) ≥ I(합; Y) ≥ R(β)로 간다. 1단계의 둘째 항 H(Z | S, W)를 버리는 셈이다. 버린 항이 바로 ½log₂K다. Chen2023이 "due to the modular arithmetic"이라고 남긴 차이가 이 항이라는 해석이다 (⚠ Chen2023의 설정은 빈도 추정이라 그대로 같은지는 미확인).

### 3단계 [계산] 균일 양자화에서는 L이 성립하고 상수까지 맞는다
고해상도(Δ ≪ σ)에서는 반올림 오차 e_k가 서로 독립인 U(−½, ½)가 된다. S가 주어지면 Z = S/Δ − Σe_k이므로, Z | S는 Irwin–Hall 밀도를 정수에 찍은 분포다. 정확 계산 (sims/hzs_exact.py):

| K | H(Z\|S) | ½log₂(2πeK/12) | ½log₂K |
|---|---|---|---|
| 2 | 0.721 | 0.755 | 0.500 |
| 4 | 1.250 | 1.255 | 1.000 |
| 8 | 1.754 | 1.755 | 1.500 |
| 16 | 2.254 | 2.255 | 2.000 |

- H(Z|S) = ½log₂K + ½log₂(2πe/12) = ½log₂K + 0.254비트.
- 대입: R = ½log₂(Kσ²/D) + ½log₂K + 0.254 = ½log₂(K²σ²/D) + 0.254. 0.254비트는 균일 양자화가 가우시안 한계보다 잃는 잘 알려진 공간 채움 손실 상수와 같은 값이다. 즉 이 부호는 A-3 가설값에 상수 0.254비트 차이로 붙는다.

### 4단계 [엄밀, ⚠ 측도론 세부 확인 필요] 찌꺼기는 0이 될 수 없다
H(Z | S, W) = 0이면 W를 고정했을 때 Σ f_k(x_k) = h(Σ x_k)가 (거의) 모든 x에서 성립한다. x_3, …, x_K를 고정하면 f_1(x) + f_2(y) = h′(x + y) (Pexider 함수방정식)이므로 f_k = φ + a_k, φ: ℝ → ℤ_M은 덧셈 준동형이다. 그런데 ℝ은 나눗셈이 되는 군(divisible group)이라 φ(x) = M·φ(x/M) = 0이다. 따라서 모든 f_k가 상수가 되고, Z가 X에 대해 아무 정보도 없으므로 D ≥ Kσ²이다.
- 결론: 쓸모 있는 부호에서는 반드시 H(Z | S, W) > 0. **"합만 정확히 전달하고 찌꺼기는 없는 부호"는 존재하지 않는다.** 남은 일은 "> 0"을 "≥ ½log₂K − c"로 정량화하는 것이다.
- ⚠ "거의 모든 x"에서 성립하는 Pexider 방정식의 가측(measurable) 판본이 필요하다. 표준 결과로 알고 있으나 문헌을 확인하지 않았다.

### 5단계 [미증명] 정량화 계획
- 5a [엄밀] 짝짓기로 독립 합 만들기: 조건을 더 걸면 엔트로피가 줄어드므로 H(Z | S, W) ≥ H(Z | V, W), V = (X_1+X_2, X_3+X_4, …). S는 V의 함수다. V가 주어지면 짝마다 차이 X_{2j−1} − X_{2j}가 서로 독립이므로 Z = Σ_j T_j, T_j = Q_{2j−1} + Q_{2j}는 서로 독립인 K/2개 항의 합이 된다.
- 5b [미증명] 짝 하나의 흔들림: H(T_j | V, W) ≥ c₀ > 0. 4단계의 정량판으로, "짝의 합을 작은 오차로 전하는 부호는 짝 안에서 흔들린다".
- 5c [미증명] 독립 합의 성장: K/2개 독립 항의 합은 √K배로 퍼져 엔트로피가 ½log₂K + O(1)이 된다. ℤ 위에서는 국소 중심극한정리(local CLT)이고, 성립 조건은 **T_j가 진부분군의 잉여류에 갇히지 않을 것**(비주기성)이다. 갇히는 경우가 정확히 Jog–Anantharam의 최소화 분포, 즉 짝수 속임수다. 이때는 Z의 하위 비트가 S로 정해져 레지스터의 유효 비트가 줄어드는 것으로 처리해야 한다 → D1의 양자택일이 여기서 나온다.
- 5d [대략] 넘침 쪽: 찌꺼기의 퍼짐 √K가 M에 닿으면 Z | S가 거의 균등해 H(Z|S) ≈ log₂M이다. 그러면 1단계에서 I(S; Z|W) ≈ 0이 되어 왜곡이 커진다. 모순이므로 이 영역은 자동으로 배제된다.

### 남은 공백
1. 5b의 정량적 상수 c₀ (해상도 D에 어떻게 의존하는지).
2. 5c를 K에 대해 균일한 오차로. 국소 중심극한정리의 오차가 K에 걸쳐 누적되지 않아야 한다.
3. 5c의 부분군 분기를 왜곡 하한으로 잇는 논증 (D1의 뒤 절반).
4. 블록 부호(d > 1)로의 확장. Q10의 차원 문제 때문에 좌표당 ½비트를 보장해야 한다.
5. 4단계의 가측성 세부.

---

## Q24. 심사 관점 자체 점검 6문항 (2026-11-19)

**[사용자]** "[질문1] 문제 설정과 가정이 명확한가? [질문2] 기존 연구와 비교해 무엇이 새롭고 중요한가? [질문3] 정리의 조건과 증명이 정확한가? [질문4] 시뮬레이션이 주장과 비교 기준을 제대로 뒷받침하는가? [질문5] 결과가 가정 밖에서도 의미가 있는가? [질문6] 설명과 재현성이 충분한가?"

**[답변 요지]** 지금 상태는 "문제와 증명 방향이 잡힌 제안 단계"다. 6문항 중 통과 수준인 것은 없다. 가장 큰 결함은 (1) 핵심 정리가 미증명이고, (2) SPEC의 블록 부호 설정(d → ∞)과 Q23의 스칼라 전개가 서로 다른 정리를 말하며, (3) 비교 기준을 보여 주는 시뮬레이션이 없다는 것이다.

| # | 판정 | 핵심 문제 |
|---|---|---|
| 1 설정·가정 | 부분적 | 스칼라 대 블록 불일치, 단일 라운드 제한의 근거 없음, 기호 미통일, 두꺼운 꼬리 미정의 |
| 2 신규성·중요성 | 주장 가능, 미검증 | 신규성은 모은 문헌과 제한된 검색 범위에서만 확인. "당연하다"는 반론에 대한 답 필요 |
| 3 정리·증명 | 1·2단계만 엄밀 | 정리 진술(상수 c, 영역)이 없음. 핵심 보조정리 L 미증명 |
| 4 시뮬레이션 | 부족 | 율 대 K 비교 그림 없음. 기존 두 스크립트는 좁은 주장만 뒷받침 |
| 5 가정 밖 | 일부 근거 있음 | THC의 RHT가 가우시안 가정을 지지. 상관·꼬리·다중 라운드는 미분석 |
| 6 설명·재현성 | 부족 | 증명이 interview.md에만 있음. 커밋 0회. 의존성 기록 없음 |

### 1. 문제 설정과 가정
- 명확한 것: 소스(독립 가우시안), 망(1단 스위치), 제약(같은 군 ℤ_M 위 덧셈만), 공유 난수 허용, 왜곡(합의 MSE, 정규화 D̄) (SPEC 3.1–3.2, Q16·Q17).
- 불명확한 것:
  - **스칼라 대 블록.** SPEC 3.1은 "블록 길이 = 차원 d, d → ∞"인데 Q23 전개는 좌표별 단발(one-shot) 부호다. 두 설정의 A-3은 다른 정리다. 블록 부호에서는 1·2단계가 d배로 그대로 성립하지만, 찌꺼기 항이 (d/2)log₂K 이상임을 보여야 하고 Q10의 차원 문제가 걸린다. 어느 쪽이 주 정리인지 정해야 한다.
  - 단일 라운드로 제한한 근거. SPEC 5.2는 "단순한 다중 라운드는 오히려 나빠짐을 계산으로 확인했다. 일반적인 경우는 미확인"이라고만 적었다.
  - 율의 정의: 상행(작업자 → 스위치)과 하행(스위치 → 작업자)이 같은 군을 쓴다고 가정했다. 비대칭 설계(THC: 상행 4비트, 하행 8비트)는 모델 밖이다. THC는 바로 이 비대칭을 쓴다.
  - 기호: K/N, X_k/g_n, 율-왜곡/레이트-왜곡이 문서마다 섞여 있다 (Q15, Q17 미결정).
  - 정리의 영역: "− c"의 c가 K, D, σ에 무관한 상수인지, D ≤ σ² 같은 영역 조건이 필요한지 정하지 않았다.

### 2. 새로움과 중요성
- 새로울 수 있는 것: (a) 가우시안에서 합 호환 부호 *전체*(공유 난수, 상관 양자화 포함)에 대한 역 한계. (b) 레지스터 비트 = 합 정보 + 찌꺼기라는 분해와, 기존 엔트로피 논증이 찌꺼기 항을 버려서 A-2에서 멈췄다는 진단 (Chen2023 §5.1이 남긴 간극의 설명). (c) 나눗셈 가능한 군 ℝ에서 유한군으로 가는 준동형이 0뿐이라는 사실을 압축 한계로 연결. (d) 부분군 분기(D1).
- 비교 위치: 제약 없는 하한(YangGroverKar Thm 2), 최악 경우 합 호환 하한(Chen2022 Cor 5.4), K = 2 달성(KrithivasanPradhan Thm 3.1)은 있다. 가우시안 합 호환 하한은 찾지 못했다.
- 약점:
  - 신규성 확인 범위가 좁다. 격자 부호·compute-and-forward·보안 집계의 2025~2026년 정보이론 문헌, Zamir 교재(2014)를 점검하지 않았다. 특히 "굵은 격자가 합의 분산을 덮어야 한다"의 필요성이 격자 문헌에 이미 있을 수 있다.
  - 예상 반론: "THC가 이미 ⌈log₂m⌉을 말했으니 당연하다." 답: 관찰은 반올림 부호에 대한 것이고, 공유 난수로 오차를 상쇄하는 부호(Suresh2022)나 짝수 같은 구조적 부호가 이를 피할 수 있는지는 열려 있었다. 이 답을 제안서에 넣어야 한다.
  - 중요성의 크기: K = 1024에서 5비트. 4비트 압축 기준으로는 크지만, 하행 비트만 늘리는 THC 방식에서는 실제 손실이 얼마인지 수치화하지 않았다.

### 3. 정리의 조건과 증명
- 엄밀: 1단계 (연쇄 법칙), 2단계 (S ⊥ W, 데이터 처리 부등식, 가우시안 율-왜곡; 단발 부호에도 성립), 5a (조건 추가로 엔트로피 감소, 짝의 차이가 짝의 합과 서로 독립).
- 조건부: 4단계는 모든 x에서의 Pexider 해를 썼다. "거의 모든 x"에서의 가측 판본은 인용이 필요하다. 결론도 "> 0"뿐이며 D에 무관한 하한을 주지 않는다.
- 계산: 3단계는 고해상도 이상화(e_k가 S와 무관한 독립 균등)를 썼다. 실제로는 S가 주어지면 X_k가 합 제약으로 서로 얽힌다. 넘침이 없다(√K ≪ M)고도 가정했다.
- 미증명: 보조정리 L 자체 (5b 짝 하나의 흔들림 c₀, 5c K에 균일한 국소 중심극한정리, 부분군 분기 → 왜곡). 이것이 정리의 전부다.
- 반례 점검: 상관 디더는 고해상도에서 이득 없음(시뮬레이션), 짝수 속임수는 해상도 손실(설명). 작업자마다 눈금이 다른 부호, 비균일 양자화는 점검하지 않았다.

### 4. 시뮬레이션
- sims/cq_dither.py: 감산 디더 균일 양자화에서 독립 디더 대 순열 디더의 합 오차 비율. 시행 6000회, 신뢰구간 없음, 율·넘침을 재지 않는다. 뒷받침하는 주장은 "이 한 가지 상관 방식은 고해상도에서 이득 없음"뿐이다.
- sims/hzs_exact.py: 시뮬레이션이 아니라 이상화된 해석 계산이다. K ≤ 16 (K = 32는 수치 상쇄로 실패). 반올림 부호에서 L이 성립함을 보일 뿐 "모든 부호"의 근거는 아니다.
- 빠진 비교 기준: 율 대 K 그림 하나에 (a) A-2 하한, (b) A-3 가설, (c) 균일 양자화 + 넓은 칸, (d) THC 방식(표 + g), (e) Krithivasan–Pradhan 격자, (f) All-Gather를 함께 그려야 한다. 실제 그래디언트 데이터 실험도 없다.

### 5. 가정 밖에서의 의미
- 근거가 있는 것: THC는 RHT로 좌표를 양자화하기 좋은 분포로 바꾼 뒤 좌표별로 양자화한다 ("pre- and post-processes them with the GPU-friendly Randomized Hadamard Transform (RHT) ... amenable to accurate quantization"). 그래서 스칼라 가우시안 모델이 실제 시스템과 가깝다 (⚠ RHT 후 분포가 가우시안에 가깝다는 것은 일반적 성질이며 THC 본문에서 확인하지 않음).
- 같은 구조라서 옮겨질 것으로 보이는 것: 링·트리(중간 노드가 같은 군에서 덧셈만 할 때, Q15 추론), 보안 집계(Chen2023의 간극).
- 미분석: 공통 성분(합이 K배로 커짐), 두꺼운 꼬리, 다중 라운드, 반복 간 부가 정보(오차 피드백), 학습 수렴 기준, 저전송률(D3: 대가가 줄어들 수 있음).

### 6. 설명과 재현성
- 증명과 판단이 interview.md의 문답 24개에 흩어져 있다. 독립된 정리·증명 노트가 없다.
- 저장소에 커밋이 0회다 (git status: 모든 산출물이 untracked).
- 시뮬레이션: 시드 고정(cq_dither seed 0), hzs_exact는 결정적. 그러나 실행 환경 기록(Python 버전)이 없고, 이 기계에는 numpy가 없다.
- 시각자료(해설 페이지)는 scratchpad에만 있고 저장소에 없다.
- 인용 일부는 에이전트가 읽은 것을 핵심 문장만 대조했다. SwitchML Thm 2 분자, Suresh Thm 2 계수는 PDF 추출이 깨져 미확인 (Q21).

### 고칠 일 (우선순위)
1. 주 정리를 스칼라(단발)로 할지 블록으로 할지 결정하고, 정리를 상수와 영역까지 포함해 진술한다.
2. 보조정리 L의 5b부터 증명한다.
3. 율 대 K 비교 그림(위 a~f)을 만든다.
4. 신규성 점검 2차: 격자·compute-and-forward·보안 집계 최신 문헌, Zamir 교재.
5. 정리·증명 노트를 별도 파일로 분리하고, 기호를 통일하고, 커밋한다.
6. 상·하행 비대칭(THC형)을 모델에 넣을지 결정한다.

---

## Q25. 6문항에 초안으로 답하기 (2026-11-19)

**[사용자]** "초안으로 답해줘."

**[해석]** Q24의 6문항 각각을 논문 초안의 절로 답하고, 미결정 사항은 잠정안으로 표시한다.

**[결과]** draft.md (논문 초안 v0). 잠정 결정:
1. 주 정리는 좌표별 단발 부호 (근거: THC의 RHT 뒤 좌표별 양자화). 블록 부호는 추측.
2. **율을 상행 R_up과 하행 R_down(레지스터 폭 log₂M)으로 나눈다. 대가 ½log₂K는 하행에 붙는다** (본 세션 정리). THC의 상행 4비트·하행 8비트와 맞는다. Q24-1의 "비대칭 설계는 모델 밖" 문제를 해소한다.
3. 정리 A의 영역 D̄ ≤ 1/4, 상수 c는 K·D̄·σ에 무관.
4. 기호는 K, X_k, U, N_k로 통일 (SPEC·proposal 개정은 아직).

**[새 계산]** D̄ = 0.01 비교표 (draft.md 4.1). 정리 A 하한은 K가 4배일 때 1비트, THC 하행 폭 ⌈log₂(30K)⌉은 2비트씩 는다. 단 THC의 왜곡이 같지 않으므로 같은 왜곡에서의 차이는 실험이 필요하다.

---

## Q26. [결정] 주제: 합 호환 CEO 문제 (2026-11-20)

**[사용자]** 주 결과 후보 셋 — (1) 독립 가우시안의 ½log₂K 대가와 원리 D1, (2) 합 호환 CEO 문제, (3) 저전송률 상전이 D3 — 중 **(2) 합 호환 CEO 문제**를 골랐다.

**[결정 내용]**
- 정식화: Zhang–Tao–Wang–Xu의 가우시안 CEO 정식화(PRIOR_CHECK 조사 B1)에 "융합 센터(스위치 뒤 복호기)가 메시지의 군 합 Z = Q₁ + ⋯ + Q_K (mod M)만 본다"는 제약을 넣는다.
- 소스: 공통 성분 모델 X_k = U + N_k가 처음부터 주 모델이다. 독립 가우시안(U = 0)은 특수 경우이며 정리 A는 그 경우의 결과로 들어간다.
- 주 결과의 모양: 공통 성분 대 작업자 잡음 비율에 따른 합 호환 대가 곡선.

**[이 결정의 의미 (본 세션 판단, 검증 전)]**
- Q16·Q17의 "기본 = 독립, 확장 = 상관" 순서가 뒤집힌다. 상관 모델이 주 모델, 독립이 특수 경우가 된다.
- 정리 A(보조정리 L)는 여전히 필요하다. 특수 경우에서 정리 A가 서지 않으면 일반 곡선의 하한도 서지 않는다.
- 비교 기준이 바뀐다. 제약 없는 쪽은 YangGroverKar Thm 2(독립)가 아니라 가우시안 CEO 합 율-왜곡(Oohama, Prabhakaran–Tse–Ramchandran; derivations/classic/10 부록)이다.
- CEO 표준 목표는 U의 추정이고 본 연구 목표는 합 S = KU + ΣN_k다. 두 목표 중 무엇을 쓸지 정해야 한다.
- PRIOR_CHECK 함의 1: 실제 학습에서 공통 성분 비율은 b/B_noise로 작을 수 있다. 실측(S2)으로 이 비율 범위를 먼저 정해야 곡선의 어느 구간이 현실인지 말할 수 있다.

**[반영 대기]** draft.md 제목·1장·2장, proposal 가제·§2.2·§4, SPEC 3.1·5장. 아래 미결과 함께 개정한다.

**[미결]** (a) 목표: U 추정 대 합 S 추정. (b) ①스칼라 단발 대 블록 부호. (c) ④기호 K 통일. (d) Zhang2023_CEO PDF 확보(arXiv 2206.13984)와 본문 정독.

**[보강, 2026-11-20] 레퍼런스 구조.** 사용자가 Slepian–Wolf → AK·Wyner–Ziv → CEO 계보와 BZV1996·Yamamoto1982·Tsitsiklis1986을 핵심 레퍼런스로 제시했다. 유도 노트와 대조한 결과를 반영해 다음과 같이 정했다 (draft.md 2장 "레퍼런스 구조").
- 29_Tsitsiklis1986은 Tsitsiklis–Bertsekas–Athans의 비동기 분산 기울기 최적화 논문이다. 분산 검정 논문이 아니다. 본 연구는 MSE 추정이라 검정 문헌은 쓰지 않고, 이 논문은 왜곡과 학습 수렴의 연결 근거로 쓴다.
- BZV1996은 유한 알파벳·해밍 왜곡의 시조 논문이다. 가우시안 2차 CEO는 Viswanathan–Berger 1997, Oohama 1998, Prabhakaran–Tse–Ramchandran 2004, Oohama 2005이며, 주 레퍼런스는 Oohama 1998이다. 넷 다 미확보 → papers/TO_DOWNLOAD.md 우선순위 A.
- Yamamoto1982는 부호기 하나 + 복호기 부가 정보 문제라 시간 부가 정보의 근거로 쓴다. 다중 부호기 합 계산은 B 줄기(Körner–Marton → Han–Kobayashi → Krithivasan–Pradhan·Wagner 2011)가 맡는다.

---

## Q27. [결정] 정리 골격 수정, 복원 목표 X, 목표 사다리 (2026-11-20)

**[사용자 제안]** 4부 구성: (1) 군 합 제약 아래 율-왜곡 영역과 단일 문자화, 구조적 부호가 ΣI(Y_k;U_k)보다 낮은 합 율을 낸다는 주장, (2) 구조적 대 무작위 부호의 간극, (3) DPI 사슬 X → Y → U → ⊕U → X̂로 조인 역정리 (피셔 정보, Wagner 역정리 확장), (4) TBA 1986·Yamamoto를 결합한 수렴 속도·정상상태 오차·적응 율 배분.

**[검토 결과, 사용자 수용]**
1. 1·2번 방향 반대: Oohama·PTR 역정리는 모든 부호에 적용되므로 군 합 제약 아래 영역 ⊆ Oohama 영역. ΣI(Y_k;U_k)보다 낮추는 것은 BT 비닝이 이미 함 (BT 합 율은 I(Y^K;U^K)). CEO는 양의 상관 + 양의 가중합이라 Wagner 조건 (2)에서 QB 최적, 격자는 ρ = 0에서도 인코더당 ½비트 손실. → "제약은 대가를 치른다"로 뒤집음.
2. BT는 손실이 아니라 실행 불가. Zamir–Feder의 독립·균등은 디더 평균에서만. Forney 선형 라벨링은 ℤ_{2^b}에서 깨짐.
3. DPI만으로는 제약 없는 크기의 하한만 나옴. 조이는 것은 log|G| ≥ I(X;Z|W) + H(Z|X,W)의 찌꺼기 항. 도구는 EPI·합집합 엔트로피. Wagner 정리 2·3은 제약 없는 문제의 하한이라 첫 항에만 재사용.
4. 단일 문자화는 두 인코더 선형 함수 문제도 미해결이라 위험.
5. 4번은 본론에서 빼 7장으로. 공중 계산(아날로그 실수 합)은 모델 밖, 보안 집계는 모델 안. Yamamoto는 부호기에도 이전 합이 있어 조건부 율-왜곡이 됨.
6. 기호: 목표 X, 관측 Y_k, 군 합 Z, 보조 V_k.

**[결정]**
- 복원 목표는 **X (작업자 공통의 참 그래디언트)**. 미결 (a) 해소.
- 사용자: "목표를 높게 잡고, 필요하면 다양한 시도를 해보자." → 4번(단일 문자화·정확한 영역)은 버리지 않고 최고 목표 S로 둔다. 목표 사다리 S(정확한 영역) → A(블록 상수 간극) → B(단발) → C(격자 부호군 한정)를 draft.md "정리 골격 v1"에 기록. 경로 여럿을 병행한다.

**[반영]** draft.md 상단 확정 사항, "정리 골격 v1" 절 신설. 1~4장 본문, proposal, SPEC 개정은 아직.

**[남은 미결]** (b) 스칼라/블록은 목표 사다리로 대체 (블록이 목표, 단발은 안전망). (c) 기호 통일: 골격 v1 기호를 SPEC·proposal에 반영. (d) Zhang–Tao–Wang–Xu, Oohama 1998 정독.

---

## Q28. [결정] 문제 명세: 어떤 CEO 문제를 왜 푸는가 (2026-11-20)

**[사용자]** "X, Y, V, W는 다른 논문도 다 보는 것 아닌가? 격자·보로노이 영역은 안 쓰나? CEO 문제 중에서 정확히 어떤 문제를 왜 해결해야 하는지 spec을 정하자."

**[답변 요지]**
- 기호는 BZV 이래 표준. 새로움은 (i) 융합 사상이 군 합 Z = ⊕Q_k로 제약됨, (ii) 율이 R_up·R_down 둘, (iii) K 척도.
- 격자는 쓴다: 모델에서 G = Λ_f/Λ_c가 군의 표준 예 (스위치 (ℤ_{2^b})ⁿ = ℤⁿ/2^bℤⁿ), 달성에서 보로노이 영역 디더·mod Λ_c·중첩비·G(Λ). 역정리는 격자에 의존하지 않고 모든 G, f_k에 대해.
- 동기: (1) 대칭 CEO의 최적 추정은 ΣV_k의 함수인데 BT는 개별 복호 필요, (2) 공통 성분 때문에 합 범위가 K²σ_X²로 결맞게 커짐. 예비 계산(θ = 2): 제약 없는 작업자당 율 ≈ ½비트 대 단순 격자 log K + ½log γ, 1비트 계수 방식은 R_up = 1·R_down = log(K+1). (3) SwitchML·THC·보안 집계.

**[결정]** 주 질문 = K → ∞ 척도 + 유한 K 상수 간극. 부가 정보 없는 모델이 주, 있는 모델은 확장. 율 = (R_up, R_down, D) 삼중 영역.

**[반영]** SPEC.md P절 (논문 명세 v1.1) 신설. draft.md 정리 골격 v1에 SPEC P절 참조.

**[미확인·위험]** 예비 계산은 고해상도 근사·손 계산이며 Oohama 식은 원문 대조 전이다. 1비트 계수 방식의 D 상수는 대략값이다. 다음 단계에서 수치로 검산한다.

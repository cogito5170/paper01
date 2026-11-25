# 세그먼트(조각·토큰) 선택 기법의 현재 위치 (2026-11-24 기준 조사)

목적: 문서 2(Seon 외, LCOMM 2024)의 세그먼트 선택이 2026년 11월 기준으로 어디까지 발전했는지 파악한다.
방법: 웹 검색 7회. arXiv 초록은 TOFS와 Model-Aware RD 두 편만 직접 확인했고, 나머지는 검색 요약에 근거한다(★ = 초록 확인).

## 1. 계보 A: 컴퓨터 비전의 조각 선택 (연산량 절감)
| 연도 | 논문 | 핵심 |
|---|---|---|
| 2020 | Uzkent–Ermon, "Learning When and Where to Zoom with DRL" (PatchDrop), CVPR 2020 Oral | 저해상도(LR)를 보고 강화학습(REINFORCE)으로 고해상도(HR) 조각을 고른다. 조각의 약 50%를 버리고도 정확도 손실이 작다. **문서 2의 직접 조상** |
| 2021 | Cordonnier 외, "Differentiable Patch Selection" (DPS), arXiv 2104.03059 | 조각 선택을 순위 문제로 바꾸고 미분 가능한 top-k를 쓴다 |
| 2023–24 | IPS(반복 조각 선택), LTRP(자기 지도 조각 순위), AgentViT(ViT용 RL 조각 선택), PAMIL(병리 WSI) | 순위·버퍼 방식, 자기 지도 방식으로 넘어감 |
| 2025 | LookWhere, NeurIPS 2025, arXiv 2505.18051 | REINFORCE와 Gumbel top-k를 시도했지만 이득이 없었다고 보고. **RL 기반 조각 선택에 비판적** |

ViT 토큰 줄이기(조각 선택의 현대판):
- 표준 기준선은 DynamicViT(학습형 가지치기), EViT(CLS 주의 + 융합), ToMe(학습 없는 병합)이다.
- 2025–26 흐름은 세 가지다. 가지치기와 병합을 섞는 혼합형(RAPID, arXiv 2606.08156), 학습·매개변수가 없는 방식(Dyna-ViT, CVPR 2026 Findings), 하드웨어 지연을 고려한 스케줄링(WACV 2025)이다. HEART-ViT(arXiv 2512.20120)도 이 흐름에 있다.
- 서베이: arXiv 2501.07451(동적 신경망), arXiv 2505.03113(경량 ViT).

## 2. 계보 B: 의미 통신에서의 선택 (통신량·연산량 절감)
| 연도 | 논문 | 핵심 |
|---|---|---|
| 2022 | Shao–Mao–Zhang, IEEE JSAC 40(1) | VIB 기반 과업 지향 통신. 문서 2가 비판하는 [4] |
| 2024 | **Seon 외, LCOMM 2024 (문서 2)** | 송신 DRL은 세그먼트 선택, 수신 DRL은 등화기 선택. 연산량은 줄였지만 통신량은 고정 |
| 2024 | "Adaptive semantic token selection for AI-native goal-oriented communications," IEEE Globecom Wkshps 2024 | 의미 토큰 선택 |
| 2025 | Seon 외, TCCN 2025 (문서 4) | 특징 압축으로 확장. 압축률을 DRL로 조절 |
| 2025 | "Adaptive Semantic Token Communication for Transformer-Based Edge Inference," arXiv 2505.17604 (IEEE TMLCN) | 토큰 선택과 무선 자원 할당을 함께 최적화 |
| 2025 | Erak 외(Bennis 포함), "Adaptive Pareto-Optimal Token Merging…," arXiv 2509.09168 (Globecom Wkshps 2025), 저널판 IEEE OJ-COMS | 사전 학습 ViT의 토큰을 학습 없이 병합하고 JSCC로 전송. 층별 병합 비율을 다목적 최적화로 정함 |
| 2025 | IRCSC, arXiv 2504.20441 | 중요도 분석기와 특징 선택기로 채널 상태에 따라 율 조절 |
| 2025 | Feature-Importance-Aware Transmission Control, ICT Express 2025 | 중요도 가중 의미 스펙트럼 효율(wSSE) 지표, 선택률에 따른 변화 분석 |
| 2025 | "Token communications: A large model-driven framework…," IEEE Wireless Commun. Mag., Oct. 2025 (Qiao, Bennis, Niyato 외) | 토큰 통신(TokCom) 틀 |
| 2026.01 | SComCP, IEEE TVT, DOI 10.1109/TVT.2026.3654968 | 협력 인지용 중요도 인지 특징 선택 |
| 2026 | 차량 인터넷 계층 의미 전송, MDPI Sensors 26(9):2606 | 이산 조각 모드 집합, 크기-비용·크기-의미 이득 모델, AoI·CSI 인지 스케줄링 + 리아푸노프 가상 큐 |
| 2026.05 | TONIC, arXiv 2605.21553 | 토큰을 고르지 않고 중요한 토큰 위치를 더 강하게 보호(LDPC 부호율 차등) |
| 2026.05 | Context-Aware Wireless Token Communication via Joint Token Masking and Detection, arXiv 2605.02123 | 토큰 마스킹과 검출을 함께 설계 |
| 2026.07 | ATS-ToDMA, arXiv 2607.03520 | 적응 토큰 선택 + 토큰 영역 다중 접속 |
| 2026.08 | Token-Oriented SC with Pretrained ViTs, arXiv 2608.25410 | 사전 학습 ViT 기반 토큰 전송 |
| 2026.10 | Queue-Aware Token Communications, arXiv 2610.16730 | 큐 상태를 고려한 토큰 전송 |
| 2026.11 | Ti-SemCom, arXiv 2611.12928 | 영상에서 객체·움직임 기반 중요 영역 → 계층적 토큰, 대역폭에 따라 전송 토큰을 고름 |
| 2026.11 | ★ **TOFS**, Zhu 외, arXiv 2611.09173 (11월 6일) | 수신기 분류 손실의 "교체(swap)" 차이로 쌍별 순위 지도 신호를 만들어 선택기를 학습. 특징 효용이 **다른 특징과 채널 왜곡에 의존**함을 명시. CIFAR-10, Rayleigh에서 84% 대 68% |

## 3. 계보 C: 선택·과업 지향 부호화의 이론
| 연도 | 논문 | 핵심 |
|---|---|---|
| 2026.02 | ★ **Enttsel–Corlay, "Model-Aware Rate–Distortion Limits for Task-Oriented Source Coding," arXiv 2602.12866** | 간접 율-왜곡 이론으로 과업 지향 원천 부호화(TOSC)의 한계를 다시 보고, 과업 모델의 비최적성과 구조 제약을 반영한 한계를 제시. 학습형 TOSC가 한계에서 멀다는 것을 실험으로 보이고 **송신기 복잡도**를 병목으로 지목 |
| 2026.06 | "Information Bottleneck Meets Quantization: Finite Rate…," arXiv 2606.10869 | 가우스 IB에서 비트 할당. β가 암묵적 특징 선택 역할을 함 |
| 2026.10 | TADIB, "Distributed IB Theory for Multi-Modal Task-Aware SC," arXiv 2510.04000 (v4) | 모달리티 **선택**을 율-관련성 절충의 새 자유도로 둠. 이산 선택을 확률적 완화로 풂 |
| 2026.10 | "Optimal Multitask Representations Under a Rate Constraint: An IB Analysis," arXiv 2610.30493 | 다중 과업 IB |

## 4. 요약: 세그먼트 기법은 어디까지 왔나
1. **단위가 바뀌었다**: 이미지 격자 조각(2020–24) → ViT 토큰(2025–) → 대규모 모델 토큰 통신(TokCom, 2025–26).
2. **선택 방식이 바뀌었다**: REINFORCE 정책(PatchDrop, 문서 2) → 미분 가능 top-k·순위 학습(DPS, TOFS) → 학습 없는 병합(ToMe 계열). RL 선택은 비전 쪽에서 비판받는다(LookWhere).
3. **목표가 바뀌었다**: 연산량 절감(문서 2) → 통신 자원과 함께 최적화(토큰 선택 + 자원 할당, 큐·AoI·다중 접속).
4. **상호작용 인식**: TOFS가 "특징의 효용은 함께 보내는 다른 특징과 채널에 달려 있다"는 점을 학습 방식으로 다룬다. 초록 v3 사슬 D(독립 점수 선택의 격차)와 같은 문제의식이다.
5. **이론은 비어 있다**: 선택 자체(어느 조각을 보낼지)를 율-왜곡·유한 길이 이론으로 다룬 결과는 찾지 못했다. 가장 가까운 것은 Enttsel–Corlay(간접 율-왜곡, 선택 없음)와 TADIB(모달리티 선택, 점근)이다.

## 5. 우리 연구(초록 v3)와의 관계
- **신규성 위험**: Enttsel–Corlay 2026은 "간접 율-왜곡 한계로 학습형 TOSC를 평가하고 송신기 제약을 넣는다"는 점에서 v3 사슬 B와 겹친다. **반드시 원문을 읽고 차별점을 정리해야 한다.** 예상 차별점은 선택 부호기 제약(S, X_S), 단발(k = 1) 체제, 채널 결합 세 가지이다.
- **동기 강화**: TOFS는 사슬 D의 실증판으로 인용할 수 있다. 상호작용 때문에 독립 점수 선택이 손해를 본다는 내용이다.
- **비교 대상**: TADIB의 모달리티 선택 완화 기법은 사슬 B 선택 부호기의 정식화와 비교할 가치가 있다.

## 내려받은 것
30편 전문을 papers/segment/에 받았다(목록과 출처는 papers/segment/README.md). MDPI Sensors 26(9):2606은 사용자가 받아 주었다. Enttsel–Corlay의 "single-TOSC"는 단발(one-shot)이 아니라 **단일 과업(single-task)** TOSC라는 뜻이다.

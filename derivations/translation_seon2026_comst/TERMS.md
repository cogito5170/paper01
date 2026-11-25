# 공통 용어 목록 (Seon 외 2024 LCOMM, 2025 TCCN, 2026 COMST 번역용, 2026-11-24)
스킬 용어집(glossary-information-theory.md, glossary-machine-learning.md)이 우선이고, 아래는 두 논문에서 새로 정한 것이다.
처음 나올 때만 한국어(영어) 또는 한국어(약어, Full English)로 쓴다. 조각(part)으로 나눠 번역할 때는 자기 조각에서 처음 나오면 괄호를 달고, 합칠 때 정리한다.


| 영어 | 번역 |
|---|---|
| semantic communication (SC) | 의미 통신(SC) |
| task-oriented semantic communication (TOSC) | 과업 지향 의미 통신(TOSC) |
| DRL-SC | DRL-SC (그대로) |
| deep reinforcement learning (DRL) | 심층 강화학습(DRL) |
| reinforcement learning | 강화학습 |
| agent / state / action / reward / policy / episode | 에이전트 / 상태 / 행동 / 보상 / 정책 / 에피소드 |
| REINFORCE algorithm | REINFORCE 알고리즘 |
| policy gradient | 정책 경사 |
| channel equalization / equalizer | 채널 등화 / 등화기 |
| variational autoencoder (VAE) | 변분 오토인코더(VAE) |
| encoder / decoder | 부호기 / 복호기 |
| semantic encoder / decoder | 의미 부호기 / 복호기 |
| segment / segment selection | 세그먼트 / 세그먼트 선택 |
| feature compression / feature vector / feature space | 특징 압축 / 특징 벡터 / 특징 공간 |
| dimensionality reduction | 차원 축소 |
| compression ratio (CR) | 압축률(CR) |
| latent (vector, space) | 잠재 (벡터, 공간) |
| reconstruction | 복원 |
| classification accuracy | 분류 정확도 |
| task-irrelevant / task-relevant | 과업과 무관한 / 과업과 관련된 |
| non-linear channel | 비선형 채널 |
| Rayleigh / Rician fading | Rayleigh / Rician 페이딩 |
| K-factor | K-인자 |
| signal-to-noise ratio (SNR) | 신호 대 잡음비(SNR) |
| peak signal-to-noise ratio (PSNR) | 최대 신호 대 잡음비(PSNR) |
| mean squared error (MSE) | 평균 제곱 오차(MSE) |
| channel state information (CSI) | 채널 상태 정보(CSI) |
| additive white Gaussian noise (AWGN) | 가산 백색 가우스 잡음(AWGN) |
| joint source-channel coding (JSCC) / DeepJSCC | 결합 원천-채널 부호화(JSCC) / DeepJSCC |
| computational complexity | 계산 복잡도 |
| state-of-the-art (SOTA) | 최신(SOTA) |
| ablation study | 절제 연구(ablation study) |
| convergence | 수렴 |
| multi-modality | 다중 모달리티 |
| precision / recall / F1 score | 정밀도 / 재현율 / F1 점수 |
| true/false positive/negative (tp, tn, fp, fn) | 참·거짓 양성·음성 (기호는 원문대로) |
| convolutional layer / fully connected layer | 합성곱 층 / 완전 연결 층 |
| activation function | 활성화 함수 |
| learning rate / batch size / epoch | 학습률 / 배치 크기 / 에포크 |
| sixth-generation (6G) | 6세대(6G) |
| transmitter / receiver | 송신기 / 수신기 |
| transmission efficiency | 전송 효율 |
| digital communication | 디지털 통신 |
| Kullback–Leibler (KL) divergence | Kullback–Leibler(KL) 발산 |
| reparameterization trick | 재매개변수화 기법 |
| Internet of Things (IoT) | 사물 인터넷(IoT) |

## 2026 COMST 서베이에서 추가 (2026-11-24)
| 영어 | 번역 |
|---|---|
| agentic semantic communication (ASC) | 에이전트형 의미 통신(ASC) |
| agentic / agency / autonomy | 에이전트형 / 행위 주체성 / 자율성 |
| intuition-driven SC | 직관 기반 의미 통신 |
| reasoning-driven SC | 추론 기반 의미 통신 |
| System 1 / System 2 | 시스템 1 / 시스템 2 |
| perceive / plan / reason / self-correct | 지각 / 계획 / 추론 / 자기 교정 |
| taxonomy | 분류 체계 |
| large language model (LLM) | 대규모 언어 모델(LLM) |
| large-scale AI model / foundation model | 대규모 AI 모델 / 기반 모델 |
| vision-language model (VLM) | 시각-언어 모델(VLM) |
| world model | 세계 모델 |
| generative AI (GAI) | 생성형 AI(GAI) |
| retrieval-augmented generation (RAG) | 검색 증강 생성(RAG) |
| knowledge base (KB) / knowledge graph (KG) | 지식 베이스(KB) / 지식 그래프(KG) |
| orchestration / orchestrator | 오케스트레이션 / 오케스트레이터 |
| emergent communication | 창발적 통신 |
| multi-agent system (MAS) | 다중 에이전트 시스템(MAS) |
| multi-agent reinforcement learning (MARL) | 다중 에이전트 강화학습(MARL) |
| token communication (TokCom) | 토큰 통신(TokCom) |
| tokenizer / token | 토크나이저 / 토큰 |
| chain-of-thought (CoT) | 사고 사슬(CoT) |
| ReAct, Transformer, diffusion model | ReAct, 트랜스포머(Transformer), 확산 모델 |
| prompt / prompting / in-context learning | 프롬프트 / 프롬프팅 / 맥락 내 학습 |
| fine-tuning / pre-training | 미세 조정 / 사전 학습 |
| knowledge distillation | 지식 증류 |
| hallucination | 환각 |
| out-of-distribution (OOD) | 분포 밖(OOD) |
| causal / causality | 인과적 / 인과성 |
| edge deployment / edge device / edge computing | 엣지 배포 / 엣지 기기 / 엣지 컴퓨팅 |
| collaborative / coordination | 협력 / 조정 |
| closed-loop | 폐루프 |
| context / contextual | 맥락 / 맥락적 |
| low Earth orbit (LEO) | 저궤도(LEO) |
| non-terrestrial network (NTN) | 비지상 네트워크(NTN) |
| use case | 활용 사례 |
| open challenge / roadmap | 미해결 과제 / 로드맵 |
| semantic similarity | 의미 유사도 |
| bit error rate (BER) | 비트 오류율(BER) |
| protocol stack | 프로토콜 스택 |
| vector quantization (VQ) | 벡터 양자화(VQ) |

## 조각 번역 중 추가로 정한 것 (2026-11-24)
| 영어 | 번역 |
|---|---|
| inference vs reasoning (한 문장에 함께 나올 때) | 추론(inference) / 추론(reasoning)으로 원어 병기 |
| emergent language (EmLang) | 창발 언어(EmLang) |
| embodied AI / agentic AI | 체화 AI / 에이전트형 AI |
| neuro-symbolic (NeSy) | 신경-기호(NeSy) |
| intent / intent alignment / semantic alignment | 의도 / 의도 정렬 / 의미 정렬 |
| semantic drift / semantic fidelity | 의미 표류 / 의미 충실도 |
| belief state | 신념 상태 |
| centralized training with decentralized execution (CTDE) | 중앙집중 학습·분산 실행(CTDE) |
| surprisal | 놀람(surprisal) |
| topographic similarity (TopSim) / compositionality | 지형 유사도(TopSim) / 구성성 |
| theory of mind (ToM) / pragmatic communication (PragCom) | 마음 이론(ToM) / 화용 통신(PragCom) |
| digital twin (DT) | 디지털 트윈(DT) |
| catastrophic forgetting / federated learning | 파국적 망각 / 연합 학습 |
| low-rank adaptation (LoRA) | 저랭크 적응(LoRA) |
| Agentic Scheduler / Controller / Transceiver | 에이전트형 스케줄러 / 제어기 / 송수신기 |

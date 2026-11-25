# 번역 지침: Finite-Blocklength Information Theory (arXiv 2504.07743v2, CC BY 4.0)

독자: 정보이론 박사과정생. 수학 증명을 하는 사람이며, 영어 원문 용어는 알지만 한국어로 막힘없이 읽고 싶어 한다.
목표: **원문의 내용은 하나도 빼거나 더하지 않되, 처음부터 한국어로 쓴 학술 글처럼 읽히게.**

## A. 문체 규칙 (영한 번역가의 기법)
1. **문체**: 학술 평서문 `-다` 체. "~이다, ~한다, ~을 보였다". 경어 금지.
2. **긴 문장은 나눈다.** 영어 한 문장에 관계절·분사구가 둘 이상이면 한국어 두세 문장으로 쪼갠다. 관형절을 두 겹 넘게 명사 앞에 쌓지 않는다.
3. **명사화 구문을 푼다.** "the characterization of the fundamental limits" → "근본 한계를 규명하는 일". "enable tractable mathematical characterizations" → "수학적으로 다루기 쉽게 해 준다".
4. **무생물 주어를 부사어로 바꾼다** (필요할 때). "This result shows that…" → "이 결과에서 …임을 알 수 있다" / "이 결과는 …을 보여 준다" 중 자연스러운 쪽.
5. **수동태를 능동으로.** "is defined as" → "~로 정의한다", "was proved in [x]" → "[x]에서 증명했다" 또는 "[x]가 증명했다". "~되어진다", "~에 의해 ~된다"는 금지.
6. **번역투 회피**: "~에 있어서", "~를 통해서"(남발), "~함에 의해", "~적인 ~의", "그것은", "그들은", "~하는 것이 가능하다"(→ "~할 수 있다"), "가지다"(have의 직역; "~이 있다", "~을 지닌다"), "-들"의 남발, "매우"·"상당히"의 기계적 반복.
7. **대명사(it, they, this, which)는** 지시 대상을 명사로 다시 쓰거나 생략한다.
8. **접속어를 다양하게**: However → 그러나 / 하지만 / 다만, Moreover → 또한 / 아울러 / 더 나아가, Specifically → 구체적으로, Notably → 특히, In other words → 다시 말해.
9. **어순**: 한국어는 정보 순서가 "배경 → 결론"이다. 영어가 결론부터 말하고 조건을 뒤에 붙이면 조건을 앞으로 옮긴다.
10. **원문 의미를 바꾸지 않는다.** 헤지(may, often, roughly, to some extent)는 살린다: "~일 수 있다", "흔히", "대략", "어느 정도".

## B. 용어 표기 규칙
- 전문 용어는 **장(section)마다가 아니라 문서 전체에서 처음 나올 때만** `한국어(영어)` 꼴로 쓰고, 그 뒤로는 한국어만 쓴다. 담당 구간에서 처음 나오면 괄호를 달아도 된다(병합 때 중복을 정리한다).
- 약어: 처음에 `한국어(약어, Full English)`, 이후 약어만. 예: 초고신뢰 저지연 통신(URLLC, ultra-reliable low latency communication) → 이후 URLLC.
- 인명은 로마자 그대로: "Kostina 등 [10]은", "Polyanskiy, Poor, Verdú [11]는". 예외 없음(Shannon도 Shannon).
- 인용 번호 [11], [9, 15]는 원문 그대로 둔다(LaTeX에서 그냥 텍스트 `[11]`).
- 수식·기호·식 번호는 원문 그대로. 식 번호는 `\tag{n}`으로 원문 번호를 유지한다.
- 원문의 명백한 오류는 고치지 말고 본문은 원문대로 옮긴 뒤 `\onote{…}` 각주로 지적한다. 옮긴이 주는 꼭 필요할 때만.

## C. 용어집 (반드시 이대로)
| 영어 | 번역 |
|---|---|
| finite blocklength | 유한 부호 길이 |
| blocklength | 부호 길이 (원천 쪽 k도 "부호 길이") |
| non-asymptotic / nonasymptotic | 비점근(적) |
| asymptotic | 점근(적) |
| achievability bound | 달성 가능성 한계 |
| converse bound | 역 한계 |
| approximation | 근사 |
| fundamental limit | 근본 한계 |
| source coding / channel coding | 원천 부호화 / 채널 부호화 |
| joint source-channel coding (JSCC) | 결합 원천-채널 부호화(JSCC) |
| separate source-channel coding (SSCC) | 분리 원천-채널 부호화(SSCC) |
| (almost) lossless compression | (거의) 무손실 압축 |
| lossy compression | 손실 압축 |
| fixed-length / variable-length | 고정 길이 / 가변 길이 |
| prefix (code, condition) | 접두(부호, 조건) |
| codebook / codeword | 부호책 / 부호어 |
| code size | 부호책 크기 |
| coding rate | 부호율 |
| rate-distortion function (RDF) | 율-왜곡 함수 |
| distortion measure | 왜곡 척도 |
| excess-distortion probability | 초과 왜곡 확률 |
| excess-rate probability | 초과율 확률 |
| information random variable | 정보 확률변수 |
| information density | 정보 밀도 |
| d-tilted information | d-기울인 정보 |
| varentropy | 바렌트로피 |
| dispersion (source/channel) | 분산도 (원천 분산도 / 채널 분산도) — variance(분산)와 구별 |
| rate-dispersion matrix / distortion-dispersion function | 율-분산도 행렬 / 왜곡-분산도 함수 |
| second-order (coding rate, term) | 2차 (부호율, 항) |
| first-order / third-order | 1차 / 3차 |
| remainder term | 나머지 항 |
| Gaussian approximation / normal approximation | 가우스 근사 / 정규 근사 |
| central limit theorem (CLT) | 중심극한정리(CLT) |
| large deviations (LD) / moderate deviations (MD) | 대편차(LD) / 중편차(MD) |
| error exponent / reliability function | 오류 지수 / 신뢰도 함수 |
| strong converse / weak converse | 강한 역정리 / 약한 역정리 |
| meta-converse | 메타 역정리 |
| binary hypothesis testing | 이진 가설 검정 |
| type I / type II error | 제1종 / 제2종 오류 |
| random coding / random binning | 무작위 부호화 / 무작위 비닝 |
| maximal coding | 최대 부호화 |
| dependence-testing (DT) bound | 의존성 검정(DT) 한계 |
| κβ bound / ββ bound | κβ 한계 / ββ 한계 |
| sphere covering / sphere packing | 구 덮기 / 구 채우기 |
| distortion d-ball | 왜곡 d-공 |
| lossy AEP | 손실 AEP(점근적 등분배 성질) |
| memoryless source | 무기억 원천 |
| binary / discrete / Gaussian memoryless source (BMS/DMS/GMS) | 이진 / 이산 / 가우스 무기억 원천(BMS/DMS/GMS) |
| Gauss-Markov source | 가우스-마르코프 원천 |
| autoregressive | 자기회귀 |
| reverse water-filling / water level | 역 물 채우기 / 수위 |
| power spectrum | 전력 스펙트럼 |
| mismatch / mismatched | 불일치 |
| spherical codebook | 구면 부호책 |
| ensemble tight | 앙상블 관점에서 tight(앙상블 tight) — 처음 한 번 풀어 쓰기: "부호 앙상블 분석이 최적" |
| side information | 부가 정보 |
| Kaspi problem | Kaspi 문제 |
| successive refinement | 점진적 정밀화 |
| joint / separate excess-distortion criterion | 결합 / 개별 초과 왜곡 기준 |
| type covering lemma | 형(type) 덮개 보조정리 |
| channel capacity / ε-capacity | 채널 용량 / ε-용량 |
| average / maximal error probability | 평균 / 최대 오류 확률 |
| AWGN channel | AWGN 채널(가산 백색 가우스 잡음 채널) |
| signal-to-noise ratio (SNR) | 신호 대 잡음비(SNR) |
| quasi-static fading | 준정적 페이딩 |
| ergodic / block-memoryless fading | 에르고딕 / 블록 무기억 페이딩 |
| channel state information (CSI) | 채널 상태 정보(CSI) |
| feedback | 되먹임 |
| wiretap channel | 도청 채널 |
| power shell / truncated Gaussian | 전력 껍질 / 절단 가우스 분포 |
| multiple access channel (MAC) | 다중 접속 채널(MAC) |
| capacity region / pentagon / polytope | 용량 영역 / 오각형 / 다면체 |
| many-access channel (MnAC) | 다수 접속 채널(MnAC) |
| massive random access | 대규모 무작위 접속 |
| unsourced random access (URA) | 무출처 무작위 접속(URA) |
| per-user probability of error (PUPE) | 사용자별 오류 확률(PUPE) |
| energy-per-bit | 비트당 에너지 |
| multi-user interference (MUI) | 다중 사용자 간섭(MUI) |
| activity detection | 활성 사용자 검출 |
| misdetection / false-alarm | 미검출 / 오경보 |
| individual / common codebook | 개별 / 공통 부호책 |
| base station (BS) | 기지국(BS) |
| cell-free massive MIMO | 셀프리 대규모 MIMO |
| list decoder | 목록 복호기 |
| maximum-likelihood (ML) decoder | 최대 우도(ML) 복호기 |
| task-oriented | 과업 지향 |
| cliff effect | 절벽 효과 |
| semantic information | 의미 정보 |
| URLLC / umMTC / IoT / 3GPP / 5G / 6G / AR / VR | 처음 한 번 풀어 쓰고 이후 약어 |
| short-packet communication | 짧은 패킷 통신 |
| payload size | 페이로드 크기 |
| tight (bound) | 촘촘한 (한계) |
| tractable | 다루기 쉬운 / 계산 가능한 (문맥) |
| insight | 통찰 |

## D. LaTeX 출력 규칙
- 서문(preamble) 없이 본문 조각만 쓴다. 공통 서식: `derivations/translation/preamble.tex`의 매크로(\E, \P, \Q, \dd, \ff, \gg, \ttl, \iinf, \onote)를 쓸 수 있다.
- 절 제목: `\section{서론}`처럼 번호 없는 명령을 쓰되 원문 번호와 일치하도록 LaTeX 자동 번호에 맡긴다(\section, \subsection, \subsubsection). 원문 2.1은 \subsection, 2.2.1은 \subsubsection.
- 원문의 "1) Converse Bounds:" 같은 단락 머리는 `\paragraph{1) 역 한계}`로.
- 그림은 `\begin{figure}[t]\centering\includegraphics[width=0.85\linewidth]{fig/figN.png}\caption{…}\end{figure}` (N=1..6). 캡션만 번역한다. 그림 번호가 원문과 맞도록 순서를 지킨다.
- 표 1은 LaTeX 표로 다시 만든다(tabularx, multirow).
- 수식은 PDF 페이지 이미지를 직접 보고 옮긴다(pdftotext 추출본은 수식이 깨져 있다). `\begin{equation}…\tag{7}\end{equation}`.
- 각주는 \footnote{} (원문 각주 번호는 LaTeX에 맡김).

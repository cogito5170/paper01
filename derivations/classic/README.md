# classic 문헌 유도 노트

작성: 2026-11-20. papers/classic/ 의 17편을 원문 PDF(텍스트 추출 + 쪽 이미지)와 대조해 유도했다. 표시: [원문] 원문 경로를 따름, [재구성] 원문이 생략했거나 현대식으로 보충함, [미확인] 확인 못 함. 각 파일 7절이 본 연구(정리 A·B, 보조정리 L)와의 연결이다.

## 파일

| 묶음 | 파일 | 유도한 주 결과 |
|---|---|---|
| 무손실 분산 부호화 | [01_Slepian-Wolf1973](01_Slepian-Wolf1973.md) | Thm 2 꼭짓점, 율 영역 (원문은 랜덤 초부호 + Gallager 지수, nats) |
| | [02_Wyner1975](02_Wyner1975.md) | Thm 2.1 ℛ=ℛ*, 역 Thm 3.1, 직접 Thm 4.1 |
| | [03_Ahlswede-Koerner1975](03_Ahlswede-Koerner1975.md) | Thm 1·2 (Fano + 볼록성의 약한 역정리), DBC R1 ≤ t(R2) |
| 손실·부가 정보 | [04_Wyner-Ziv1976](04_Wyner-Ziv1976.md) | Thm 1·2·4, DSBS g*(d), 가우시안 R_WZ = ½log(σ²_{X\|Y}/D) [재구성] |
| | [07_Yamamoto1982](07_Yamamoto1982.md) | Thm 1 R(d)=inf I(Y₂;Ŷ₂\|Y₁) [재구성], Thm 2–6 |
| | [10_Berger-Zhang-Viswanathan1996](10_Berger-Zhang-Viswanathan1996.md) | Thm 1 α(p,W), Prop 1; 부록: 가우시안 CEO 합 율 (후대 문헌, 검증함) |
| 함수 계산·선형 부호 | [05_Koerner-Marton1979](05_Koerner-Marton1979.md) | Thm 1 (3성분 영역), Prop 1, 선형 대 랜덤 비닝 |
| | [08_Han-Kobayashi1987](08_Han-Kobayashi1987.md) | 조건 (3.1)(3.11)(3.13), Thm 1. 모듈로 합은 (3.13)만 위배 |
| | [S1_Wagner2011](S1_Wagner2011.md) | Prop 2 (KP 격자), Thm 1–3. 식 (17)은 ½ 누락 오식 |
| 양자화·디더 | [15_Max1960](15_Max1960.md) | 중점·중심 조건, Panter–Dite 2.72σ²N⁻² |
| | [16_Schuchman1964](16_Schuchman1964.md) | Φ_d(2πm/q)=0 ⇔ 오차 독립 균일 (감산 디더) |
| | [21_Ziv1985](21_Ziv1985.md) | Thm 1, 0.754 = ½log₂(πe/3) |
| | [23_Zamir-Feder1992](23_Zamir-Feder1992.md) | Thm 1 H(Q\|Z)=I(X;Y), Thm 2 C<0.754, Thm 3 ½log 2πeG_K |
| 격자·총설 | [22_Forney1988_CosetCodesI](22_Forney1988_CosetCodesI.md) | 격자 분할, γ_c, 구성 A, 형상 이득 1.53 dB, 합에 닫힘 조건 |
| | [S2_Gray-Neuhoff1998](S2_Gray-Neuhoff1998.md) | Bennett 적분, Panter–Dite, ECSQ 0.2546 bit, Zador/Gersho |
| 기타 | [09_Gallager1988_LIDS-report](09_Gallager1988_LIDS-report.md) | 식 (12) m ≤ [ln ln(N/P*)+A]/ln α + 2 |
| | [29_Tsitsiklis1986](29_Tsitsiklis1986.md) | Thm 3.1 (상수 스텝), Thm 3.2 (감소 스텝), Cor 3.1 |

## 묶음을 가로지르는 결론 (본 연구)

1. **독립 가우시안 합에서 구조적 부호는 이득이 아니라 손해다.** Wagner 2011 (ρ=0, c=1): 비구조 QB가 최적이고 영역은 2^{−2R₁}+2^{−2R₂} ≤ Δ. 합 호환 격자(KP)는 ≤ Δ/2로 인코더당 ½비트를 잃는다. 이것이 K=2의 ½log₂K 대가다. KP는 "합 호환 쪽 달성"(정리 A의 상한 측)으로 위치를 바꾼다.
2. **보조정리 L의 항 H(Z|S,W)는 고전 역정리가 0으로 버리는 항이다.** Wyner·Körner–Marton에서는 출력이 목표의 결정적 함수라 0이다. Hom(ℝ, ℤ_M)={0}이라 본 연구에서는 0이 될 수 없다. 고전 하한(컷셋·지니형)은 원리적으로 이 항을 잡지 못한다.
3. **고해상도 이상화 정정 (Zamir–Feder, Schuchman).** 오차의 독립·균일은 디더에 대해 평균했을 때만 성립한다. W를 조건으로 두면 "합이 고정된 부분 토러스 위 균일"로 고쳐야 하며, 이때 균일 양자화에서 E H(T|S,W) = h(U₁+⋯+U_K) ≥ ½log₂K (EPI, c=0) [재구성, 몬테카를로 확인]. 디더는 작업자별 독립이어야 한다.
4. **정리 B 수정.** H(T|W) ≈ ½log₂(K(1+D̄)/D̄) + 0.254. 고정 레지스터는 복호기의 감김 해제 때문에 log₂M ≈ ½log₂(K/D̄) + log₂(2t/√12). 0.254의 증명된 출처는 Zamir–Feder Thm 3 (K=1), 0.754는 Ziv 1985 Thm 1 (대 ECVQ)과 Zamir–Feder Thm 2 (대 R(D)).
5. **블록 부호.** 상수는 ½log₂(2πeG(Λ_f))로 줄어든다(E₈ 0.146, Λ₂₄ 0.084, d→∞에서 0). 정리 A가 참이면 가장 빡빡한 형태는 c=0일 수 있다(추측).
6. **ℤ_{2^b}의 걸림돌.** Han–Kobayashi Lemma 4–5와 Forney의 선형 라벨링은 체 또는 mod 2에서만 성립한다. 합성수 M에서는 자리올림 때문에 깨진다.

## papers/SURVEY.md 정정 대상

- 01: 기법은 결합 전형성·랜덤 비닝이 아니라 랜덤 초부호 + ML 복호 + Gallager 지수. 단위 nats.
- 03: 역정리는 블로우업이 아니라 Fano + 볼록성(약한 역정리). DBC 결과 누락.
- 05: Thm 1은 3성분 영역. Prop 1 누락. 역정리는 AGK 강한 역정리에 기댐.
- 07: 인코더·부가 정보 역할이 뒤바뀜 (원문: 부호기 Y₂, 복호기 Y₁, I(Y₂;Ŷ₂|Y₁)). Thm 1 증명은 원문에 없음.
- 08: KM을 일반화하는 것은 Lemma 5. 모듈로 합은 (3.13)만 위배.
- 09: 식 (12)의 A는 분자 안.
- 10: Thm 2는 역정리가 아니라 비교환 에이전트 일반화.
- 16: 감산 디더 (SURVEY의 "비감산"은 오류).
- 21: 0.254는 Ziv의 증명 결과가 아님 (Gish–Pierce 인용).
- 22: 형상 이득 1.53 dB는 I부 §I.B에 있음.
- 29: 간격 증가는 B₁n^β 속도까지, 지연은 유계.
- S1: "가우시안 합 + 구조적 부호 이득의 직접 선례"가 아님. "1비트 이내"는 c=1 따름 결과(인코더당 ½비트).

## 원문 오식으로 보이는 곳

Slepian–Wolf "Theorem c = Theorem 2"(c/d 뒤바뀜), Wyner (3.11) log 누락, Wagner (17) ½ 누락, Yamamoto (A5) 분모 2φ → 2(1−φ), Gallager 6쪽 ε^(−Nm) → ε^(Nm)과 식 (22) n → N, Gray–Neuhoff (14) −log Δ → −k log Δ, Schuchman III절 y = n+x+d.

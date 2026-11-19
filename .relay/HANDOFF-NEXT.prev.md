STATUS: CONTINUE
META: 2026-11-19 16:00 · main@8c1df16 · uncommitted 7 files
## Done
- 인터뷰 Q9~Q25 기록. 안정성 문헌 7편과 Zhou 2022 수집, Tao 정독.
- 논문 11편의 해법을 다섯 갈래로 정리 (Q21).
- 스칼라 A-3 전개: R ≥ I(S;Z|W) + H(Z|S,W). 찌꺼기 항을 정확히 계산 (sims/hzs_exact.py).
- 해설 페이지: https://claude.ai/code/artifact/4e50c491-4173-4186-9549-fa6e8195ba7d (원본은 scratchpad의 overflow.html).
- 논문 초안 v0: draft.md.
## Decisions
- 소스 모델: 독립 가우시안이 기본, 다음이 상관 가우시안 X_k = U + N_k, 두꺼운 꼬리는 3단계 (사용자 결정, Q16·Q17).
- 목표는 발견(D1~D3)이고, 한계 정리는 그것을 담는 형식 (Q14).
- A-3은 보조정리 L, 즉 찌꺼기 H(Z|S,W) ≥ ½log₂K − c와 동치.
- 잠정 결정 (사용자 확인 대기): 주 정리는 스칼라 단발 부호, 율은 상행·하행으로 나누고 대가는 하행에 붙음, 기호는 K로 통일.
- Zamir–Shamai–Erez 인용 오류를 바로잡음. 해당 제목은 실제로 Krithivasan–Pradhan의 논문.
## Next
1. 사용자에게 확인받기: draft.md의 잠정 결정 1~4, 제안서 §4.2에 K = 2 달성 추가, 커밋 여부.
2. 확인되면 SPEC과 proposal의 기호·모델을 개정.
3. 보조정리 L의 5b(짝 하나의 흔들림 c₀) 증명 착수.
4. 율-K 비교 시뮬레이션 (draft.md 4.2).
5. 신규성 2차 점검: 격자·compute-and-forward·보안 집계 문헌.
## Files
- draft.md:1-139
- interview.md:787-926
- interview.md:339-679
- sims/hzs_exact.py:1-15
- proposal.md:47-60
- SPEC.md:59-80

STATUS: CONTINUE
META: 2026-11-19 18:15 · main@4edc56a · uncommitted 2 files
## Done
- 문헌 70편(classic 17, modern 53)을 sonnet 에이전트 6개로 조사해 papers/SURVEY.md 로 합침. 맨 앞 "0. 종합"에 묶음별 역할, 관점별 정리, 신규성 판단, 미확인 목록이 있음.
- Krithivasan–Pradhan Thm 3.1(식 19)을 원문으로 확인: 대칭이면 R ≥ ½log₂(2/D̄), 가설 A-3의 N=2 꼴. 달성만 있고 하한·N>2·군 덧셈 제약은 없음.
- 커밋 4edc56a: 저장소가 PUBLIC이라 PDF는 .gitignore로 빼고 문서·sims·.relay만 커밋. push 안 함.
## Decisions
- 공개 저장소이므로 PDF는 커밋하지 않고 DOI(papers/README.md)만 둔다 (사용자 지시).
- ①~④ 확정과 §4.2 추가는 아직 답을 받지 못함.
## Next
1. ①~④(스칼라 단발, 단일 라운드, 상행·하행 율 분리, 기호 K) 확정 여부와 §4.2 추가 여부를 묻는다.
2. 확정되면 SPEC·proposal을 개정하고, 관련 연구에 Krithivasan–Pradhan, Chen2022 Cor 5.4, Chen2023, Wagner 2011 비교를 넣어 커밋한다.
3. push 여부를 묻는다. interview.md와 .relay/가 공개돼도 되는지 확인을 받는다.
4. papers/README.md에서 #02 Wyner와 #16 Schuchman이 "기관 구독 필요"로 남아 있음. 실제 PDF가 있으니 고칠지 묻는다.
5. 보조정리 L의 5b 증명(SURVEY 0.2-3: (ℤ_{2^b})^d에서 부분군 균등 문제), 율-K 시뮬레이션, 신규성 2차 점검.
## Files
- papers/SURVEY.md:1-75
- proposal.md:47-60
- SPEC.md:59-80
- draft.md:1-139
- papers/README.md:1-110

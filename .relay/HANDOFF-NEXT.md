STATUS: CONTINUE
META: 2026-11-25 03:19 · main@5a2ca0a · uncommitted 22 files
## Done
- v3 초록 검토, 문서 2 보상식 원문 확인(선택 수↑ → 보상↑), 질문방 (9) 검토 메모 추가.
- 번역: COMST 2026 서베이(78쪽), Enttsel–Corlay 2602.12866(15쪽, CC BY).
- 세그먼트 SOTA 지도 + papers/segment/ 30편.
- 질문방-2026-11-25 (2) 결론 정리(채팅), 반박 모드 토론으로 연구 주제 좁힘.
## Decisions
- 주제 2(연판정 V)는 분류에서 이득 수 비트 → 대규모 K 과업에서만 의미.
- "같은 예산 E&C > 분할"은 문서 7의 주장(미검증) → 아이디어 아닌 검증 기여.
- 독창 후보: 제한된 부호기 집합(분할·조각 선택) 아래 모델 인지 RD 한계; 제약 없으면 [11] 분할 불변성으로 층별 한계가 TMRD와 같아짐.
- 구조안: 전단+조기 종료 헤드, T·τ는 오프라인 보정 후 송신기 저장, 불확실 입력만 특징 전송; 온라인 루프는 측정 가능한 양(ACK, 불확실 비율, FLOPs)만 제어.
- 사용자 요청 "반박 모드"는 사용자가 그만이라 할 때까지 유지 중.
## Next
1. 사용자에게 반박 모드 지속 여부 확인 후 토론 이어 가기.
2. 검색: 물리 계층(FBL·페이딩·JSCC) 고려 분할 지점 선택 선행 연구 유무.
3. 확인: [11] 분할 불변성 증명이 H(Y|X)=0에 기대는지; [36] Table 4(INT8/INT4 정확도).
4. 제안 대기: 결론을 질문방 파일/v4 초록에 기록, 번역 폴더 커밋, Doppler PDF(사용자 제공 대기).
## Files
- idea/질문방-2026-11-25 (2).md:1-1888
- idea/abstract_v3_IB_patch_selection.md:1-93
- derivations/translation_enttsel2026/body.tex:1-300
- derivations/translation_seon2025_tccn/part_C.tex:1-170
- papers/SEGMENT_SOTA_2026-11-24.md:1-63

STATUS: CONTINUE
META: 2026-11-24 20:01 · main@5a2ca0a · uncommitted 15 files
## Done
- 경로 2(시스템·알고리즘 논문) 선택. 오류율 기반 통신 기술 10종 서베이 + #4 데이터센터 FEC, #8 QKD 정보 조정 심층 → papers/TO_DOWNLOAD.md 우선순위 D.
- IB 논문 4편 확보(papers/modern/, README 갱신). Tishby 2015 번역본.
- 전역 스킬 ko-paper-translate 제작(/slash 가능, 용어집 2개, crop_fig.sh, check_translation.py, eval 3건: skill 100% vs 기준 77.8%).
- 김진영 교수(광운대) 최근 논문 조사. Seon 외 레터(LCOMM 2024, 9쪽)·저널(TCCN 2025, 27쪽) 전문 번역, 검사기 경고 0.
- main pull(5a2ca0a): idea/ IB 패치 선택 초록 v2·v3, 질문방 기록 4개 추가.
## Decisions
- 비CC 번역본은 .gitignore로 커밋 차단. 이유: 공개 저장소.
- 용어 통일: 행위자/비평자, 리턴, 하이퍼파라미터. 이유: 두 논문 일관성.
## Next
1. idea/abstract_v3_IB_patch_selection.md 검토(새로 들어온 연구 방향).
2. 선택: 두 Seon 논문 원천 부호화 부분을 문제 P·IB와 비교 정리.
3. 스킬 개선 대기: 벡터 그림 자르기, 최종 보고 대화체. eval viewer(포트 3117) 피드백 미수령.
4. 미응답 제안: 합 호환 디더 양자화 시뮬레이션, TCCN/LCOMM/JSAC 2025 논문 TO_DOWNLOAD 추가.
5. 이전 Next(후보 B 결정, O1·O2, C₀ 대조) 여전히 대기. 커밋 여부 사용자 확인.
## Files
- papers/TO_DOWNLOAD.md:1-400
- derivations/translation_seon2024_lcomm/ko.tex:1-400
- derivations/translation_seon2025_tccn/ko.tex:1-38
- idea/abstract_v3_IB_patch_selection.md:1-93
- SPEC.md:1-120

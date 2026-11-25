# 조각 번역 지시 (공통)
원문: src/orig.pdf (IEEE COMST 2026 "Agentic Semantic Communication: Concepts, Architectures, and Visions", 37쪽, 2단 조판, CC BY 4.0 저자판). 추출 텍스트: src/orig.txt (pdftotext -layout, 2단이 섞여 있으니 문장 순서는 쪽 이미지로 확인).
출력 폴더: /Users/cogito/paper01/paper01/derivations/translation_seon2026_comst

## 반드시 먼저 읽을 것
1. /Users/cogito/.claude/skills/ko-paper-translate/SKILL.md (문체·표기 규칙 전부 따른다. 5절 "문체", "표기")
2. 용어집 두 개: /Users/cogito/.claude/skills/ko-paper-translate/references/glossary-information-theory.md, glossary-machine-learning.md
3. TERMS.md (이 폴더). 용어집 > TERMS.md 순으로 우선. 목록에 없는 새 용어를 정했으면 최종 보고에 "새 용어" 목록으로 적는다(TERMS.md는 고치지 않는다).

## 규칙
- 맡은 범위만 번역해 자기 part_X.tex 하나에 쓴다. 다른 파일(ko.tex, preamble.tex, TERMS.md, 다른 part)은 고치지 않는다. 필요한 패키지·매크로가 있으면 보고에 적는다. ko.tex에 이미 longtable, makecell, pdflscape, booktabs, tabularx, multirow가 있다.
- 내용을 빼거나 더하지 않는다. 요약 금지. 모든 문단·각주·표 칸을 옮긴다.
- 절 명령: \section{서론} 처럼 \section, \subsection, \subsubsection 사용(번호는 ko.tex가 I / A / 1) 로 만든다). 원문 단락 머리 "1) Xxx:"가 문단 머리글이면 \paragraph{1) 한국어} 로 쓴다. 원문 절 번호와 개수가 맞아야 한다.
- 인용은 원문처럼 일반 텍스트 [12], [3]--[5] 로 쓴다(\cite 쓰지 않음).
- 약어·전문 용어 괄호는 자기 조각에서 처음 나올 때 단다(합칠 때 메인이 정리한다).
- 그림: 원문 번호대로 fig/figN.png. 자르기:
  bash /Users/cogito/.claude/skills/ko-paper-translate/scripts/crop_fig.sh src/orig.pdf <쪽> <x> <y> <폭> <높이> fig/figN   (200 dpi 픽셀 좌표)
  쪽 이미지는 pdftoppm -r 200 -f p -l p -png src/orig.pdf /tmp 대신 이 폴더의 src/pages/ 에 만들어 Read로 본다. 자른 결과를 반드시 Read로 열어 캡션·옆 단 글자가 안 들어갔는지 확인하고 고친다. 캡션은 번역해 \caption{}에. \begin{figure}[htbp] … \label{fig:N}. 큰 그림은 width=\linewidth.
- 그림 번호 강제: 원문 번호와 맞도록 각 그림 앞에 \setcounter{figure}{N-1} 을 둔다. 표도 \setcounter{table}{N-1} (표 번호는 로마 숫자로 출력됨).
- 표: 이미지가 아니라 LaTeX로 다시 만든다. 길거나 넓은 표는 longtable 또는 \small/\footnotesize + tabularx(\linewidth). 칸 내용도 번역한다(논문 제목·고유명사·기법 이름·인용 번호는 그대로). 체크 표시 등 기호는 원문대로(✓는 $\checkmark$).
- 수식 있으면 쪽 이미지를 보고 옮기고 원문 번호는 \tag{n}.
- 원문 오류는 본문 그대로 옮기고 \onote{…}로 지적(꼭 필요할 때만).
- 끝나면 이 폴더에서 아래로 자기 조각만 단독 컴파일 검사:
  mkdir -p src/test && 와 같은 방식으로 src/test_X.tex 를 만들어( ko.tex 머리말 복사 + \input{../part_X.tex} 대신 경로 주의: 이 폴더에 test_X.tex 를 만들고 \input{part_X.tex}) tectonic test_X.tex 로 오류 없이 컴파일되는지 확인한 뒤 test_X.* 파일은 지운다. 
  python3 /Users/cogito/.claude/skills/ko-paper-translate/scripts/check_translation.py part_X.tex 경고를 판단해 고친다.
- 최종 보고(짧게): 옮긴 절·그림·표·각주 개수, 옮긴이 주 목록, 새 용어, 남은 문제.

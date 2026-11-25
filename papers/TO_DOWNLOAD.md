# 직접 받아야 할 문헌 (IEEE Xplore 등 유료, 무료 원문 없음)

작성: 2026-11-18. 받은 PDF는 `papers/classic/` 에 `<번호>_<저자><연도>.pdf` 로 넣으면 된다. 번호는 SPEC.md 11장 번호.

## 받음 (2026-11-18)
| 파일 | 서지 |
|---|---|
| classic/02_Wyner1975.pdf | A. D. Wyner, "On source coding with side information at the decoder," IEEE Trans. Inf. Theory, vol. IT-21, no. 3, pp. 294–300, May 1975 |
| classic/16_Schuchman1964.pdf | L. Schuchman, "Dither signals and their effect on quantization noise," IEEE Trans. Commun. Technol., vol. COM-12, no. 4, pp. 162–165, Dec. 1964 |
| classic/S1_Wagner2011.pdf | A. B. Wagner, "On distributed compression of linear functions," IEEE Trans. Inf. Theory, vol. 57, no. 1, pp. 79–94, Jan. 2011 (처음부터 있었음. 목록에 잘못 올렸던 항목) |

## 우선순위 A — 제안서·핵심 정리의 직접 근거
(현재 없음. 2026-11-22에 아래 다섯 편을 받음)

| 파일 | 서지 |
|---|---|
| classic/S3_Oohama1998.pdf | Y. Oohama, "The rate-distortion function for the quadratic Gaussian CEO problem," IEEE TIT 44(3), pp. 1057–1070, 1998, DOI 10.1109/18.669162 (14쪽) **주 레퍼런스** |
| classic/S4_PrabhakaranTseRamchandran2004.pdf | V. Prabhakaran, D. Tse, K. Ramchandran, "Rate region of the quadratic Gaussian CEO problem," ISIT 2004, p. 117, DOI 10.1109/ISIT.2004.1365154 (1쪽 요약, 증명 없음) |
| classic/S5_ViswanathanBerger1997.pdf | H. Viswanathan, T. Berger, "The quadratic Gaussian CEO problem," IEEE TIT 43(5), pp. 1549–1559, 1997, DOI 10.1109/18.623151 (11쪽) |
| classic/S6_Oohama2005.pdf | Y. Oohama, "Rate-distortion theory for Gaussian multiterminal source coding systems with several side informations at the decoder," IEEE TIT 51(7), pp. 2577–2593, 2005, DOI 10.1109/TIT.2005.850110 (17쪽) |
| classic/S7_AhlswedeHan1983.pdf | R. Ahlswede, T. S. Han, "On source coding with side information via a multiple-access channel and related problems in multi-user information theory," IEEE TIT 29(3), pp. 396–412, 1983, DOI 10.1109/TIT.1983.1056669 (17쪽) |

PTR 2004는 1쪽 요약이다. 율 영역 증명이 필요하면 Prabhakaran 박사논문(UC Berkeley)이나 후속 저널판을 따로 찾는다 (미확인).

## 우선순위 B — 학위논문 다른 장(시간 상관·오차 피드백·간접 율-왜곡)의 근거
| SPEC # | 서지 |
|---|---|
| 24 | P. Elias, "Predictive coding—Part I, II," IRE Trans. Inf. Theory, vol. 1, no. 1, pp. 16–33, 1955 |
| 25 | H. Inose, Y. Yasuda, J. Murakami, "A telemetering system by code modulation—Δ-Σ modulation," IRE Trans. Space Electron. Telem., vol. 8, pp. 204–209, 1962 |
| 26 | H. A. Spang & P. M. Schultheiss, "Reduction of quantizing noise by use of feedback," IRE Trans. Commun. Syst., vol. 10, no. 4, pp. 373–380, 1962 ⚠ 서지 미확인 |
| 28 | R. M. Gray, "Oversampled sigma-delta modulation," IEEE Trans. Commun., vol. 35, no. 5, pp. 481–489, 1987 ⚠ |
| 11 | R. L. Dobrushin & B. S. Tsybakov, "Information transmission with additional noise," IRE Trans. Inf. Theory, vol. 8, no. 5, pp. 293–304, 1962 ⚠ |
| 12 | J. K. Wolf & J. Ziv, "Transmission of noisy information to a noisy receiver with minimum distortion," IEEE Trans. Inf. Theory, vol. 16, no. 4, pp. 406–411, 1970 |
| 13 | J. Ziv & M. Zakai, "On functionals satisfying a data-processing theorem," IEEE Trans. Inf. Theory, vol. 19, no. 3, pp. 275–283, 1973 |
| 14 | H. S. Witsenhausen, "Indirect rate distortion problems," IEEE Trans. Inf. Theory, vol. 26, no. 5, pp. 518–521, 1980 |

## 우선순위 C — 배경 (양자화 일반, 기타)
| SPEC # | 서지 |
|---|---|
| 6 | T. M. Cover, A. El Gamal, M. Salehi, "Multiple access channels with arbitrarily correlated sources," IEEE Trans. Inf. Theory, vol. 26, no. 6, pp. 648–657, 1980 |
| 17 | H. Gish & J. N. Pierce, "Asymptotically efficient quantizing," IEEE Trans. Inf. Theory, vol. 14, no. 5, pp. 676–683, 1968 ⚠ |
| 18 | A. Gersho, "Asymptotically optimal block quantization," IEEE Trans. Inf. Theory, vol. 25, no. 4, pp. 373–380, 1979 ⚠ |
| 19 | S. P. Lloyd, "Least squares quantization in PCM," IEEE Trans. Inf. Theory, vol. 28, no. 2, pp. 129–137, 1982 |
| 20 | J. H. Conway & N. J. A. Sloane, "Fast quantizing and decoding algorithms for lattice quantizers and codes," IEEE Trans. Inf. Theory, vol. 28, no. 2, pp. 227–232, 1982 |
| 27 | N. S. Jayant, "Digital coding of speech waveforms: PCM, DPCM, and DM quantizers," Proc. IEEE, vol. 62, no. 5, pp. 611–632, 1974 |
| 30 | H. Harashima & H. Miyakawa, "Matched-transmission technique for channels with intersymbol interference," IEEE Trans. Commun., vol. 20, no. 4, pp. 774–780, 1972 |

⚠ = SPEC 11장에서 서지(쪽수·권호) 확신이 낮다고 표시된 항목. 받을 때 IEEE Xplore 서지로 SPEC을 고친다.

## 우선순위 D — 오류율 기반 통신 기술 서베이 (2026-11-24 웹 검색)
목적: 2장(원천 부호화)·3장(통신로 부호화)의 유한 블록 길이 이론이 실제로 쓰이는 분야 탐색. 서지는 검색 결과 기준이며 원문 대조 전이다. ★ = IEEE 게재.

### 10개 분야 대표 서베이
| # | 분야 | 서지 | 비고 |
|---|---|---|---|
| 1 | Wi-Fi 링크 적응 | ★ S. Szott 외, "Wi-Fi Meets ML: A Survey on Improving IEEE 802.11 Performance with Machine Learning," IEEE COMST 24, 2022, arXiv 2109.04786 | Wi-Fi 전용 최신판 없음 |
| 2 | 심우주 통신 | ★ S. Karmous 외, "How Can Optical Communications Shape the Future of Deep Space Communications? A Survey," IEEE COMST 27(1), pp. 725–747, 2025, DOI 10.1109/COMST.2024.3403873, arXiv 2212.04933 | |
| 2 | 심우주 통신 | "A History of Channel Coding in Aeronautical Mobile Telemetry and Deep-Space Telemetry," Entropy 26(8):694, 2024 | 보조 |
| 3 | 위성 (DVB-S2X) | Sharma 외, "A comprehensive systematic literature review on AI for error correction and modulation schemes in next-generation satellite communications," Artif. Intell. Rev. 58:321, 2025 | IEEE 아님 |
| 5 | GPU·칩 간 연결 | "Survey of Intra-Node GPU Interconnection in Scale-Up Network," Future Internet 17(12):537, 2025 | IEEE 아님. NVLink·UALink·PCIe FEC 비교표 |
| 5 | 칩 간 연결 | "An Introduction to the Universal Chiplet Interconnect Express (UCIe)," ACM, DOI 10.1145/3819235 | 보조 |
| 6 | NAND SSD | "Error correction and mitigation techniques in SSDs: A survey," Comput. Electr. Eng., 2026 (S0045790626005033) | IEEE 아님 |
| 6 | NAND SSD | "Device-Level Optimization Techniques for Solid-State Drives: A Survey," arXiv 2507.10573, 2025 | 보조 |
| 7 | LoRa / LPWAN | "A Comprehensive Survey of Data-Driven Solutions for LoRaWAN," ACM TIOT 6(1), 2025, DOI 10.1145/3711953 | IEEE 아님. ★ 고전: Sundaram–Du–Zhao, IEEE COMST 22(1), 2020 |
| 9 | 분수 부호 (RaptorQ) | ★ N. Bonello, S. Chen, L. Hanzo, "Low-Density Parity-Check Codes and Their Rateless Relatives," IEEE COMST 13(1), pp. 3–26, 2011, DOI 10.1109/SURV.2011.040410.00042 | 최신판 없음 |
| 10 | 차량 내 통신 (CAN) | "Vehicular Intrusion Detection System for CAN: A Comprehensive Survey and Evaluation," arXiv 2505.17274, 2025 | 보안 중심. 오류 검출 서베이 없음 |

### 4번 심층: 데이터센터 이더넷·광 연결 FEC
IEEE 기준 FEC 전용 서베이는 찾지 못했다. 아래가 가장 가까운 자료다.
| 종류 | 서지 | 비고 |
|---|---|---|
| ★ 요구 사항 분석 | "Forward Error Correction Requirements for Data Center Connectivity," IEEE, 2025, ieeexplore 10982726 | 저자·게재처 미확인. 연결용 FEC 사양 도출, BCH(255,207) 16nm 구현. **가장 가까운 1순위** |
| ★ 리뷰 | X. Zhou 외, "State-of-the-Art 800G/1.6T Datacom Interconnects and Outlook for 3.2T," OFC 2023, ieeexplore 10117322 | 200G/레인 IM-DD 전반 |
| ★ 리뷰 | "Modulation Format and DSP for IM-DD Optics at Post-200G Era," IEEE, ieeexplore 10238466 | 변조·DSP 중심 |
| ★ 리뷰 | X. Zhou, R. Urata, H. Liu, "Beyond 1 Tb/s Intra-Data Center Interconnect Technology: IM-DD or Coherent?," JLT 38(2), 2020 | 배경 |
| ★ 튜토리얼 | A. Leven, L. Schmalen, "Status and Recent Advances on FEC Technologies for Lightwave Systems," JLT 32(16), pp. 2735–2750, 2014 | 고전 |
| ★ 서베이 | C. Kachris, I. Tomkos, "A Survey on Optical Interconnects for Data Centers," IEEE COMST 14(4), pp. 1021–1036, 2012 | FEC는 다루지 않음 |
| ★ 비교 | "Real-Time FPGA Investigation of Potential FEC Schemes for 800G-ZR/ZR+," JLT, ieeexplore 9935118 | 코히런트 DCI |
| 연구 | "Concatenated FEC with KP4 and Single Parity Check Codes," arXiv 2212.10523 | BER < 10⁻¹³, 지연 < 100 ns 조건 명시 |
| 표준 기고 | IEEE 802.3df/dj: farhood_3df_01_2211 (FEC 구조 개관), farhood_3df_02b_2211 (연접 SFEC), he_3dj_logic_01_230615 (FEC_I, 길쌈 인터리버) | 내부 부호 Hamming(128,120) + 외부 KP4 RS(544,514) 채택, 지연 약 110 ns |
| 산업 | Liu, "200+ Gbps Ethernet FEC Analysis," DesignCon 2024 | Type-1/2 연접, 연판정 Hamming |

### 8번 심층: QKD 정보 조정 (Slepian–Wolf)
IEEE 기준 정보 조정 전용 서베이는 찾지 못했다.
| 종류 | 서지 | 비고 |
|---|---|---|
| ★ 서베이 | Y. Cao, Y. Zhao, Q. Wang, J. Zhang, S. X. Ng, L. Hanzo, "The Evolution of QKD Networks: On the Road to the Qinternet," IEEE COMST 24(2), pp. 839–894, 2022, DOI 10.1109/COMST.2022.3144219 | QKD 망 전반 |
| ★ 서베이 | Lauterbach 외, "Quantum Cryptography in 5G Networks: A Comprehensive Overview," IEEE COMST 26(1), pp. 302–346, 2024 | QKD·PQC 통합 |
| ★ 서베이 | "Quantum key distribution secured optical networks: a survey," IEEE OJ-COMS | 연도 미확인 |
| 리뷰 | L. Martial, A. Rosio, E. Diamanti, A. Cassagne, B. Gouraud, "Multidimensional Reconciliation in CV-QKD: Review, Coding Schemes, and Open-Source Simulation," arXiv 2606.02323, 2026 | **정보 조정 전용 리뷰. 1순위.** BIAWGN 가상 채널 변환 |
| 리뷰 | "QKD: Bridging Theoretical Security Proofs, Practical Attacks, and Error Correction," arXiv 2511.20602, 2025 | |
| 리뷰 | "A Survey of Continuous Variable QKD in Quantum Communication," ResearchGate 395554660 | 게재처 미확인 (IEEE Access 추정) |
| 비교 | "Performance of Cascade and LDPC-codes for Information Reconciliation on Industrial QKD Systems," arXiv 2408.15758, 2024 | DV-QKD |
| 짧은 블록 | Gümüş 외, arXiv 2409.13667 (2024), arXiv 2507.03529 (ECOC 2025) | 1000비트 부호로 140 km에서 키율 최대 7.3배 |
| 유한 키 기초 | A. Leverrier 외, "Finite-size analysis of CV-QKD," Phys. Rev. A 81, 2010, arXiv 1005.0339 | 유한 블록 길이와 직결 |
| 유한 키 기초 | M. Tomamichel 외, "Tight finite-key analysis for quantum cryptography," Nat. Commun., 2012 | ⚠ 서지 기억 기반 |
| 리뷰 | F. Xu 외, "Secure quantum key distribution with realistic devices," Rev. Mod. Phys. 92, 2020 | ⚠ 서지 기억 기반 |

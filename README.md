# 📖 한글 설교 도서관 (Korean Sermon Library)

> **은혜로운 설교를 언제 어디서든** — Streamlit 기반 한글 설교 디지털 도서관

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io)

---

## 📚 소개

한글 설교 도서관은 위대한 설교자들의 설교를 한국어로 읽고 탐색할 수 있는 웹 애플리케이션입니다.

### 현재 수록
- **C. H. 스펄전** (C. H. Spurgeon) — 약 1,280편
  - 뉴 파크 스트리트 강단 (The New Park Street Pulpit)
  - 메트로폴리탄 태버내클 강단 (The Metropolitan Tabernacle Pulpit)

---

## 🚀 실행 방법

### 로컬 실행
```bash
# 의존성 설치
pip install -r requirements.txt

# 인덱스 빌드 (최초 1회)
python build_index.py

# 앱 실행
streamlit run app.py
```

### Streamlit Cloud 배포
1. 이 리포지토리를 GitHub에 push
2. [share.streamlit.io](https://share.streamlit.io) 에서 리포지토리 연결
3. Main file path: `app.py`

---

## 📁 프로젝트 구조

```
sermon-library/
├── app.py                # Streamlit 메인 앱
├── build_index.py        # 인덱스 빌더 스크립트
├── requirements.txt      # Python 패키지 의존성
├── .streamlit/
│   └── config.toml       # Streamlit 테마 설정
├── utils/
│   ├── __init__.py
│   ├── data_loader.py    # MD 파일 파싱 모듈
│   └── search.py         # 검색 기능 모듈
├── sermons/              # 설교 데이터
│   ├── index.json        # 메타데이터 인덱스
│   └── spurgeon/         # 스펄전 설교 MD 파일
├── README.md
└── .gitignore
```

---

## ➕ 새 목사님 설교 추가

1. `sermons/` 아래에 새 폴더 생성 (예: `sermons/lloyd-jones/`)
2. 한글 번역 마크다운 파일 배치
3. `python build_index.py` 실행
4. 앱이 자동으로 새 설교를 인식합니다

---

## 🙏 감사의 글

*"말씀이 육신이 되어 우리 가운데 거하시매" — 요한복음 1:14*

Soli Deo Gloria — 오직 하나님께만 영광을

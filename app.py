"""
📖 한글 설교 도서관 (Korean Sermon Library)
Streamlit 기반 설교 열람 웹 애플리케이션

스펄전 설교를 비롯한 한글 번역 설교를 탐색하고 읽을 수 있는
프리미엄 디지털 도서관입니다.
"""

import streamlit as st
import json
import os
from pathlib import Path

# ─── 페이지 설정 ──────────────────────────────────────────────
st.set_page_config(
    page_title="📖 한글 설교 도서관",
    page_icon="📖",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── 커스텀 CSS ───────────────────────────────────────────────
st.markdown("""
<style>
    /* Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Noto+Serif+KR:wght@400;700&family=Noto+Sans+KR:wght@300;400;500;700&display=swap');

    /* 전역 스타일 */
    .stApp {
        font-family: 'Noto Sans KR', sans-serif;
    }

    /* 헤더 영역 */
    .main-header {
        text-align: center;
        padding: 1.5rem 0 1rem 0;
        border-bottom: 1px solid rgba(201, 164, 76, 0.2);
        margin-bottom: 2rem;
    }
    .main-header h1 {
        font-family: 'Noto Serif KR', serif;
        color: #c9a44c;
        font-size: 2.2rem;
        margin-bottom: 0.3rem;
        letter-spacing: 2px;
    }
    .main-header p {
        color: #8b949e;
        font-size: 0.95rem;
    }

    /* 통계 카드 */
    .stat-card {
        background: linear-gradient(135deg, #1c2333 0%, #161b22 100%);
        border: 1px solid #30363d;
        border-radius: 16px;
        padding: 1.5rem;
        text-align: center;
        transition: all 0.3s ease;
    }
    .stat-card:hover {
        border-color: #c9a44c;
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(201, 164, 76, 0.1);
    }
    .stat-number {
        font-size: 2.5rem;
        font-weight: 700;
        color: #c9a44c;
        line-height: 1.2;
    }
    .stat-label {
        color: #8b949e;
        font-size: 0.9rem;
        margin-top: 0.3rem;
    }

    /* 설교 카드 */
    .sermon-card {
        background: linear-gradient(135deg, #1c2333 0%, #161b22 100%);
        border: 1px solid #30363d;
        border-radius: 12px;
        padding: 1.2rem 1.5rem;
        margin-bottom: 0.8rem;
        transition: all 0.3s ease;
        cursor: pointer;
    }
    .sermon-card:hover {
        border-color: #c9a44c;
        box-shadow: 0 4px 15px rgba(201, 164, 76, 0.12);
    }
    .sermon-no {
        display: inline-block;
        background: rgba(201, 164, 76, 0.15);
        color: #c9a44c;
        padding: 0.15rem 0.6rem;
        border-radius: 6px;
        font-size: 0.8rem;
        font-weight: 600;
        margin-bottom: 0.5rem;
    }
    .sermon-title {
        color: #e6e1d8;
        font-size: 1.15rem;
        font-weight: 600;
        font-family: 'Noto Serif KR', serif;
        margin-bottom: 0.4rem;
        line-height: 1.5;
    }
    .sermon-meta {
        color: #8b949e;
        font-size: 0.82rem;
        line-height: 1.6;
    }
    .sermon-meta span {
        margin-right: 1rem;
    }
    .sermon-preview {
        color: #6e7681;
        font-size: 0.85rem;
        margin-top: 0.5rem;
        line-height: 1.5;
        border-left: 2px solid rgba(201, 164, 76, 0.3);
        padding-left: 0.8rem;
    }

    /* 읽기 뷰 */
    .reader-header {
        text-align: center;
        padding: 2rem 0;
        border-bottom: 2px solid rgba(201, 164, 76, 0.2);
        margin-bottom: 2rem;
    }
    .reader-header h1 {
        font-family: 'Noto Serif KR', serif;
        color: #e6e1d8;
        font-size: 1.8rem;
        line-height: 1.4;
    }
    .reader-meta {
        color: #8b949e;
        font-size: 0.9rem;
        margin-top: 0.8rem;
    }
    .reader-content {
        font-family: 'Noto Serif KR', serif;
        line-height: 2;
        color: #d4cfc6;
        font-size: 1.05rem;
        max-width: 800px;
        margin: 0 auto;
    }

    /* 사이드바 */
    [data-testid="stSidebar"] {
        background: #0d1117;
        border-right: 1px solid #21262d;
    }
    [data-testid="stSidebar"] .stRadio > label {
        font-family: 'Noto Sans KR', sans-serif;
    }

    /* 검색 결과 하이라이트 */
    .search-highlight {
        background: rgba(201, 164, 76, 0.2);
        padding: 0.1rem 0.3rem;
        border-radius: 3px;
        color: #e8c86e;
    }

    /* 구분선 */
    .gold-divider {
        height: 1px;
        background: linear-gradient(90deg, transparent, #c9a44c, transparent);
        margin: 1.5rem 0;
        border: none;
    }

    /* 페이지 하단 */
    .footer {
        text-align: center;
        color: #484f58;
        font-size: 0.8rem;
        padding: 2rem 0 1rem 0;
        border-top: 1px solid #21262d;
        margin-top: 3rem;
    }

    /* 버튼 스타일 */
    .stButton > button {
        border: 1px solid #30363d;
        border-radius: 8px;
        transition: all 0.3s ease;
    }
    .stButton > button:hover {
        border-color: #c9a44c;
        color: #c9a44c;
    }

    /* pastor info card */
    .pastor-card {
        background: linear-gradient(135deg, #1a1f2e 0%, #151921 100%);
        border: 1px solid #30363d;
        border-left: 4px solid #c9a44c;
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1rem;
    }
    .pastor-name {
        font-family: 'Noto Serif KR', serif;
        font-size: 1.3rem;
        color: #c9a44c;
        margin-bottom: 0.3rem;
    }
    .pastor-desc {
        color: #8b949e;
        font-size: 0.9rem;
    }

    /* 네비게이션 버튼 */
    .nav-btn {
        display: inline-block;
        background: rgba(201, 164, 76, 0.1);
        border: 1px solid rgba(201, 164, 76, 0.3);
        border-radius: 8px;
        padding: 0.4rem 1rem;
        color: #c9a44c;
        text-decoration: none;
        font-size: 0.9rem;
        transition: all 0.2s ease;
    }
    .nav-btn:hover {
        background: rgba(201, 164, 76, 0.2);
        border-color: #c9a44c;
    }

    /* hide default streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)


# ─── 데이터 로딩 ──────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SERMONS_DIR = os.path.join(BASE_DIR, "sermons", "spurgeon")
INDEX_PATH = os.path.join(BASE_DIR, "sermons", "index.json")


@st.cache_data(ttl=3600)
def load_index():
    """인덱스 파일 로딩 (캐시)"""
    if not os.path.exists(INDEX_PATH):
        return None
    with open(INDEX_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)


def load_sermon_content(file_name):
    """개별 설교 파일 로딩"""
    filepath = os.path.join(SERMONS_DIR, file_name)
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    return None


# ─── 초기 상태 ────────────────────────────────────────────────
if "selected_sermon" not in st.session_state:
    st.session_state.selected_sermon = None
if "page" not in st.session_state:
    st.session_state.page = "📊 대시보드"


def navigate_to_sermon(sermon_id):
    """설교 읽기 페이지로 이동"""
    st.session_state.selected_sermon = sermon_id
    st.session_state.page = "📖 설교 읽기"


# ─── 사이드바 ─────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="text-align:center; padding: 1rem 0;">
        <div style="font-size: 2.5rem;">📖</div>
        <div style="font-family: 'Noto Serif KR', serif; color: #c9a44c; 
                    font-size: 1.2rem; font-weight: 700; letter-spacing: 1px;">
            한글 설교 도서관
        </div>
        <div style="color: #6e7681; font-size: 0.75rem; margin-top: 0.3rem;">
            Korean Sermon Library
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="gold-divider"></div>', unsafe_allow_html=True)

    pages = ["📊 대시보드", "📚 설교 탐색", "📖 설교 읽기", "🔍 검색", "ℹ️ 소개"]
    selected_page = st.radio(
        "메뉴",
        pages,
        index=pages.index(st.session_state.page) if st.session_state.page in pages else 0,
        label_visibility="collapsed",
    )
    st.session_state.page = selected_page

    st.markdown('<div class="gold-divider"></div>', unsafe_allow_html=True)

    # 인덱스 정보
    index_data = load_index()
    if index_data:
        meta = index_data.get("metadata", {})
        st.markdown(f"""
        <div style="color: #6e7681; font-size: 0.8rem; padding: 0.5rem 0;">
            📄 총 {meta.get('total_sermons', 0):,}편 설교<br>
            📁 {meta.get('volumes', 0)}개 볼륨<br>
            🔄 {meta.get('last_updated', '알 수 없음')} 업데이트
        </div>
        """, unsafe_allow_html=True)


# ─── 페이지: 대시보드 ────────────────────────────────────────
def show_dashboard():
    st.markdown("""
    <div class="main-header">
        <h1>📖 한글 설교 도서관</h1>
        <p>Korean Sermon Library — 은혜로운 설교를 언제 어디서든</p>
    </div>
    """, unsafe_allow_html=True)

    index_data = load_index()
    if not index_data:
        st.error("⚠️ 인덱스 파일이 없습니다. `python build_index.py`를 먼저 실행해 주세요.")
        return

    meta = index_data["metadata"]
    sermons = index_data["sermons"]
    pastors = meta.get("pastors", [])

    # 통계 카드
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-number">{meta.get('total_sermons', 0):,}</div>
            <div class="stat-label">총 설교 수</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-number">{len(pastors)}</div>
            <div class="stat-label">설교자</div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-number">{meta.get('volumes', 0)}</div>
            <div class="stat-label">볼륨 수</div>
        </div>
        """, unsafe_allow_html=True)
    with col4:
        # 성경 본문이 있는 설교 수
        with_scripture = sum(1 for s in sermons if s.get("scripture"))
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-number">{with_scripture:,}</div>
            <div class="stat-label">성경본문 추출</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('<div class="gold-divider"></div>', unsafe_allow_html=True)

    # 설교자 정보
    st.markdown("### 📋 설교자 목록")
    for pastor in pastors:
        st.markdown(f"""
        <div class="pastor-card">
            <div class="pastor-name">{pastor.get('full_name', '')}</div>
            <div class="pastor-desc">
                {pastor.get('description', '')}<br>
                📄 {pastor.get('sermon_count', 0):,}편의 설교
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('<div class="gold-divider"></div>', unsafe_allow_html=True)

    # 최근 설교 미리보기
    st.markdown("### 📑 설교 미리보기")
    preview_sermons = sermons[:12]

    cols = st.columns(3)
    for i, sermon in enumerate(preview_sermons):
        with cols[i % 3]:
            title = sermon.get("title_ko", "제목 없음")
            sno = sermon.get("sermon_no", "?")
            scripture = sermon.get("scripture", "")
            date = sermon.get("date", "")

            if st.button(
                f"📖 No.{sno} | {title[:25]}{'...' if len(title) > 25 else ''}",
                key=f"dash_{sermon['id']}",
                use_container_width=True,
            ):
                navigate_to_sermon(sermon["id"])
                st.rerun()

            st.markdown(f"""
            <div style="color: #6e7681; font-size: 0.8rem; margin-bottom: 1rem; padding-left: 0.5rem;">
                {f'📜 {scripture}' if scripture else ''} {f'📅 {date}' if date else ''}
            </div>
            """, unsafe_allow_html=True)


# ─── 페이지: 설교 탐색 ───────────────────────────────────────
def show_browse():
    st.markdown("""
    <div class="main-header">
        <h1>📚 설교 탐색</h1>
        <p>필터를 사용하여 원하는 설교를 찾아보세요</p>
    </div>
    """, unsafe_allow_html=True)

    index_data = load_index()
    if not index_data:
        st.error("⚠️ 인덱스 파일이 없습니다.")
        return

    sermons = index_data["sermons"]

    # 필터 영역
    col1, col2, col3, col4 = st.columns([2, 2, 2, 2])
    with col1:
        # 볼륨 필터
        volumes = sorted(set(s.get("volume", 0) for s in sermons))
        vol_options = ["전체"] + [f"Volume {v}" for v in volumes]
        selected_vol = st.selectbox("📁 볼륨", vol_options, key="browse_vol")

    with col2:
        # 시리즈 필터
        series_set = sorted(set(s.get("series", "") for s in sermons if s.get("series")))
        series_options = ["전체"] + series_set
        selected_series = st.selectbox("📚 시리즈", series_options, key="browse_series")

    with col3:
        # 설교 번호 범위
        if sermons:
            min_no = min(s.get("sermon_no", 0) for s in sermons if s.get("sermon_no"))
            max_no = max(s.get("sermon_no", 0) for s in sermons if s.get("sermon_no"))
            range_start, range_end = st.slider(
                "📖 설교 번호 범위",
                min_value=min_no, max_value=max_no,
                value=(min_no, max_no),
                key="browse_range",
            )
        else:
            range_start, range_end = 1, 9999

    with col4:
        # 정렬
        sort_option = st.selectbox("🔄 정렬", ["번호 순", "번호 역순"], key="browse_sort")

    # 키워드 검색
    search_query = st.text_input("🔍 제목 검색", placeholder="설교 제목을 입력하세요...", key="browse_search")

    st.markdown('<div class="gold-divider"></div>', unsafe_allow_html=True)

    # 필터링
    filtered = sermons

    if selected_vol != "전체":
        vol_num = int(selected_vol.replace("Volume ", ""))
        filtered = [s for s in filtered if s.get("volume") == vol_num]

    if selected_series != "전체":
        filtered = [s for s in filtered if s.get("series") == selected_series]

    filtered = [s for s in filtered
                if s.get("sermon_no") and range_start <= s["sermon_no"] <= range_end]

    if search_query:
        q = search_query.lower()
        filtered = [s for s in filtered
                    if q in (s.get("title_ko", "") + " " + s.get("title_en", "")).lower()]

    # 정렬
    reverse = sort_option == "번호 역순"
    filtered.sort(key=lambda s: s.get("sermon_no", 0), reverse=reverse)

    # 결과 수 표시
    st.markdown(f"**검색 결과: {len(filtered):,}편**")

    # 페이지네이션
    ITEMS_PER_PAGE = 20
    total_pages = max(1, (len(filtered) + ITEMS_PER_PAGE - 1) // ITEMS_PER_PAGE)

    if "browse_page" not in st.session_state:
        st.session_state.browse_page = 1

    # 페이지 선택
    if total_pages > 1:
        page_col1, page_col2, page_col3 = st.columns([1, 3, 1])
        with page_col1:
            if st.button("◀ 이전", disabled=st.session_state.browse_page <= 1, key="prev_page"):
                st.session_state.browse_page -= 1
                st.rerun()
        with page_col2:
            st.markdown(
                f"<div style='text-align:center; color:#8b949e;'>"
                f"페이지 {st.session_state.browse_page} / {total_pages}</div>",
                unsafe_allow_html=True,
            )
        with page_col3:
            if st.button("다음 ▶", disabled=st.session_state.browse_page >= total_pages, key="next_page"):
                st.session_state.browse_page += 1
                st.rerun()

    # 현재 페이지 아이템
    start_idx = (st.session_state.browse_page - 1) * ITEMS_PER_PAGE
    end_idx = start_idx + ITEMS_PER_PAGE
    page_sermons = filtered[start_idx:end_idx]

    # 설교 목록 렌더링
    for sermon in page_sermons:
        title = sermon.get("title_ko", "제목 없음")
        title_en = sermon.get("title_en", "")
        sno = sermon.get("sermon_no", "?")
        date = sermon.get("date", "")
        scripture = sermon.get("scripture", "")
        preview = sermon.get("preview", "")
        volume = sermon.get("volume", "?")

        col_main, col_btn = st.columns([5, 1])
        with col_main:
            st.markdown(f"""
            <div class="sermon-card">
                <span class="sermon-no">No. {sno}</span>
                <span class="sermon-no" style="background: rgba(139, 148, 158, 0.1); color: #8b949e;">Vol. {volume}</span>
                <div class="sermon-title">{title}</div>
                {f'<div style="color:#6e7681; font-size:0.85rem; margin-bottom:0.3rem;">{title_en}</div>' if title_en else ''}
                <div class="sermon-meta">
                    {f'<span>📜 {scripture}</span>' if scripture else ''}
                    {f'<span>📅 {date}</span>' if date else ''}
                </div>
                {f'<div class="sermon-preview">{preview[:150]}</div>' if preview else ''}
            </div>
            """, unsafe_allow_html=True)
        with col_btn:
            st.markdown("<div style='padding-top: 1.5rem;'></div>", unsafe_allow_html=True)
            if st.button("읽기 →", key=f"read_{sermon['id']}", use_container_width=True):
                navigate_to_sermon(sermon["id"])
                st.rerun()


# ─── 페이지: 설교 읽기 ───────────────────────────────────────
def show_reader():
    index_data = load_index()
    if not index_data:
        st.error("⚠️ 인덱스 파일이 없습니다.")
        return

    sermons = index_data["sermons"]
    sermon_map = {s["id"]: s for s in sermons}

    # 설교 선택
    if not st.session_state.selected_sermon:
        st.markdown("""
        <div class="main-header">
            <h1>📖 설교 읽기</h1>
            <p>왼쪽 설교 탐색에서 설교를 선택하거나 아래에서 직접 선택하세요</p>
        </div>
        """, unsafe_allow_html=True)

        # 설교 선택 드롭다운
        sermon_options = {
            f"No.{s['sermon_no']} - {s.get('title_ko', '제목 없음')}": s["id"]
            for s in sermons if s.get("sermon_no")
        }
        selected_label = st.selectbox(
            "설교 선택",
            ["선택하세요..."] + list(sermon_options.keys()),
            key="reader_select",
        )
        if selected_label != "선택하세요..." and selected_label in sermon_options:
            navigate_to_sermon(sermon_options[selected_label])
            st.rerun()
        return

    # 선택된 설교 로딩
    sermon_id = st.session_state.selected_sermon
    if sermon_id not in sermon_map:
        st.error(f"설교를 찾을 수 없습니다: {sermon_id}")
        return

    sermon = sermon_map[sermon_id]
    content = load_sermon_content(sermon.get("file_name", ""))

    if not content:
        st.error(f"설교 파일을 찾을 수 없습니다: {sermon.get('file_name', '')}")
        return

    # 네비게이션 바
    sorted_sermons = sorted(sermons, key=lambda s: s.get("sermon_no", 0))
    current_idx = next(
        (i for i, s in enumerate(sorted_sermons) if s["id"] == sermon_id), -1
    )

    nav_col1, nav_col2, nav_col3 = st.columns([1, 3, 1])
    with nav_col1:
        if current_idx > 0:
            prev_sermon = sorted_sermons[current_idx - 1]
            if st.button(f"◀ No.{prev_sermon.get('sermon_no', '?')}", key="nav_prev"):
                navigate_to_sermon(prev_sermon["id"])
                st.rerun()
    with nav_col2:
        st.markdown(
            f"<div style='text-align:center; color:#c9a44c; font-size:0.9rem;'>"
            f"No. {sermon.get('sermon_no', '?')} / {len(sermons)}</div>",
            unsafe_allow_html=True,
        )
    with nav_col3:
        if current_idx < len(sorted_sermons) - 1:
            next_sermon = sorted_sermons[current_idx + 1]
            if st.button(f"No.{next_sermon.get('sermon_no', '?')} ▶", key="nav_next"):
                navigate_to_sermon(next_sermon["id"])
                st.rerun()

    st.markdown('<div class="gold-divider"></div>', unsafe_allow_html=True)

    # 설교 헤더
    title_ko = sermon.get("title_ko", "제목 없음")
    title_en = sermon.get("title_en", "")
    scripture = sermon.get("scripture", "")
    date = sermon.get("date", "")
    series = sermon.get("series", "")

    st.markdown(f"""
    <div class="reader-header">
        <div style="color:#c9a44c; font-size:0.9rem; margin-bottom:0.5rem;">
            설교 제 {sermon.get('sermon_no', '?')}호 · {series}
        </div>
        <h1>{title_ko}</h1>
        {f'<div style="color:#6e7681; font-size:1rem; margin-top:0.5rem;">{title_en}</div>' if title_en else ''}
        <div class="reader-meta">
            C. H. 스펄전 (C. H. Spurgeon)
            {f' · 📅 {date}' if date else ''}
            {f'<br>📜 {scripture}' if scripture else ''}
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 글꼴 크기 조절
    font_size = st.slider("📏 글꼴 크기", 14, 24, 18, 1, key="font_size")

    # 설교 본문
    st.markdown(f"""
    <div class="reader-content" style="font-size: {font_size}px;">
    """, unsafe_allow_html=True)

    st.markdown(content)

    st.markdown("</div>", unsafe_allow_html=True)

    # 하단 네비게이션
    st.markdown('<div class="gold-divider"></div>', unsafe_allow_html=True)
    bot_col1, bot_col2, bot_col3 = st.columns([1, 2, 1])
    with bot_col1:
        if current_idx > 0:
            prev_s = sorted_sermons[current_idx - 1]
            if st.button(
                f"◀ 이전: No.{prev_s.get('sermon_no', '?')}",
                key="nav_prev_bot",
            ):
                navigate_to_sermon(prev_s["id"])
                st.rerun()
    with bot_col2:
        if st.button("📚 목록으로 돌아가기", key="back_to_list", use_container_width=True):
            st.session_state.page = "📚 설교 탐색"
            st.rerun()
    with bot_col3:
        if current_idx < len(sorted_sermons) - 1:
            next_s = sorted_sermons[current_idx + 1]
            if st.button(
                f"다음: No.{next_s.get('sermon_no', '?')} ▶",
                key="nav_next_bot",
            ):
                navigate_to_sermon(next_s["id"])
                st.rerun()


# ─── 페이지: 검색 ────────────────────────────────────────────
def show_search():
    st.markdown("""
    <div class="main-header">
        <h1>🔍 설교 검색</h1>
        <p>제목, 성경구절, 본문 내용으로 설교를 검색하세요</p>
    </div>
    """, unsafe_allow_html=True)

    index_data = load_index()
    if not index_data:
        st.error("⚠️ 인덱스 파일이 없습니다.")
        return

    sermons = index_data["sermons"]

    # 검색 입력
    col1, col2 = st.columns([4, 1])
    with col1:
        query = st.text_input(
            "검색어",
            placeholder="제목, 성경구절, 키워드를 입력하세요...",
            key="search_query",
            label_visibility="collapsed",
        )
    with col2:
        search_scope = st.selectbox(
            "범위",
            ["전체", "제목", "성경구절", "본문"],
            key="search_scope",
            label_visibility="collapsed",
        )

    if query:
        q_lower = query.strip().lower()
        results = []

        if search_scope in ("전체", "제목"):
            for s in sermons:
                title_text = (s.get("title_ko", "") + " " + s.get("title_en", "")).lower()
                if q_lower in title_text and s not in results:
                    results.append(s)

        if search_scope in ("전체", "성경구절"):
            for s in sermons:
                if q_lower in s.get("scripture", "").lower() and s not in results:
                    results.append(s)

        if search_scope in ("전체", "본문"):
            # 미리보기 텍스트에서 검색 + 전문 검색
            for s in sermons:
                if s in results:
                    continue
                if q_lower in s.get("preview", "").lower():
                    results.append(s)
                    continue
                # 전문 검색
                content = load_sermon_content(s.get("file_name", ""))
                if content and q_lower in content.lower():
                    results.append(s)
                if len(results) >= 100:
                    break

        st.markdown(f"**검색 결과: {len(results)}건**")
        st.markdown('<div class="gold-divider"></div>', unsafe_allow_html=True)

        for sermon in results:
            title = sermon.get("title_ko", "제목 없음")
            sno = sermon.get("sermon_no", "?")
            scripture = sermon.get("scripture", "")

            col_main, col_btn = st.columns([5, 1])
            with col_main:
                st.markdown(f"""
                <div class="sermon-card">
                    <span class="sermon-no">No. {sno}</span>
                    <div class="sermon-title">{title}</div>
                    <div class="sermon-meta">
                        {f'<span>📜 {scripture}</span>' if scripture else ''}
                    </div>
                </div>
                """, unsafe_allow_html=True)
            with col_btn:
                st.markdown("<div style='padding-top: 1rem;'></div>", unsafe_allow_html=True)
                if st.button("읽기", key=f"search_{sermon['id']}", use_container_width=True):
                    navigate_to_sermon(sermon["id"])
                    st.rerun()
    else:
        # 검색어 없을 때 안내
        st.markdown("""
        <div style="text-align: center; padding: 3rem 0; color: #6e7681;">
            <div style="font-size: 3rem; margin-bottom: 1rem;">🔍</div>
            <div style="font-size: 1.1rem;">검색어를 입력해 주세요</div>
            <div style="font-size: 0.9rem; margin-top: 0.5rem;">
                예: "은혜", "로마서", "구원", "십자가"
            </div>
        </div>
        """, unsafe_allow_html=True)


# ─── 페이지: 소개 ────────────────────────────────────────────
def show_about():
    st.markdown("""
    <div class="main-header">
        <h1>ℹ️ 한글 설교 도서관 소개</h1>
        <p>Korean Sermon Library</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    ### 📖 프로젝트 소개

    **한글 설교 도서관**은 위대한 설교자들의 설교를 한국어로 읽고 탐색할 수 있는 
    디지털 도서관입니다.

    ---

    ### 📚 현재 수록된 설교

    #### C. H. 스펄전 (Charles Haddon Spurgeon, 1834-1892)
    - **뉴 파크 스트리트 강단** (The New Park Street Pulpit, 1855-1860)
    - **메트로폴리탄 태버내클 강단** (The Metropolitan Tabernacle Pulpit, 1861-1917)
    - 영국의 '설교 왕자'로 불리며, 역사상 가장 위대한 설교자 중 한 분입니다.

    ---

    ### 🛠️ 새로운 목사님 설교 추가 방법

    1. `sermons/` 폴더 아래에 새 폴더를 만듭니다 (예: `sermons/lloyd-jones/`)
    2. 한글 번역된 마크다운 파일을 넣습니다
    3. `python build_index.py`를 실행하여 인덱스를 업데이트합니다
    4. 앱이 자동으로 새 설교를 인식합니다

    ---

    ### 🔧 기술 정보

    - **프레임워크**: Streamlit
    - **데이터 형식**: Markdown (.md)
    - **호스팅**: Streamlit Community Cloud
    - **소스 코드**: GitHub

    ---

    ### 🙏 감사의 글

    이 프로젝트는 하나님의 말씀을 한국어로 더 많은 사람들에게 전하기 위해 
    만들어졌습니다. 스펄전 목사님의 설교는 
    [The Spurgeon Center](https://www.spurgeon.org/)에서 원문을 확인할 수 있습니다.

    ---

    <div style="text-align: center; color: #c9a44c; font-family: 'Noto Serif KR', serif; 
                font-size: 1.1rem; padding: 1rem 0;">
        "말씀이 육신이 되어 우리 가운데 거하시매" (요한복음 1:14)
    </div>
    """, unsafe_allow_html=True)


# ─── 메인 라우팅 ──────────────────────────────────────────────
page = st.session_state.page

if page == "📊 대시보드":
    show_dashboard()
elif page == "📚 설교 탐색":
    show_browse()
elif page == "📖 설교 읽기":
    show_reader()
elif page == "🔍 검색":
    show_search()
elif page == "ℹ️ 소개":
    show_about()

# ─── 하단 푸터 ────────────────────────────────────────────────
st.markdown("""
<div class="footer">
    📖 한글 설교 도서관 · Korean Sermon Library<br>
    Soli Deo Gloria — 오직 하나님께만 영광을
</div>
""", unsafe_allow_html=True)

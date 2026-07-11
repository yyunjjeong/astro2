import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# --- 1. 페이지 설정 및 제목 ---
st.set_page_config(page_title="세페이드 변광성 시뮬레이터", layout="wide")
st.title("🔭 세페이드 변광성의 주기-광도 관계 및 오차 보정 시뮬레이터")
st.write("지구과학Ⅱ 천체 탐구 프로젝트: 표준 촛대의 금속 함량 및 성간 소광 오차 분석 앱")

# --- 2. 이론적 배경 설명 (사이드바) ---
st.sidebar.markdown("## 💡 지구과학Ⅱ 천체 원리 요약")
st.sidebar.info(
    """
    1. **주기-광도 관계 (P-L Relation):** 세페이드 변광성은 변광 주기($P$)가 길수록 절대 등급($M$)이 밝아집니다(오차가 없는 기본 법칙).
    
    2. **금속 함량(집단)에 따른 차이:**
       - **Ⅰ족 항성 (젊고 금속 풍부):** 더 밝음 ($M = -2.8 \\log P - 1.4$)
       - **Ⅱ족 항성 (늙고 금속 부족):** 더 어두움 ($M = -2.8 \\log P + 0.1$)
       ※ 금속 함량을 잘못 알면 거리가 완전히 다르게 계산됩니다!
    
    3. **성간 소광 ($A$):**
       성간 티끌이 별빛을 가려 겉보기 등급($m$)이 더 어둡게(숫자가 크게) 보입니다. 소광을 보정하지 않으면 별이 실제보다 더 멀리 있다고 착각하게 됩니다.
    """
)

# --- 3. [가상 관측 데이터 생성] (고정된 은하 X의 데이터) ---
np.random.seed(100)
true_distance_pc = 12000  # 12 kpc
true_log_P = np.random.uniform(0.5, 1.8, 25)

# 실제 Ⅱ족 항성의 절대등급 계산
M_true = -2.8 * true_log_P + 0.1
# 실제 관측되는 겉보기 등급 (m - M = 5 log d - 5 + A)
m_true = M_true + 5 * np.log10(true_distance_pc) - 5 + 0.5
m_obs = m_true + np.random.normal(0, 0.15, 25)

# --- 4. 사용자 조작 UI ---
st.subheader("🛠️ 관측 데이터 분석 및 모델 매칭 (슬라이더를 조절해 보세요)")

col1, col2, col3 = st.columns(3)

with col1:
    user_pop = st.radio(
        "1. 가정할 별의 집단 (금속 함량)",
        ["Ⅰ족 항성 (금속 풍부, 젊은 별)", "Ⅱ족 항성 (금속 부족, 늙은 별)"],
        index=0
    )

with col2:
    user_extinction = st.slider(
        "2. 성간 소광량 보정치 (A)",
        min_value=0.0, max_value=2.0, value=0.0, step=0.1,
        help="성간 티끌에 의해 빛이

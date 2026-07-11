import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# --- 1. 페이지 설정 및 제목 ---
st.set_page_config(page_title="세페이드 변광성 시뮬레이터", layout="wide")
st.title("🔭 세페이드 변광성의 주기-광도 관계 및 오차 보정 시뮬레이터")
st.write("지구과학Ⅱ 천체 탐구 프로젝트: 표준 촛대의 금속 함량 및 성간 소광 오차 분석 앱")

# --- 2. 이론적 배경 설명 (사이드바 또는 상단) ---
st.sidebar.markdown("## 💡 지구과학Ⅱ 천체 원리 요약")
st.sidebar.info(
    """
    1. **주기-광도 관계 (P-L Relation):** 세페이드 변광성은 변광 주기($P$)가 길수록 절대 등급($M$)이 밝아집니다(오차가 없는 기본 법칙).
    
    2. **금속 함량(집단)에 따른 차이:**
       - **Ⅰ족 항성 (젊고 금속 풍부):** 더 밝음 ($M = -2.8 \log P - 1.4$)
       - **Ⅱ족 항성 (늙고 금속 부족):** 더 어두움 ($M = -2.8 \log P + 0.1$)
       - ※ 금속 함량을 잘못 알면 거리가 완전히 다르게 계산됩니다!
    
    3. **성간 소광 ($A$):**
       성간 티끌이 별빛을 가려 겉보기 등급($m$)이 더 어둡게(숫자가 크게) 보입니다. 소광을 보정하지 않으면 별이 실제보다 더 멀리 있다고 착각하게 됩니다.
    """
)

# --- 3. [가상 관측 데이터 생성] (고정된 은하 X의 데이터) ---
# 이 은하의 진짜 비밀: 실제 거리 12.0 kpc, 실제 별의 집단은 'Ⅱ족 항성', 실제 성간 소광량은 0.5 등급
np.random.seed(100)
true_distance_pc = 12000  # 12 kpc
true_log_P = np.random.uniform(0.5, 1.8, 25)  # 25개 변광성의 주기 (log 값)

# 실제 Ⅱ족 항성의 절대등급 계산
M_true = -2.8 * true_log_P + 0.1
# 실제 관측되는 겉보기 등급 (거리 지수 공식: m - M = 5 log d - 5 + A)
m_true = M_true + 5 * np.log10(true_distance_pc) - 5 + 0.5
# 약간의 관측 오차 추가
m_obs = m_true + np.random.normal(0, 0.15, 25)

# --- 4. 사용자 조작 UI (슬라이더 및 선택 상자) ---
st.subheader("🛠️ 관측 데이터 분석 및 모델 매칭 (슬라이더를 조절해 보세요)")

col1, col2, col3 = st.columns(3)

with col1:
    user_pop = st.radio(
        "1. 가정할 별의 집단 (금속 함량)",
        ["Ⅰ족 항성 (금속 풍부, 젊은 별)", "Ⅱ족 항성 (금속 부족, 늙은 별)"],
        index=0  # 처음에 일부러 틀린 Ⅰ족을 선택하게 하여 오차를 유도함
    )

with col2:
    user_extinction = st.slider(
        "2. 성간 소광량 보정치 (A)",
        min_value=0.0, max_value=2.0, value=0.0, step=0.1,
        help="성간 티끌에 의해 빛이 가려진 양을 입력하여 보정합니다."
    )

with col3:
    user_distance_kpc = st.slider(
        "3. 예측할 은하까지의 거리 (kpc)",
        min_value=1.0, max_value=30.0, value=5.0, step=0.1,
        help="슬라이더를 움직여 이론선이 관측 데이터 점들 가운데에 오도록 맞추세요."
    )

# --- 5. 사용자가 입력한 조건에 따른 이론적 겉보기 등급 계산 ---
# 주기에 따른 연속적인 선을 그리기 위한 log P 배열
line_log_P = np.linspace(0.3, 2.0, 100)

if "Ⅰ족" in user_pop:
    M_theory = -2.8 * line_log_P - 1.4
else:
    M_theory = -2.8 * line_log_P + 0.1

# 사용자가 입력한 거리(kpc -> pc 변환)를 기반으로 이론적 겉보기 등급 선 유도
user_distance_pc = user_distance_kpc * 1000
# 거리 지수 변형: m = M + 5 log d - 5 + A
m_theory = M_theory + 5 * np.log10(user_distance_pc) - 5 + user_extinction

# --- 6. 그래프 시각화 ---
fig, ax = plt.subplots(figsize=(10, 5))

# 관측 데이터 점 찍기
ax.scatter(true_log_P, m_obs, color="blue", alpha=0.7, label="은하 X에서 관측된 변광성 데이터 (점)")
# 사용자의 이론선 그리기
ax.plot(line_log_P, m_theory, color="red", linewidth=2.5, label="내가 설정한 이론적 모델 선")

# 천문학 그래프 특성: 등급은 숫자가 작을수록 밝으므로 Y축을 뒤집어야 함 (★지학2 핵심 센스)
ax.invert_yaxis()

ax.set_xlabel("변광 주기 (log P [days])", fontsize=12)
ax.set_ylabel("관측된 겉보기 등급 (m)", fontsize=12)
ax.set_title("세페이드 변광성 주기-광도 데이터 Fitting", fontsize=14, fontweight='bold')
ax.grid(True, linestyle="--", alpha=0.5)
ax.legend(fontsize=10)

st.pyplot(fig)

# --- 7. 결과 분석 및 오차 도출 ---
st.divider()
st.subheader("📊 데이터 분석 결과 보고서")

# 정답 판정 (실제 정답: Ⅱ족 항성, 소광 0.5, 거리 12.0kpc)
is_pop_correct = "Ⅱ족" in user_pop
is_ext_correct = abs(user_extinction - 0.5) < 0.1
is_dist_correct = abs(user_distance_kpc - 12.0) < 0.5

out_col1, out_col2 = st.columns(2)

with out_col1:
    st.markdown("### 🔍 현재 모델 매칭 상태")
    if is_pop_correct and is_ext_correct and is_dist_correct:
        st.success("🎉 대단합니다! 금속 함량, 성간 소광, 거리를 모두 정확하게 보정하여 완벽한 모델을 찾았습니다!")
    else:
        st.warning("⚠️ 이론선이 데이터 점들의 중심을 관통하도록 슬라이더를 더 정밀하게 조절해 보세요.")
        
    st.write(f"• 설정된 별의 집단: **{user_pop.split(' ')[0]}**")
    st.write(f"• 설정된 성간 소광량: **{user_extinction} 등급**")
    st.write(f"• 계산된 은하의 거리: **{user_distance_kpc} kpc** (약 {user_distance_kpc * 3260:,.0f} 광년)")

with out_col2:
    st.markdown("### 🚨 오차 분석 (지구과학Ⅰ 탐구와의 연계)")
    
    # 만약 소광이나 집단을 잘못 설정했을 때 일어나는 과학적 왜곡 설명
    if "Ⅰ족" in user_pop:
        st.error("❗ [오차 원인 1] 실제보다 별을 '금속이 많은 젊은 별(Ⅰ족)'로 잘못 가정했습니다. 이 경우 별의 실제 절대등급(원래 밝기)을 너무 밝게 추정하게 되므로, 이론선에 맞추다 보면 은하의 거리가 실제(12.0kpc)보다 훨씬 멀리 있는 것으로 왜곡됩니다.")
    
    if user_extinction == 0.0:
        st.error("❗ [오차 원인 2] 성간 소광(A=0)을 전혀 고려하지 않았습니다. 우주 공간의 티끌 때문에 별빛이 흐려진 것을 고려하지 않으면, 별이 단순히 '멀리 있어서 어두운 것'으로 착각하게 되어 은하의 거리가 실제보다 더 멀게 계산됩니다.")
        
    if is_pop_correct and is_ext_correct:
        st.info("✅ **오차 보정 성공:** 금속 함량 오차와 성간 소광을 모두 올바르게 입력하니, 은하의 실제 거리인 **12.0 kpc** 부근에서 그래프가 완벽히 일치하는 것을 볼 수 있습니다. 이를 통해 표준 촛대를 이용한 거리 측정에서 '천체의 물리적 성질(금속 함량)'과 '성간 환경(소광)'을 모두 고려하는 것이 얼마나 중요한지 증명되었습니다.")

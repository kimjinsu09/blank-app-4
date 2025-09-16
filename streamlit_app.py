# 파일명: streamlit_app.py
import streamlit as st
import pandas as pd
import pydeck as pdk

st.set_page_config(page_title="대기오염 시각화", layout="wide")

st.title("🌍 대기오염 데이터 시각화 대시보드")

# --- 1. 사용자 입력 데이터 ---
st.header("📊 내 관측 데이터 입력")
user_data = []

with st.form("data_input"):
    date = st.date_input("측정 날짜")
    pm10 = st.number_input("PM10 (㎍/㎥)", min_value=0, value=30)
    pm25 = st.number_input("PM2.5 (㎍/㎥)", min_value=0, value=15)
    submitted = st.form_submit_button("추가하기")
    if submitted:
        user_data.append({"날짜": date, "PM10": pm10, "PM2.5": pm25})

# 세션 상태로 데이터 저장
if "user_df" not in st.session_state:
    st.session_state["user_df"] = pd.DataFrame(columns=["날짜", "PM10", "PM2.5"])

if user_data:
    st.session_state["user_df"] = pd.concat(
        [st.session_state["user_df"], pd.DataFrame(user_data)], ignore_index=True
    )

st.subheader("내 데이터 미리보기")
st.dataframe(st.session_state["user_df"])

# --- 2. 예시 데이터 (API 대신) ---
st.header("🌐 예시 공식 데이터 (테스트용)")
example_data = pd.DataFrame({
    "국가": ["대한민국", "일본", "미국"],
    "PM2.5": [23, 14, 9],
    "위도": [36.5, 36.2, 37.1],
    "경도": [127.8, 138.3, -95.7],
})

st.dataframe(example_data)

# --- 3. 지도 시각화 ---
st.header("🗺️ 지도에서 시각화")
st.map(example_data.rename(columns={"위도": "lat", "경도": "lon"}))

# --- 4. 차트 시각화 ---
st.header("📈 추세 차트")
if not st.session_state["user_df"].empty:
    st.line_chart(st.session_state["user_df"].set_index("날짜")[["PM10", "PM2.5"]])
else:
    st.info("아직 입력된 데이터가 없습니다. 위에서 데이터를 추가해보세요!")

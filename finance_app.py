with tab2:
    st.subheader("📥 Apply for a Loan")
    loan_amount = st.number_input("Enter loan amount (₹)", min_value=1000, step=500)
    if loan_amount:
        tax = 0.05 * loan_amount
        total_payable = loan_amount + tax
        st.warning(f"⚠️ You must pay ₹{total_payable:.2f} (₹{tax:.2f} is tax).")

        upi_url_loan = f"upi://pay?pa=ayushbhradwaj009-1@okicici&pn=AyushBhardwaj&am={total_payable}&cu=INR"
        qr_url_loan = f"https://api.qrserver.com/v1/create-qr-code/?size=200x200&data={urllib.parse.quote(upi_url_loan)}"
        st.image(qr_url_loan, caption="Scan to Pay", use_container_width=True)
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

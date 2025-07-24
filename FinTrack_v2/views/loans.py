import streamlit as st
from datetime import date, timedelta
from db import Database


class LoansPage:
    def __init__(self):
        self.db = Database()

    def show(self):
        if not st.session_state.user:
            st.warning("You must be logged in to view this page.")
            st.session_state.page = "landing"
            return

        self.apply_style()

        st.markdown("""
        <div class="finance-container">
            <div class="finance-title">Loan Management</div>
            <div class="finance-subtitle">Track and manage your loan obligations</div>
        </div>
        """, unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            loan_type = st.selectbox("Loan Category", ["Home", "Car", "Personal", "Education", "Other"])
            bank_name = st.text_input("Lender Name", placeholder="e.g., HDFC Bank")
            emi_amount = st.number_input("EMI Amount (₹)", min_value=0.0, format="%.2f")

        with col2:
            start_date = st.date_input("Loan Start Date", value=date.today())
            end_date = st.date_input("Loan End Date", value=start_date + timedelta(days=365))
            st.write("")

        if st.button("Add Loan"):
            if not bank_name or emi_amount <= 0 or end_date <= start_date:
                st.warning("Please fill all fields with valid values.")
            else:
                username = st.session_state.user["username"]
                self.db.execute(
                    """INSERT INTO loans (username, loan_type, bank_name, emi_amount, start_date, end_date)
                       VALUES (%s, %s, %s, %s, %s, %s)""",
                    (username, loan_type, bank_name, emi_amount, start_date, end_date)
                )
                st.success(f"{loan_type} loan from {bank_name} successfully added!")

        st.markdown("</div></div>", unsafe_allow_html=True)

        st.markdown("""
        <div class="section-card">
            <div class="section-title">EMI Schedule</div>
        """, unsafe_allow_html=True)

        username = st.session_state.user["username"]
        today = date.today()

        user_loans = self.db.fetchall(
            "SELECT loan_type, bank_name, emi_amount, start_date, end_date FROM loans WHERE username=%s", (username,)
        )

        active_loans = []
        total_emi_amount = 0.0

        for loan in user_loans:
            try:
                start = loan["start_date"]
                end = loan["end_date"]
                if isinstance(start, str):
                    start = date.fromisoformat(start)
                if isinstance(end, str):
                    end = date.fromisoformat(end)
            except (KeyError, ValueError):
                continue

            next_due = start
            while next_due < today:
                next_due = self.add_months(next_due, 1)

            if next_due <= end:
                total_emi_amount += float(loan["emi_amount"])

                days_until_due = (next_due - today).days
                due_status = "Due Soon" if days_until_due <= 7 else "On Track"

                loan_display = {
                    "Loan Type": loan["loan_type"],
                    "Lender": loan["bank_name"],
                    "EMI Amount": f"₹{loan['emi_amount']:,.2f}",
                    "Next Due Date": str(next_due),
                    "Days Until Due": days_until_due,
                    "Status": due_status
                }
                active_loans.append(loan_display)

        if active_loans:
            st.markdown(f"""
            <div class="loan-summary">
                <div class="summary-row">
                    <span class="summary-label">Active Loans:</span>
                    <span class="summary-value">{len(active_loans)} obligations</span>
                </div>
                <div class="summary-row">
                    <span class="summary-label">Total Monthly EMI:</span>
                    <span class="summary-value">₹{total_emi_amount:,.2f}</span>
                </div>
                <div class="summary-row">
                    <span class="summary-label">Annual Obligation:</span>
                    <span class="summary-value">₹{total_emi_amount * 12:,.2f}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

            st.markdown('<div class="emi-table">', unsafe_allow_html=True)
            st.dataframe(active_loans, use_container_width=True, hide_index=True)
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.info("No active loans in your portfolio.")

        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("← Back to Dashboard"):
            st.session_state.page = "dashboard"
            st.rerun()

    @staticmethod
    def add_months(d, months):
        year = d.year + (d.month + months - 1) // 12
        month = (d.month + months - 1) % 12 + 1
        day = min(d.day, [31,
                          29 if year % 4 == 0 and (year % 100 != 0 or year % 400 == 0) else 28,
                          31, 30, 31, 30, 31, 31, 30, 31, 30, 31][month - 1])
        return date(year, month, day)

    def apply_style(self):
        st.markdown("""
        <style>
        .finance-container {
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
            padding: 30px;
            border-radius: 12px;
            margin-bottom: 25px;
            box-shadow: 0 8px 32px rgba(0,0,0,0.3);
            border: 1px solid rgba(255,255,255,0.1);
        }
        .finance-title {
            color: #ffffff;
            text-align: center;
            font-size: 2.8rem;
            font-weight: 700;
            margin-bottom: 8px;
            letter-spacing: -0.5px;
        }
        .finance-subtitle {
            color: #b8c6db;
            text-align: center;
            font-size: 1.1rem;
            margin-bottom: 0;
            font-weight: 400;
        }
        .section-card {
            background: #ffffff;
            padding: 30px;
            border-radius: 8px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.08);
            margin-bottom: 25px;
            border: 1px solid #e8ecf3;
        }
        .section-title {
            color: #2c3e50;
            font-size: 1.4rem;
            font-weight: 600;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 2px solid #3498db;
        }
        .loan-summary {
            background: #f8f9fa;
            padding: 20px;
            border-radius: 8px;
            margin-bottom: 20px;
            border: 1px solid #dee2e6;
        }
        .summary-row {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 8px;
        }
        .summary-label {
            color: #6c757d;
            font-weight: 500;
            font-size: 0.95rem;
        }
        .summary-value {
            color: #2c3e50;
            font-weight: 600;
            font-size: 1rem;
        }
        
        .form-container {
            background: #f8f9fa;
            padding: 25px;
            border-radius: 8px;
            margin-bottom: 20px;
            border: 1px solid #dee2e6;
        }
        .stSelectbox > div > div {
            background-color: #ffffff;
            border-radius: 6px;
            border: 1px solid #ced4da;
            transition: border-color 0.3s ease;
        }
        .stSelectbox > div > div:focus-within {
            border-color: #3498db;
            box-shadow: 0 0 0 3px rgba(52, 152, 219, 0.1);
        }
        .stTextInput > div > div {
            background-color: #ffffff;
            border-radius: 6px;
            border: 1px solid #ced4da;
            transition: border-color 0.3s ease;
        }
        .stTextInput > div > div:focus-within {
            border-color: #3498db;
            box-shadow: 0 0 0 3px rgba(52, 152, 219, 0.1);
        }
        .stNumberInput > div > div {
            background-color: #ffffff;
            border-radius: 6px;
            border: 1px solid #ced4da;
        }
        .stNumberInput > div > div:focus-within {
            border-color: #3498db;
            box-shadow: 0 0 0 3px rgba(52, 152, 219, 0.1);
        }
        .stDateInput > div > div {
            background-color: #ffffff;
            border-radius: 6px;
            border: 1px solid #ced4da;
        }
        .stDateInput > div > div:focus-within {
            border-color: #3498db;
            box-shadow: 0 0 0 3px rgba(52, 152, 219, 0.1);
        }
        .stButton > button {
            background: #3498db;
            color: white;
            border: none;
            border-radius: 6px;
            padding: 12px 24px;
            font-weight: 600;
            font-size: 0.95rem;
            width: 100%;
        }
        .stButton > button:hover {
            background: #2980b9;
            transform: translateY(-1px);
            box-shadow: 0 4px 12px rgba(52, 152, 219, 0.3);
        }
        .back-button {
            background: #6c757d;
            color: white;
            border: none;
            border-radius: 6px;
            padding: 10px 20px;
            font-weight: 500;
            font-size: 0.9rem;
            transition: all 0.3s ease;
            width: 100%;
        }
        .stDataFrame {
            background: white;
            border-radius: 8px;
            padding: 0;
            box-shadow: 0 2px 8px rgba(0,0,0,0.06);
            border: 1px solid #e8ecf3;
        }
        .emi-table {
            margin-top: 20px;
        }
        .input-label {
            color: #495057;
            font-weight: 500;
            font-size: 0.9rem;
            margin-bottom: 5px;
        }
        </style>
        """, unsafe_allow_html=True)


import streamlit as st
from datetime import datetime, timedelta
from collections import defaultdict
from components.utils import load_json
import plotly.express as px

EXPENSE_FILE = "data/expenses.json"

def show_dashboard():
    if not st.session_state.user:
        st.warning("You must be logged in to view this page.")
        st.session_state.page = "landing"
        return

    st.markdown("""
    <style>
    .stApp {
        background-color: #f8f9fa;
        max-width: 100%;
    }
    
    .welcome-section {
        background: linear-gradient(135deg, #2c3e50 0%, #3498db 100%);
        color: white;
        padding: 2.5rem;
        border-radius: 15px;
        text-align: center;
        margin-bottom: 3rem;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
    }
    
    .welcome-title {
        font-size: 2.5rem;
        font-weight: 300;
        margin-bottom: 0.5rem;
        text-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
    }
    
    .welcome-subtitle {
        font-size: 1.2rem;
        font-weight: 300;
        opacity: 0.9;
    }
    
   
    .nav-title {
        color: #2c3e509;
        font-size: 1.5rem;
        font-weight: 600;
        margin-bottom: 1.5rem;
        text-align: center;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #27ae60 0%, #2ecc71 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 1rem 2rem;
        font-size: 1rem;
        font-weight: 500;
        width: 100%;
        transition: all 0.3s ease;
        box-shadow: 0 4px 12px rgba(46, 204, 113, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(46, 204, 113, 0.4);
    }
    
    /* Section 3: Upcoming Loan Payment */
    .loan-section {
        background: white;
        padding: 2rem;
        border-radius: 12px;
        margin-bottom: 3rem;
        box-shadow: 0 5px 15px rgba(0, 0, 0, 0.08);
        border-left: 4px solid #e74c3c;
    }
    
    .loan-header {
        color: #2c3e50;
        font-size: 1.5rem;
        font-weight: 600;
        margin-bottom: 1.5rem;
        text-align: center;
        padding-bottom: 1rem;
        border-bottom: 2px solid #ecf0f1;
        background: #FF5733;
        border-radius: 12px;
        width: 100% ;
    }
    
    .loan-card {
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #e74c3c;
        margin-bottom: 1rem;
    }
    
    .loan-card.urgent {
        border-left-color: #e74c3c;
        background: #ffeaea;
    }
    
    .loan-card.warning {
        border-left-color: #f39c12;
        background: #fff9e6;
    }
    
    .loan-card.normal {
        border-left-color: #27ae60;
        background: #eafaf1;
    }
    
    .loan-title {
        color: #2c3e50;
        font-size: 1.2rem;
        font-weight: 600;
        margin-bottom: 1rem;
    }
    
    .loan-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 1rem;
    }
    
    .loan-item {
        display: flex;
        flex-direction: column;
        gap: 0.3rem;
    }
    
    .loan-label {
        font-weight: 500;
        color: #7f8c8d;
        font-size: 0.9rem;
    }
    
    .loan-value {
        font-weight: 600;
        color: #2c3e50;
        font-size: 1rem;
    }
    
    .days-remaining {
        color: #e74c3c;
        font-size: 1.1rem;
        font-weight: 700;
    }
    
    .no-loans {
        background: #e8f5e8;
        color: #27ae60;
        padding: 1.5rem;
        border-radius: 8px;
        text-align: center;
        font-style: italic;
    }
    
    /* Section 4: Expense Summary */
    .expense-section {
        background: white;
        padding: 2rem;
        border-radius: 12px;
        margin-bottom: 3rem;
        box-shadow: 0 5px 15px rgba(0, 0, 0, 0.08);
        border-left: 4px solid #f39c12;
    }
    
    .expense-header {
        color: #2c3e50;
        font-size: 1.5rem;
        font-weight: 600;
        margin-bottom: 1.5rem;
        text-align: center;
        padding-bottom: 1rem;
        border-bottom: 2px solid #ecf0f1;
        background: #FF5733;
        border-radius: 12px;
        width: 100% ;
    }
    
    .date-selector {
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 8px;
        margin-bottom: 1.5rem;
        border-left: 4px solid #3498db;
    }
    
    .date-selector-title {
        color: #2c3e50;
        font-size: 1.1rem;
        font-weight: 600;
        margin-bottom: 1rem;
    }
    
    .expense-summary {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        margin-bottom: 1.5rem;
        border-left: 4px solid #3498db;
    }
    
    .period-title {
        color: #2c3e50;
        font-size: 1.1rem;
        font-weight: 600;
        margin-bottom: 1rem;
    }
    
    .total-spent {
        background: #e8f4f8;
        padding: 0.8rem;
        border-radius: 6px;
        margin-bottom: 1rem;
        text-align: center;
        border: 1px solid #3498db;
    }
    
    .total-amount {
        color: #2c3e50;
        font-size: 1.2rem;
        font-weight: 700;
    }
    
    .expense-item {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 0.7rem;
        background: #f8f9fa;
        border-radius: 6px;
        margin-bottom: 0.5rem;
        border-left: 3px solid #27ae60;
    }
    
    .expense-category {
        color: #2c3e50;
        font-weight: 500;
        font-size: 0.95rem;
    }
    
    .expense-amount {
        color: #27ae60;
        font-weight: 600;
        font-size: 1rem;
    }
    
    .no-expenses {
        background: #fff3cd;
        color: #856404;
        padding: 1.5rem;
        border-radius: 8px;
        text-align: center;
        font-style: italic;
    }
    
    .logout-section {
        text-align: center;
        margin-top: 2rem;
        padding: 2rem;
        background: white;
        border-radius: 12px;
        box-shadow: 0 5px 15px rgba(0, 0, 0, 0.08);
    }
    
    .logout-button {
        background: linear-gradient(135deg, #e74c3c 0%, #c0392b 100%);
        color: white;
        border: none;
        padding: 0.8rem 2rem;
        border-radius: 8px;
        font-weight: 600;
        transition: all 0.3s ease;
        cursor: pointer;
    }
    
    .logout-button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(231, 76, 60, 0.3);
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="welcome-section">
        <h1 class="welcome-title">Welcome, {st.session_state.user['username']}!</h1>
        <p class="welcome-subtitle">Your Personal Finance Dashboard</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("Loan Tracker", key="loan_btn"):
            st.session_state.page = "loans"
            st.rerun()
    with col2:
        if st.button("Expenses Tracker", key="expense_btn"):
            st.session_state.page = "expenses"
            st.rerun()
    with col3:
        if st.button("Investments", key="investment_btn"):
            st.session_state.page = "investments"
            st.rerun()

    st.markdown("""
    <div>
        <h2 class="loan-header">Upcoming Loan Payment</h2>
    </div>
    """, unsafe_allow_html=True)
    
    all_loans = load_json("data/loans.json")
    user_loans = [
        loan for loan in all_loans
        if loan.get("username") == st.session_state.user["username"]
    ]
    
    if user_loans:
        today = datetime.today()
        closest_loan = None
        min_days_diff = float('inf')
        
        for loan in user_loans:
            try:
                end_date = datetime.strptime(loan["end_date"], "%Y-%m-%d")
                days_diff = (end_date - today).days
                
                if days_diff >= 0 and days_diff < min_days_diff:
                    min_days_diff = days_diff
                    closest_loan = loan
            except ValueError:
                continue
        
        if closest_loan:
            days_remaining = min_days_diff
            
            if days_remaining <= 7:
                card_class = "urgent"
            elif days_remaining <= 30:
                card_class = "warning"
            else:
                card_class = "normal"
            
            st.markdown(f"""
            <div class="loan-card {card_class}">
                <h3 class="loan-title">{closest_loan['loan_type']}</h3>
                <div class="loan-grid">
                    <div class="loan-item">
                        <span class="loan-label">Bank:</span>
                        <span class="loan-value">{closest_loan['bank_name']}</span>
                    </div>
                    <div class="loan-item">
                        <span class="loan-label">EMI Amount:</span>
                        <span class="loan-value">₹{closest_loan['emi_amount']}</span>
                    </div>
                    <div class="loan-item">
                        <span class="loan-label">Final End Date:</span>
                        <span class="loan-value">{closest_loan['end_date']}</span>
                    </div>
                    <div class="loan-item">
                        <span class="loan-label">Days Remaining:</span>
                        <span class="loan-value days-remaining">{days_remaining%30} days</span>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="no-loans">
                <p>No active loans found or all loans have ended</p>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="no-loans">
            <p>No loans recorded yet. Add loans to track upcoming payments!</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
    <div>
        <h2 class="expense-header">Expense Summary Overview</h2>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="date-selector">
        <h3 class="date-selector-title">Select Date Range</h3>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("Start Date", value=datetime.today() - timedelta(days=30))
    with col2:
        end_date = st.date_input("End Date", value=datetime.today())
    
    if start_date > end_date:
        st.error("Start date must be before or equal to end date.")
        return

    all_expenses = load_json("data/expenses.json")
    user_expenses = [
        e for e in all_expenses
        if e.get("username") == st.session_state.user["username"]
    ]

    if not user_expenses:
        st.markdown("""
        <div class="no-expenses">
            <h4>No expenses recorded yet</h4>
            <p>Start tracking your expenses to see detailed analytics here!</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        for e in user_expenses:
            try:
                e["date"] = datetime.strptime(e["date"], "%Y-%m-%d")
            except ValueError:
                continue

        filtered_expenses = [
            e for e in user_expenses
            if start_date <= e["date"].date() <= end_date
        ]
        
        if filtered_expenses:
            totals = defaultdict(float)
            for e in filtered_expenses:
                totals[e["category"]] += float(e["amount"])
            
            if totals:
                total_amount = sum(totals.values())
                st.markdown(f"""
                <div class="total-spent">
                    <span class="total-amount">Total Spent: ₹{total_amount:.2f}</span>
                </div>
                """, unsafe_allow_html=True)
                
                for category, total in totals.items():
                    st.markdown(f"""
                    <div class="expense-item">
                        <span class="expense-category">{category}</span>
                        <span class="expense-amount">₹{total:.2f}</span>
                    </div>
                    """, unsafe_allow_html=True)
                
                categories = list(totals.keys())
                amounts = list(totals.values())
                fig = px.pie(
                    names=categories,
                    values=amounts,
                    title=f"Expense Distribution ({start_date.strftime('%m/%d/%Y')} - {end_date.strftime('%m/%d/%Y')})",
                    hole=0.4,
                    color_discrete_sequence=px.colors.qualitative.Set3
                )

                fig.update_layout(
                    plot_bgcolor='white',
                    paper_bgcolor='white',
                    font=dict(color='#2c3e50'),
                    title_font_size=16,
                    title_font_color='#2c3e50'
                )

                st.plotly_chart(fig, use_container_width=True)
            else:
                st.markdown("""
                <div class="no-expenses">
                    <p>No expenses recorded for this period</p>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="no-expenses">
                <p>No expenses found for the selected date range</p>
            </div>
            """, unsafe_allow_html=True)

    if st.button("Logout", key="logout_btn"):
        st.session_state.user = None
        st.session_state.page = "landing"
        st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)
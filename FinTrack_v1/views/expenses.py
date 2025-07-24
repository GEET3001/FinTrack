import streamlit as st
from components.utils import load_json, save_json
from datetime import date
import pandas as pd

EXPENSE_FILE = "data/expenses.json"

def show_expenses():
    if not st.session_state.user:
        st.warning("You must be logged in to view this page.")
        st.session_state.page = "landing"
        return

    apply_finance_theme()
    
    render_header()
    
    col1, col2 = st.columns([2, 3])
    
    with col1:
        add_transaction_form()
    
    with col2:
        display_expense_summary()
    
    display_transaction_history()
    
    render_navigation()

def apply_finance_theme():
    """Apply finance-themed styling"""
    st.markdown("""
    <style>
    /* Main Container */
    .main-container {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        padding: 20px;
        border-radius: 12px;
        margin-bottom: 20px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .main-title {
        color: white;
        text-align: center;
        font-size: 2.2rem;
        font-weight: 600;
        margin-bottom: 5px;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
    }
    
    .main-subtitle {
        color: #e8f4f8;
        text-align: center;
        font-size: 1rem;
        margin-bottom: 0;
        font-weight: 300;
    }
    
    .finance-card {
        background: white;
        padding: 24px;
        border-radius: 12px;
        box-shadow: 0 4px 24px rgba(0, 0, 0, 0.1);
        border: 1px solid #e1e8ed;
        margin-bottom: 20px;
    }
    
    .add-transaction-card {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        color: white;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .summary-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .history-card {
        background: white;
        border-left: 4px solid #1e3c72;
    }
    
    .form-header {
        font-size: 1.3rem;
        font-weight: 600;
        margin-bottom: 20px;
        color: white;
        text-align: center;
    }
    
    .section-header {
        font-size: 1.3rem;
        font-weight: 600;
        margin-bottom: 20px;
        color: #1e3c72;
        border-bottom: 2px solid #1e3c72;
        padding-bottom: 8px;
    }
    
    .stSelectbox > div > div {
        background-color: rgba(255, 255, 255, 0.95);
        border: 2px solid #e1e8ed;
        border-radius: 8px;
        transition: all 0.3s ease;
    }
    
    .stSelectbox > div > div:hover,
    .stSelectbox > div > div:focus {
        border-color: #1e3c72;
        box-shadow: 0 0 0 3px rgba(30, 60, 114, 0.1);
    }
    
    .stNumberInput > div > div > input {
        background-color: rgba(255, 255, 255, 0.95);
        border: 2px solid #e1e8ed;
        border-radius: 8px;
        transition: all 0.3s ease;
    }
    
    .stNumberInput > div > div > input:hover,
    .stNumberInput > div > div > input:focus {
        border-color: #1e3c72;
        box-shadow: 0 0 0 3px rgba(30, 60, 114, 0.1);
    }
    
    .stDateInput > div > div > input {
        background-color: rgba(255, 255, 255, 0.95);
        border: 2px solid #e1e8ed;
        border-radius: 8px;
        transition: all 0.3s ease;
    }
    
    .stDateInput > div > div > input:hover,
    .stDateInput > div > div > input:focus {
        border-color: #1e3c72;
        box-shadow: 0 0 0 3px rgba(30, 60, 114, 0.1);
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 12px 24px;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.3s ease;
        width: 100%;
        box-shadow: 0 4px 16px rgba(30, 60, 114, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 24px rgba(30, 60, 114, 0.4);
    }
    
    /* Summary Metrics */
    .metric-row {
        display: flex;
        justify-content: space-between;
        margin-bottom: 16px;
        color: white;
    }
    
    .metric-item {
        text-align: center;
        flex: 1;
        padding: 16px;
        background: rgba(255, 255, 255, 0.1);
        border-radius: 8px;
        margin: 0 8px;
        backdrop-filter: blur(10px);
    }
    
    .metric-value {
        font-size: 1.8rem;
        font-weight: 700;
        margin-bottom: 4px;
    }
    
    .metric-label {
        font-size: 0.9rem;
        opacity: 0.8;
    }
    
    .stDataFrame {
        background: white;
        border-radius: 8px;
        overflow: hidden;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    }
    
    .stSuccess {
        background: linear-gradient(135deg, #28a745 0%, #20c997 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 12px 16px;
        font-weight: 500;
    }
    
    .stWarning {
        background: linear-gradient(135deg, #ffc107 0%, #ffb3d1 100%);
        color: #332d2d;
        border: none;
        border-radius: 8px;
        padding: 12px 16px;
        font-weight: 500;
    }
    
    .stInfo {
        background: linear-gradient(135deg, #17a2b8 0%, #1e7e9f 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 12px 16px;
        font-weight: 500;
    }
    
    .category-badge {
        display: inline-block;
        padding: 4px 8px;
        border-radius: 16px;
        font-size: 0.8rem;
        font-weight: 500;
        margin-right: 8px;
    }
    
    .category-food { background: #ffeaa7; color: #6c5ce7; }
    .category-transport { background: #fd79a8; color: #2d3436; }
    .category-utilities { background: #a29bfe; color: #2d3436; }
    .category-entertainment { background: #fdc2c7; color: #2d3436; }
    .category-health { background: #82b3d3; color: #2d3436; }
    .category-other { background: #ddd; color: #2d3436; }
    
    .nav-button {
        background: linear-gradient(135deg, #6c5ce7 0%, #a29bfe 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 12px 24px;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.3s ease;
        width: 100%;
        box-shadow: 0 4px 16px rgba(108, 92, 231, 0.3);
    }
    </style>
    """, unsafe_allow_html=True)

def render_header():
    """Render the header section"""
    st.markdown("""
    <div class="main-container">
        <div class="main-title">Finance Expense Tracker</div>
        <div class="main-subtitle">Manage your expenses with professional insight</div>
    </div>
    """, unsafe_allow_html=True)

def add_transaction_form():
    """Render the add transaction form"""
    st.markdown("""
    <div class="finance-card add-transaction-card">
        <div class="form-header"> Add New Transaction</div>
    </div>
    """, unsafe_allow_html=True)
    
    category = st.selectbox(
        "Category",
        ["Food", "Transport", "Utilities", "Entertainment", "Health", "Other"],
        help="Select the expense category"
    )
    
    amount = st.number_input(
        "Amount ($)",
        min_value=0.0,
        format="%.2f",
        help="Enter the expense amount"
    )
    
    expense_date = st.date_input(
        "Date",
        value=date.today(),
        help="Select the expense date"
    )
    
    if st.button(" Add Transaction"):
        if amount == 0.0:
            st.warning(" Amount must be greater than zero.")
        else:
            new_transaction = {
                "username": st.session_state.user["username"],
                "category": category,
                "amount": amount,
                "date": str(expense_date)
            }
            all_expenses = load_json(EXPENSE_FILE)
            all_expenses.append(new_transaction)
            save_json(EXPENSE_FILE, all_expenses)
            st.success(" Transaction added successfully!")

def display_expense_summary():
    """Display expense summary metrics"""
    all_expenses = load_json(EXPENSE_FILE)
    user_expenses = [e for e in all_expenses if e["username"] == st.session_state.user["username"]]
    
    if user_expenses:
        total_amount = sum(float(e["amount"]) for e in user_expenses)
        transaction_count = len(user_expenses)
        avg_amount = total_amount / transaction_count if transaction_count > 0 else 0
        
        categories = {}
        for expense in user_expenses:
            category = expense["category"]
            categories[category] = categories.get(category, 0) + float(expense["amount"])
        
        most_used_category = max(categories, key=categories.get) if categories else "None"
        
        st.markdown("""
        <div class="finance-card summary-card">
            <div class="form-header">Financial Summary</div>
            <div class="metric-row">
                <div class="metric-item">
                    <div class="metric-value">%.2f</div>
                    <div class="metric-label">Total Spent</div>
                </div>
                <div class="metric-item">
                    <div class="metric-value">%d</div>
                    <div class="metric-label">Transactions</div>
                </div>
            </div>
            <div class="metric-row">
                <div class="metric-item">
                    <div class="metric-value">%.2f</div>
                    <div class="metric-label">Average</div>
                </div>
                <div class="metric-item">
                    <div class="metric-value">%s</div>
                    <div class="metric-label">Top Category</div>
                </div>
            </div>
        </div>
        """ % (total_amount, transaction_count, avg_amount, most_used_category), unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="finance-card summary-card">
            <div class="form-header"> Financial Summary</div>
            <div class="metric-row">
                <div class="metric-item">
                    <div class="metric-value">0.00</div>
                    <div class="metric-label">Total Spent</div>
                </div>
                <div class="metric-item">
                    <div class="metric-value">0</div>
                    <div class="metric-label">Transactions</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

def display_transaction_history():
    st.markdown("""
    <div class="finance-card history-card">
        <div class="section-header"> Transaction History</div>
    </div>
    """, unsafe_allow_html=True)
    
    all_expenses = load_json(EXPENSE_FILE)
    user_expenses = [e for e in all_expenses if e["username"] == st.session_state.user["username"]]
    
    if user_expenses:
        user_expenses.sort(key=lambda x: x["date"], reverse=True)
        
        df = pd.DataFrame(user_expenses)
        
        df['amount'] = df['amount'].apply(lambda x: f"{x:.2f}")
        df['date'] = pd.to_datetime(df['date']).dt.strftime('%Y-%m-%d')
        df['category'] = df['category'].apply(lambda x: f" {x}")
        
        df = df[['date', 'category', 'amount']]
        df.columns = ['Date', 'Category', 'Amount']
        
        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Date": st.column_config.DateColumn(
                    "Date",
                    format="YYYY-MM-DD",
                    width="small"
                ),
                "Category": st.column_config.TextColumn(
                    "Category",
                    width="medium"
                ),
                "Amount": st.column_config.TextColumn(
                    "Amount",
                    width="small"
                )
            }
        )
    else:
        st.info("No transactions found. Start by adding your first expense!")

def render_navigation():
    """Render navigation buttons"""
    st.markdown("<br>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        if st.button("Back to Dashboard", key="back_to_dashboard"):
            st.session_state.page = "dashboard"
            st.rerun()
import streamlit as st
from datetime import datetime
import random
from db import Database

class InvestmentPortfolio:
    def __init__(self):
        self.db = Database()

    def show(self):
        if not st.session_state.user:
            st.warning("You must be logged in to view this page.")
            st.session_state.page = "landing"
            return

        self._apply_theme()
        self._render_header()
        self._entry_form()
        self._show_holdings()
        self._render_back_button()

    def _apply_theme(self):
        st.markdown("""
        <style>
        .finance-container {
            background: #0f3460;
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
        .portfolio-summary {
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
        .profit-positive {
            color: #27ae60;
            font-weight: 600;
        }
        .profit-negative {
            color: #e74c3c;
            font-weight: 600;
        }
        .form-container {
            background: #f8f9fa;
            padding: 25px;
            border-radius: 8px;
            margin-bottom: 20px;
            border: 1px solid #dee2e6;
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
            transition: border-color 0.3s ease;
        }
        .stNumberInput > div > div:focus-within {
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
            transition: all 0.3s ease;
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
      
        .holdings-table {
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

    def _render_header(self):
        st.markdown("""
        <div class="finance-container">
            <div class="finance-title">Portfolio Management</div>
            <div class="finance-subtitle">Track and monitor your equity investments</div>
        </div>
        """, unsafe_allow_html=True)

    def _entry_form(self):
        col1, col2, col3 = st.columns(3)
        with col1:
            stock_name = st.text_input("Stock Symbol", placeholder="e.g., RELIANCE")
        with col2:
            buy_price = st.number_input("Purchase Price (₹)", min_value=0.0, format="%.2f")
        with col3:
            units = st.number_input("Quantity", min_value=1, step=1)

        if st.button("Add to Portfolio"):
            if not stock_name or buy_price <= 0 or units <= 0:
                st.warning("Please fill all fields with valid values.")
            else:
                username = st.session_state.user["username"]
                dt = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                self.db.execute(
                    "INSERT INTO investments (username, stock_name, buy_price, units, timestamp) VALUES (%s, %s, %s, %s, %s)",
                    (username, stock_name.upper(), buy_price, units, dt)
                )
                st.success(f"{stock_name.upper()} successfully added to portfolio!")
        st.markdown("</div></div>", unsafe_allow_html=True)

    def _show_holdings(self):
        st.markdown("""
        <div class="section-card">
            <div class="section-title">Current Holdings</div>
        """, unsafe_allow_html=True)
        username = st.session_state.user["username"]
        results = self.db.fetchall(
            "SELECT stock_name, buy_price, units, timestamp FROM investments WHERE username=%s",
            (username,)
        )

        if results:
            holdings = []
            total_invested = 0
            total_current_value = 0
            for entry in results:
                buy_price = float(entry["buy_price"])
                units = int(entry["units"])
                fluctuation = random.uniform(-0.05, 0.05)
                current_price = round(buy_price * (1 + fluctuation), 2)
                investment_cost = round(buy_price * units, 2)
                current_value = round(current_price * units, 2)
                pnl = round(current_value - investment_cost, 2)
                pnl_percentage = round((pnl / investment_cost) * 100, 2) if investment_cost else 0
                total_invested += investment_cost
                total_current_value += current_value
                holdings.append({
                    "Stock": entry["stock_name"],
                    "Buy Price": f"₹{buy_price:.2f}",
                    "Current Price": f"₹{current_price:.2f}",
                    "Quantity": units,
                    "Invested": f"₹{investment_cost:,.2f}",
                    "Current Value": f"₹{current_value:,.2f}",
                    "P&L": f"₹{pnl:,.2f} ({pnl_percentage:+.2f}%)"
                })
            total_pnl = total_current_value - total_invested
            portfolio_return = ((total_current_value - total_invested) / total_invested * 100) if total_invested > 0 else 0
            pnl_class = "profit-positive" if total_pnl >= 0 else "profit-negative"

            st.markdown(f"""
            <div class="portfolio-summary">
                <div class="summary-row">
                    <span class="summary-label">Total Holdings:</span>
                    <span class="summary-value">{len(holdings)} securities</span>
                </div>
                <div class="summary-row">
                    <span class="summary-label">Total Invested:</span>
                    <span class="summary-value">₹{total_invested:,.2f}</span>
                </div>
                <div class="summary-row">
                    <span class="summary-label">Current Value:</span>
                    <span class="summary-value">₹{total_current_value:,.2f}</span>
                </div>
                <div class="summary-row">
                    <span class="summary-label">Total P&L:</span>
                    <span class="summary-value {pnl_class}">₹{total_pnl:,.2f} ({portfolio_return:+.2f}%)</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            st.markdown('<div class="holdings-table">', unsafe_allow_html=True)
            st.dataframe(holdings, use_container_width=True, hide_index=True)
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.info("No investments in your portfolio yet. Add your first investment above.")
        st.markdown("</div>", unsafe_allow_html=True)

    def _render_back_button(self):
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("← Back to Dashboard"):
            st.session_state.page = "dashboard"
            st.rerun()

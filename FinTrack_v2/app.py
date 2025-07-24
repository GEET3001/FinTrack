import streamlit as st
import base64

from views.dashboard import Dashboard
from views.loans import LoansPage
from views.expenses import ExpenseTracker
from views.investments import InvestmentPortfolio
from components.auth import AuthManager  

if "auth" not in st.session_state:
    st.session_state.auth = AuthManager()
if "dashboard" not in st.session_state:
    st.session_state.dashboard = Dashboard()
if "loans" not in st.session_state:
    st.session_state.loans = LoansPage()
if "expenses" not in st.session_state:
    st.session_state.expenses = ExpenseTracker()
if "investments" not in st.session_state:
    st.session_state.investments = InvestmentPortfolio()

if "page" not in st.session_state:
    st.session_state.page = "landing"
if "user" not in st.session_state:
    st.session_state.user = None


class AppTheme:
    @staticmethod
    def set_background(image_file):
        with open(image_file, "rb") as f:
            encoded = base64.b64encode(f.read()).decode()
        css = f"""
        <style>
            .stApp {{
                background-image: url("data:image/jpg;base64,{encoded}");
                background-size: cover;
                background-position: center;
                background-repeat: no-repeat;
            }}
            
            
            
            .stApp > header [data-testid="stToolbar"] {{
                background: transparent !important;
            }}
            
            .main .block-container {{
                padding-top: 0rem !important;
                padding-bottom: 0rem !important;
                max-width: 100% !important;
            }}
            
            .stApp > div:first-child {{
                padding-top: 0 !important;
            }}
            
            .title {{
                font-size: 4rem;
                text-align: center;
                color: white;
                margin-top: 3rem;
                text-shadow: 3px 6px 8px rgba(0,0,0,0.7);
                font-weight: 700;
                letter-spacing: 3px;
                animation: fadeInDown 1.5s ease-out;
            }}
            
            .content {{
                font-size: 1.5rem;
                text-align: center;
                color: rgba(255,255,255,0.95);
                margin-top: 2rem;
                margin-bottom: 4rem;
                text-shadow: 2px 3px 6px rgba(0,0,0,0.6);
                font-weight: 400;
                letter-spacing: 1px;
                animation: fadeInUp 1.5s ease-out;
            }}
            
            .features-container {{
                display: flex;
                justify-content: center;
                gap: 2rem;
                margin: 3rem 0;
                animation: fadeIn 2s ease-out;
            }}
            
            .feature-item {{
                background: rgba(255,255,255,0.1);
                backdrop-filter: blur(10px);
                padding: 1.5rem;
                border-radius: 15px;
                border: 1px solid rgba(255,255,255,0.2);
                text-align: center;
                color: white;
                box-shadow: 0 8px 32px rgba(0,0,0,0.3);
                transition: all 0.3s ease;
            }}
            
            .feature-item:hover {{
                transform: translateY(-5px);
                box-shadow: 0 15px 45px rgba(0,0,0,0.4);
                background: rgba(255,255,255,0.15);
            }}
            
            .feature-icon {{
                font-size: 2.5rem;
                margin-bottom: 1rem;
                display: block;
            }}
            
            .feature-title {{
                font-size: 1.2rem;
                font-weight: 600;
                margin-bottom: 0.5rem;
                text-shadow: 1px 2px 4px rgba(0,0,0,0.5);
            }}
            
            .feature-desc {{
                font-size: 0.9rem;
                opacity: 0.9;
                text-shadow: 1px 1px 3px rgba(0,0,0,0.5);
            }}
            
            .button-container {{
                display: flex;
                justify-content: center;
                gap: 2rem;
                margin-top: 3rem;
                animation: fadeInUp 2s ease-out;
            }}
            
            .stButton > button {{
                background: linear-gradient(135deg, #2E8B57 0%, #228B22 100%);
                color: white;
                border: none;
                border-radius: 30px;
                padding: 15px 40px;
                font-size: 1.2rem;
                font-weight: 600;
                box-shadow: 0 8px 25px rgba(46, 139, 87, 0.4);
                transition: all 0.3s ease;
                text-transform: uppercase;
                letter-spacing: 1px;
                backdrop-filter: blur(10px);
                border: 2px solid rgba(255,255,255,0.2);
            }}
            
            .stButton > button:hover {{
                transform: translateY(-3px);
                box-shadow: 0 12px 35px rgba(46, 139, 87, 0.6);
                background: linear-gradient(135deg, #228B22 0%, #2E8B57 100%);
            }}
            
            .stButton > button:active {{
                transform: translateY(-1px);
            }}
            
            @keyframes fadeInDown {{
                from {{
                    opacity: 0;
                    transform: translateY(-50px);
                }}
                to {{
                    opacity: 1;
                    transform: translateY(0);
                }}
            }}
            
            @keyframes fadeInUp {{
                from {{
                    opacity: 0;
                    transform: translateY(50px);
                }}
                to {{
                    opacity: 1;
                    transform: translateY(0);
                }}
            }}
            
            @keyframes fadeIn {{
                from {{
                    opacity: 0;
                }}
                to {{
                    opacity: 1;
                }}
            }}
            
            @media (max-width: 768px) {{
                .title {{
                    font-size: 2.5rem;
                    margin-top: 2rem;
                }}
                
                .content {{
                    font-size: 1.2rem;
                    margin-bottom: 2rem;
                }}
                
                .features-container {{
                    flex-direction: column;
                    gap: 1rem;
                    margin: 2rem 1rem;
                }}
                
                .button-container {{
                    flex-direction: column;
                    gap: 1rem;
                    margin-top: 2rem;
                }}
            }}
            
            .overlay {{
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background: rgba(0,0,0,0.1);
                z-index: -1;
                pointer-events: none;
            }}
        </style>
        """
        st.markdown(css, unsafe_allow_html=True)


class LandingPage:
    @staticmethod
    def show():
        AppTheme.set_background("assets/background.jpg")
        st.markdown('<div class="overlay"></div>', unsafe_allow_html=True)
        st.markdown('<div class="title">FinTrack</div>', unsafe_allow_html=True)
        st.markdown('<div class="content">Your Personal Financial Management Hub</div>', unsafe_allow_html=True)
        st.markdown("""
        <div class="features-container">
            <div class="feature-item">
                <div class="feature-title">Expense Tracking</div>
                <div class="feature-desc">Monitor your daily expenses by category and date</div>
            </div>
            <div class="feature-item">
                <div class="feature-title">Investment Monitor</div>
                <div class="feature-desc">Track your stock portfolio and performance</div>
            </div>
            <div class="feature-item">
                <div class="feature-title">Loan Management</div>
                <div class="feature-desc">Keep track of EMIs and loan schedules</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown('<div class="button-container">', unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Login"):
                st.session_state.page = "login"
                st.rerun()
        with col2:
            if st.button("Sign Up"):
                st.session_state.page = "signup"
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)


def main():
    st.set_page_config(
        page_title="FinTrack",
        layout="wide",
        initial_sidebar_state="collapsed"
    )
    
    st.markdown("""
    <style>
    .main .block-container {
        padding-top: 0rem !important;
        max-width: 100% !important;
    }
    .stApp > header {
        background: transparent !important;
        height: 0rem !important;
    }
    .stApp > header [data-testid="stToolbar"] {
        display: none !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    if st.session_state.page == "landing":
        LandingPage.show()
    elif st.session_state.page == "login":
        st.session_state.auth.login_user()
    elif st.session_state.page == "signup":
        st.session_state.auth.signup_user()
    elif st.session_state.page == "dashboard":
        st.session_state.dashboard.show()
    elif st.session_state.page == "loans":
        st.session_state.loans.show()
    elif st.session_state.page == "expenses":
        st.session_state.expenses.show_expenses()
    elif st.session_state.page == "investments":
        st.session_state.investments.show()


if __name__ == "__main__":
    main()
import streamlit as st
from streamlit_option_menu import option_menu
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="Smart Expense Tracker",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Add logo and title
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.markdown("""
    <div style='text-align: center; margin-bottom: 2rem;'>
        <h1 style='color: #4CAF50; margin-bottom: 0.5rem;'>Smart Expense Tracker</h1>
        <p style='color: #666; margin-top: 0;'>Track, Analyze, and Optimize Your Spending</p>
    </div>
    """, unsafe_allow_html=True)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main {
        padding: 1rem 2rem 2rem 2rem;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        border-radius: 8px;
        padding: 0.5rem 1.5rem;
        font-weight: 500;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #45a049;
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    .stTextInput>div>div>input {
        border-radius: 8px;
        border: 1px solid #ddd;
        padding: 10px 15px;
    }
    .stSelectbox>div>div>div {
        border-radius: 8px;
    }
    .stNumberInput>div>div>input {
        border-radius: 8px;
    }
    .stDateInput>div>div>input {
        border-radius: 8px;
    }
    }
    .stSelectbox>div>div>div {
        border-radius: 5px;
    }
    </style>
""", unsafe_allow_html=True)

# Sidebar navigation
with st.sidebar:
    st.title("💰 Smart Expense Tracker")
    st.write("Track and analyze your expenses with ease")
    
    selected = option_menu(
        menu_title=None,
        options=["Add Expenses", "View Expenses", "Analytics", "AI Insights"],
        icons=["plus-circle", "table", "bar-chart", "robot"],
        default_index=0,
        styles={
            "container": {"padding": "0!important", "background-color": "#096723"},
            "icon": {"color": "orange", "font-size": "18px"}, 
            "nav-link": {"font-size": "16px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
            "nav-link-selected": {"background-color": "#4CAF50"},
        },
    )

# Streamlit will automatically handle the page routing based on the file names in the pages directory
# No need for explicit imports or routing here

# Add a footer
st.sidebar.markdown("---")
st.sidebar.markdown("### Database")

# Initialize session state for confirmation
if 'show_clear_confirm' not in st.session_state:
    st.session_state.show_clear_confirm = False

# Add Clear All Data button with confirmation
if st.sidebar.button("⚠️ Clear All Data"):
    st.session_state.show_clear_confirm = True

if st.session_state.show_clear_confirm:
    st.sidebar.warning("This will delete ALL your expense and category data. This action cannot be undone!")
    col1, col2 = st.sidebar.columns(2)
    if col1.button("❌ Yes, Delete All"):
        from utils.database import clear_all_data
        clear_all_data()
        st.session_state.show_clear_confirm = False
        st.sidebar.success("All data has been cleared successfully!")
        st.rerun()
    if col2.button("✅ Cancel"):
        st.session_state.show_clear_confirm = False
        st.rerun()

st.sidebar.markdown("---")
st.sidebar.markdown("### About")
st.sidebar.info(
    "Smart Expense Tracker helps you track and analyze your spending habits. "
    "Built with ❤️ using Streamlit."
)

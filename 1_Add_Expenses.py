import streamlit as st
import pandas as pd
from datetime import datetime, date as dt_date
from utils.database import (
    add_expense, get_categories, add_category, 
    delete_expense, get_expenses, update_expense, 
    get_expense_by_id
)
from utils.config import CURRENCY, DEFAULT_PAYMENT_METHODS, DATE_FORMAT

# Page configuration
st.set_page_config(page_title="Expense Tracker", layout="wide")

# Custom CSS for better styling
st.markdown("""
    <style>
    .main {
        max-width: 1200px;
        padding: 2rem;
    }
    .expense-card {
        border-left: 4px solid #4CAF50;
        padding: 1rem;
        margin-bottom: 1rem;
        border-radius: 0.5rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .expense-amount {
        font-size: 1.2rem;
        font-weight: bold;
        color: #2E7D32;
    }
    .expense-category {
        font-weight: 500;
        color: #424242;
    }
    .expense-date {
        color: #757575;
        font-size: 0.9rem;
    }
    .action-button {
        margin: 0.2rem;
    }
    .form-section {
        background-color: #f8f9fa;
        padding: 1.5rem;
        border-radius: 0.5rem;
        margin-bottom: 2rem;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'form_data' not in st.session_state:
    st.session_state.form_data = {
        'id': None,
        'amount': '',
        'category': '',
        'payment_method': DEFAULT_PAYMENT_METHODS[0],
        'description': '',
        'date': dt_date.today().strftime(DATE_FORMAT),
        'is_editing': False
    }

# Get existing categories
existing_categories = get_categories()

# Common expense categories
COMMON_CATEGORIES = [
    'Food & Dining', 'Shopping', 'Transportation', 'Housing',
    'Bills & Utilities', 'Entertainment', 'Healthcare', 'Education',
    'Travel', 'Groceries', 'Personal Care', 'Gifts & Donations',
    'Investments', 'Insurance', 'Others'
]

# Combine and sort categories
ALL_CATEGORIES = sorted(list(set(COMMON_CATEGORIES + existing_categories)))

# Helper Functions
def reset_form():
    """Reset the form to its default state"""
    st.session_state.form_data = {
        'id': None,
        'amount': '',
        'category': '',
        'payment_method': DEFAULT_PAYMENT_METHODS[0],
        'description': '',
        'date': datetime.now().strftime(DATE_FORMAT),
        'is_editing': False
    }
    # Don't directly modify widget state here as it causes issues

def load_expense_for_editing(expense_id):
    """Load expense data into the form for editing"""
    expense = get_expense_by_id(expense_id)
    if expense:
        st.session_state.form_data = {
            'id': expense['id'],
            'amount': float(expense['amount']),
            'category': expense['category'],
            'payment_method': expense['payment_method'],
            'description': expense['description'] or '',
            'date': expense['date'],
            'is_editing': True
        }
        st.rerun()

def handle_expense_submission():
    """Handle form submission for both add and update operations"""
    form_data = st.session_state.form_data
    
    # Validate inputs
    if not form_data['amount'] or float(form_data['amount']) <= 0:
        st.error("Please enter a valid amount greater than zero.")
        return False
        
    if not form_data['category'].strip():
        st.error("Please select a category.")
        return False
    
    try:
        if form_data['is_editing']:
            # Update existing expense
            success = update_expense(
                expense_id=form_data['id'],
                amount=float(form_data['amount']),
                category_name=form_data['category'].strip(),
                payment_method=form_data['payment_method'],
                description=form_data['description'],
                date=form_data['date']
            )
            if success:
                st.success("✅ Expense updated successfully!")
                return True
            else:
                st.error("Failed to update expense.")
                return False
        else:
            # Add new expense
            expense_id = add_expense(
                amount=float(form_data['amount']),
                category_name=form_data['category'].strip(),
                payment_method=form_data['payment_method'],
                description=form_data['description'],
                date=form_data['date']
            )
            if expense_id:
                # Don't show success message here, we'll show it after reset
                return True
            else:
                st.error("Failed to add expense.")
                return False
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        return False

# Main Layout
st.title("💰 Expense Manager")
st.write("Track and manage your expenses in one place.")

# Form Section
with st.container():
    st.subheader("➕ Add/Edit Expense")
    with st.form("expense_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            # Amount
            amount = st.number_input(
                f"Amount ({CURRENCY}) *",
                min_value=0.0,
                step=0.01,
                format="%.2f",
                value=float(st.session_state.form_data['amount']) if st.session_state.form_data['amount'] else 0.0,
                key="form_amount"
            )
            
            # Date
            expense_date = st.date_input(
                "Date *",
                value=datetime.strptime(st.session_state.form_data['date'], DATE_FORMAT).date() 
                    if st.session_state.form_data['date'] else dt_date.today(),
                key="form_date"
            )
            
            # Payment Method
            payment_method = st.selectbox(
                "Payment Method *",
                options=DEFAULT_PAYMENT_METHODS,
                index=DEFAULT_PAYMENT_METHODS.index(st.session_state.form_data['payment_method']) 
                    if st.session_state.form_data['payment_method'] in DEFAULT_PAYMENT_METHODS else 0,
                key="form_payment_method"
            )
        
        with col2:
            # Category with new category option
            category_col1, category_col2 = st.columns([3, 1])
            with category_col1:
                category = st.selectbox(
                    "Category *",
                    options=[""] + ALL_CATEGORIES + ["+ Add New Category"],
                    index=0 if not st.session_state.form_data.get('category') else 
                        (ALL_CATEGORIES.index(st.session_state.form_data['category']) + 1 
                         if st.session_state.form_data['category'] in ALL_CATEGORIES 
                         else len(ALL_CATEGORIES) + 1),
                    format_func=lambda x: "Select a category" if x == "" else x,
                    key="form_category"
                )
            
            # New category input (shown when "+ Add New Category" is selected)
            if category == "+ Add New Category":
                new_category = st.text_input("New Category Name", key="new_category")
                if new_category.strip():
                    category = new_category.strip()
            
            # Description
            description = st.text_area(
                "Description",
                value=st.session_state.form_data.get('description', ''),
                placeholder="Add any additional details...",
                key="form_description"
            )
        
        # Form buttons
        col1, col2, _ = st.columns([1, 1, 3])
        
        with col1:
            submit_button = st.form_submit_button(
                "💾 Update Expense" if st.session_state.form_data.get('is_editing') else "💾 Add Expense",
                type="primary",
                use_container_width=True
            )
        
        with col2:
            if st.session_state.form_data.get('is_editing'):
                if st.form_submit_button("❌ Cancel", type="secondary", use_container_width=True):
                    reset_form()
                    st.rerun()
        
        # Handle form submission
        if submit_button:
            # Update form data in session state
            st.session_state.form_data.update({
                'amount': amount,
                'category': category if category != "+ Add New Category" else new_category,
                'payment_method': payment_method,
                'description': description,
                'date': expense_date.strftime(DATE_FORMAT)
            })
            
            if handle_expense_submission():
                # Reset form data before rerun
                reset_form()
                
                # Show success message and rerun
                st.success("✅ Expense added successfully!")
                st.rerun()

# Recent Expenses Section
st.markdown("---")
st.subheader("📋 Recent Expenses")

# Get and display recent expenses
try:
    # Get all expenses and then limit to last 10 in Python
    all_expenses = get_expenses()
    expenses = all_expenses.sort_values('date', ascending=False).head(10)
    
    if not expenses.empty:
        # Display expenses as cards
        for _, expense in expenses.iterrows():
            with st.container():
                cols = st.columns([1, 2, 2, 2, 3, 2])
                
                # Date
                with cols[0]:
                    exp_date = expense['date']
                    if isinstance(exp_date, str):
                        exp_date = datetime.strptime(exp_date, DATE_FORMAT)
                    st.markdown(f"<div class='expense-date'>{exp_date.strftime('%b %d, %Y')}</div>", unsafe_allow_html=True)
                
                # Category
                with cols[1]:
                    st.markdown(f"<div class='expense-category'>{expense['category']}</div>", unsafe_allow_html=True)
                
                # Amount
                with cols[2]:
                    st.markdown(f"<div class='expense-amount'>{CURRENCY}{float(expense['amount']):.2f}</div>", unsafe_allow_html=True)
                
                # Payment Method
                with cols[3]:
                    st.text(expense['payment_method'])
                
                # Description (truncated if too long)
                with cols[4]:
                    desc = expense.get('description', '')
                    st.text(desc[:30] + "..." if len(str(desc)) > 30 else desc)
                
                # Action Buttons
                with cols[5]:
                    btn_col1, btn_col2 = st.columns(2)
                    with btn_col1:
                        if st.button("✏️", key=f"edit_{expense['id']}", help="Edit this expense"):
                            load_expense_for_editing(expense['id'])
                    
                    with btn_col2:
                        if st.button("🗑️", key=f"delete_{expense['id']}", help="Delete this expense"):
                            if delete_expense(expense['id']):
                                st.success("Expense deleted successfully!")
                                st.rerun()
                            else:
                                st.error("Failed to delete expense.")
                
                st.divider()
        
        # View All Expenses button
        if st.button("📊 View All Expenses", use_container_width=True):
            st.switch_page("pages/2_View_Expenses.py")
    
    else:
        st.info("No expenses recorded yet. Add your first expense using the form above!")

except Exception as e:
    st.error(f"Error loading expenses: {str(e)}")

# Add some stats at the bottom
try:
    st.markdown("---")
    st.subheader("📊 Quick Stats")
    
    today = dt_date.today().strftime(DATE_FORMAT)
    month_start = dt_date.today().replace(day=1).strftime(DATE_FORMAT)
    
    # Get today's and this month's expenses
    all_expenses = get_expenses()
    
    if not all_expenses.empty:
        # Convert date strings to datetime for comparison
        all_expenses['date'] = pd.to_datetime(all_expenses['date']).dt.date
        
        # Today's total
        today_total = all_expenses[all_expenses['date'] == dt_date.today()]['amount'].sum()
        
        # This month's total
        month_total = all_expenses[
            (all_expenses['date'] >= dt_date.today().replace(day=1)) &
            (all_expenses['date'] <= dt_date.today())
        ]['amount'].sum()
        
        # Total expenses
        total_expenses = all_expenses['amount'].sum()
        
        # Display metrics
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Today's Total", f"{CURRENCY}{today_total:.2f}")
        
        with col2:
            st.metric("This Month", f"{CURRENCY}{month_total:.2f}")
        
        with col3:
            st.metric("All Time Total", f"{CURRENCY}{total_expenses:.2f}")
    
    else:
        st.info("No expense data available yet.")

except Exception as e:
    st.error(f"Error loading stats: {str(e)}")

# Initialize session state on first run
if 'initialized' not in st.session_state:
    reset_form()
    st.session_state.initialized = True

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from utils.database import get_expenses, get_categories, delete_expense
from utils.config import CURRENCY, DATE_FORMAT

# Page configuration
st.title("📋 View Expenses")
st.write("View and manage your expense history.")

# Get all categories for filtering
all_categories = ["All"] + get_categories()

# Date range filter
col1, col2, col3 = st.columns([1, 1, 1])

with col1:
    # Default to first day of current month
    default_start = datetime.now().replace(day=1).strftime(DATE_FORMAT)
    start_date = st.date_input(
        "From",
        value=datetime.strptime(default_start, DATE_FORMAT) if default_start else datetime.now() - timedelta(days=30)
    )

with col2:
    end_date = st.date_input("To", value=datetime.now())

with col3:
    selected_category = st.selectbox("Category", all_categories)

# Convert dates to string format for database query
start_date_str = start_date.strftime(DATE_FORMAT)
end_date_str = end_date.strftime(DATE_FORMAT)

# Get filtered expenses
df = get_expenses(
    start_date=start_date_str,
    end_date=end_date_str,
    category=selected_category if selected_category != "All" else None
)

# Display summary stats
if not df.empty:
    total_spent = df['amount'].sum()
    avg_per_day = total_spent / ((end_date - start_date).days + 1)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Expenses", f"{CURRENCY}{total_spent:,.2f}")
    with col2:
        st.metric("Average per Day", f"{CURRENCY}{avg_per_day:,.2f}")
    with col3:
        st.metric("Number of Transactions", len(df))
    
    # Add a divider
    st.markdown("---")

# Display the data table
if not df.empty:
    # Format the display
    df_display = df.copy()
    df_display['amount'] = df_display['amount'].apply(lambda x: f"{CURRENCY}{x:.2f}")
    
    # Reorder columns for better display
    df_display = df_display[['date', 'amount', 'category', 'payment_method', 'description']]
    
    # Display the table with some styling
    st.dataframe(
        df_display,
        use_container_width=True,
        hide_index=True,
        column_config={
            "date": st.column_config.DateColumn("Date", format="YYYY-MM-DD"),
            "amount": st.column_config.NumberColumn("Amount", format=f"{CURRENCY}%.2f"),
            "category": "Category",
            "payment_method": "Payment Method",
            "description": "Description"
        }
    )
    
    # Add export button
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Export as CSV",
        data=csv,
        file_name=f"expenses_{start_date_str}_to_{end_date_str}.csv",
        mime="text/csv"
    )
    
    # Add a button to go back to add expenses
    if st.button("➕ Add New Expense"):
        st.experimental_set_query_params(page="1_Add_Expenses")
        st.rerun()
    
else:
    st.info("No expenses found for the selected filters.")
    
    # Add a button to go back to add expenses
    if st.button("➕ Add Your First Expense"):
        st.experimental_set_query_params(page="1_Add_Expenses")
        st.rerun()

def main():
    pass  # All the code is executed when the module is imported

if __name__ == "__main__":
    main()

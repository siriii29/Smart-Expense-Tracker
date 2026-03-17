import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
import numpy as np
from utils.database import get_expenses, get_expense_summary
from utils.config import CURRENCY, DATE_FORMAT

def get_insight_messages(filtered_df, total_spent, avg_daily_spend, top_category, top_category_amount):
    messages = []
    
    # 1. Overall spending insight
    daily_avg = filtered_df.groupby('date')['amount'].sum().mean()
    if daily_avg > avg_daily_spend * 1.2:
        messages.append({
            'text': f"⚠️ Your daily spending (${daily_avg:,.2f}) is {((daily_avg/avg_daily_spend)-1)*100:.1f}% higher than usual. Consider reviewing your recent expenses.",
            'type': 'warning'
        })
    
    # 2. Category analysis
    category_spending = filtered_df.groupby('category')['amount'].sum()
    top_3_categories = category_spending.nlargest(3)
    
    for i, (category, amount) in enumerate(top_3_categories.items(), 1):
        pct_of_total = (amount / total_spent) * 100
        if pct_of_total > 40:
            messages.append({
                'text': f"🚨 {category} accounts for {pct_of_total:.1f}% of your total spending. This seems high - you might want to review expenses in this category.",
                'type': 'danger'
            })
        else:
            messages.append({
                'text': f"📊 {i}. {category}: {CURRENCY}{amount:,.2f} ({pct_of_total:.1f}% of total)",
                'type': 'info'
            })
    
    # 3. Monthly trend analysis
    monthly_spending = filtered_df.groupby(filtered_df['date'].dt.to_period('M'))['amount'].sum()
    if len(monthly_spending) > 1:
        monthly_change = ((monthly_spending.iloc[-1] - monthly_spending.iloc[-2]) / monthly_spending.iloc[-2]) * 100
        if monthly_change > 20:
            messages.append({
                'text': f"📈 Your spending increased by {monthly_change:.1f}% compared to last month. Be mindful of this trend.",
                'type': 'warning' if monthly_change > 50 else 'info'
            })
    
    # 4. Large transactions
    large_transactions = filtered_df[filtered_df['amount'] > (filtered_df['amount'].median() * 5)]
    if not large_transactions.empty:
        messages.append({
            'text': f"💸 You had {len(large_transactions)} large transactions (over {CURRENCY}{filtered_df['amount'].median() * 5:,.2f} each). Review these for potential savings.",
            'type': 'warning'
        })
    
    # 5. Positive reinforcement
    savings_categories = ['savings', 'investment']
    for cat in savings_categories:
        if cat in [c.lower() for c in filtered_df['category'].unique()]:
            saved = filtered_df[filtered_df['category'].str.lower() == cat.lower()]['amount'].sum()
            messages.append({
                'text': f"✅ Great job! You've saved/invested {CURRENCY}{saved:,.2f} in {cat.capitalize()}.",
                'type': 'success'
            })
    
    return messages

# Page configuration
st.title("🤖 AI Insights")
st.write("Get personalized insights and recommendations about your spending habits.")

# Get expense data
df = get_expenses()
summary = get_expense_summary()

# Display summary cards
if not df.empty:
    # Convert date to datetime and sort
    df['date'] = pd.to_datetime(df['date'])
    df = df.sort_values('date')
    
    # Calculate metrics
    total_spent = df['amount'].sum()
    avg_daily_spend = df.groupby('date')['amount'].sum().mean()
    top_category = df.groupby('category')['amount'].sum().idxmax()
    top_category_amount = df.groupby('category')['amount'].sum().max()
    
    # Display metrics
    st.subheader("📊 Spending Overview")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Spent", f"{CURRENCY}{total_spent:,.2f}")
    with col2:
        st.metric("Avg. Daily Spend", f"{CURRENCY}{avg_daily_spend:,.2f}")
    with col3:
        st.metric("Top Category", f"{top_category}", f"{CURRENCY}{top_category_amount:,.2f}")
    
    # Add a divider
    st.markdown("---")
    
    # Interactive date range selector
    st.subheader("📅 Filter by Date Range")
    min_date = df['date'].min().date()
    max_date = df['date'].max().date()
    
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("Start date", min_value=min_date, max_value=max_date, value=min_date)
    with col2:
        end_date = st.date_input("End date", min_value=min_date, max_value=max_date, value=max_date)
    
    # Filter data based on date range
    mask = (df['date'].dt.date >= start_date) & (df['date'].dt.date <= end_date)
    filtered_df = df[mask]
    
    if not filtered_df.empty:
        # Calculate filtered metrics
        filtered_total = filtered_df['amount'].sum()
        filtered_avg = filtered_df.groupby('date')['amount'].sum().mean()
        
        # Display filtered metrics
        st.metric("Total in Selected Period", f"{CURRENCY}{filtered_total:,.2f}", 
                 delta=f"{CURRENCY}{(filtered_total / len(filtered_df['date'].unique()) - avg_daily_spend):,.2f} vs average daily")
        
        # Generate and display insights
        st.subheader("🔍 AI-Powered Insights")
        insights = get_insight_messages(filtered_df, filtered_total, avg_daily_spend, top_category, top_category_amount)
        
        for insight in insights:
            if insight['type'] == 'danger':
                st.error(insight['text'])
            elif insight['type'] == 'warning':
                st.warning(insight['text'])
            elif insight['type'] == 'success':
                st.success(insight['text'])
            else:
                st.info(insight['text'])
        
        st.markdown("---")
        
        # Category breakdown
        st.subheader("📈 Spending by Category")
        category_df = filtered_df.groupby('category')['amount'].sum().reset_index().sort_values('amount', ascending=False)
        
        # Create a bar chart
        fig = px.bar(
            category_df, 
            x='category', 
            y='amount',
            labels={'amount': 'Amount Spent', 'category': 'Category'},
            color='amount',
            color_continuous_scale='Blues'
        )
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
        
        # Monthly trend
        st.subheader("📅 Monthly Spending Trend")
        monthly_df = filtered_df.copy()
        monthly_df['month'] = monthly_df['date'].dt.to_period('M').astype(str)
        monthly_totals = monthly_df.groupby('month')['amount'].sum().reset_index()
        
        fig = px.line(
            monthly_totals, 
            x='month', 
            y='amount',
            labels={'amount': 'Total Spent', 'month': 'Month'},
            markers=True
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Top expenses table
        st.subheader("💸 Top 10 Largest Expenses")
        top_expenses = filtered_df.nlargest(10, 'amount')[['date', 'category', 'description', 'amount']]
        top_expenses['date'] = top_expenses['date'].dt.strftime('%Y-%m-%d')
        st.dataframe(
            top_expenses,
            column_config={
                "date": "Date",
                "category": "Category",
                "description": "Description",
                "amount": st.column_config.NumberColumn(
                    "Amount",
                    format=f"{CURRENCY}%.2f"
                )
            },
            hide_index=True,
            use_container_width=True
        )
        
        # Spending by day of week
        st.subheader("📆 Spending by Day of Week")
        day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        daily_df = filtered_df.copy()
        daily_df['day_of_week'] = daily_df['date'].dt.day_name()
        daily_totals = daily_df.groupby('day_of_week')['amount'].sum().reindex(day_order).reset_index()
        
        fig = px.bar(
            daily_totals,
            x='day_of_week',
            y='amount',
            labels={'amount': 'Total Spent', 'day_of_week': 'Day of Week'},
            color='amount',
            color_continuous_scale='Greens'
        )
        st.plotly_chart(fig, use_container_width=True)
        
    else:
        st.warning("No data available for the selected date range.")
    
    # Add a button to go to analytics
    st.markdown("---")
    if st.button("📊 View Detailed Analytics"):
        st.experimental_set_query_params(page="3_Analytics")
        st.rerun()

else:
    st.info("No expense data available. Start by adding some expenses to see insights!")
    
    # Add a button to go to add expenses
    if st.button("➕ Add Your First Expense"):
        st.experimental_set_query_params(page="1_Add_Expenses")
        st.rerun()

def main():
    pass  # All the code is executed when the module is imported

if __name__ == "__main__":
    main()

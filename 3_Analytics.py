import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
from utils.database import get_expenses, get_expense_summary
from utils.config import CURRENCY, DATE_FORMAT, CHART_COLORS

# Page configuration
st.title("📊 Analytics")
st.write("Visualize your spending patterns and gain insights.")

# Get expense summary data
summary = get_expense_summary()

# Display summary cards
if summary['total_expenses'] > 0:
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Expenses", f"{CURRENCY}{summary['total_expenses']:,.2f}")
    
    with col2:
        if summary['monthly_spending']:
            current_month = summary['monthly_spending'][0]['total']
            prev_month = summary['monthly_spending'][1]['total'] if len(summary['monthly_spending']) > 1 else 0
            change = ((current_month - prev_month) / prev_month * 100) if prev_month > 0 else 0
            st.metric(
                "This Month", 
                f"{CURRENCY}{current_month:,.2f}",
                f"{change:+.1f}% vs last month"
            )
    
    with col3:
        if summary['top_categories']:
            top_category = summary['top_categories'][0]
            st.metric("Top Category", f"{top_category['category']}", f"{CURRENCY}{top_category['total']:,.2f}")

# Add a divider
st.markdown("---")

# Get all expenses for analysis
df = get_expenses()

if not df.empty:
    # Convert date to datetime
    df['date'] = pd.to_datetime(df['date'])
    
    # Create tabs for different visualizations
    tab1, tab2, tab3 = st.tabs(["📈 Trends", "🍕 Categories", "💳 Payment Methods"])
    
    with tab1:
        st.subheader("Monthly Spending Trend")
        
        # Group by month and calculate total spending
        df_monthly = df.copy()
        df_monthly['month'] = df_monthly['date'].dt.to_period('M').astype(str)
        monthly_totals = df_monthly.groupby('month')['amount'].sum().reset_index()
        
        # Create line chart
        fig = px.line(
            monthly_totals, 
            x='month', 
            y='amount',
            labels={'amount': 'Amount', 'month': 'Month'},
            title="Monthly Spending Trend"
        )
        
        # Add bar chart for monthly totals
        fig.add_bar(
            x=monthly_totals['month'],
            y=monthly_totals['amount'],
            name="Monthly Total",
            marker_color=CHART_COLORS[0]
        )
        
        # Update layout
        fig.update_layout(
            xaxis_title="Month",
            yaxis_title=f"Amount ({CURRENCY})",
            hovermode="x unified",
            showlegend=False
        )
        
        # Display the chart
        st.plotly_chart(fig, use_container_width=True)
        
        # Add daily spending trend for the current month
        st.subheader("Daily Spending This Month")
        
        # Filter for current month
        current_month = datetime.now().strftime("%Y-%m")
        df_current_month = df[df['date'].dt.strftime("%Y-%m") == current_month].copy()
        
        if not df_current_month.empty:
            # Group by day
            df_daily = df_current_month.groupby('date')['amount'].sum().reset_index()
            
            # Create a complete date range for the current month
            start_date = datetime.now().replace(day=1)
            end_date = (start_date + timedelta(days=32)).replace(day=1) - timedelta(days=1)
            date_range = pd.date_range(start=start_date, end=end_date, freq='D')
            
            # Create a DataFrame with all dates and merge with actual data
            df_all_dates = pd.DataFrame({'date': date_range})
            df_daily = df_all_dates.merge(df_daily, on='date', how='left').fillna(0)
            
            # Create bar chart for daily spending
            fig_daily = px.bar(
                df_daily,
                x='date',
                y='amount',
                labels={'amount': 'Amount', 'date': 'Date'},
                title=f"Daily Spending - {datetime.now().strftime('%B %Y')}"
            )
            
            # Add a line for 7-day moving average
            df_daily['7_day_avg'] = df_daily['amount'].rolling(window=7, min_periods=1).mean()
            fig_daily.add_scatter(
                x=df_daily['date'],
                y=df_daily['7_day_avg'],
                mode='lines',
                name='7-Day Avg',
                line=dict(color='red', width=2)
            )
            
            # Update layout
            fig_daily.update_layout(
                xaxis_title="Date",
                yaxis_title=f"Amount ({CURRENCY})",
                hovermode="x unified"
            )
            
            st.plotly_chart(fig_daily, use_container_width=True)
    
    with tab2:
        st.subheader("Spending by Category")
        
        # Group by category
        category_totals = df.groupby('category')['amount'].sum().reset_index()
        category_totals = category_totals.sort_values('amount', ascending=False)
        
        # Create two columns for the charts
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # Create treemap
            fig_treemap = px.treemap(
                category_totals,
                path=['category'],
                values='amount',
                title="Spending Distribution by Category"
            )
            st.plotly_chart(fig_treemap, use_container_width=True)
        
        with col2:
            # Create donut chart
            fig_donut = px.pie(
                category_totals,
                values='amount',
                names='category',
                hole=0.4,
                title="Spending by Category"
            )
            fig_donut.update_traces(
                textposition='inside',
                textinfo='percent+label',
                hovertemplate="%{label}<br>%{value:,.2f} (%{percent})"
            )
            st.plotly_chart(fig_donut, use_container_width=True)
        
        # Add bar chart for category spending over time
        st.subheader("Category Trends")
        
        # Group by month and category
        df_cat_monthly = df.copy()
        df_cat_monthly['month'] = df_cat_monthly['date'].dt.to_period('M').astype(str)
        category_monthly = df_cat_monthly.groupby(['month', 'category'])['amount'].sum().reset_index()
        
        # Get top 5 categories by total spending
        top_categories = df.groupby('category')['amount'].sum().nlargest(5).index.tolist()
        
        # Filter to only show top categories
        category_monthly_top = category_monthly[category_monthly['category'].isin(top_categories)]
        
        # Create line chart for category trends
        fig_cat_trend = px.line(
            category_monthly_top,
            x='month',
            y='amount',
            color='category',
            title="Monthly Spending by Top Categories",
            labels={'amount': f'Amount ({CURRENCY})', 'month': 'Month'}
        )
        
        # Update layout
        fig_cat_trend.update_layout(
            xaxis_title="Month",
            yaxis_title=f"Amount ({CURRENCY})",
            hovermode="x unified",
            legend_title="Category"
        )
        
        st.plotly_chart(fig_cat_trend, use_container_width=True)
    
    with tab3:
        st.subheader("Spending by Payment Method")
        
        # Group by payment method
        payment_totals = df.groupby('payment_method')['amount'].sum().reset_index()
        payment_totals = payment_totals.sort_values('amount', ascending=False)
        
        # Create two columns for the charts
        col1, col2 = st.columns(2)
        
        with col1:
            # Create bar chart
            fig_bar = px.bar(
                payment_totals,
                x='payment_method',
                y='amount',
                title="Total Spending by Payment Method",
                labels={'amount': f'Amount ({CURRENCY})', 'payment_method': 'Payment Method'}
            )
            st.plotly_chart(fig_bar, use_container_width=True)
        
        with col2:
            # Create pie chart
            fig_pie = px.pie(
                payment_totals,
                values='amount',
                names='payment_method',
                title="Payment Method Distribution"
            )
            fig_pie.update_traces(
                textposition='inside',
                textinfo='percent+label',
                hovertemplate="%{label}<br>%{value:,.2f} (%{percent})"
            )
            st.plotly_chart(fig_pie, use_container_width=True)
        
        # Add time series of payment methods
        st.subheader("Payment Method Trends")
        
        # Group by month and payment method
        df_payment_monthly = df.copy()
        df_payment_monthly['month'] = df_payment_monthly['date'].dt.to_period('M').astype(str)
        payment_monthly = df_payment_monthly.groupby(['month', 'payment_method'])['amount'].sum().reset_index()
        
        # Create line chart for payment method trends
        fig_payment_trend = px.line(
            payment_monthly,
            x='month',
            y='amount',
            color='payment_method',
            title="Monthly Spending by Payment Method",
            labels={'amount': f'Amount ({CURRENCY})', 'month': 'Month'}
        )
        
        # Update layout
        fig_payment_trend.update_layout(
            xaxis_title="Month",
            yaxis_title=f"Amount ({CURRENCY})",
            hovermode="x unified",
            legend_title="Payment Method"
        )
        
        st.plotly_chart(fig_payment_trend, use_container_width=True)

else:
    st.info("No expense data available. Start by adding some expenses to see analytics!")
    
    # Add a button to go to analytics
    if st.button("📊 View Detailed Analytics"):
        st.experimental_set_query_params(page="3_Analytics")
        st.rerun()

def main():
    pass  # All the code is executed when the module is imported

if __name__ == "__main__":
    main()

# 🚀 AI-Powered Smart Expense Tracker

<div align="center">
  <img src="https://img.shields.io/badge/Python-3.8%2B-blue" alt="Python 3.8+">
  <img src="https://img.shields.io/badge/Streamlit-FF4B4B?style=flat&logo=streamlit&logoColor=white" alt="Streamlit">
  <img src="https://img.shields.io/badge/OpenAI-412991?style=flat&logo=openai&logoColor=white" alt="OpenAI">
  <a href="https://github.com/dandekarsiddique03/AI-Based-Smart-Expense-Tracker">
    <img src="https://img.shields.io/github/stars/dandekarsiddique03/AI-Based-Smart-Expense-Tracker?style=social" alt="GitHub Stars">
  </a>
</div>

A powerful, AI-driven expense tracking application that helps you monitor your spending patterns, generate insightful analytics, and receive personalized financial advice using OpenAI's GPT model. Built with Streamlit for a beautiful, responsive interface.

## Features

- **Add Expenses**: Record your expenses with details like date, category, amount, payment method, and description.
- **View Expenses**: Browse and filter your expense history in a clean tabular format with sorting and export options.
- **Analytics**: Visualize your spending patterns with interactive charts and graphs.
- **AI Insights**: Get personalized spending insights and recommendations powered by OpenAI's GPT model.

## Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/expense-tracker.git
   cd expense-tracker
   ```

2. Create a virtual environment (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: .\venv\Scripts\activate
   ```

3. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Start the Streamlit application:
   ```bash
   streamlit run app.py
   ```

2. Open your web browser and navigate to `http://localhost:8501`

3. Start adding your expenses and exploring the analytics!

## 🛠️ Tech Stack

- **Frontend**: Streamlit
- **Backend**: Python 3.8+
- **Database**: SQLite
- **AI/ML**: OpenAI GPT-3.5/4
- **Data Visualization**: Plotly, Matplotlib
- **Authentication**: Environment-based API keys

## 🏗️ Project Structure

```
expense-tracker/
├── .env                    # Environment variables
├── app.py                 # Main application file
├── requirements.txt       # Python dependencies
├── README.md              # This file
├── data/                  # Database and data files
│   └── expenses.db        # SQLite database
├── pages/                 # Streamlit pages
│   ├── 1_Add_Expenses.py  # Add/Edit expenses
│   ├── 2_View_Expenses.py # View and manage expenses
│   ├── 3_Analytics.py     # Data visualization
│   └── 4_AI_Insights.py   # AI-powered insights
└── utils/                 # Utility modules
    ├── __init__.py
    ├── database.py        # Database operations
    └── config.py          # Configuration settings
```

## Features in Detail

### 1. Add Expenses
- Intuitive form for adding new expenses
- Support for multiple categories and payment methods
- Option to add custom categories
- Input validation and error handling

### 2. View Expenses
- Tabular display of all expenses
- Filter by date range and category
- Sort by any column
- Export data to CSV
- Delete expenses

### 3. Analytics
- Monthly spending trends
- Category-wise spending distribution
- Payment method analysis
- Interactive charts and graphs
- Responsive design for all screen sizes

### 4. AI Insights
- Personalized spending analysis
- Anomaly detection
- Budgeting recommendations
- Chat interface for asking questions about your spending

## Customization

You can customize the application by modifying the following files:

- `utils/config.py`: Update colors, currency, and other settings
- `utils/database.py`: Modify database schema or queries
- `pages/*.py`: Customize the individual pages

## 🚀 Deployment

### Local Development
1. Clone the repository
2. Set up a virtual environment
3. Install dependencies
4. Run the Streamlit app

### Cloud Deployment
1. **Streamlit Cloud**: [Deploy Guide](https://docs.streamlit.io/streamlit-community-cloud/get-started/deploy-an-app)
2. **Heroku**: [![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=YOUR_REPO_URL)
3. **Vercel**: [![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=YOUR_REPO_URL)

## 🤝 Contributing

Contributions are what make the open-source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.

## 📧 Contact

Project Link: (https://ai-based-smart-expense-tracker.streamlit.app/)
## 🙏 Acknowledgments

- [Streamlit](https://streamlit.io/) for the amazing framework
- [OpenAI](https://openai.com/) for the powerful AI models
- [Font Awesome](https://fontawesome.com/) for icons
- [Shields.io](https://shields.io/) for badges

- Icons from [Font Awesome](https://fontawesome.com/)

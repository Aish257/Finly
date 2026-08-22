# ⚡ Finly — Personal Finance & Financial Literacy Platform

Finly is a beginner-friendly personal finance and financial literacy web application built for hackathons. It features a complete black theme, responsive card-based dashboard navigation, SQLite database persistence, interactive Plotly visualizations, an 8-chapter financial academy with quizzes, an investment simulator, a financial goals manager, and an AI Financial Coach powered by Google Gemini 2.5 Flash with an offline fallback mode.

---

## 🌟 Key Features

1. **Dashboard**: Central landing page with 7 large interactive feature cards.
2. **💰 Expense Tracker**: Record, edit, delete expenses by category; view monthly spending, Plotly pie/bar charts, and automatic insights.
3. **📚 Learn Investing**: 8 structured chapters covering stock market basics, compounding, SIPs, mutual funds, and bull/bear markets with 16 interactive quizzes.
4. **📈 Market Overview**: Latest Indian market developments simply explained with clear disclaimers.
5. **🧪 Investment Simulator**: Test a virtual ₹10,000 portfolio across Bull, Bear, Volatile, and Sideways market scenarios.
6. **⚠️ Beginner Mistakes**: Interactive breakdown of 7 common financial traps.
7. **🎯 Financial Goals**: Create savings targets with progress bars and monthly required savings calculator.
8. **🤖 AI Financial Coach**: Gemini 2.5 Flash chatbot with guardrails against stock recommendations, plus smart local offline fallbacks.

---

## 🛠️ Tech Stack

- **Python**
- **Streamlit**
- **SQLite**
- **Plotly**
- **Google Gemini 2.5 Flash** (`google-genai` / fallback engine)

---

## 🚀 How to Run Locally

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. (Optional) Set Google Gemini API Key
To enable live Gemini 2.5 Flash responses for the AI Coach, set your API key in environment variables or Streamlit secrets:

**Linux / Mac**:
```bash
export GEMINI_API_KEY="your_api_key_here"
```

**Windows (PowerShell)**:
```powershell
$env:GEMINI_API_KEY="your_api_key_here"
```

*(Note: If no API key is set, Finly automatically operates using its smart offline fallback engine!)*

### 3. Launch Application
```bash
streamlit run app.py
```

---

## 📂 Project Structure

```
d:/FinHub/
├── app.py              # Main Streamlit app, page routing & card UI
├── database.py         # SQLite database management (expenses & goals)
├── ai_coach.py         # Gemini 2.5 Flash integration & offline fallback
├── learning_data.py    # 8 financial literacy chapters & 16 quizzes
├── market_data.py      # Indian market overview updates & disclaimers
├── simulator.py        # Virtual ₹10,000 investment simulator engine
├── styles.css          # Complete deep black theme CSS
├── requirements.txt    # Python package dependencies
└── README.md           # Project documentation
```

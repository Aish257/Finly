import os
import streamlit as st

# System instruction to enforce financial coach safety guardrails
COACH_SYSTEM_PROMPT = """
You are "Finly Coach", a friendly, patient, and beginner-focused AI financial literacy assistant for Finly.

Your goal is to explain financial concepts, investing terms, expense tracking insights, and investment simulator results in simple, plain language.

STRICT SAFETY RULES:
1. NEVER provide specific stock, mutual fund, crypto, or real estate BUY / SELL recommendations.
2. NEVER promise or guarantee financial returns or interest rates.
3. NEVER act as a licensed financial advisor.
4. If a user asks "Which stock should I buy today?" or "Where should I invest ₹10,000 for guaranteed money?", politely decline and explain the importance of diversification, risk assessment, and consulting a certified SEBI professional.
5. Keep explanations short, clear, encouraging, and easy to read (use bullet points when helpful).
"""

# Smart offline fallback response engine
FALLBACK_RESPONSES = {
    "stock": "A stock represents fractional ownership in a business. When you buy a company's stock, you own a small piece of its assets and future earnings. Stock prices rise or fall based on company growth and market demand.",

    "mutual fund": "A mutual fund pools money from many individual investors to buy a diversified basket of stocks, bonds, or gold. Professional fund managers handle the buying and selling for you.",

    "sip": "SIP stands for Systematic Investment Plan. It allows you to invest a fixed sum (like ₹500 or ₹1,000) automatically every month into a mutual fund. It helps build discipline and averages your purchase costs.",

    "emergency fund": "An emergency fund is liquid savings set aside for unexpected crises like medical bills or temporary job loss. Ideally, it should cover 3 to 6 months of basic living expenses in a bank account or liquid fund.",

    "diversification": "Diversification means spreading your money across different investments (stocks, mutual funds, gold, fixed deposits) so that a crash in one asset doesn't destroy your entire wealth.",

    "budget": "The 50/30/20 budget rule is great for beginners: Spend 50% on Needs (rent, groceries, bills), 30% on Wants (entertainment, dining out), and direct 20% into Savings & Investments.",

    "compounding": "Compounding means earning returns on your initial savings AND on the past returns already earned. Over 10-20 years, compounding accelerates your wealth creation exponentially.",

    "buy": "As Finly Coach, I cannot recommend specific stocks or buy/sell actions! A safe approach for beginners is to explore low-cost Index Mutual Funds (like Nifty 50) through monthly SIPs.",

    "recommend": "I cannot provide personalized financial recommendations. I can, however, help you understand risk levels, asset classes, and budgeting rules!"
}


def get_gemini_client():
    """
    Get Gemini client using the API key stored in
    Streamlit secrets or environment variables.
    """

    api_key = None

    # ---------------------------------------------------------
    # 1. Try Streamlit secrets
    # ---------------------------------------------------------
    try:
        if "GEMINI_API_KEY" in st.secrets:
            api_key = st.secrets["GEMINI_API_KEY"]
    except Exception as e:
        return None, f"Secrets Error: {e}"

    # ---------------------------------------------------------
    # 2. Try environment variable if secret wasn't found
    # ---------------------------------------------------------
    if not api_key:
        api_key = os.environ.get("GEMINI_API_KEY")

    # ---------------------------------------------------------
    # 3. Stop if no API key was found
    # ---------------------------------------------------------
    if not api_key:
        return None, "No GEMINI_API_KEY found"

    # ---------------------------------------------------------
    # 4. Use the new Google GenAI SDK
    # ---------------------------------------------------------
    try:
        from google import genai

        client = genai.Client(api_key=api_key)

        return ("new_sdk", client), None

    except ImportError:
        pass

    except Exception as e:
        return None, f"Gemini Client Error: {e}"

    # ---------------------------------------------------------
    # 5. Legacy SDK fallback
    # ---------------------------------------------------------
    try:
        import google.generativeai as genai

        genai.configure(api_key=api_key)

        return ("legacy_sdk", genai), None

    except ImportError:
        pass

    except Exception as e:
        return None, f"Legacy SDK Error: {e}"

    return None, "Google GenAI SDK not installed"


def ask_ai_coach(user_query, context=""):
    """
    Asks Gemini for a financial coaching response,
    falling back to the local engine if needed.
    """

    client_tuple, err = get_gemini_client()

    # ---------------------------------------------------------
    # If Gemini client could not be created
    # ---------------------------------------------------------
    if not client_tuple:

        # Show the real error instead of silently hiding it
        if err:
            return f"⚠️ Gemini Error:\n\n{err}"

        # Local fallback
        query_lower = user_query.lower()

        for key, response_text in FALLBACK_RESPONSES.items():
            if key in query_lower:
                return (
                    "💡 **Finly Assistant (Offline Mode):**\n\n"
                    + response_text
                )

        return (
            "💡 **Finly Assistant (Offline Mode):**\n\n"
            "Great question! As a beginner-friendly principle, always remember:\n"
            "1. Build a 3-6 month **Emergency Fund** in liquid savings first.\n"
            "2. Start investing small amounts regularly via **Automated SIPs** in low-cost index funds.\n"
            "3. **Diversify** across stocks, mutual funds, and gold to protect your capital.\n\n"
            "*(Note: Connect a valid Google Gemini API key to activate full real-time AI responses!)*"
        )

    # ---------------------------------------------------------
    # Gemini client exists
    # ---------------------------------------------------------
    sdk_type, client_obj = client_tuple

    full_prompt = (
        f"{COACH_SYSTEM_PROMPT}\n\n"
        f"Context: {context}\n\n"
        f"User Question: {user_query}"
    )

    try:

        # -----------------------------------------------------
        # New Google GenAI SDK
        # -----------------------------------------------------
        if sdk_type == "new_sdk":

            response = client_obj.models.generate_content(
                model="gemini-3.5-flash-lite",
                contents=full_prompt
            )

            if response and hasattr(response, "text") and response.text:
                return response.text.strip()

        # -----------------------------------------------------
        # Legacy Google Generative AI SDK
        # -----------------------------------------------------
        elif sdk_type == "legacy_sdk":

            model = client_obj.GenerativeModel(
                "gemini-3.5-flash-lite"
            )

            response = model.generate_content(
                full_prompt
            )

            if response and hasattr(response, "text") and response.text:
                return response.text.strip()

    except Exception as e:

        # IMPORTANT:
        # Do not hide Gemini errors.
        # Show the actual error so we can fix it.
        return f"⚠️ Gemini API Error:\n\n{e}"

    # ---------------------------------------------------------
    # If Gemini returned no usable response
    # ---------------------------------------------------------
    return (
        "⚠️ Gemini connected, but no response was returned."
    )
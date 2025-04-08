import google.generativeai as genai
import markdown
import re

# Configure API key
genai.configure(api_key="AIzaSyDxpor2viPS9Q4W9Ud1Jzu_cvRFxgebu10")

# Set up the model
model = genai.GenerativeModel("gemini-pro")

def is_finance_related(text):
    keywords = ['money', 'budget', 'spending', 'saving', 'finance', 'income', 'expenses', 'cost', 'save', 'spend']
    return any(re.search(rf'\b{kw}\b', text.lower()) for kw in keywords)

def get_gemini_response(user_input):
    if not is_finance_related(user_input):
        return "I'm here to help with financial and budgeting questions! Try asking something money related."
    try:
        prompt = (
            "You are a financial assistant for a budgeting app. Only respond to financial questions or "
            "questions about saving money. Be positive and enthusiastic but not overly enthusiastic. "
            "Keep your response detailed but relatively concise... under 2000 characters if possible. "
            f"User: {user_input}"
        )
        response = model.generate_content(prompt)
        return markdown.markdown(response.text.strip())
    except Exception as e:
        print("Gemini API error:", e)
        return "Sorry, I couldn't process that request."
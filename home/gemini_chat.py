from google import genai
import markdown
import re

client = genai.Client(api_key="AIzaSyDxpor2viPS9Q4W9Ud1Jzu_cvRFxgebu10")

def is_finance_related(text):
    keywords = ['money', 'budget', 'spending', 'saving', 'finance', 'income', 'expenses', 'cost', 'save', 'spend']
    return any(re.search(rf'\b{kw}\b', text.lower()) for kw in keywords)

def get_gemini_response(user_input):
    if not is_finance_related(user_input):
        return "I'm here to help with financial and budgeting questions! Try asking something money related."
    try:
        prompt = f"""You are a financial assistant for a budgeting app. Only respond to financial questions or questions about saving money. Be positive and enthusiastic but not overly enthusiastic. Keep your response detailed but relatively concise...  under 2000 characters if possible. User: {user_input}"""
        response = client.models.generate_content(model = "gemini-2.0-flash", contents = prompt)
        return markdown.markdown(response.text.strip())
    except Exception as e:
        print("Gemini API error:", e)
        return "Sorry, I couldn't process that request."
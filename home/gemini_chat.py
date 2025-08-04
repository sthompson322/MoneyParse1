import google.generativeai as genai
import markdown
import re
from finances.models import Transaction, Budget, Income
from django.db.models import Sum
from decimal import Decimal

# Configure API key
genai.configure(api_key="AIzaSyDxpor2viPS9Q4W9Ud1Jzu_cvRFxgebu10")
model = genai.GenerativeModel("gemini-1.5-flash")

def is_finance_related(text):
    keywords = ['money', 'budget', 'spending', 'saving', 'finance', 'income', 'expenses', 'cost', 'save', 'spend']
    return any(re.search(rf'\b{kw}\b', text.lower()) for kw in keywords)

def get_gemini_response(user_input, user):
    if not is_finance_related(user_input):
        return "I'm here to help with financial and budgeting questions! Try asking something money related."

    try:
        # Pull in user data
        transactions = Transaction.objects.filter(user=user, type=False)
        budgets = Budget.objects.filter(user=user)
        income_total = Income.objects.filter(user=user).aggregate(total=Sum("amount"))["total"] or Decimal("0.00")

        has_data = transactions.exists() or budgets.exists()

        user_context = ""

        if has_data:
            high_spending = transactions.order_by('-amount').first()
            top_category = transactions.values('category').annotate(total=Sum('amount')).order_by('-total').first()
            over_budget = [b.category for b in budgets if b.percent_used > 100]

            user_context = (
                f"The user has an income total of ${income_total:.2f}. "
                f"Their top spending category is {top_category['category']} with ${top_category['total']:.2f} spent. "
                f"Their most recent large transaction was ${high_spending.amount:.2f} in {high_spending.category}. "
            )

            if over_budget:
                user_context += f"They are currently over budget in: {', '.join(over_budget)}. "
            else:
                user_context += "They are within their set budget limits."
        else:
            user_context = (
                "You do not have any data on this user's spending habits yet. "
                "Provide general advice about budgeting, saving, and good financial habits."
            )

        # Craft the full prompt
        prompt = (
            f"You are Mona, a smart financial assistant in a budgeting app. "
            f"{user_context} "
            "Answer the following question in a friendly but informative tone. "
            "Avoid being too robotic or too enthusiastic. Keep it under 2000 characters.\n\n"
            f"User: {user_input}"
        )

        # Gemini call
        response = model.generate_content(prompt)
        #response = client.models.generate_content(model="gemini-1.5-flash", contents=prompt)
        return markdown.markdown(response.text.strip())

    except Exception as e:
        print("Gemini API error:", e)
        return "Sorry, I couldn't process that request."

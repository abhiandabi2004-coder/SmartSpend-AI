"""
AI Financial Advisor — calls Anthropic API with user's expense data
Returns structured insights: summary, warnings, tips.
"""

from __future__ import annotations
import os
import json
import streamlit as st
import anthropic

CATEGORY_BUDGETS = {
    "Food": 4000,
    "Transport": 2000,
    "Entertainment": 1500,
    "Shopping": 3000,
    "Health": 1500,
    "Education": 2000,
    "Utilities": 2000,
    "Rent": 10000,
    "Other": 2000,
}

TOTAL_BUDGET_THRESHOLD = 15000  # ₹ per month — warn if exceeded


def build_expense_prompt(expenses: list[dict], summary: dict) -> str:
    """Build a concise prompt describing the user's spending."""
    cat_lines = "\n".join(
        f"  - {cat}: ₹{amt:,.2f}" for cat, amt in summary["by_category"].items()
    )

    recent = expenses[:5]
    recent_lines = "\n".join(
        f"  - {e['description']} ({e['category']}): ₹{e['amount']:,.2f}"
        for e in recent
    )

    over_budget_cats = [
        f"{cat} (₹{amt:,.0f} vs budget ₹{CATEGORY_BUDGETS.get(cat, 2000):,.0f})"
        for cat, amt in summary["by_category"].items()
        if amt > CATEGORY_BUDGETS.get(cat, 2000)
    ]

    return f"""You are SpendSmart AI, a friendly and smart personal finance advisor for Indian students and young professionals.

The user's expense data:
- Total spent: ₹{summary['total']:,.2f}
- Number of transactions: {summary['count']}
- Average transaction: ₹{summary['avg_transaction']:,.2f}
- Top spending category: {summary['top_category']} (₹{summary['top_category_amount']:,.2f})

Spending by category:
{cat_lines}

Recent transactions:
{recent_lines}

Over-budget categories: {', '.join(over_budget_cats) if over_budget_cats else 'None'}
Total budget threshold: ₹{TOTAL_BUDGET_THRESHOLD:,}/month ({"EXCEEDED" if summary['total'] > TOTAL_BUDGET_THRESHOLD else "within limits"})

Please respond with a JSON object (no markdown, no backticks) with this exact structure:
{{
  "summary": "2-3 sentence overview of spending patterns in a friendly tone",
  "warnings": ["warning 1 if applicable", "warning 2 if applicable"],
  "tips": ["actionable tip 1", "actionable tip 2", "actionable tip 3"],
  "score": <integer 1-100 representing financial health score>,
  "score_label": "<one of: Excellent, Good, Fair, Needs Work>"
}}

Rules:
- warnings array can be empty [] if spending is healthy
- tips must be specific and actionable, not generic
- Use ₹ symbol for Indian Rupees
- Be encouraging and non-judgmental
- Reference specific categories from their data
- Keep each string under 120 characters
"""


def get_ai_insights(expenses: list[dict], summary: dict) -> dict:
    """Call Anthropic API and return parsed insight dict."""
    if not expenses:
        return {
            "summary": "No expenses recorded yet. Start adding expenses to get personalized insights!",
            "warnings": [],
            "tips": [
                "Add your daily expenses to track your spending habits.",
                "Set a monthly budget goal for each category.",
                "Review your expenses weekly for better awareness.",
            ],
            "score": 100,
            "score_label": "Excellent",
        }

    try:
        try:
            api_key = st.secrets.get("ANTHROPIC_API_KEY", "")
        except Exception:
            api_key = os.environ.get("ANTHROPIC_API_KEY", "")

        if not api_key:
            return _fallback_insights(summary)

        client = anthropic.Anthropic(api_key=api_key)
        prompt = build_expense_prompt(expenses, summary)

        message = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=800,
            messages=[{"role": "user", "content": prompt}],
        )

        raw = message.content[0].text.strip()
        # Strip any accidental markdown fences
        raw = raw.replace("```json", "").replace("```", "").strip()
        return json.loads(raw)

    except json.JSONDecodeError:
        return _fallback_insights(summary)
    except Exception as e:
        st.warning(f"AI advisor unavailable: {e}")
        return _fallback_insights(summary)


def _fallback_insights(summary: dict) -> dict:
    """Rule-based fallback when API is unavailable."""
    warnings = []
    tips = []
    score = 75

    top = summary.get("top_category", "Other")
    total = summary.get("total", 0)
    by_cat = summary.get("by_category", {})

    if total > TOTAL_BUDGET_THRESHOLD:
        warnings.append(f"⚠️ Total spending ₹{total:,.0f} exceeds monthly threshold of ₹{TOTAL_BUDGET_THRESHOLD:,}.")
        score -= 20

    for cat, amt in by_cat.items():
        budget = CATEGORY_BUDGETS.get(cat, 2000)
        if amt > budget:
            warnings.append(f"⚠️ {cat} spending (₹{amt:,.0f}) exceeds budget of ₹{budget:,}.")
            score -= 10

    if top == "Food":
        tips.append("🍱 Try meal prepping on weekends to cut Food costs by 20-30%.")
    elif top == "Entertainment":
        tips.append("🎬 Look for free or discounted entertainment options in your city.")
    elif top == "Shopping":
        tips.append("🛍️ Use a 24-hour rule before non-essential purchases.")
    else:
        tips.append(f"💡 Review your {top} expenses — it's your biggest spend category.")

    tips.append("📊 Aim to save at least 20% of your monthly income.")
    tips.append("🔄 Review subscriptions monthly and cancel unused ones.")

    score = max(10, min(100, score))
    label = "Excellent" if score >= 85 else "Good" if score >= 65 else "Fair" if score >= 45 else "Needs Work"

    summary_text = (
        f"You've spent ₹{total:,.2f} across {summary.get('count', 0)} transactions. "
        f"Your biggest category is {top}."
        + (" Consider reviewing your budget." if warnings else " Keep it up!")
    )

    return {
        "summary": summary_text,
        "warnings": warnings,
        "tips": tips,
        "score": score,
        "score_label": label,
    }

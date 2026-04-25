from utils.supabase_client import supabase

def get_budget(user_id):
    res = supabase.table("user_budget").select("*").eq("user_id", user_id).execute()
    return res.data[0] if res.data else None

def save_budget(user_id, income, limit):
    existing = get_budget(user_id)

    if existing:
        supabase.table("user_budget").update({
            "monthly_income": income,
            "budget_limit": limit
        }).eq("user_id", user_id).execute()
    else:
        supabase.table("user_budget").insert({
            "user_id": user_id,
            "monthly_income": income,
            "budget_limit": limit
        }).execute()
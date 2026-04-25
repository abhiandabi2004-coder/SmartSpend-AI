"""Category definitions, icons, and colors"""

CATEGORIES = [
    "Food",
    "Transport",
    "Entertainment",
    "Shopping",
    "Health",
    "Education",
    "Utilities",
    "Rent",
    "Other",
]

CATEGORY_ICONS: dict[str, str] = {
    "Food":          "🍜",
    "Transport":     "🚌",
    "Entertainment": "🎬",
    "Shopping":      "🛍️",
    "Health":        "💊",
    "Education":     "📚",
    "Utilities":     "⚡",
    "Rent":          "🏠",
    "Other":         "📌",
}

CATEGORY_COLORS: dict[str, str] = {
    "Food":          "#fc6d6d",
    "Transport":     "#63b3ed",
    "Entertainment": "#a78bfa",
    "Shopping":      "#f6c90e",
    "Health":        "#56cfae",
    "Education":     "#4ecdc4",
    "Utilities":     "#fb923c",
    "Rent":          "#e879f9",
    "Other":         "#8b93a7",
}

CATEGORY_BG: dict[str, str] = {
    "Food":          "rgba(252,109,109,0.12)",
    "Transport":     "rgba(99,179,237,0.12)",
    "Entertainment": "rgba(167,139,250,0.12)",
    "Shopping":      "rgba(246,201,14,0.12)",
    "Health":        "rgba(86,207,174,0.12)",
    "Education":     "rgba(78,205,196,0.12)",
    "Utilities":     "rgba(251,146,60,0.12)",
    "Rent":          "rgba(232,121,249,0.12)",
    "Other":         "rgba(139,147,167,0.12)",
}


def get_icon(category: str) -> str:
    return CATEGORY_ICONS.get(category, "💳")

def get_color(category: str) -> str:
    return CATEGORY_COLORS.get(category, "#8b93a7")

def get_bg(category: str) -> str:
    return CATEGORY_BG.get(category, "rgba(139,147,167,0.12)")

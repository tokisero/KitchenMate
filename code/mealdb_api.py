"""Клиент TheMealDB: загрузка рецепта по id, единый разбор полей для избранного и списка покупок."""

from __future__ import annotations

import requests

BASE = "https://www.themealdb.com/api/json/v1/1"


def meal_to_dict(meal: dict) -> dict:
    ingredients: list[dict[str, str]] = []
    for i in range(1, 21):
        name = meal.get(f"strIngredient{i}")
        meas = meal.get(f"strMeasure{i}")
        if name and str(name).strip():
            ingredients.append(
                {"name": str(name).strip(), "amount": (meas or "").strip() if meas else ""}
            )
    ing_str = ", ".join(f"{x['name']} ({x['amount']})" for x in ingredients if x["name"])
    return {
        "name": meal.get("strMeal") or "Без названия",
        "id": meal.get("idMeal"),
        "ingredients": ing_str,
        "instructions": (meal.get("strInstructions") or "").strip() or "Инструкция отсутствует.",
        "time": (meal.get("strCategory") or meal.get("strArea") or "—"),
        "full_ingredients": ingredients,
        "local": False,
    }


def lookup_meal(meal_id: str) -> dict | None:
    """Полные данные рецепта по id TheMealDB."""
    try:
        r = requests.get(f"{BASE}/lookup.php?i={meal_id}", timeout=15)
        r.raise_for_status()
        data = r.json()
        meals = data.get("meals")
        if not meals:
            return None
        return meal_to_dict(meals[0])
    except (requests.RequestException, ValueError, KeyError):
        return None


def search_by_ingredient(ingredient_en: str) -> list[dict]:
    """Краткий список блюд по основному ингредиенту (англ. имя)."""
    try:
        r = requests.get(f"{BASE}/filter.php?i={ingredient_en}", timeout=15)
        r.raise_for_status()
        data = r.json()
        meals = data.get("meals") or []
        out = []
        for meal in meals[:10]:
            out.append(
                {
                    "name": meal.get("strMeal", "Без названия"),
                    "id": meal.get("idMeal"),
                    "local": False,
                }
            )
        return out
    except (requests.RequestException, ValueError, KeyError):
        return []


def search_by_name(query: str) -> list[dict]:
    """Поиск блюд по названию (если фильтр по ингредиенту не подошёл)."""
    try:
        r = requests.get(f"{BASE}/search.php", params={"s": query.strip()}, timeout=15)
        r.raise_for_status()
        data = r.json()
        meals = data.get("meals") or []
        out = []
        for meal in meals[:10]:
            out.append(
                {
                    "name": meal.get("strMeal", "Без названия"),
                    "id": meal.get("idMeal"),
                    "local": False,
                }
            )
        return out
    except (requests.RequestException, ValueError, KeyError):
        return []

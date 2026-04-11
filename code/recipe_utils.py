"""Чистые функции для поиска рецептов и списка покупок — без зависимости от Tkinter и сети."""

import re


def filter_favorites_by_query(favorites, query):
    """Локальный поиск по названию среди избранных рецептов."""
    if not query:
        return []
    q = query.lower()
    return [r for r in favorites if q in r['name'].lower()]


def merge_missing_into_shopping(shopping_items, missing_ings):
    """
    Добавляет недостающие ингредиенты в список покупок без дубликатов по имени
    (сравнение без учёта регистра для уже имеющихся позиций).
    """
    items = [dict(x) for x in shopping_items]
    for ing in missing_ings:
        name = ing['name']
        if not any(p['name'].lower() == name.lower() for p in items):
            items.append(
                {'name': ing['name'], 'amount': ing.get('amount', ''), 'checked': False}
            )
    return items


def parse_ingredients_string(s: str) -> list[dict]:
    """Разбор строки ингредиентов из БД вида «Название (кол-во), ...» в список словарей."""
    if not s or not str(s).strip():
        return []
    parts = [p.strip() for p in str(s).split(",") if p.strip()]
    out: list[dict] = []
    for p in parts:
        m = re.match(r"^(.+?)\s*\(([^)]*)\)\s*$", p)
        if m:
            out.append({"name": m.group(1).strip(), "amount": m.group(2).strip()})
        else:
            out.append({"name": p, "amount": ""})
    return out


def missing_ingredients_vs_pantry(full_ingredients: list[dict], pantry_items: list[dict]) -> list[dict]:
    """Ингредиенты рецепта, которых нет в кладовой (по имени без учёта регистра)."""
    missing: list[dict] = []
    seen: set[str] = set()
    for ing in full_ingredients:
        name = (ing.get("name") or "").strip()
        if not name:
            continue
        key = name.lower()
        if key in seen:
            continue
        if not any(p["name"].lower() == key for p in pantry_items):
            missing.append({"name": ing["name"], "amount": ing.get("amount", "")})
            seen.add(key)
    return missing

"""Чистые функции для поиска рецептов и списка покупок — без зависимости от Tkinter и сети."""


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

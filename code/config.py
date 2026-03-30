# Константы и мокап-данные

# Цвета (более современные оттенки)
GREEN = "#2D5A27"       # Глубокий лесной зеленый
SOFT_GREEN = "#E8F5E9"  # Светлый фон для карточек
RED = "#C62828"         # Мягкий красный
GRAY = "#455A64"        # Антрацитовый для текста
BG_COLOR = "#FAFAFA"    # Почти белый фон

# Шрифты
TITLE_FONT = ("Segoe UI", 24, "bold")
HEADER_FONT = ("Segoe UI", 14, "bold")
BODY_FONT = ("Segoe UI", 11)
SMALL_FONT = ("Segoe UI", 10)

# Мокап-данные (БД перезапишет)
PANTRY_ITEMS = [
    {'name': 'Помидоры', 'amount': '2'},
    {'name': 'Сыр', 'amount': '500г'},
    {'name': 'Рис', 'amount': '500г'},
    {'name': 'Курица', 'amount': '1кг'}
]

SHOPPING_ITEMS = [
    {'name': 'Мука', 'amount': '500г', 'checked': True},
    {'name': 'Молоко', 'amount': '1л', 'checked': False},
    {'name': 'Огурцы', 'amount': '2', 'checked': False}
]

FAVORITES = [
    {'name': 'Борщ', 'ingredients': 'Свёкла, капуста, мясо', 'instructions': 'Варить 1 час', 'time': '60 мин'},
    {'name': 'Плов', 'ingredients': 'Рис, мясо, морковь', 'instructions': 'Жарить и тушить', 'time': '45 мин'}
]

INGREDIENTS_OPTIONS = ['Помидоры', 'Сыр', 'Рис', 'Курица']
TIME_OPTIONS = ['10 мин', '20 мин', '30 мин']
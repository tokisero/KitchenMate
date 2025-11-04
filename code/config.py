# Константы и мокап-данные

# Цвета из мокапов
GREEN = '#4CAF50'
RED = '#F44336'
GRAY = '#9E9E9E'

# Шрифты (единый стиль)
TITLE_FONT = ('Arial', 20, 'bold')
HEADER_FONT = ('Arial', 16, 'bold')
BODY_FONT = ('Arial', 12)
SMALL_FONT = ('Arial', 10)

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
# Глоссарий ключевых понятий

На основе спецификации SRS.md (разделы 1.2, 2.3, 3.1).

- **Ingredient (Ингредиент/Продукт)**: Элемент в кладовой или рецепте. Атрибуты: name (string) — название; quantity (double) — количество; unit (enum: g, kg, ml, шт.) — единица. Операции: валидация ввода. Источник: 3.1.1.1 (управление кладовой, формы ввода).

- **Pantry (Кладовая)**: Локальное хранилище ингредиентов пользователя (SQLite). Состоит из списка Ingredient. Операции: add/remove/edit/view. GUI: таблица на pantry_screen.png. Источник: 3.1.1.1.

- **Recipe (Рецепт)**: Описание блюда. Атрибуты: title (string) — название; ingredients (List<Ingredient>) — требуемые ингредиенты с количествами; steps (List<String>) — шаги приготовления; source (enum: API, Manual) — источник. Операции: search, generateShoppingList. GUI: recipes_screen.png, add_recipe_screen.png. Источник: 3.1.1.2, 3.1.1.4.

- **ShoppingList (Список покупок)**: Чек-лист недостающих ингредиентов. Атрибуты: missingIngredients (List<Ingredient>) — недостающие; additional (List<Ingredient>) — пользовательские добавки; bought (boolean per item) — статус. Операции: generate, markAsBought, addAdditional. GUI: shopping_list.png. Источник: 3.1.1.3.

- **Favorite (Избранное)**: Список сохранённых Recipe (локально в SQLite). Операции: add/edit/remove. GUI: favorites_recipes_screen.png. Источник: 3.1.1.4.

- **User (Пользователь)**: Актер (студент/семья/вегетарианец, 2.3.1). Предпочтения: dietary (enum: vegan и т.д.), но без регистрации — implicit в поиске.

Ассоциации: Pantry содержит Ingredient; Recipe требует Ingredient; ShoppingList генерируется из Recipe + Pantry.
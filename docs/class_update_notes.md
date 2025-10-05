# Заметки по уточнению диаграммы классов (v2)

На основе этапа A (sequence: методы как getIngredients(), compareWithPantry()) и B (state: поля как status для ошибок). Из SRS: SQLite storage (3.2.1.3), API integration (2.1).

Изменения:
  - Добавлены методы: validateInput() в Ingredient (из activity UC1 decisions), compareWithPantry() в Recipe (из sequence UC2).
  - Новые поля: status: enum<Status> {Valid, Invalid} в Ingredient (для ошибок в state).
  - Уточнены ассоциации: ShoppingList 1..1 Recipe (генерируется из одного).
  - Enum Unit расширен: {g, kg, ml, l, pcs} (из GUI форм, 2.2).

Нет: expiry dates (вне границ, 3.1.2). Проверить в CASE: все методы вызываются в sequence.
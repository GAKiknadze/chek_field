# Form Validator

## Запуск

1. Установите зависимости:
   ```bash
   pip install -r requirements.txt
   ```

2. Запустите приложение:
   ```bash
   uvicorn app:app
   ```

3. Откройте http://localhost:8000/docs для Swagger UI.

## Тестирование

1. Установите зависимости:
   ```bash
   pip install -r requirements.test.txt
   ```

2. Запустите тесты:
   ```bash
   pytest
   ```

### Описание тестов

1. **`test_valid_templates`**: Проверяет, что API правильно находит подходящий шаблон для входных данных.
2. **`test_infer_field_types`**: Проверяет корректность определения типов для входных данных, которые не соответствуют ни одному из шаблонов.


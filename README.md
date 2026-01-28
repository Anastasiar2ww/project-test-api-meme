# project-test-api-meme

Это учебный проект, в котором показано, как реализовать тесты API в Python

Base URL: http://memesapi.course.qa-practice.com

---
В проекте используются:

- Python
- Requests
- Allure для отчетов
---

# Установка зависимости
```
pip install -r requirements.txt
```

# Запуск тестов
```
pytest -v
```
# С отчетом Allure

```
pytest --alluredir=allure-results
allure serve allure-results
```

# Установка Allure. Windows (через Scoop)
```
scoop install allure
```

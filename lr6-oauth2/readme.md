OAUTH 2.0 - Костылева Э.П. ИВТ 4 курс

Быстрый старт
# 1. Установка
python -m venv venv
source venv/bin/activate      # Linux/Mac
venv\Scripts\activate        # Windows
pip install requests

# 2. Регистрация OAuth-приложения
#    Перейти: https://github.com/settings/applications/new
#    Callback URL: http://localhost:8000/callback

# 3. Запуск
python 1_github_oauth.py

Отчет:

Создание application on GitHub
![img.png](img.png)


Задание 1. Реализация Authorization Code Flow

запускаем oauth_github.py
![img_1.png](img_1.png)
После ввода требуемых значений открывается страница, чей URL надо скопировать и вставить в терминале
![img_2.png](img_2.png)

Итог: 
![img_3.png](img_3.png)


Задание 2. Обновление токена (refresh token)

Запускаем oauth_google_refresh.py
Открывается страница для авторизации
![img_4.png](img_4.png)
После авторизации копируем ссылку как в 1 задании и вставляем в терминал
![img_5.png](img_5.png)
Итог:
![img_6.png](img_6.png)

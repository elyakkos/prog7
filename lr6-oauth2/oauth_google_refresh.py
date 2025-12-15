
import os

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
os.environ['OAUTHLIB_RELAX_TOKEN_SCOPE'] = '1'

from google_auth_oauthlib.flow import Flow
import json
import requests
import webbrowser


def google_refresh_token():
    print("=" * 70)
    print("ЗАДАНИЕ 2: Refresh Token для Google API")
    print("=" * 70)

    print("\n📋 ПОДГОТОВКА:")
    print("1. Убедитесь, что у вас есть файл 'google_client_secret.json'")
    print("2. Проверьте, что в Google Cloud Console настроен redirect_uri:")
    print("   http://localhost:8080/callback")
    print("=" * 70)

    # Проверяем наличие файла с credentials
    if not os.path.exists('google_client_secret.json'):
        print("\n ФАЙЛ 'google_client_secret.json' НЕ НАЙДЕН!")
        print("\n Как его получить:")
        print("1. Перейдите: https://console.cloud.google.com/")
        print("2. Создайте проект (или выберите существующий)")
        print("3. APIs & Services → Credentials")
        print("4. Create Credentials → OAuth client ID")
        print("5. Application type: Web application")
        print("6. Добавьте Authorized Redirect URI:")
        print("   http://localhost:8080/callback")
        print("7. Скачайте JSON и сохраните как 'google_client_secret.json'")
        return


    SCOPES = [
        'https://www.googleapis.com/auth/userinfo.email',
        'https://www.googleapis.com/auth/userinfo.profile',
        'openid'
    ]

    # 1. Создание OAuth flow
    print("\n[1/5] Инициализация OAuth потока...")
    try:
        flow = Flow.from_client_secrets_file(
            'google_client_secret.json',
            scopes=SCOPES,
            redirect_uri='http://localhost:8080/callback'  # Явно указываем здесь
        )
        flow.redirect_uri = 'http://localhost:8080/callback'  # И здесь для уверенности
        print("✅ Поток инициализирован")
    except Exception as e:
        print(f" Ошибка: {e}")
        return

    # 2. Генерация URL для авторизации
    print("\n[2/5] Генерация URL для авторизации...")
    try:

        authorization_url, state = flow.authorization_url(
            access_type='offline',
            prompt='consent',
            include_granted_scopes='true'
        )

        print("✅ URL сгенерирован")
        print(f"\n🔗 State параметр: {state}")

    except Exception as e:
        print(f" Ошибка генерации URL: {e}")
        return

    # 3. Открываем браузер для авторизации
    print("\n[3/5] Открываю браузер для авторизации...")
    print(f"\n URL для авторизации:")
    print("-" * 50)
    print(authorization_url)
    print("-" * 50)

    webbrowser.open(authorization_url)

    print("\n ИНСТРУКЦИЯ ПО АВТОРИЗАЦИИ:")
    print("1. Войдите в ваш Google аккаунт")
    print("2. Нажмите 'Continue' на странице предупреждения")
    print("3. Нажмите 'Allow' чтобы предоставить доступ")
    print("4. Браузер перенаправит на неработающую страницу")
    print("5. Скопируйте ВЕСЬ URL из адресной строки браузера")

    # 4. Получаем callback URL от пользователя
    print("\n[4/5] Вставьте callback URL из браузера...")
    print("\nПример callback URL:")
    print("http://localhost:8080/callback?state=XYZ&code=4/0AfJohXkLch7dKJThTOzMKHcEall...")

    callback_url = input("\n👉 Вставьте URL сюда: ").strip()

    # Очищаем URL от кавычек
    callback_url = callback_url.strip('"').strip("'")

    # 5. Обмен code на tokens
    print("\n[5/5] Получение access token и refresh token...")
    try:
        flow.fetch_token(authorization_response=callback_url)
        credentials = flow.credentials

        print("\n✅ТОКЕНЫ УСПЕШНО ПОЛУЧЕНЫ!")
        print("=" * 50)


        tokens = {
            "token": credentials.token,
            "refresh_token": credentials.refresh_token,
            "token_uri": credentials.token_uri,
            "client_id": credentials.client_id,
            "client_secret": credentials.client_secret,
            "scopes": credentials.scopes,
            "expiry": credentials.expiry.isoformat() if credentials.expiry else None
        }

        # Показываем токены
        safe_tokens = tokens.copy()
        if safe_tokens.get('token'):
            safe_tokens['token'] = safe_tokens['token'][:30] + "..."
        if safe_tokens.get('refresh_token'):
            safe_tokens['refresh_token'] = safe_tokens['refresh_token'][:10] + "..."
        if safe_tokens.get('client_secret'):
            safe_tokens['client_secret'] = "***HIDDEN***"

        print("Полученные токены:")
        print(json.dumps(safe_tokens, indent=2, ensure_ascii=False))

        # Сохраняем в файл
        with open('google_tokens.json', 'w') as f:
            json.dump(tokens, f, indent=2)

        print(f"\n Полные токены сохранены в 'google_tokens.json'")

    except Exception as e:
        print(f"\n Ошибка при получении токенов: {e}")
        print("\nВозможные причины:")
        print("• Authorization code устарел (действует 5 минут)")
        print("• Неверный redirect_uri")
        print("• Проблемы с файлом client_secret.json")
        return

    # 6. Демонстрация использования токенов

    # A. Использование access token для запроса данных
    print("\nA. Запрос данных пользователя через API...")
    try:
        headers = {"Authorization": f"Bearer {credentials.token}"}
        response = requests.get(
            "https://www.googleapis.com/oauth2/v2/userinfo",
            headers=headers
        )

        if response.status_code == 200:
            user_info = response.json()
            print("✅ Данные получены:")
            print(f"   • Email: {user_info.get('email')}")
            print(f"   • Имя: {user_info.get('name', 'Не указано')}")
            print(f"   • ID: {user_info.get('id')}")
        else:
            print(f" Ошибка API: {response.status_code}")
            print(f"   Ответ: {response.text[:200]}")

    except Exception as e:
        print(f" Ошибка запроса: {e}")

    print("\nB. Обновление access token через refresh token...")
    try:
        refresh_data = {
            'grant_type': 'refresh_token',
            'client_id': credentials.client_id,
            'client_secret': credentials.client_secret,
            'refresh_token': credentials.refresh_token
        }

        refresh_response = requests.post(
            'https://oauth2.googleapis.com/token',
            data=refresh_data
        )

        if refresh_response.status_code == 200:
            new_tokens = refresh_response.json()
            print("✅ Токен успешно обновлен!")
            print(f"   • Новый access token: {new_tokens.get('access_token', '')[:30]}...")
            print(f"   • Действует: {new_tokens.get('expires_in', 3600)} секунд")

            # Обновляем сохраненный файл
            tokens['token'] = new_tokens['access_token']
            with open('google_tokens.json', 'w') as f:
                json.dump(tokens, f, indent=2)
            print(" Файл с токенами обновлен")
        else:
            print(f" Ошибка обновления: {refresh_response.status_code}")
            print(f"   Ответ: {refresh_response.text}")

    except Exception as e:
        print(f" Ошибка refresh: {e}")

    print("\n" + "=" * 70)
    print("✅ ЗАДАНИЕ ВЫПОЛНЕНО!")
    print("=" * 70)


if __name__ == "__main__":
    google_refresh_token()
import os

# РАЗРЕШАЕМ HTTP ДЛЯ LOCALHOST (только для разработки!)
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

from requests_oauthlib import OAuth2Session
import webbrowser


def github_oauth():
    print("ЗАДАНИЕ 1: Authorization Code Flow (GitHub)")



    print("\n Введите данные GitHub OAuth App:")
    client_id = input("Client ID: ").strip()
    client_secret = input("Client Secret: ").strip()

    REDIRECT_URI = "http://localhost:8000/callback"

    print(f"\n✅ Используем:")
    print(f"   Client ID: {client_id[:10]}...")
    print(f"   Redirect URI: {REDIRECT_URI}")

    # 1. Создание OAuth сессии
    github = OAuth2Session(
        client_id,
        redirect_uri=REDIRECT_URI,
        scope=["read:user"]
    )

    # 2. Генерация URL для авторизации
    auth_url, state = github.authorization_url(
        "https://github.com/login/oauth/authorize",
        state="lab_state_" + str(hash(client_id))[:10]
    )

    print(f"\n1. Открываю ссылку для авторизации...")
    webbrowser.open(auth_url)

    print(f"\n2. После авторизации GitHub перенаправит вас на:")
    print(f"   {REDIRECT_URI}?code=XYZ&state={state}")
    print(f"   Просто скопируйте ВЕСЬ URL из адресной строки браузера")

    callback_url = input("\n📋 Введите полный URL: ").strip()

    # Очистка URL
    callback_url = callback_url.strip('"').strip("'")

    # 3. Обмен code на access token
    print("\n3. Обмен authorization code на access token...")
    try:
        token = github.fetch_token(
            "https://github.com/login/oauth/access_token",
            authorization_response=callback_url,
            client_secret=client_secret,
            include_client_id=True
        )

        print(f"✅ Access token получен!")
        print(f"   Token: {token.get('access_token', '')[:30]}...")

    except Exception as e:
        print(f" Ошибка: {e}")
        print("\nВозможные причины:")
        print("• Неверный client_secret")
        print("• Код устарел (действует 10 минут)")
        print("• Redirect URI не совпадает")
        return

    # 4. Использование access token
    print("\n4. Запрос защищенного ресурса...")
    response = github.get("https://api.github.com/user")

    if response.status_code == 200:
        user = response.json()
        print("\n УСПЕХ! Данные получены:")
        print(f"   Логин: {user.get('login')}")
        print(f"   Имя: {user.get('name', 'Не указано')}")
        print(f"   Компания: {user.get('company', 'Не указана')}")
        print(f"   Репозиториев: {user.get('public_repos', 0)}")
        print(f"   Подписчиков: {user.get('followers', 0)}")

        # Показываем заголовок
        print(f"\n Использованный заголовок Authorization:")
        print(f"   Bearer {token.get('access_token', '')[:30]}...")
    else:
        print(f" Ошибка API: {response.status_code}")
        print(f"   {response.text[:200]}")


if __name__ == "__main__":
    github_oauth()
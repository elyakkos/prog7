import requests

BASE_URL = "http://localhost:8000/api/microservices/"


def test_statistics():
    response = requests.get(f"{BASE_URL}stats/")
    print("Статистика всех голосований:", response.status_code)

    response = requests.get(f"{BASE_URL}stats/1/")
    print("Статистика голосования 1:", response.status_code)


def test_charts():
    response = requests.get(f"{BASE_URL}charts/1/?chart_type=bar")
    print("График голосования 1:", response.status_code)


def test_export():
    response = requests.get(f"{BASE_URL}export/1/?format=csv")
    print("Экспорт голосования 1:", response.status_code)


def test_filter():
    response = requests.get(f"{BASE_URL}filter/?sort_by=popularity")
    print("Фильтрация голосований:", response.status_code)


if __name__ == "__main__":
    test_statistics()
    test_charts()
    test_export()
    test_filter()
    print("Тестирование завершено!")
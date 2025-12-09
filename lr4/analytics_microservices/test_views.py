from django.http import JsonResponse
from datetime import datetime

def test_endpoint(request):
    """Простой тестовый endpoint"""
    return JsonResponse({
        'status': 'ok',
        'message': 'Микросервисы работают!',
        'timestamp': datetime.now().isoformat(),
        'endpoints': [
            '/api/microservices/stats/',
            '/api/microservices/filter/',
            '/api/microservices/charts/1/',
            '/api/microservices/dashboard/'
        ]
    })

def health_check(request):
    """Проверка здоровья сервиса"""
    return JsonResponse({
        'service': 'analytics_microservices',
        'status': 'healthy',
        'version': '1.0',
        'timestamp': datetime.now().isoformat()
    })
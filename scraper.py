import requests

def upload_photo_to_s3(image_url, object_id, photo_index):
    """Заглушка: просто проверяет, что фото доступно"""
    try:
        response = requests.get(image_url, timeout=10)
        if response.status_code == 200:
            return f"mock_s3://photos/{object_id}/{photo_index}.jpg"
        return None
    except Exception as e:
        print(f"Ошибка загрузки {image_url}: {e}")
        return None

def scrape_listings():
    """Парсинг данных о недвижимости"""
    listings = [
        {
            "id": 1,
            "price": 5000000,
            "area": 45.5,
            "floor": 3,
            "total_floors": 9,
            "address": "ул. Ленина, 10",
            "photo_urls": [
                "https://images.unsplash.com/photo-1560448204-e02f11c3d0e2",
                "https://images.unsplash.com/photo-1580587771525-78b9dba3b914"
            ]
        },
        {
            "id": 2,
            "price": 8500000,
            "area": 67.2,
            "floor": 5,
            "total_floors": 12,
            "address": "пр. Мира, 25",
            "photo_urls": [
                "https://images.unsplash.com/photo-1512917774080-9991f1c4c750"
            ]
        },
        {
            "id": 3,
            "price": 12500000,
            "area": 89.3,
            "floor": 7,
            "total_floors": 10,
            "address": "ул. Пушкина, 15",
            "photo_urls": []
        }
    ]
    return listings
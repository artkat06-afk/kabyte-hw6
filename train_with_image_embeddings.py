import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer
from PIL import Image
from scraper import scrape_listings
import warnings

warnings.filterwarnings('ignore')

print("1. Загрузка данных...")
listings = scrape_listings()
df = pd.DataFrame(listings)


# Создаём текстовое описание для каждой квартиры
def make_text(row):
    return f"Адрес: {row['address']}. Цена: {row['price']} руб. Площадь: {row['area']} кв.м. Этаж: {row['floor']} из {row['total_floors']}."


df['description'] = df.apply(make_text, axis=1)

print("\n2. Загрузка модели CLIP...")
model = SentenceTransformer('clip-ViT-B-32')

print("\n3. Генерация эмбеддингов для фотографий...")


def get_avg_image_embedding(photo_urls, model):
    embeddings = []
    for url in photo_urls:
        try:
            import requests
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                from io import BytesIO
                img = Image.open(BytesIO(response.content)).convert('RGB')
                img_emb = model.encode(img)
                embeddings.append(img_emb)
                print(f"    Загружено фото: {url[:50]}...")
        except Exception as e:
            print(f"    Ошибка загрузки {url}: {e}")
            continue

    if not embeddings:
        return np.zeros(model.get_sentence_embedding_dimension())

    return np.mean(embeddings, axis=0)


image_embeddings = []
for idx, row in df.iterrows():
    print(f"  Обработка квартиры {row['id']}...")
    emb = get_avg_image_embedding(row.get('photo_urls', []), model)
    image_embeddings.append(emb)

image_emb_df = pd.DataFrame(
    image_embeddings,
    columns=[f'img_emb_{i}' for i in range(len(image_embeddings[0]))]
)

print("\n4. Формирование датасета с эмбеддингами...")

# Базовые признаки
feature_cols = ['price', 'area', 'floor', 'total_floors']
X_base = df[feature_cols].reset_index(drop=True)

# Текстовые эмбеддинги
text_embeddings = model.encode(df['description'].tolist())
text_emb_df = pd.DataFrame(
    text_embeddings,
    columns=[f'text_emb_{i}' for i in range(text_embeddings.shape[1])]
)

# Объединяем всё вместе
X_augmented = pd.concat([X_base, text_emb_df, image_emb_df], axis=1)

print(f"\nРезультат:")
print(f"Исходных признаков: {X_base.shape[1]}")
print(f"Текстовых эмбеддингов: {text_emb_df.shape[1]}")
print(f"Визуальных эмбеддингов: {image_emb_df.shape[1]}")
print(f"Всего признаков в обогащённом датасете: {X_augmented.shape[1]}")
print(f"Количество квартир: {len(df)}")

print("\n5. Пример визуального эмбеддинга для первой квартиры:")
print(f"Размер вектора: {len(image_embeddings[0])}")
print(f"Первые 10 значений: {image_embeddings[0][:10]}")

print("\n6. Пример текстового эмбеддинга для первой квартиры:")
print(f"Размер вектора: {len(text_embeddings[0])}")
print(f"Первые 10 значений: {text_embeddings[0][:10]}")

print("Готово! Векторы изображений добавлены в датасет.")
print("Теперь у каждой квартиры есть визуальное представление интерьера.")
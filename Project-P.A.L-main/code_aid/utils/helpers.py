import json
import os
from datetime import datetime

def load_json_file(filepath, default=None):
    """Загружает данные из JSON файла"""
    if default is None:
        default = {}
    
    try:
        if os.path.exists(filepath):
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
    except Exception as e:
        print(f"Ошибка загрузки файла {filepath}: {e}")
    
    return default

def save_json_file(filepath, data):
    """Сохраняет данные в JSON файл"""
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        print(f"Ошибка сохранения файла {filepath}: {e}")
        return False

def format_code_time_complexity(complexity):
    """Форматирует описание сложности алгоритма"""
    complexities = {
        "O(1)": "Константная сложность",
        "O(log n)": "Логарифмическая сложность",
        "O(n)": "Линейная сложность",
        "O(n log n)": "Линейно-логарифмическая сложность",
        "O(n²)": "Квадратичная сложность",
        "O(2ⁿ)": "Экспоненциальная сложность",
        "O(n!)": "Факториальная сложность"
    }
    
    return complexities.get(complexity, complexity)

def get_timestamp():
    """Возвращает текущую метку времени"""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def count_snippets_by_language(snippets_data):
    """Подсчитывает количество примеров по языкам"""
    stats = {}
    for lang, topics in snippets_data.items():
        total = 0
        for topic_examples in topics.values():
            total += len(topic_examples)
        stats[lang] = total
    return stats

def filter_snippets_by_tag(snippets_data, tag):
    """Фильтрует примеры по тегу"""
    results = []
    for lang, topics in snippets_data.items():
        for topic_name, examples in topics.items():
            for example in examples:
                if 'tags' in example and tag in example['tags']:
                    results.append({
                        'language': lang,
                        'topic': topic_name,
                        'title': example['title']
                    })
    return results
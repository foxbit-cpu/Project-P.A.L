python_snippets = {
    "Основы Python": [
        {
            "title": "Приветствие",
            "code": "# Простая функция приветствия\ndef greet(name):\n    return f\"Привет, {name}!\"\n\nprint(greet(\"Мир\"))",
            "explanation": "Функция принимает имя и возвращает приветствие",
            "use_case": "Начало изучения Python, создание функций",
            "complexity": "O(1)",
            "tags": ["функции", "строки", "основы"]
        },
        {
            "title": "Калькулятор",
            "code": "# Простой калькулятор\nimport operator\n\noperations = {\n    '+': operator.add,\n    '-': operator.sub,\n    '*': operator.mul,\n    '/': operator.truediv\n}\n\ndef calculate(a, b, op):\n    return operations[op](a, b)\n\nprint(calculate(10, 5, '+'))  # 15",
            "explanation": "Использование словаря функций для калькулятора",
            "use_case": "Обработка пользовательского ввода, меню операций",
            "complexity": "O(1)",
            "tags": ["словари", "функции", "математика"]
        }
    ],
    
    "Алгоритмы": [
        {
            "title": "Бинарный поиск",
            "code": "def binary_search(arr, target):\n    left, right = 0, len(arr) - 1\n    \n    while left <= right:\n        mid = (left + right) // 2\n        \n        if arr[mid] == target:\n            return mid\n        elif arr[mid] < target:\n            left = mid + 1\n        else:\n            right = mid - 1\n    \n    return -1\n\n# Пример использования\narr = [1, 3, 5, 7, 9, 11]\nprint(binary_search(arr, 7))  # 3",
            "explanation": "Алгоритм поиска в отсортированном массиве",
            "use_case": "Поиск в больших отсортированных массивах",
            "complexity": "O(log n)",
            "tags": ["поиск", "алгоритмы", "сортировка"]
        },
        {
            "title": "Сортировка пузырьком",
            "code": "def bubble_sort(arr):\n    n = len(arr)\n    \n    for i in range(n):\n        # Флаг для оптимизации\n        swapped = False\n        \n        for j in range(0, n - i - 1):\n            if arr[j] > arr[j + 1]:\n                arr[j], arr[j + 1] = arr[j + 1], arr[j]\n                swapped = True\n        \n        # Если не было обменов, массив отсортирован\n        if not swapped:\n            break\n    \n    return arr\n\nprint(bubble_sort([64, 34, 25, 12, 22, 11, 90]))",
            "explanation": "Простейший алгоритм сортировки",
            "use_case": "Обучение алгоритмам, сортировка небольших массивов",
            "complexity": "O(n²)",
            "tags": ["сортировка", "алгоритмы", "массивы"]
        }
    ],
    
    "Структуры данных": [
        {
            "title": "Стек на списке",
            "code": "class Stack:\n    def __init__(self):\n        self.items = []\n    \n    def push(self, item):\n        self.items.append(item)\n    \n    def pop(self):\n        if not self.is_empty():\n            return self.items.pop()\n        return None\n    \n    def peek(self):\n        if not self.is_empty():\n            return self.items[-1]\n        return None\n    \n    def is_empty(self):\n        return len(self.items) == 0\n    \n    def size(self):\n        return len(self.items)\n\n# Пример использования\nstack = Stack()\nstack.push(1)\nstack.push(2)\nprint(stack.pop())  # 2",
            "explanation": "Реализация стека (LIFO) на основе списка",
            "use_case": "Обработка выражений, отмена действий, рекурсия",
            "complexity": "O(1) для push/pop",
            "tags": ["стек", "структуры данных", "ООП"]
        },
        {
            "title": "Очередь на списке",
            "code": "from collections import deque\n\nclass Queue:\n    def __init__(self):\n        self.items = deque()\n    \n    def enqueue(self, item):\n        self.items.append(item)\n    \n    def dequeue(self):\n        if not self.is_empty():\n            return self.items.popleft()\n        return None\n    \n    def is_empty(self):\n        return len(self.items) == 0\n    \n    def size(self):\n        return len(self.items)\n\nqueue = Queue()\nqueue.enqueue('a')\nqueue.enqueue('b')\nprint(queue.dequeue())  # 'a'",
            "explanation": "Реализация очереди (FIFO) с использованием deque",
            "use_case": "Очереди задач, BFS обход графов",
            "complexity": "O(1) для enqueue/dequeue",
            "tags": ["очередь", "структуры данных", "алгоритмы"]
        }
    ],
    
    "Работа с файлами": [
        {
            "title": "Чтение и запись JSON",
            "code": "import json\n\n# Запись данных в JSON\ndata = {\n    'name': 'Alice',\n    'age': 30,\n    'skills': ['Python', 'Java']\n}\n\nwith open('data.json', 'w', encoding='utf-8') as f:\n    json.dump(data, f, ensure_ascii=False, indent=2)\n\n# Чтение данных из JSON\nwith open('data.json', 'r', encoding='utf-8') as f:\n    loaded_data = json.load(f)\n    print(loaded_data['name'])  # Alice",
            "explanation": "Сериализация и десериализация JSON данных",
            "use_case": "Конфигурация, хранение данных, API",
            "complexity": "O(n)",
            "tags": ["json", "файлы", "сериализация"]
        },
        {
            "title": "Обработка CSV",
            "code": "import csv\n\n# Запись в CSV\nwith open('data.csv', 'w', newline='', encoding='utf-8') as f:\n    writer = csv.writer(f)\n    writer.writerow(['Name', 'Age', 'City'])\n    writer.writerow(['Alice', 30, 'Moscow'])\n    writer.writerow(['Bob', 25, 'London'])\n\n# Чтение из CSV\nwith open('data.csv', 'r', encoding='utf-8') as f:\n    reader = csv.reader(f)\n    for row in reader:\n        print(row)",
            "explanation": "Работа с CSV файлами для табличных данных",
            "use_case": "Импорт/экспорт данных, отчеты",
            "complexity": "O(n)",
            "tags": ["csv", "файлы", "данные"]
        }
    ]
}
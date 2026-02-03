java_snippets = {
    "Основы Java": [
        {
            "title": "Hello World",
            "code": "public class HelloWorld {\n    public static void main(String[] args) {\n        System.out.println(\"Hello, World!\");\n    }\n}",
            "explanation": "Базовая программа на Java",
            "use_case": "Начало изучения Java",
            "complexity": "O(1)",
            "tags": ["основы", "вывод"]
        },
        {
            "title": "Класс и объект",
            "code": "public class Person {\n    private String name;\n    private int age;\n    \n    public Person(String name, int age) {\n        this.name = name;\n        this.age = age;\n    }\n    \n    public String getName() { return name; }\n    public void setName(String name) { this.name = name; }\n    \n    public void sayHello() {\n        System.out.println(\"Hello, I'm \" + name);\n    }\n}\n\n// Использование\nPerson person = new Person(\"Alice\", 30);\nperson.sayHello();",
            "explanation": "Создание класса и работа с объектами",
            "use_case": "ООП в Java, инкапсуляция",
            "complexity": "O(1)",
            "tags": ["ООП", "классы", "объекты"]
        }
    ],
    
    "Коллекции": [
        {
            "title": "ArrayList",
            "code": "import java.util.ArrayList;\n\npublic class ArrayListExample {\n    public static void main(String[] args) {\n        ArrayList<String> list = new ArrayList<>();\n        \n        // Добавление элементов\n        list.add(\"Apple\");\n        list.add(\"Banana\");\n        list.add(\"Cherry\");\n        \n        // Перебор элементов\n        for (String fruit : list) {\n            System.out.println(fruit);\n        }\n        \n        // Получение элемента\n        System.out.println(list.get(1));  // Banana\n    }\n}",
            "explanation": "Динамический массив в Java",
            "use_case": "Хранение коллекций переменного размера",
            "complexity": "O(1) для get/set, O(n) для вставки",
            "tags": ["коллекции", "массивы", "списки"]
        },
        {
            "title": "HashMap",
            "code": "import java.util.HashMap;\n\npublic class HashMapExample {\n    public static void main(String[] args) {\n        HashMap<String, Integer> map = new HashMap<>();\n        \n        // Добавление пар ключ-значение\n        map.put(\"Apple\", 10);\n        map.put(\"Banana\", 5);\n        map.put(\"Cherry\", 15);\n        \n        // Получение значения\n        System.out.println(map.get(\"Apple\"));  // 10\n        \n        // Проверка наличия ключа\n        System.out.println(map.containsKey(\"Banana\"));  // true\n        \n        // Перебор элементов\n        for (String key : map.keySet()) {\n            System.out.println(key + \": \" + map.get(key));\n        }\n    }\n}",
            "explanation": "Хэш-таблица для хранения пар ключ-значение",
            "use_case": "Быстрый поиск по ключу, кэширование",
            "complexity": "O(1) в среднем случае",
            "tags": ["коллекции", "словари", "хэш-таблицы"]
        }
    ]
}
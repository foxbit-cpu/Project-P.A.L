csharp_snippets = {
    "Основы C#": [
        {
            "title": "Hello World на C#",
            "code": "using System;\n\nclass Program\n{\n    static void Main()\n    {\n        Console.WriteLine(\"Hello, World!\");\n    }\n}",
            "explanation": "Базовая программа на C#",
            "use_case": "Начало изучения C#",
            "complexity": "O(1)",
            "tags": ["основы", "вывод"]
        },
        {
            "title": "Классы и свойства",
            "code": "using System;\n\npublic class Product\n{\n    public string Name { get; set; }\n    public decimal Price { get; set; }\n    public int Stock { get; set; }\n    \n    public Product(string name, decimal price, int stock)\n    {\n        Name = name;\n        Price = price;\n        Stock = stock;\n    }\n    \n    public decimal CalculateTotalValue()\n    {\n        return Price * Stock;\n    }\n}\n\nclass Program\n{\n    static void Main()\n    {\n        Product product = new Product(\"Laptop\", 999.99m, 10);\n        Console.WriteLine($\"{product.Name}: {product.CalculateTotalValue():C}\");\n    }\n}",
            "explanation": "Класс с свойствами и методами в C#",
            "use_case": "ООП в C#, инкапсуляция данных",
            "complexity": "O(1)",
            "tags": ["ООП", "классы", "свойства"]
        }
    ],
    
    "LINQ и коллекции": [
        {
            "title": "Работа с List",
            "code": "using System;\nusing System.Collections.Generic;\n\nclass Program\n{\n    static void Main()\n    {\n        List<string> fruits = new List<string> {\"Apple\", \"Banana\", \"Cherry\"};\n        \n        // Добавление элемента\n        fruits.Add(\"Date\");\n        \n        // Удаление элемента\n        fruits.Remove(\"Banana\");\n        \n        // Перебор элементов\n        foreach (string fruit in fruits)\n        {\n            Console.WriteLine(fruit);\n        }\n        \n        // Проверка наличия элемента\n        bool hasApple = fruits.Contains(\"Apple\");\n        Console.WriteLine($\"Has Apple: {hasApple}\");\n    }\n}",
            "explanation": "Обобщенный список в C#",
            "use_case": "Хранение коллекций объектов",
            "complexity": "O(n) для поиска, O(1) для доступа",
            "tags": ["коллекции", "списки", "обобщения"]
        },
        {
            "title": "LINQ запросы",
            "code": "using System;\nusing System.Collections.Generic;\nusing System.Linq;\n\nclass Program\n{\n    static void Main()\n    {\n        List<int> numbers = new List<int> {1, 2, 3, 4, 5, 6, 7, 8, 9, 10};\n        \n        // Фильтрация четных чисел\n        var evenNumbers = numbers.Where(n => n % 2 == 0);\n        \n        // Проекция (квадраты чисел)\n        var squares = numbers.Select(n => n * n);\n        \n        // Сортировка\n        var sorted = numbers.OrderByDescending(n => n);\n        \n        // Агрегация\n        int sum = numbers.Sum();\n        double average = numbers.Average();\n        \n        Console.WriteLine($\"Sum: {sum}, Average: {average:F2}\");\n        \n        // Вывод четных чисел\n        foreach (int num in evenNumbers)\n        {\n            Console.Write(num + \" \");\n        }\n    }\n}",
            "explanation": "Language Integrated Query в C#",
            "use_case": "Запросы к коллекциям данных",
            "complexity": "O(n) для большинства операций",
            "tags": ["LINQ", "коллекции", "запросы"]
        }
    ]
}
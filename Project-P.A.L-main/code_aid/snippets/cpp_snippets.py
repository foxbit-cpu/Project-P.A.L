cpp_snippets = {
    "Основы C++": [
        {
            "title": "Hello World на C++",
            "code": "#include <iostream>\n\nint main() {\n    std::cout << \"Hello, World!\" << std::endl;\n    return 0;\n}",
            "explanation": "Базовая программа на C++ с использованием iostream",
            "use_case": "Начало изучения C++",
            "complexity": "O(1)",
            "tags": ["основы", "вывод"]
        },
        {
            "title": "Классы и объекты",
            "code": "#include <iostream>\n#include <string>\n\nclass Car {\nprivate:\n    std::string brand;\n    int year;\n    \npublic:\n    Car(std::string b, int y) : brand(b), year(y) {}\n    \n    void displayInfo() {\n        std::cout << \"Brand: \" << brand << \", Year: \" << year << std::endl;\n    }\n    \n    std::string getBrand() { return brand; }\n    void setBrand(std::string b) { brand = b; }\n};\n\nint main() {\n    Car myCar(\"Toyota\", 2020);\n    myCar.displayInfo();\n    return 0;\n}",
            "explanation": "Создание класса с конструктором и методами",
            "use_case": "ООП в C++, инкапсуляция",
            "complexity": "O(1)",
            "tags": ["ООП", "классы", "объекты"]
        }
    ],
    
    "STL (Standard Template Library)": [
        {
            "title": "Вектор (Vector)",
            "code": "#include <iostream>\n#include <vector>\n\nint main() {\n    std::vector<int> numbers = {1, 2, 3, 4, 5};\n    \n    // Добавление элементов\n    numbers.push_back(6);\n    numbers.push_back(7);\n    \n    // Доступ к элементам\n    std::cout << \"First element: \" << numbers[0] << std::endl;\n    std::cout << \"Size: \" << numbers.size() << std::endl;\n    \n    // Итерация по вектору\n    for (int num : numbers) {\n        std::cout << num << \" \";\n    }\n    std::cout << std::endl;\n    \n    return 0;\n}",
            "explanation": "Динамический массив из STL",
            "use_case": "Хранение последовательностей данных",
            "complexity": "O(1) для доступа, O(n) для вставки",
            "tags": ["STL", "вектор", "массивы"]
        },
        {
            "title": "Карта (Map)",
            "code": "#include <iostream>\n#include <map>\n#include <string>\n\nint main() {\n    std::map<std::string, int> scores;\n    \n    // Вставка элементов\n    scores[\"Alice\"] = 95;\n    scores[\"Bob\"] = 87;\n    scores[\"Charlie\"] = 92;\n    \n    // Поиск элемента\n    auto it = scores.find(\"Alice\");\n    if (it != scores.end()) {\n        std::cout << \"Alice's score: \" << it->second << std::endl;\n    }\n    \n    // Итерация по карте\n    for (const auto& pair : scores) {\n        std::cout << pair.first << \": \" << pair.second << std::endl;\n    }\n    \n    return 0;\n}",
            "explanation": "Ассоциативный контейнер из STL",
            "use_case": "Хранение пар ключ-значение",
            "complexity": "O(log n) для операций",
            "tags": ["STL", "map", "словари"]
        }
    ]
}
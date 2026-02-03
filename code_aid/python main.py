import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, font
import pyperclip
import json
import os
import sys
import subprocess
import tempfile
import random
from datetime import datetime

# Добавляем пути к модулям
sys.path.append(os.path.join(os.path.dirname(__file__), 'snippets'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'warmups'))

# Импортируем данные
from snippets.python_snippets import python_snippets
from snippets.java_snippets import java_snippets
from snippets.cpp_snippets import cpp_snippets
from snippets.csharp_snippets import csharp_snippets

from warmups.python_warmups import python_warmups
from warmups.java_warmups import java_warmups
from warmups.cpp_warmups import cpp_warmups
from warmups.csharp_warmups import csharp_warmups

# Собираем все данные в словари
ALL_SNIPPETS = {
    "Python": python_snippets,
    "Java": java_snippets,
    "C++": cpp_snippets,
    "C#": csharp_snippets
}

ALL_WARMUPS = {
    "Python": python_warmups,
    "Java": java_warmups,
    "C++": cpp_warmups,
    "C#": csharp_warmups
}


class CodeAidApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Programming Aid & Liberator v3.0")
        self.root.geometry("1100x800")
        self.root.minsize(900, 650)
        
        # Иконка приложения
        try:
            self.root.iconbitmap(default='icon.ico')
        except:
            pass
        
        # Загрузка настроек
        self.settings = self.load_settings()
        
        # Переменные для состояния
        self.lang_var = tk.StringVar()
        self.topic_var = tk.StringVar()
        self.search_var = tk.StringVar()
        self.font_size_var = tk.IntVar(value=self.settings.get('font_size', 11))
        self.dark_mode_var = tk.BooleanVar(value=self.settings.get('dark_mode', False))
        
        # Данные
        self.snippets_data = ALL_SNIPPETS
        self.warmups_data = ALL_WARMUPS
        
        # История и избранное
        self.history = []
        self.history_index = -1
        self.favorites = set()
        self.load_favorites()
        
        # Текущие вопросы для разогрева
        self.current_warmup = None
        self.warmup_score = 0
        self.warmup_total = 0
        
        # Создание интерфейса
        self.setup_styles()
        self.create_widgets()
        
        # Заполнение данных
        self.update_lang_combo()
        
        # Установка обработчиков
        self.setup_event_handlers()
        self.setup_keyboard_shortcuts()
        
        # Загрузка первого примера
        self.load_first_example()
        
        # Запуск приветствия
        self.root.after(1000, self.show_welcome_message)

    def setup_styles(self):
        """Настройка стилей элементов интерфейса"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Цветовая схема
        if self.dark_mode_var.get():
            self.bg_color = '#2b2b2b'
            self.fg_color = '#ffffff'
            self.code_bg = '#1e1e1e'
            self.code_fg = '#d4d4d4'
            self.listbox_bg = '#3c3c3c'
            self.listbox_fg = '#ffffff'
            self.accent_color = '#569cd6'
            self.error_color = '#f48771'
            self.success_color = '#89d185'
        else:
            self.bg_color = '#f8f9fa'
            self.fg_color = '#212529'
            self.code_bg = '#ffffff'
            self.code_fg = '#212529'
            self.listbox_bg = '#ffffff'
            self.listbox_fg = '#212529'
            self.accent_color = '#0d6efd'
            self.error_color = '#dc3545'
            self.success_color = '#198754'
        
        # Настройка стилей
        style.configure('TButton', font=('Segoe UI', 9), padding=6)
        style.configure('Title.TLabel', font=('Segoe UI', 20, 'bold'), 
                       foreground=self.accent_color)
        style.configure('Header.TLabel', font=('Segoe UI', 10, 'bold'))
        style.configure('Status.TLabel', font=('Segoe UI', 9), foreground='#6c757d')
        style.configure('Error.TLabel', foreground=self.error_color)
        style.configure('Success.TLabel', foreground=self.success_color)
        
        self.root.configure(bg=self.bg_color)

    def create_widgets(self):
        """Создание всех элементов интерфейса"""
        # Главный контейнер
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Заголовок
        header_frame = ttk.Frame(main_frame)
        header_frame.pack(fill='x', pady=(0, 20))
        
        title_label = ttk.Label(header_frame, 
            text="🚀 Programming Aid & Liberator", 
            style='Title.TLabel')
        title_label.pack(side='left')
        
        # Статистика в заголовке
        stats_frame = ttk.Frame(header_frame)
        stats_frame.pack(side='right')
        
        self.stats_label = ttk.Label(stats_frame, 
            text="Загружено примеров: 0", 
            style='Status.TLabel')
        self.stats_label.pack(anchor='e')
        
        # Панель навигации
        nav_frame = ttk.LabelFrame(main_frame, text="Навигация", padding=15)
        nav_frame.pack(fill='x', pady=(0, 20))
        
        # Первый ряд: выбор языка и темы
        row1 = ttk.Frame(nav_frame)
        row1.pack(fill='x', pady=(0, 10))
        
        # Язык программирования
        lang_frame = ttk.Frame(row1)
        lang_frame.pack(side='left', fill='x', expand=True, padx=(0, 15))
        
        ttk.Label(lang_frame, text="Язык программирования:",
                 style='Header.TLabel').pack(anchor='w')
        self.lang_combo = ttk.Combobox(lang_frame, 
            textvariable=self.lang_var,
            state='readonly',
            font=('Segoe UI', 10))
        self.lang_combo.pack(fill='x', pady=(5, 0))
        
        # Категория
        topic_frame = ttk.Frame(row1)
        topic_frame.pack(side='left', fill='x', expand=True, padx=(0, 15))
        
        ttk.Label(topic_frame, text="Категория:",
                 style='Header.TLabel').pack(anchor='w')
        self.topic_combo = ttk.Combobox(topic_frame,
            textvariable=self.topic_var,
            state='readonly',
            font=('Segoe UI', 10))
        self.topic_combo.pack(fill='x', pady=(5, 0))
        
        # Второй ряд: поиск и кнопки
        row2 = ttk.Frame(nav_frame)
        row2.pack(fill='x')
        
        # Поиск
        search_frame = ttk.Frame(row2)
        search_frame.pack(side='left', fill='x', expand=True)
        
        ttk.Label(search_frame, text="Поиск:",
                 style='Header.TLabel').pack(anchor='w')
        
        search_container = ttk.Frame(search_frame)
        search_container.pack(fill='x', pady=(5, 0))
        
        self.search_entry = ttk.Entry(search_container,
            textvariable=self.search_var,
            font=('Segoe UI', 10))
        self.search_entry.pack(side='left', fill='x', expand=True)
        
        ttk.Button(search_container, text="🔍", width=3,
                  command=self.on_search).pack(side='left', padx=(5, 2))
        ttk.Button(search_container, text="✖", width=3,
                  command=self.clear_search).pack(side='left')
        
        # Кнопки действий
        action_frame = ttk.Frame(row2)
        action_frame.pack(side='right', padx=(20, 0))
        
        ttk.Button(action_frame, text="🔥 Разогрев",
                  command=self.start_warmup).pack(side='left', padx=2)
        ttk.Button(action_frame, text="⭐ Избранное",
                  command=self.show_favorites).pack(side='left', padx=2)
        
        # Основная область
        content_frame = ttk.Frame(main_frame)
        content_frame.pack(fill='both', expand=True)
        
        # Левая панель (список примеров)
        left_panel = ttk.LabelFrame(content_frame, text="Примеры кода", padding=10)
        left_panel.pack(side='left', fill='y', padx=(0, 10))
        left_panel.pack_propagate(False)
        left_panel.configure(width=300)
        
        # Панель инструментов списка
        list_toolbar = ttk.Frame(left_panel)
        list_toolbar.pack(fill='x', pady=(0, 10))
        
        self.fav_btn = ttk.Button(list_toolbar, text="☆", width=3,
                                 command=self.toggle_favorite)
        self.fav_btn.pack(side='left', padx=(0, 5))
        
        self.count_label = ttk.Label(list_toolbar, 
            text="Примеров: 0",
            style='Status.TLabel')
        self.count_label.pack(side='right')
        
        # Список примеров
        list_container = ttk.Frame(left_panel)
        list_container.pack(fill='both', expand=True)
        
        scrollbar = ttk.Scrollbar(list_container)
        scrollbar.pack(side='right', fill='y')
        
        self.examples_listbox = tk.Listbox(list_container,
            yscrollcommand=scrollbar.set,
            font=('Segoe UI', 10),
            bg=self.listbox_bg,
            fg=self.listbox_fg,
            selectbackground=self.accent_color,
            selectforeground='white',
            relief='flat',
            highlightthickness=0)
        self.examples_listbox.pack(side='left', fill='both', expand=True)
        scrollbar.config(command=self.examples_listbox.yview)
        
        # Правая панель (код и объяснение)
        right_panel = ttk.Frame(content_frame)
        right_panel.pack(side='left', fill='both', expand=True)
        
        # Вкладки
        self.notebook = ttk.Notebook(right_panel)
        self.notebook.pack(fill='both', expand=True)
        
        # Вкладка с кодом
        code_tab = ttk.Frame(self.notebook)
        self.notebook.add(code_tab, text="Код")
        
        # Панель инструментов кода
        code_toolbar = ttk.Frame(code_tab)
        code_toolbar.pack(fill='x', pady=(0, 10))
        
        ttk.Button(code_toolbar, text="📋 Копировать",
                  command=self.copy_code).pack(side='left', padx=(0, 5))
        ttk.Button(code_toolbar, text="💾 Сохранить",
                  command=self.save_code_to_file).pack(side='left', padx=5)
        ttk.Button(code_toolbar, text="▶ Запустить",
                  command=self.run_code).pack(side='left', padx=5)
        
        # Размер шрифта
        ttk.Label(code_toolbar, text="Шрифт:").pack(side='left', padx=(20, 5))
        ttk.Spinbox(code_toolbar, from_=8, to=20,
                   textvariable=self.font_size_var,
                   width=4,
                   command=self.update_font_size).pack(side='left')
        
        # Область кода
        code_container = ttk.Frame(code_tab)
        code_container.pack(fill='both', expand=True)
        
        self.code_text = scrolledtext.ScrolledText(code_container,
            font=('Cascadia Code', self.font_size_var.get()),
            wrap=tk.WORD,
            bg=self.code_bg,
            fg=self.code_fg,
            insertbackground=self.code_fg,
            relief='flat',
            padx=15,
            pady=15)
        self.code_text.pack(fill='both', expand=True)
        
        # Настройка тегов для подсветки
        self.setup_syntax_highlighting()
        
        # Вкладка с объяснением
        explanation_tab = ttk.Frame(self.notebook)
        self.notebook.add(explanation_tab, text="Объяснение")
        
        self.explanation_text = scrolledtext.ScrolledText(explanation_tab,
            font=('Segoe UI', 11),
            wrap=tk.WORD,
            bg=self.code_bg,
            fg=self.code_fg,
            relief='flat',
            padx=15,
            pady=15)
        self.explanation_text.pack(fill='both', expand=True)
        
        # Вкладка для разогрева
        self.warmup_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.warmup_tab, text="Разогрев")
        
        # Инициализация вкладки разогрева
        self.init_warmup_tab()
        
        # Статус бар
        status_frame = ttk.Frame(main_frame, height=30, relief='sunken')
        status_frame.pack(fill='x', pady=(15, 0))
        status_frame.pack_propagate(False)
        
        self.status_label = ttk.Label(status_frame,
            text="Готов к работе",
            style='Status.TLabel')
        self.status_label.pack(side='left', padx=15)
        
        # Индикатор темы
        theme_btn = ttk.Checkbutton(status_frame,
            text="Темная тема",
            variable=self.dark_mode_var,
            command=self.toggle_theme)
        theme_btn.pack(side='right', padx=15)

    def init_warmup_tab(self):
        """Инициализация вкладки разогрева"""
        # Очищаем вкладку
        for widget in self.warmup_tab.winfo_children():
            widget.destroy()
        
        # Контейнер для разогрева
        warmup_container = ttk.Frame(self.warmup_tab)
        warmup_container.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Заголовок
        ttk.Label(warmup_container,
            text="🔥 Разогрев: Алгоритмы и задачи",
            font=('Segoe UI', 16, 'bold'),
            foreground=self.accent_color).pack(pady=(0, 20))
        
        # Область для вопросов
        self.warmup_frame = ttk.Frame(warmup_container)
        self.warmup_frame.pack(fill='both', expand=True)
        
        # Кнопки управления
        btn_frame = ttk.Frame(warmup_container)
        btn_frame.pack(fill='x', pady=(20, 0))
        
        ttk.Button(btn_frame, text="Начать разогрев",
                  command=self.start_warmup).pack(side='left')
        ttk.Button(btn_frame, text="Сбросить",
                  command=self.reset_warmup).pack(side='left', padx=10)
        
        # Статистика разогрева
        self.warmup_stats = ttk.Label(btn_frame,
            text="Пройдено: 0/0 | Счет: 0",
            style='Status.TLabel')
        self.warmup_stats.pack(side='right')

    def setup_event_handlers(self):
        """Настройка обработчиков событий"""
        self.lang_var.trace('w', self.on_lang_changed)
        self.topic_var.trace('w', self.on_topic_changed)
        self.search_var.trace('w', lambda *args: self.root.after(500, self.on_search))
        self.examples_listbox.bind('<<ListboxSelect>>', self.on_example_selected)
        self.font_size_var.trace('w', lambda *args: self.update_font_size())
        
        # Двойной клик
        self.examples_listbox.bind('<Double-Button-1>', self.on_example_selected)
        
        # Закрытие окна
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def setup_keyboard_shortcuts(self):
        """Настройка горячих клавиш"""
        shortcuts = [
            ('<Control-c>', self.copy_code),
            ('<Control-s>', self.save_code_to_file),
            ('<Control-f>', lambda e: self.search_entry.focus()),
            ('<Control-r>', self.run_code),
            ('<Control-w>', self.start_warmup),
            ('<F1>', self.show_help),
            ('<F5>', self.refresh_data),
        ]
        
        for shortcut, handler in shortcuts:
            self.root.bind(shortcut, handler)

    def setup_syntax_highlighting(self):
        """Настройка подсветки синтаксиса"""
        colors = {
            'keyword': '#569cd6' if self.dark_mode_var.get() else '#0000ff',
            'string': '#ce9178' if self.dark_mode_var.get() else '#a31515',
            'comment': '#6a9955' if self.dark_mode_var.get() else '#008000',
            'number': '#b5cea8' if self.dark_mode_var.get() else '#098658',
            'function': '#dcdcaa' if self.dark_mode_var.get() else '#795e26',
        }
        
        for tag, color in colors.items():
            self.code_text.tag_config(tag, foreground=color)

    def update_lang_combo(self):
        """Заполняет комбобокс списком языков"""
        languages = list(self.snippets_data.keys())
        self.lang_combo['values'] = languages
        if languages:
            self.lang_combo.current(0)
        self.update_stats()

    def on_lang_changed(self, *args):
        """При изменении языка обновляет список тем"""
        lang = self.lang_var.get()
        if lang in self.snippets_data:
            topics = list(self.snippets_data[lang].keys())
            self.topic_combo['values'] = topics
            if topics:
                self.topic_combo.current(0)
        else:
            self.topic_combo['values'] = []
            self.topic_var.set('')
            self.examples_listbox.delete(0, tk.END)
        self.update_stats()

    def on_topic_changed(self, *args):
        """При изменении темы обновляет список примеров"""
        lang = self.lang_var.get()
        topic = self.topic_var.get()
        
        self.examples_listbox.delete(0, tk.END)
        
        if lang in self.snippets_data and topic in self.snippets_data[lang]:
            for snippet in self.snippets_data[lang][topic]:
                self.examples_listbox.insert(tk.END, snippet['title'])
            
            if self.examples_listbox.size() > 0:
                self.examples_listbox.selection_set(0)
                self.on_example_selected(None)
        
        self.update_status(f"Тема: {topic}")
        self.update_stats()

    def on_example_selected(self, event=None):
        """При выборе примера отображает код и пояснение"""
        selection = self.examples_listbox.curselection()
        if not selection:
            return
            
        idx = selection[0]
        lang = self.lang_var.get()
        topic = self.topic_var.get()
        
        if lang in self.snippets_data and topic in self.snippets_data[lang]:
            snippet = self.snippets_data[lang][topic][idx]
            
            # Добавляем в историю
            self.add_to_history(lang, topic, idx)
            
            # Обновляем код
            self.code_text.delete(1.0, tk.END)
            self.code_text.insert(1.0, snippet['code'])
            self.apply_syntax_highlighting(lang)
            
            # Обновляем объяснение
            self.explanation_text.delete(1.0, tk.END)
            explanation = f"📖 {snippet['explanation']}\n\n"
            explanation += f"🎯 Применение: {snippet['use_case']}\n\n"
            if 'complexity' in snippet:
                explanation += f"⚡ Сложность: {snippet['complexity']}\n"
            if 'tags' in snippet:
                explanation += f"🏷️ Теги: {', '.join(snippet['tags'])}"
            self.explanation_text.insert(1.0, explanation)
            
            # Обновляем кнопку избранного
            self.update_favorite_button(lang, topic, idx)
            
            self.update_status(f"Загружен: {snippet['title']}")
            self.notebook.select(0)  # Переключаем на вкладку кода

    def apply_syntax_highlighting(self, lang):
        """Применяет подсветку синтаксиса для выбранного языка"""
        # Базовая реализация - можно расширить
        if lang == "Python":
            self.highlight_python()
        elif lang == "Java":
            self.highlight_java()
        elif lang == "C++":
            self.highlight_cpp()
        elif lang == "C#":
            self.highlight_csharp()

    def highlight_python(self):
        """Подсветка синтаксиса Python"""
        keywords = [
            'def', 'class', 'if', 'elif', 'else', 'for', 'while',
            'try', 'except', 'finally', 'with', 'import', 'from',
            'as', 'return', 'yield', 'async', 'await', 'lambda'
        ]
        
        self.highlight_keywords(keywords, 'keyword')

    def highlight_java(self):
        """Подсветка синтаксиса Java"""
        keywords = [
            'public', 'private', 'protected', 'class', 'interface',
            'extends', 'implements', 'void', 'int', 'String', 'boolean',
            'if', 'else', 'for', 'while', 'try', 'catch', 'finally',
            'return', 'new', 'static', 'final'
        ]
        
        self.highlight_keywords(keywords, 'keyword')

    def highlight_cpp(self):
        """Подсветка синтаксиса C++"""
        keywords = [
            'int', 'float', 'double', 'char', 'void', 'bool',
            'if', 'else', 'for', 'while', 'do', 'switch', 'case',
            'class', 'struct', 'public', 'private', 'protected',
            'virtual', 'override', 'template', 'typename', 'namespace',
            'return', 'new', 'delete', 'const', 'static'
        ]
        
        self.highlight_keywords(keywords, 'keyword')

    def highlight_csharp(self):
        """Подсветка синтаксиса C#"""
        keywords = [
            'public', 'private', 'protected', 'internal', 'class',
            'interface', 'namespace', 'using', 'var', 'void', 'int',
            'string', 'bool', 'if', 'else', 'for', 'foreach', 'while',
            'switch', 'case', 'break', 'continue', 'return', 'new',
            'this', 'base', 'virtual', 'override', 'async', 'await',
            'try', 'catch', 'finally', 'throw'
        ]
        
        self.highlight_keywords(keywords, 'keyword')

    def highlight_keywords(self, keywords, tag):
        """Подсветка ключевых слов"""
        code = self.code_text.get(1.0, tk.END)
        
        for keyword in keywords:
            start_pos = '1.0'
            while True:
                start_pos = self.code_text.search(
                    r'\b' + keyword + r'\b',
                    start_pos,
                    stopindex=tk.END,
                    regexp=True
                )
                if not start_pos:
                    break
                end_pos = f"{start_pos}+{len(keyword)}c"
                self.code_text.tag_add(tag, start_pos, end_pos)
                start_pos = end_pos

    def on_search(self, *args):
        """Фильтрует примеры по ключевому слову"""
        query = self.search_var.get().lower().strip()
        lang = self.lang_var.get()
        topic = self.topic_var.get()
        
        self.examples_listbox.delete(0, tk.END)
        
        if not lang or not topic or lang not in self.snippets_data or topic not in self.snippets_data[lang]:
            return
            
        examples = self.snippets_data[lang][topic]
        
        if not query:
            for snippet in examples:
                self.examples_listbox.insert(tk.END, snippet['title'])
        else:
            found_examples = []
            for snippet in examples:
                search_fields = [
                    snippet['title'].lower(),
                    snippet['code'].lower(),
                    snippet['explanation'].lower(),
                    snippet['use_case'].lower()
                ]
                
                if any(query in field for field in search_fields):
                    found_examples.append(snippet['title'])
            
            for title in found_examples:
                self.examples_listbox.insert(tk.END, title)
        
        if self.examples_listbox.size() > 0:
            self.examples_listbox.selection_set(0)
            self.on_example_selected(None)
        
        self.update_status(f"Найдено: {self.examples_listbox.size()} примеров")

    def start_warmup(self):
        """Начинает сессию разогрева"""
        lang = self.lang_var.get()
        topic = self.topic_var.get()
        
        if not lang or not topic:
            messagebox.showwarning("Предупреждение", "Выберите язык и тему для разогрева")
            return
            
        if lang not in self.warmups_data or topic not in self.warmups_data[lang]:
            messagebox.showinfo("Информация", f"Разогрев для темы '{topic}' пока не доступен")
            return
        
        # Получаем вопросы
        questions = self.warmups_data[lang][topic]
        if not questions:
            messagebox.showinfo("Информация", "Вопросы для этой темы еще не добавлены")
            return
        
        # Выбираем 3 случайных вопроса
        selected_questions = random.sample(questions, min(3, len(questions)))
        
        # Сохраняем текущий разогрев
        self.current_warmup = {
            'lang': lang,
            'topic': topic,
            'questions': selected_questions,
            'current_question': 0,
            'score': 0
        }
        
        # Переключаем на вкладку разогрева
        self.notebook.select(2)
        
        # Отображаем первый вопрос
        self.show_warmup_question()

    def show_warmup_question(self):
        """Показывает текущий вопрос разогрева"""
        if not self.current_warmup:
            return
            
        # Очищаем область
        for widget in self.warmup_frame.winfo_children():
            widget.destroy()
        
        question_data = self.current_warmup['questions'][self.current_warmup['current_question']]
        
        # Вопрос
        question_text = ttk.Label(self.warmup_frame,
            text=f"Вопрос {self.current_warmup['current_question'] + 1} из {len(self.current_warmup['questions'])}",
            font=('Segoe UI', 11, 'bold'))
        question_text.pack(anchor='w', pady=(0, 10))
        
        # Текст вопроса
        ttk.Label(self.warmup_frame,
            text=question_data['question'],
            font=('Segoe UI', 12),
            wraplength=600).pack(anchor='w', pady=(0, 20))
        
        # Варианты ответов
        self.answer_vars = []
        
        for i, option in enumerate(question_data['options']):
            var = tk.StringVar(value="")
            self.answer_vars.append(var)
            
            frame = ttk.Frame(self.warmup_frame)
            frame.pack(fill='x', pady=5)
            
            rb = ttk.Radiobutton(frame,
                text=option,
                variable=var,
                value=str(i))
            rb.pack(side='left')
            
            # Сохраняем ссылку на radiobutton для подсветки
            rb.option_index = i
        
        # Кнопки навигации
        btn_frame = ttk.Frame(self.warmup_frame)
        btn_frame.pack(fill='x', pady=(20, 0))
        
        if self.current_warmup['current_question'] > 0:
            ttk.Button(btn_frame, text="← Предыдущий",
                      command=self.prev_warmup_question).pack(side='left')
        
        if self.current_warmup['current_question'] < len(self.current_warmup['questions']) - 1:
            ttk.Button(btn_frame, text="Следующий →",
                      command=self.next_warmup_question).pack(side='right')
        else:
            ttk.Button(btn_frame, text="Завершить",
                      command=self.finish_warmup,
                      style='Success.TButton').pack(side='right')
        
        # Кнопка проверки
        ttk.Button(btn_frame, text="✓ Проверить",
                  command=self.check_warmup_answer,
                  style='Accent.TButton').pack(side='left', padx=(10, 0))
        
        # Обновляем статистику
        self.update_warmup_stats()

    def check_warmup_answer(self):
        """Проверяет ответ на текущий вопрос"""
        if not self.current_warmup:
            return
            
        question_data = self.current_warmup['questions'][self.current_warmup['current_question']]
        
        # Находим выбранный ответ
        selected = None
        for i, var in enumerate(self.answer_vars):
            if var.get():
                selected = i
                break
        
        if selected is None:
            messagebox.showwarning("Предупреждение", "Выберите вариант ответа")
            return
        
        # Проверяем ответ
        is_correct = (selected == question_data['correct'])
        
        if is_correct:
            self.current_warmup['score'] += 1
            messagebox.showinfo("Правильно!", "Верный ответ!")
        else:
            # Подсвечиваем правильный ответ зеленым, неправильный красным
            for widget in self.warmup_frame.winfo_children():
                if hasattr(widget, 'option_index'):
                    if widget.option_index == selected:
                        widget.configure(style='Error.TRadiobutton')
                    elif widget.option_index == question_data['correct']:
                        widget.configure(style='Success.TRadiobutton')
            
            messagebox.showerror("Неправильно", 
                f"Правильный ответ: {question_data['options'][question_data['correct']]}")
        
        # Обновляем статистику
        self.update_warmup_stats()

    def next_warmup_question(self):
        """Переход к следующему вопросу"""
        if self.current_warmup:
            self.current_warmup['current_question'] += 1
            self.show_warmup_question()

    def prev_warmup_question(self):
        """Переход к предыдущему вопросу"""
        if self.current_warmup:
            self.current_warmup['current_question'] -= 1
            self.show_warmup_question()

    def finish_warmup(self):
        """Завершает сессию разогрева"""
        if not self.current_warmup:
            return
            
        score = self.current_warmup['score']
        total = len(self.current_warmup['questions'])
        
        # Показываем результат
        result_text = f"Разогрев завершен!\n\n"
        result_text += f"Правильных ответов: {score} из {total}\n"
        result_text += f"Результат: {score/total*100:.1f}%\n\n"
        
        if score == total:
            result_text += "🎉 Отличный результат! Вы хорошо знаете эту тему!"
        elif score >= total * 0.7:
            result_text += "👍 Хороший результат! Есть что повторить."
        else:
            result_text += "📚 Рекомендуем изучить тему подробнее."
        
        messagebox.showinfo("Результат разогрева", result_text)
        
        # Сбрасываем разогрев
        self.current_warmup = None
        self.init_warmup_tab()

    def update_warmup_stats(self):
        """Обновляет статистику разогрева"""
        if self.current_warmup:
            current = self.current_warmup['current_question'] + 1
            total = len(self.current_warmup['questions'])
            score = self.current_warmup['score']
            
            self.warmup_stats.config(
                text=f"Вопрос: {current}/{total} | Счет: {score}"
            )

    def reset_warmup(self):
        """Сбрасывает текущий разогрев"""
        self.current_warmup = None
        self.init_warmup_tab()
        messagebox.showinfo("Разогрев", "Разогрев сброшен")

    def copy_code(self):
        """Копирует код в буфер обмена"""
        code = self.code_text.get(1.0, tk.END).strip()
        if code:
            try:
                self.root.clipboard_clear()
                self.root.clipboard_append(code)
                self.update_status("Код скопирован")
            except:
                pyperclip.copy(code)
                self.update_status("Код скопирован")

    def save_code_to_file(self):
        """Сохраняет текущий код в файл"""
        code = self.code_text.get(1.0, tk.END).strip()
        if not code:
            return
            
        from tkinter import filedialog
        
        # Определяем расширение по языку
        ext_map = {
            "Python": ".py",
            "Java": ".java",
            "C++": ".cpp",
            "C#": ".cs"
        }
        
        ext = ext_map.get(self.lang_var.get(), ".txt")
        
        file_path = filedialog.asksaveasfilename(
            defaultextension=ext,
            filetypes=[
                ("All files", "*.*"),
                ("Text files", "*.txt"),
                ("Python files", "*.py"),
                ("Java files", "*.java"),
                ("C++ files", "*.cpp"),
                ("C# files", "*.cs")
            ]
        )
        
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(code)
                self.update_status(f"Сохранено: {os.path.basename(file_path)}")
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось сохранить: {str(e)}")

    def run_code(self):
        """Пытается запустить код (только для Python)"""
        if self.lang_var.get() != "Python":
            messagebox.showinfo("Запуск кода", 
                "Автоматический запуск доступен только для Python")
            return
            
        code = self.code_text.get(1.0, tk.END).strip()
        if not code:
            return
            
        # Сохраняем во временный файл и запускаем
        import tempfile
        
        try:
            with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
                f.write(code)
                temp_file = f.name
            
            # Запускаем Python процесс
            result = subprocess.run(['python', temp_file], 
                                  capture_output=True, text=True, timeout=10)
            
            # Показываем результат
            output_window = tk.Toplevel(self.root)
            output_window.title("Результат выполнения")
            output_window.geometry("600x400")
            
            text = scrolledtext.ScrolledText(output_window)
            text.pack(fill='both', expand=True, padx=10, pady=10)
            
            if result.returncode == 0:
                text.insert(1.0, "✅ Выполнение успешно\n\n")
                text.insert(tk.END, result.stdout)
            else:
                text.insert(1.0, "❌ Ошибка выполнения\n\n")
                text.insert(tk.END, result.stderr)
            
            text.config(state='disabled')
            
            # Удаляем временный файл
            os.unlink(temp_file)
            
        except subprocess.TimeoutExpired:
            messagebox.showerror("Ошибка", "Время выполнения истекло")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось запустить код: {str(e)}")

    def add_to_history(self, lang, topic, idx):
        """Добавляет пример в историю"""
        history_item = (lang, topic, idx)
        if not self.history or self.history[-1] != history_item:
            self.history.append(history_item)
            if len(self.history) > 50:
                self.history.pop(0)
            self.history_index = len(self.history) - 1

    def toggle_favorite(self):
        """Добавляет/удаляет текущий пример из избранного"""
        selection = self.examples_listbox.curselection()
        if not selection:
            return
            
        idx = selection[0]
        lang = self.lang_var.get()
        topic = self.topic_var.get()
        
        if lang in self.snippets_data and topic in self.snippets_data[lang]:
            favorite_key = f"{lang}|{topic}|{idx}"
            
            if favorite_key in self.favorites:
                self.favorites.remove(favorite_key)
                self.update_status("Удалено из избранного")
            else:
                self.favorites.add(favorite_key)
                self.update_status("Добавлено в избранное")
            
            self.save_favorites()
            self.update_favorite_button(lang, topic, idx)
            self.update_stats()

    def update_favorite_button(self, lang, topic, idx):
        """Обновляет состояние кнопки избранного"""
        favorite_key = f"{lang}|{topic}|{idx}"
        if favorite_key in self.favorites:
            self.fav_btn.config(text="★")
        else:
            self.fav_btn.config(text="☆")

    def show_favorites(self):
        """Показывает диалог с избранными примерами"""
        if not self.favorites:
            messagebox.showinfo("Избранное", "Нет избранных примеров")
            return
        
        fav_window = tk.Toplevel(self.root)
        fav_window.title("Избранные примеры")
        fav_window.geometry("500x400")
        
        # Список
        listbox = tk.Listbox(fav_window, font=('Segoe UI', 10))
        listbox.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Заполняем список
        fav_items = []
        for fav_key in self.favorites:
            parts = fav_key.split('|')
            if len(parts) == 3:
                lang, topic, idx = parts
                idx = int(idx)
                if (lang in self.snippets_data and topic in self.snippets_data[lang] and 
                    idx < len(self.snippets_data[lang][topic])):
                    snippet = self.snippets_data[lang][topic][idx]
                    fav_items.append((lang, topic, idx, snippet['title']))
        
        fav_items.sort(key=lambda x: x[0])  # Сортировка по языку
        
        for lang, topic, idx, title in fav_items:
            listbox.insert(tk.END, f"{lang}: {title}")
        
        # Кнопки
        btn_frame = ttk.Frame(fav_window)
        btn_frame.pack(fill='x', padx=10, pady=(0, 10))
        
        def load_selected():
            selection = listbox.curselection()
            if selection:
                lang, topic, idx, title = fav_items[selection[0]]
                fav_window.destroy()
                self.lang_var.set(lang)
                self.on_lang_changed()
                self.topic_var.set(topic)
                self.on_topic_changed()
                if self.examples_listbox.size() > idx:
                    self.examples_listbox.selection_clear(0, tk.END)
                    self.examples_listbox.selection_set(idx)
                    self.on_example_selected()
        
        ttk.Button(btn_frame, text="Загрузить",
                  command=load_selected).pack(side='left')
        ttk.Button(btn_frame, text="Закрыть",
                  command=fav_window.destroy).pack(side='right')

    def update_font_size(self):
        """Обновляет размер шрифта"""
        size = self.font_size_var.get()
        self.code_text.configure(font=('Cascadia Code', size))
        self.settings['font_size'] = size
        self.save_settings()

    def toggle_theme(self):
        """Переключает тему"""
        self.settings['dark_mode'] = self.dark_mode_var.get()
        self.save_settings()
        messagebox.showinfo("Тема", 
            "Тема будет изменена после перезапуска приложения")

    def update_stats(self):
        """Обновляет статистику"""
        lang = self.lang_var.get()
        topic = self.topic_var.get()
        
        total_examples = 0
        if lang in self.snippets_data:
            if topic and topic in self.snippets_data[lang]:
                total_examples = len(self.snippets_data[lang][topic])
            else:
                for topic_data in self.snippets_data[lang].values():
                    total_examples += len(topic_data)
        
        self.count_label.config(text=f"Примеров: {total_examples}")
        
        # Общая статистика
        total_all = 0
        for lang_data in self.snippets_data.values():
            for topic_data in lang_data.values():
                total_all += len(topic_data)
        
        self.stats_label.config(
            text=f"Всего примеров: {total_all} | Языков: {len(self.snippets_data)}"
        )

    def update_status(self, message):
        """Обновляет статус бар"""
        self.status_label.config(text=message)
        if message != "Готов к работе":
            self.root.after(3000, lambda: self.update_status("Готов к работе"))

    def show_welcome_message(self):
        """Показывает приветственное сообщение"""
        welcome_text = "Добро пожаловать в Programming Aid & Liberator v3.0!\n\n"
        welcome_text += "Доступные функции:\n"
        welcome_text += "• 4 языка программирования (Python, Java, C++, C#)\n"
        welcome_text += "• Поиск и фильтрация примеров кода\n"
        welcome_text += "• Разогрев с вопросами по алгоритмам\n"
        welcome_text += "• Избранное и история просмотров\n"
        welcome_text += "• Подсветка синтаксиса\n\n"
        welcome_text += "Используйте горячие клавиши:\n"
        welcome_text += "Ctrl+C - копировать, Ctrl+S - сохранить, Ctrl+W - разогрев"
        
        messagebox.showinfo("Добро пожаловать!", welcome_text)

    def show_help(self, event=None):
        """Показывает справку"""
        help_text = """Справка по использованию:

Основные функции:
1. Выберите язык программирования и категорию
2. Выберите пример из списка для просмотра
3. Используйте поиск для быстрого доступа

Разогрев:
• Нажмите "Разогрев" для проверки знаний
• Ответьте на 3 вопроса по текущей теме
• Неправильные ответы выделяются красным

Горячие клавиши:
Ctrl+C - Копировать код
Ctrl+S - Сохранить код в файл
Ctrl+F - Фокус на поиск
Ctrl+R - Запустить код (Python)
Ctrl+W - Начать разогрев
F1 - Эта справка
F5 - Обновить данные

Избранное:
• Нажмите ☆ чтобы добавить в избранное
• ★ означает, что пример в избранном"""
        
        messagebox.showinfo("Справка", help_text)

    def refresh_data(self, event=None):
        """Обновляет данные"""
        self.update_stats()
        self.update_status("Данные обновлены")

    def clear_search(self):
        """Очищает поиск"""
        self.search_var.set("")
        self.search_entry.focus()

    def load_first_example(self):
        """Загружает первый пример"""
        if self.examples_listbox.size() > 0:
            self.examples_listbox.selection_set(0)
            self.on_example_selected()

    def load_settings(self):
        """Загружает настройки"""
        settings_file = "settings.json"
        default_settings = {
            'font_size': 11,
            'dark_mode': False,
            'auto_save': True,
            'show_welcome': True
        }
        
        try:
            if os.path.exists(settings_file):
                with open(settings_file, 'r', encoding='utf-8') as f:
                    loaded = json.load(f)
                    default_settings.update(loaded)
        except:
            pass
            
        return default_settings

    def save_settings(self):
        """Сохраняет настройки"""
        settings_file = "settings.json"
        try:
            with open(settings_file, 'w', encoding='utf-8') as f:
                json.dump(self.settings, f, ensure_ascii=False, indent=2)
        except:
            pass

    def load_favorites(self):
        """Загружает избранное"""
        favorites_file = "favorites.json"
        try:
            if os.path.exists(favorites_file):
                with open(favorites_file, 'r', encoding='utf-8') as f:
                    self.favorites = set(json.load(f))
        except:
            self.favorites = set()

    def save_favorites(self):
        """Сохраняет избранное"""
        favorites_file = "favorites.json"
        try:
            with open(favorites_file, 'w', encoding='utf-8') as f:
                json.dump(list(self.favorites), f, ensure_ascii=False, indent=2)
        except:
            pass

    def on_closing(self):
        """Обработчик закрытия окна"""
        self.save_settings()
        self.save_favorites()
        self.root.destroy()


def main():
    root = tk.Tk()
    app = CodeAidApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
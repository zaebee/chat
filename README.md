# 🐝 Hive Chat - Многопользовательский Чат на FastAPI

[![Python](https://img.shields.io/badge/Python-3.7%2B-blue)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.95.2-green)](https://fastapi.tiangolo.com/)
[![WebSocket](https://img.shields.io/badge/WebSocket-Enabled-orange)](https://developer.mozilla.org/en-US/docs/Web/API/WebSockets_API)

Простой многопользовательский чат, реализованный на FastAPI с поддержкой WebSocket. Подходит для демонстрации работы с реальным временем и управлением пользователями.

## 🚀 Особенности

- ✅ Поддержка нескольких пользователей
- ✅ История сообщений
- ✅ Уведомления о входе/выходе
- ✅ Цветовые метки пользователей
- ✅ Сохранение имени пользователя в localStorage

## 📦 Установка

1. Клонируйте репозиторий:

```bash
   git clone https://github.com/zaebee/chat.git
   cd chat
```

2. Установите зависимости:

```bash
uv sync
```

## 🏃 Запуск

```bash
uv run chat.py
```

После запуска откройте в браузере:

`<http://localhost:8000>`

## 📂 Структура проекта

```bash
🌿 hive-chat/
├── 📂 templates/          # HTML-шаблоны
│   └── 📜 chat.html       # Основной интерфейс чата
├── 📂 static/             # Статические файлы (CSS, JS)
├── 📜 chat.py             # Основной сервер
└── 📜 README.md           # Этот файл
```

## 🛠 Технологии

- **Backend**: FastAPI + Uvicorn
- **Frontend**: HTML/CSS/JavaScript
- **Реальное время**: WebSocket
- **Шаблонизация**: Jinja2

## 🔧 Настройка

Вы можете изменить:

Цветовую схему в CSS
Количество хранимых сообщений (по умолчанию 100)

## 🤝 Вклад

Если вы хотите внести вклад:

- Форкните репозиторий
- Создайте ветку для вашей фичи (`git checkout -b feature/amazing-feature`)
- Закоммитьте изменения (`git commit -m 'Add some amazing feature'`)
- Отправьте изменения (`git push origin feature/amazing-feature`)
- Откройте Pull Request

## 📜 Лицензия

Этот проект лицензирован под MIT License - см. файл [LICENSE](LISENCE) для деталей.

## 📞 Контакты

Если у вас есть вопросы, пишите на почту <sinezub@yandex.ru>

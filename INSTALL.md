# Установка DreamTeam

## Из клона (новая папка)

```powershell
# 1. Клонировать
git clone https://github.com/budagov/DreamTeam.git
cd DreamTeam

# 2. Установить (один скрипт)
.\setup.ps1
# Linux/Mac: ./setup.sh

# 3. Проверить
python -m dreamteam
```

Или вручную: `pip install -e .` — после этого `python -m dreamteam` работает из любой папки.

## Создать новый проект

**Важно:** DreamTeam и проект — разные вещи. Клонируйте DreamTeam в отдельную папку (например `C:\Projects\DreamTeam`), установите его, затем создавайте проект в своей папке.

```powershell
# 1. DreamTeam — отдельно (один раз)
cd C:\Projects
git clone https://github.com/budagov/DreamTeam.git
cd DreamTeam
pip install -e .

# 2. Проект — своя папка
cd C:\Projects\my-new-project

# Развернуть окружение В ТЕКУЩУЮ ПАПКУ (точка!)
dreamteam new-project .

# Запустить
dreamteam run-next
```

**Структура проекта (один корень):**

```
my-new-project/
├── .cursor/      # агенты, правила
├── db/           # SQLite
├── memory/       # архитектура, summaries
├── tasks/        # task_XXX.md
├── .dreamteam    # маркер корня
└── src/          # ваш код (создайте сами)
```

Не используйте `dreamteam new-project dreamteam_project` — так создастся вложенная папка. Используйте `dreamteam new-project .` для развёртывания в текущей папке.

## Если dreamteam не найден

```
No module named dreamteam
```

**Решение:** выполните `pip install -e .` из папки DreamTeam.

## Альтернатива без установки

Если не хотите устанавливать, можно запускать из папки DreamTeam:

```powershell
cd C:\Projects\DreamTeam
python -m dreamteam new-project C:\Projects\my-project
```

Но тогда для работы с my-project нужно указывать путь или использовать `DREAMTEAM_PROJECT`:

```powershell
$env:DREAMTEAM_PROJECT = "C:\Projects\my-project"
python -m dreamteam run-next
```

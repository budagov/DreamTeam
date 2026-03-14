# Публикация на GitHub

## Шаг 1: Создать репозиторий на GitHub

1. Откройте https://github.com/new
2. Repository name: `DreamTeam` (или другое имя)
3. Description: `Autonomous Development System — 500-1000 tasks without quality degradation`
4. Выберите **Public**
5. **Не** добавляйте README, .gitignore, LICENSE (уже есть локально)
6. Нажмите **Create repository**

## Шаг 2: Добавить remote и push

```powershell
cd path/to/DreamTeam

# Replace YOUR_USERNAME with your GitHub username
git remote add origin https://github.com/YOUR_USERNAME/DreamTeam.git

# Или SSH:
# git remote add origin git@github.com:YOUR_USERNAME/DreamTeam.git

git branch -M main
git push -u origin main
```

## Шаг 3: Опционально — GitHub CLI

Если установите [GitHub CLI](https://cli.github.com/):

```powershell
gh auth login
gh repo create DreamTeam --public --source=. --push
```

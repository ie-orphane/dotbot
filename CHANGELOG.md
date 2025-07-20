
# Changelog

## [Unrealesed]

**`Timeline`**: Apr 11, 2025
**`Commits`**: [fb7cbcd](https://github.com/ie-orphane/lionbot/commit/fb7cbcd75c2ee713792669bb0f26ee1f5ed2ad25) ... [75ee19d](https://github.com/ie-orphane/lionbot/commit/75ee19d2f8e01b84665e37289df9c8e279228d4e)

### ✨ Added

- prevent using `contexts` in **dm** except for owner.
- `>stats coins` show the **statistics** of lioncoin with line chart and bar chart.
- `run` script to execute the bot or test it.
- `log` the evaluation `task` process.
- `>challenge preview`, `>challenge usage`.
- `/random`, `/evaluate`.
- fees and donations in `/transfer`

### 🔄 Changed

- charts `utils` to `dir` base module.
- move `challenges` from `model` base to `config` base.

### 🗑️ Removed

- `/blacklist out` slash command.

## 3.0.2

**`Timeline`**: Mar 08, 2025
**`Commits`**: [fb7cbcd](https://github.com/ie-orphane/lionbot/commit/fb7cbcd75c2ee713792669bb0f26ee1f5ed2ad25) ... [75ee19d](https://github.com/ie-orphane/lionbot/commit/75ee19d2f8e01b84665e37289df9c8e279228d4e)

### ✨ Added

### 🔧 Fixed

### 🔄 Changed

### 🗑️ Removed

## 3.0.1

**`Timeline`**: Mar 07, 2025

**`Commits`**: [ff9ad8e](https://github.com/ie-orphane/lionbot/commit/ff9ad8e03f5922c6cf7b75dc7473273068d8b25d) ... [ce300eb](https://github.com/ie-orphane/lionbot/commit/ce300eb04a577868adadd8e9f98780ee1b26d792)

### ✨ Added

- **approve** or **deny** with feedback of a shop `item`.
- when an `item` approved, send it to the `#shop`, otherwise send the **feedback** to the author.

### 🔄 Changed

- rename `item.title` to `item.name`

## 3.0.0

**`Timeline`**: Mar 6, 2025

**`Commits`**: [b3f018d](https://github.com/ie-orphane/lionbot/commit/b3f018d5eb9e4879fe3566c3ac885c8c19740df3) ... [f697812](https://github.com/ie-orphane/lionbot/commit/f69781254f95af3b6d05c3200dd2555281b095d6)

### ✨ Added

- model for shop `item` data with a random unique `id`.
- `/shop add` command to send an `item` to review.

### 🔄 Changed

- `ui` components to `dir` base.

### 🗑️ Removed

- env variable `GITHUB_ACCESS_TOKEN`

## [2.0.0]

### ✨ Added

### 🔧 Fixed

### 🔄 Changed

### 🗑️ Removed

## [1.0.0]

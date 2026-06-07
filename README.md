# Курсовая работа (Typst)

![ГОСТ](https://img.shields.io/badge/%D0%93%D0%9E%D0%A1%D0%A2-1F2937?style=for-the-badge&logo=readthedocs&logoColor=white)
![Typst](https://img.shields.io/badge/Typst-239DAD?style=for-the-badge&logo=typst&logoColor=white)
![Zotero](https://img.shields.io/badge/Zotero-CC2936?style=for-the-badge&logo=zotero&logoColor=white)
![NixOS](https://img.shields.io/badge/NixOS-5277C3?style=for-the-badge&logo=nixos&logoColor=white)

Данный репозиторий содержит шаблон для написания курсовой работы по ГОСТ на Typst с использованием пакета `modern-g7-32`.

Проект решает следующие задачи:
- Структурированная подготовка курсовой работы с разбиением текста по отдельным файлам (главы, введение, заключение, приложения).
- Автоматическая сборка итогового PDF и режим живого предпросмотра (live preview) через `tinymist`.
- Управление библиографией в формате `.bib` (поддерживается экспорт из Zotero).

## Структура проекта

```
.
├── src/
│   ├── 000-main.typ - основной файл (преамбула, настройки, подключение разделов).
│   ├── 000-title.pdf - сканированный титульный лист работы.
│   ├── 001-intro.typ - введение.
│   ├── 002-chapter1.typ - глава 1.
│   ├── 003-chapter2.typ - глава 2.
│   ├── 004-chapter3.typ - глава 3.
│   ├── 005-conclusion.typ - заключение.
│   ├── 006-biblio.typ - библиографический список.
│   ├── 007-appendix.typ - приложения.
│   ├── assets/ - папка с изображениями (схемы, графики калибровок).
│   └── example.typ - пример оформления базовых элементов.
├── biblio.bib - библиографическая база источников.
├── Makefile.
└── flake.nix.
```

## Сборка и предпросмотр

При использовании Nix окружение разработки активируется автоматически (через `nix develop` или `direnv`). В него входят `tinymist` и необходимые шрифты (Times New Roman).

### Запуск режима live preview (живой предпросмотр)

Запускает автоматическое отслеживание изменений с отображением в реальном времени (по умолчанию на `localhost:23626`):
```bash
make preview
```

### Сборка итогового PDF

Компилирует документ в `document.pdf`:
```bash
make build
```

## Библиография

Файл `biblio.bib` формируется через Zotero с плагином Better BibTeX / Better BibLaTeX.

Рекомендуемый рабочий процесс (workflow):
1. Добавьте источники в библиотеку Zotero.
2. Настройте автоэкспорт коллекции (Better BibLaTeX) в файл `biblio.bib` в корне проекта.
3. Цитируйте источники в тексте через `@citekey`. Список литературы сгенерируется автоматически.

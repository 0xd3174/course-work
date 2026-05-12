# Курсовая работа (LaTeX)

![ГОСТ](https://img.shields.io/badge/%D0%93%D0%9E%D0%A1%D0%A2-1F2937?style=for-the-badge&logo=readthedocs&logoColor=white)
![LaTeX](https://img.shields.io/badge/LaTeX-008080?style=for-the-badge&logo=latex&logoColor=white)
![biblatex](https://img.shields.io/badge/biblatex-000000?style=for-the-badge&logo=latex&logoColor=white)
![Zotero](https://img.shields.io/badge/Zotero-CC2936?style=for-the-badge&logo=zotero&logoColor=white)
![NixOS](https://img.shields.io/badge/NixOS-5277C3?style=for-the-badge&logo=nixos&logoColor=white)

Данный репозиторий содержит минимальный шаблон для написания курсовой работы по ГОСТ. Проект выполняет следующие задачи:


- Подготовка курсовой в структурированном виде с разбиением на отдельные файлы (с поддержкой изображений, формул).
- Автоматическая однокомандная сборка итогового PDF через `latexmk`.
- Ведение библиографии через `biblatex` + `biber` (с генерацией `biblio.bib` с помощью `zotero` с плагином `better biblatex`)

## Структура

```
.
├── src/
│   ├── 000-main.tex — основной файл (преамбула, настройки, подключение частей).
│   ├── 001-intro.tex — введение.
│   ├── 002-chapter-one.tex — пример главы основной части.
│   ├── 003-conclusion.tex — заключение.
│   ├── 004-biblio.tex — библиография.
│   ├── 005-appendix.tex — приложение.
│   └── example.tex — референсы на разные элементы. 
├── biblio.bib — библиографическая база.
└── latexmkrc конфигурация сборки.
```

## Запуск проекта

Выполнить корня проекта:

```bash
latexmk
```

Результатом сборки является: `document.pdf`.

Очистка артефактов (кэша):

```bash
latexmk -C
```


## Библиография

Файл `biblio.bib` формируется через Zotero с плагином Better BibLaTeX.

Рекомендуемый workflow:

1. Добавляете источники в Zotero.
2. Экспортируете/обновляете `.bib` (Better BibLaTeX) в `biblio.bib`.
3. Запускаете `latexmk`.

## Необходимые пакеты и инструменты

Подробнее в флейке: https://github.com/0xd3174/course-work/blob/master/flake.nix

Минимально нужны:

- `latexmk`
- `biber`
- TeX Live `scheme-medium`
- пакет `biblatex`
- пакет `biblatex-gost`
- пакет `extsizes`
- пакет `titlesec`
- пакет `tocloft`
- пакет `enumitem`
- шрифты `corefonts` (в частности Times New Roman)
- для библиографии `zotero` + Better BibLaTeX

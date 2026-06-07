#import "@preview/modern-g7-32:0.2.0": gost

#show: gost.with(
  hide-title: true,
  add-pagebreaks: false,
)

#outline()

= Введение

= Первая глава
== Первая подглава

= Вторая глава
== Первая подглава

= Заключение

// Изображения
#figure(
  image("assets/002-img1.png", width: 80%),
  caption: [Placeholder image],
) <fig:placeholder_image>

Ссылка на рисунок: @fig:placeholder_image

// Цитирование
Цитата: @smirnov2025latex

// Формулы
$ y = alpha x^2 + beta x + gamma $ <eq:placeholder_formula>

Ссылка на формулу: @eq:placeholder_formula

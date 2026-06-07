#import "@preview/modern-g7-32:0.2.0": abstract, gost

#show: gost.with(
  hide-title: true,
  add-pagebreaks: false,
  text-size: (default: 14pt),
)

#set par(leading: 1.5em - 0.35em) // Word'овский "полуторный" интервал

#[
  #set page(margin: 0mm)
  #image("000-title.pdf")
]

#outline()

#include "001-intro.typ"
#include "006-biblio.typ"
#include "007-appendix.typ"

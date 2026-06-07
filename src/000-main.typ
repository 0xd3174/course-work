#import "@preview/modern-g7-32:0.2.0": abstract, appendixes, gost

#show: gost.with(
  hide-title: true,
  text-size: (default: 12pt, small: 8pt),
  indent: 1.5cm,
)

#show heading.where(level: 1): it => {
  show text: upper
  align(center, it)
}

#show heading.where(level: 2): it => {
  show text: upper
  it
}

#show heading.where(level: 3): it => {
  set text(tracking: 1.5pt)
  it
}

#set text(font: "Times New Roman")

#set par(leading: 1.5em - 0.35em) // Word'овский "полуторный" интервал

#[
  #set page(margin: 0mm)
  #image("000-title.pdf")
]

#show outline.entry: set block(above: 0.75em, below: 0.75em)
#outline(indent: 0.75cm)


#include "001-intro.typ"
#include "002-chapter1.typ"
#include "003-chapter2.typ"
#include "004-chapter3.typ"
#include "005-conclusion.typ"
#include "006-biblio.typ"
#include "007-appendix.typ"

preview:
	tinymist preview src/000-main.typ --input mode=dev

build:
	tinymist compile src/000-main.typ document.pdf --input mode=production

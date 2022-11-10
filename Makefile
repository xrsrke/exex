test:
	pytest .

typecheck:
	mypy ./exex --disallow-any-expr --disallow-untyped-defs --strict-optional --no-implicit-optional --html-report reports ./reports/mypy
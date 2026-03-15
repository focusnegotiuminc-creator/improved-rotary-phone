.PHONY: run stage qa visual-check publish

run:
	python3 focus_ai/scripts/engine.py

stage:
	python3 focus_ai/scripts/engine.py --stage $(N)

qa:
	python3 -m py_compile focus_ai/scripts/engine.py focus_ai/scripts/verify_visuals.py focus_ai/scripts/publish_ebooks.py

visual-check:
	python3 focus_ai/scripts/verify_visuals.py

publish:
	python3 focus_ai/scripts/publish_ebooks.py

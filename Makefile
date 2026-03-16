.PHONY: run stage qa visual-check publish public-build deploy-infinityfree replit-export

run:
	python3 focus_ai/scripts/engine.py

stage:
	python3 focus_ai/scripts/engine.py --stage $(N)

qa:
	python3 -m py_compile focus_ai/scripts/engine.py focus_ai/scripts/verify_visuals.py focus_ai/scripts/publish_ebooks.py focus_ai/scripts/build_public_site.py focus_ai/scripts/deploy_infinityfree.py focus_ai/scripts/export_replit_bundle.py

visual-check:
	python3 focus_ai/scripts/verify_visuals.py

publish:
	python3 focus_ai/scripts/publish_ebooks.py

public-build:
	python3 focus_ai/scripts/publish_ebooks.py
	python3 focus_ai/scripts/build_public_site.py

deploy-infinityfree:
	python3 focus_ai/scripts/deploy_infinityfree.py

replit-export:
	python3 focus_ai/scripts/export_replit_bundle.py

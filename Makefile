.PHONY: run stage qa visual-check publish merge-gh merge-gh-dry-run setup-desktop-ai

run:
	python3 focus_ai/scripts/engine.py

stage:
	python3 focus_ai/scripts/engine.py --stage $(N)

qa:
	python3 -m py_compile focus_ai/scripts/engine.py focus_ai/scripts/verify_visuals.py focus_ai/scripts/publish_ebooks.py focus_ai/scripts/merge_github_repositories.py focus_ai/scripts/setup_desktop_focus_master_ai.py

visual-check:
	python3 focus_ai/scripts/verify_visuals.py

publish:
	python3 focus_ai/scripts/publish_ebooks.py

merge-gh:
	python3 focus_ai/scripts/merge_github_repositories.py --owner $(OWNER)

merge-gh-dry-run:
	python3 focus_ai/scripts/merge_github_repositories.py --owner $(OWNER) --dry-run

setup-desktop-ai:
	python3 focus_ai/scripts/setup_desktop_focus_master_ai.py

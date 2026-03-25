.PHONY: run stage qa visual-check publish public-build deploy-infinityfree replit-export merge-prs go-live install-gh unblock-live

run:
	python3 focus_ai/scripts/engine.py

stage:
	python3 focus_ai/scripts/engine.py --stage $(N)

qa:
	python3 -m py_compile focus_ai/scripts/engine.py focus_ai/scripts/verify_visuals.py focus_ai/scripts/publish_ebooks.py focus_ai/scripts/build_public_site.py focus_ai/scripts/deploy_infinityfree.py focus_ai/scripts/export_replit_bundle.py focus_ai/scripts/github_ops.py
	bash -n focus_ai/scripts/install_gh_cli.sh focus_ai/scripts/unblock_and_live.sh

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

merge-prs:
	python3 focus_ai/scripts/github_ops.py merge-prs

go-live:
	python3 focus_ai/scripts/github_ops.py go-live

install-gh:
	bash focus_ai/scripts/install_gh_cli.sh

unblock-live:
	bash focus_ai/scripts/unblock_and_live.sh

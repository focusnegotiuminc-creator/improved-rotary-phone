.PHONY: run stage qa visual-check publish merge-gh merge-gh-dry-run setup-desktop-ai
.PHONY: run stage qa visual-check publish public-build deploy-infinityfree replit-export full-check backup verify-live
.PHONY: run stage qa visual-check publish public-build deploy-infinityfree replit-export merge-prs go-live install-gh unblock-live setup-autopilot

run:
	python3 focus_ai/scripts/engine.py

stage:
	python3 focus_ai/scripts/engine.py --stage $(N)

qa:
	python3 -m py_compile focus_ai/scripts/engine.py focus_ai/scripts/verify_visuals.py focus_ai/scripts/publish_ebooks.py focus_ai/scripts/merge_github_repositories.py focus_ai/scripts/setup_desktop_focus_master_ai.py
	python3 -m py_compile focus_ai/scripts/engine.py focus_ai/scripts/verify_visuals.py focus_ai/scripts/publish_ebooks.py focus_ai/scripts/build_public_site.py
	python3 -m py_compile focus_ai/scripts/engine.py focus_ai/scripts/verify_visuals.py focus_ai/scripts/publish_ebooks.py focus_ai/scripts/build_public_site.py focus_ai/scripts/deploy_infinityfree.py focus_ai/scripts/export_replit_bundle.py focus_ai/scripts/backup_working_copy.py focus_ai/scripts/verify_live_app.py
	python3 -m py_compile focus_ai/scripts/engine.py focus_ai/scripts/verify_visuals.py focus_ai/scripts/publish_ebooks.py focus_ai/scripts/build_public_site.py focus_ai/scripts/deploy_infinityfree.py focus_ai/scripts/export_replit_bundle.py focus_ai/scripts/github_ops.py
	bash -n focus_ai/scripts/install_gh_cli.sh focus_ai/scripts/unblock_and_live.sh focus_ai/scripts/setup_autopilot.sh

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

setup-autopilot:
	bash focus_ai/scripts/setup_autopilot.sh

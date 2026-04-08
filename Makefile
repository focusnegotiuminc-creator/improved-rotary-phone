.PHONY: run stage qa visual-check publish sync merge-gh merge-gh-dry-run setup-desktop-ai public-build deploy-infinityfree deploy-replit deploy-thefocuscorp deploy-live-strict operator-live deploy-local-live replit-export final-system live-stack full-check backup verify-live merge-prs go-live install-gh unblock-live setup-autopilot configure-actions

PYTHON := python3
ifeq ($(OS),Windows_NT)
PYTHON := python
endif

run:
	$(PYTHON) focus_ai/scripts/engine.py

stage:
	$(PYTHON) focus_ai/scripts/engine.py --stage $(N)

qa:
	$(PYTHON) -m py_compile focus_ai/scripts/engine.py focus_ai/scripts/verify_visuals.py focus_ai/scripts/publish_ebooks.py focus_ai/scripts/sync_drive_assets.py
	$(PYTHON) -m py_compile focus_ai/scripts/engine.py focus_ai/scripts/verify_visuals.py focus_ai/scripts/publish_ebooks.py focus_ai/scripts/merge_github_repositories.py focus_ai/scripts/setup_desktop_focus_master_ai.py
	$(PYTHON) -m py_compile focus_ai/scripts/engine.py focus_ai/scripts/verify_visuals.py focus_ai/scripts/publish_ebooks.py focus_ai/scripts/build_public_site.py focus_ai/scripts/build_final_system.py focus_ai/scripts/live_stack.py
	$(PYTHON) -m py_compile focus_ai/scripts/engine.py focus_ai/scripts/verify_visuals.py focus_ai/scripts/publish_ebooks.py focus_ai/scripts/build_public_site.py focus_ai/scripts/deploy_infinityfree.py focus_ai/scripts/deploy_replit.py focus_ai/scripts/export_replit_bundle.py focus_ai/scripts/backup_working_copy.py focus_ai/scripts/verify_live_app.py
	$(PYTHON) -m py_compile focus_ai/scripts/engine.py focus_ai/scripts/verify_visuals.py focus_ai/scripts/publish_ebooks.py focus_ai/scripts/build_public_site.py focus_ai/scripts/deploy_infinityfree.py focus_ai/scripts/deploy_replit.py focus_ai/scripts/deploy_wordpress_plugins.py focus_ai/scripts/run_single_operator_live.py focus_ai/scripts/run_sierra_payroll_prep.py focus_ai/scripts/export_replit_bundle.py focus_ai/scripts/github_ops.py focus_ai/scripts/configure_github_actions.py
ifeq ($(OS),Windows_NT)
	@where bash >NUL 2>&1 && bash -n focus_ai/scripts/install_gh_cli.sh focus_ai/scripts/unblock_and_live.sh focus_ai/scripts/setup_autopilot.sh || echo "Skipping bash syntax check (bash not found in PATH)."
else
	bash -n focus_ai/scripts/install_gh_cli.sh focus_ai/scripts/unblock_and_live.sh focus_ai/scripts/setup_autopilot.sh
endif

visual-check:
	$(PYTHON) focus_ai/scripts/verify_visuals.py

publish:
	$(PYTHON) focus_ai/scripts/publish_ebooks.py

sync:
	$(PYTHON) focus_ai/scripts/sync_drive_assets.py --clean

merge-gh:
	$(PYTHON) focus_ai/scripts/merge_github_repositories.py --owner $(OWNER)

merge-gh-dry-run:
	$(PYTHON) focus_ai/scripts/merge_github_repositories.py --owner $(OWNER) --dry-run

setup-desktop-ai:
	$(PYTHON) focus_ai/scripts/setup_desktop_focus_master_ai.py

public-build:
	$(PYTHON) focus_ai/scripts/publish_ebooks.py
	$(PYTHON) focus_ai/scripts/build_public_site.py

deploy-infinityfree:
	$(PYTHON) focus_ai/scripts/deploy_infinityfree.py

deploy-replit:
	$(PYTHON) focus_ai/scripts/deploy_replit.py

deploy-thefocuscorp:
	$(PYTHON) focus_ai/scripts/publish_ebooks.py
	$(PYTHON) focus_ai/scripts/build_public_site.py
	$(PYTHON) focus_ai/scripts/deploy_replit.py
	$(PYTHON) focus_ai/scripts/deploy_infinityfree.py
	$(PYTHON) focus_ai/scripts/deploy_wordpress_theme.py
	$(PYTHON) focus_ai/scripts/deploy_wordpress_plugins.py
	$(PYTHON) focus_ai/scripts/verify_live_app.py

deploy-live-strict:
	$(PYTHON) focus_ai/scripts/publish_ebooks.py
	$(PYTHON) focus_ai/scripts/build_public_site.py
	$(PYTHON) focus_ai/scripts/deploy_replit.py
	$(PYTHON) focus_ai/scripts/deploy_infinityfree.py
	$(PYTHON) focus_ai/scripts/deploy_wordpress_theme.py
	$(PYTHON) focus_ai/scripts/deploy_wordpress_plugins.py
	$(PYTHON) focus_ai/scripts/verify_live_app.py

operator-live:
	FOCUS_OPERATOR_MODE=single_owner $(PYTHON) focus_ai/scripts/run_single_operator_live.py

deploy-local-live:
	$(PYTHON) focus_ai/scripts/deploy_local_live.py

replit-export:
	$(PYTHON) focus_ai/scripts/export_replit_bundle.py

final-system:
	$(PYTHON) focus_ai/scripts/build_final_system.py

live-stack:
	$(PYTHON) focus_ai/scripts/live_stack.py

merge-prs:
	$(PYTHON) focus_ai/scripts/github_ops.py merge-prs

go-live:
	$(PYTHON) focus_ai/scripts/github_ops.py go-live

install-gh:
	bash focus_ai/scripts/install_gh_cli.sh

unblock-live:
	bash focus_ai/scripts/unblock_and_live.sh

setup-autopilot:
	bash focus_ai/scripts/setup_autopilot.sh

configure-actions:
	$(PYTHON) focus_ai/scripts/configure_github_actions.py

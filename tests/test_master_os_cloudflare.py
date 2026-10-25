from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_cloudflare_env_example_contains_required_keys():
    text = (ROOT / '.env.example').read_text()
    for key in [
        'CLOUDFLARE_API_TOKEN','CLOUDFLARE_ACCOUNT_ID','CLOUDFLARE_ZONE_ID','CLOUDFLARE_EMAIL','CLOUDFLARE_PROJECT_NAME','CLOUDFLARE_KV_NAMESPACE_ID','CLOUDFLARE_D1_DATABASE_ID','CLOUDFLARE_R2_BUCKET'
    ]:
        assert f'{key}=' in text


def test_wrangler_has_dev_staging_production_presets():
    text = (ROOT / 'wrangler.toml').read_text()
    assert 'name = "focus-master-os"' in text
    assert '[env.staging]' in text
    assert '[env.production]' in text
    assert 'FOCUS_MASTER_OS_KV' in text
    assert 'FOCUS_MASTER_OS_D1' in text
    assert 'FOCUS_MASTER_OS_R2' in text


def test_connector_covers_required_cloudflare_checks():
    text = (ROOT / 'connectors' / 'cloudflare.ts').read_text()
    for method in ['verifyToken','lookupAccount','lookupZone','checkWorkersSubdomain','checkPagesProject','checkKvNamespace','checkD1Database','checkR2Bucket','checkDeploymentStatus','fetchAuditLogs','healthCheck']:
        assert method in text


def test_dashboard_lists_agents_and_confirmation_controls():
    text = (ROOT / 'dashboard' / 'cloudflare-status.tsx').read_text()
    assert 'masterOsAgents' in text
    assert 'GitHub' in text and 'Google Drive' in text and 'Cloudflare' in text
    assert 'Confirm' in text


def test_no_obvious_hardcoded_cloudflare_secret():
    for path in ['connectors/cloudflare.ts', 'wrangler.toml', '.env.example']:
        text = (ROOT / path).read_text()
        assert 'sk-' not in text
        assert 'api_token=ey' not in text.lower()
        assert 'CLOUDFLARE_API_TOKEN=<' not in text

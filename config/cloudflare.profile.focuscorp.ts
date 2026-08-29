export const focusCorpCloudflareProfile = {
  id: 'focuscorp',
  label: 'The Focus Corp Cloudflare',
  ownerEmail: 'theFocusCorp@proton.me',
  supportEmails: ['Focusnegotiuminc@gmail.com', 'fninc@proton.me', 'rlcsolutions@proton.me'],
  accountIdEnv: 'CLOUDFLARE_ACCOUNT_ID',
  zoneIdEnv: 'CLOUDFLARE_ZONE_ID',
  projectNameEnv: 'CLOUDFLARE_PROJECT_NAME',
  requiredChecks: ['token','account','zone','workers','pages','kv','d1','r2','deployment','audit'],
  deploymentTargets: { primary: 'cloudflare-workers-pages', fallback: 'vercel' },
} as const;

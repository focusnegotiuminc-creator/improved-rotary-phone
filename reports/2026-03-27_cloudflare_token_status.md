# Cloudflare Token Status - 2026-03-27

## Result
- 11 provided Cloudflare API tokens verified as active using the account token verification endpoint.
- Masked token identifiers retained for reference:
  - `token_01_2f9c01`
  - `token_02_90874c`
  - `token_03_77d62a`
  - `token_04_4b1bfe`
  - `token_05_616f6a`
  - `token_06_9c8aa8`
  - `token_07_1f00f4`
  - `token_08_6ae575`
  - `token_09_2ac347`
  - `token_10_3f6507`
  - `token_11_45a9d1`

## Scope check
- Token verification endpoint succeeded.
- Tested account APIs for zone lookup, Workers subdomain, and R2 buckets did not produce a usable backup path from this session.
- `thefocuscorp.com` did not appear in the zone lookup result for the tested token.
- Two masked tokens showed broader account reach:
  - `token_05_616f6a`
  - `token_11_45a9d1`
- Those two returned a successful Workers subdomain response, but R2 still returned:
  - `10042: Please enable R2 through the Cloudflare Dashboard.`
- Most of the remaining tokens returned authentication errors on Workers and R2 endpoints.

## Handling
- Raw token values were not written into repo-tracked files.
- Tokens should be treated as exposed because they were pasted into chat.
- Recommended follow-up is to rotate them after the backup path is finalized.

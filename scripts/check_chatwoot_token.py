import os
import sys
import json
import httpx
from dotenv import load_dotenv


def main() -> int:
    load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))
    base = os.getenv('CHATWOOT_BASE_URL')
    token = os.getenv('CHATWOOT_ACCESS_TOKEN')
    account_id = os.getenv('CHATWOOT_ACCOUNT_ID')
    if not base or not token:
        print('Missing CHATWOOT_BASE_URL or CHATWOOT_ACCESS_TOKEN in environment/.env', file=sys.stderr)
        return 2
    base = base.rstrip('/')
    # Prefer account endpoint with api_access_token header (Chatwoot Account API)
    url_profile = f"{base}/api/v1/profile"
    url_account = f"{base}/api/v1/accounts/{account_id}" if account_id else None
    headers = {'api_access_token': token}
    try:
        with httpx.Client(timeout=10.0) as c:
            r = c.get(url_profile, headers=headers)
            print('GET', url_profile, '->', r.status_code)
            try:
                print(json.dumps(r.json(), indent=2)[:2000])
            except Exception:
                print(r.text[:1000])
            if r.status_code == 200:
                return 0
            if url_account:
                r2 = c.get(url_account, headers=headers)
                print('GET', url_account, '->', r2.status_code)
                try:
                    print(json.dumps(r2.json(), indent=2)[:2000])
                except Exception:
                    print(r2.text[:1000])
                return 0 if r2.status_code == 200 else 1
            return 1
    except Exception as e:
        print('REQUEST_ERROR', e, file=sys.stderr)
        return 3


if __name__ == '__main__':
    raise SystemExit(main())

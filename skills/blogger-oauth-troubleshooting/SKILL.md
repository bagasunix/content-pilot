---
name: blogger-oauth-troubleshooting
description: "Use when Blogger API authentication fails — token refresh, API quota management, error handling, multi-bot authentication patterns."
category: publisher
tags: [oauth, blogger, api, authentication, token, troubleshooting]
---

# Blogger OAuth Troubleshooting

## OAuth 2.0 Flow

### Token Lifecycle
- **Access token**: expires in 1 hour
- **Refresh token**: long-lived (months)
- **Token refresh**: automatic before expiry

### Common Errors

**401 Unauthorized**
```
Cause: Token expired or invalid
Fix: Refresh token or re-authenticate
```

**403 Forbidden**
```
Cause: API quota exceeded or insufficient permissions
Fix: Wait for quota reset or check scopes
```

**400 Bad Request**
```
Cause: Invalid request body
Fix: Check JSON format and required fields
```

## Token Refresh Flow

### Automatic Refresh
```python
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

creds = Credentials(
    token=access_token,
    refresh_token=refresh_token,
    token_uri='https://oauth2.googleapis.com/token',
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET
)

if creds.expired:
    creds.refresh(Request())
```

### Manual Refresh
```bash
curl -X POST https://oauth2.googleapis.com/token   -d "client_id=CLIENT_ID"   -d "client_secret=CLIENT_SECRET"   -d "refresh_token=REFRESH_TOKEN"   -d "grant_type=refresh_token"
```

## API Quota Management

### Quota Limits
- **Per user per 100 seconds**: 100 requests
- **Per day**: 1,000,000 requests
- **Per 100 seconds per user**: 100 requests

### Quota Optimization
- **Batch requests**: combine multiple calls
- **Cache responses**: avoid duplicate calls
- **Rate limiting**: add delays between calls
- **Off-peak**: schedule heavy operations

### Quota Exceeded
1. Wait 100 seconds for reset
2. Implement exponential backoff
3. Cache frequently accessed data
4. Reduce API call frequency

## Multi-Bot Authentication

### Pattern: Shared Token
- Single OAuth token for all bots
- Store securely in .env
- Refresh centrally

### Pattern: Service Account
- Use Google service account
- No user interaction needed
- Share blog access with service account

### Pattern: User Delegation
- Each bot has own token
- More complex but isolated
- Better security

## Error Handling

### Retry Logic
```python
def api_call_with_retry(func, max_retries=3):
    for attempt in range(max_retries):
        try:
            return func()
        except HttpError as e:
            if e.resp.status == 401:
                refresh_token()
            elif e.resp.status == 403:
                time.sleep(100)  # Quota reset
            elif e.resp.status >= 500:
                time.sleep(2 ** attempt)  # Exponential backoff
            else:
                raise
    raise Exception("Max retries exceeded")
```

### Logging
- Log all API errors
- Track: error type, frequency, resolution
- Alert: repeated failures

## Pitfalls
1. Don't hardcode tokens (use .env)
2. Don't ignore 401 errors (token issue)
3. Don't retry on 400 (fix request)
4. Don't forget quota limits
5. Don't share tokens across environments

## Verification
- OAuth flow working
- Token refresh automatic
- Error handling implemented
- Quota monitoring active
- Logging comprehensive

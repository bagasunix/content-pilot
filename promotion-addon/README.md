# Promotion Addon

> Distribute articles ke social media dan newsletter setelah publish.

## Features

- **Social Media Auto-Post** — TikTok, Instagram, YouTube Shorts
- **Newsletter Integration** — Email campaigns
- **Content Recycling** — Repurpose articles ke berbagai format
- **Analytics Tracking** — Track performance

## Installation

```bash
cd contentpilot
cp -r promotion-addon/skills/* skills/
cp -r promotion-addon/docs/* workspace/docs/
```

## Supported Platforms

| Platform | Type | Status |
|----------|------|--------|
| TikTok | Video | ✅ Supported |
| Instagram | Reels/Stories | ✅ Supported |
| YouTube Shorts | Video | ✅ Supported |
| Twitter/X | Thread | ⏳ Coming soon |
| LinkedIn | Article | ⏳ Coming soon |
| Newsletter | Email | ⏳ Coming soon |

## Usage

### Auto-Post to Social Media

```bash
# After publish, run promotion
python3 scripts/promote.py --article <idea_id> --platform tiktok
```

### Content Recycling

```bash
# Convert article to video script
python3 scripts/recycle.py --article <idea_id> --format video-script

# Convert to newsletter
python3 scripts/recycle.py --article <idea_id> --format newsletter
```

## Configuration

Add to `config/config.yaml`:

```yaml
promotion:
  enabled: true
  platforms:
    tiktok:
      enabled: true
      account: "@yourusername"
    instagram:
      enabled: true
      account: "@yourusername"
    youtube:
      enabled: true
      channel_id: "UC..."
```

## License

MIT License (same as ContentPilot)

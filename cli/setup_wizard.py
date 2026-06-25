#!/usr/bin/env python3
"""
ContentPilot — Setup Wizard

Interactive setup untuk generate config dari template.

Usage:
    python3 scripts/setup_wizard.py
    python3 scripts/setup_wizard.py --batch domain=myblog.com blog_id=123 email=user@example.com
"""

import json
import sys
import yaml
from pathlib import Path
from datetime import datetime

DEFAULT_CONFIG = {
    "domain": "",
    "blog_id": "",
    "email": "",
    "language": "id",
    "publish_mode": "draft",
    "wip_limit": 3,
    "ai_provider": "ollama",
    "ai_model": "llama2",
}

def get_input(prompt, default="", required=True):
    while True:
        value = input(f"{prompt} [{default}]: ").strip()
        if not value and default:
            return default
        if not value and required:
            print("  ⚠️  Required field.")
            continue
        return value

def interactive_setup():
    print("=" * 50)
    print("  ContentPilot — Setup Wizard")
    print("=" * 50)
    print()

    config = DEFAULT_CONFIG.copy()

    print("📝 BLOG CONFIGURATION")
    print("-" * 40)
    config["domain"] = get_input("Domain blog (e.g., myblog.com)")
    config["blog_id"] = get_input("Blogger Blog ID (angka)")
    config["email"] = get_input("Email untuk OAuth")

    print()
    print("🤖 AI PROVIDER")
    print("-" * 40)
    print("  1. ollama  (local, free)")
    print("  2. openai  (paid)")
    print("  3. deepseek (paid, cheaper)")
    choice = get_input("Pilih (1/2/3)", "1")
    providers = {"1": ("ollama", "llama2"), "2": ("openai", "gpt-4"), "3": ("deepseek", "deepseek-chat")}
    config["ai_provider"], config["ai_model"] = providers.get(choice, ("ollama", "llama2"))

    print()
    print("⚙️  ADVANCED (tekan Enter untuk default)")
    print("-" * 40)
    config["publish_mode"] = get_input("Publish mode (draft/live)", "draft", required=False)
    config["wip_limit"] = int(get_input("WIP limit", str(config["wip_limit"]), required=False))

    return config

def batch_setup(args):
    config = DEFAULT_CONFIG.copy()
    for arg in args:
        if "=" in arg:
            key, value = arg.split("=", 1)
            if key in config:
                config[key] = value
    return config

def generate_config(config):
    content = f"""# ContentPilot — Workspace Config
# Generated: {datetime.now().isoformat()}

domain: {config['domain']}
platform: blogger
blog_id: "{config['blog_id']}"
language: {config['language']}

publish_mode: {config['publish_mode']}
autonomy: gated
wip_limit: {config['wip_limit']}

ai:
  provider: {config['ai_provider']}
  model: {config['ai_model']}
"""
    Path("workspace/config.yaml").write_text(content)
    print("  ✅ workspace/config.yaml")

def generate_env_example():
    content = """# ContentPilot — Environment Variables
# Copy to .env and fill in your values

# Blogger OAuth (run setup_credentials.py)
BLOGGER_CLIENT_ID=""
BLOGGER_CLIENT_SECRET=""

# AI Provider (pilih salah satu)
# OpenAI: OPENAI_API_KEY=sk-...
# DeepSeek: DEEPSEEK_API_KEY=sk-...
# Ollama: tidak perlu API key
"""
    Path(".env.example").write_text(content)
    print("  ✅ .env.example")

def main():
    if len(sys.argv) > 1 and sys.argv[1] == "--batch":
        config = batch_setup(sys.argv[2:])
    else:
        config = interactive_setup()

    if not config["domain"] or not config["blog_id"] or not config["email"]:
        print("❌ domain, blog_id, email required")
        sys.exit(1)

    print()
    print("=" * 50)
    print("  Generating config...")
    print("=" * 50)
    print()

    generate_config(config)
    generate_env_example()

    print()
    print("=" * 50)
    print("  ✅ Setup Complete!")
    print("=" * 50)
    print()
    print("NEXT:")
    print(f"  1. cp .env.example .env && edit .env")
    print(f"  2. python3 scripts/setup_credentials.py")
    print(f"  3. python3 python3 -m contentpilot.pipeline status")
    print()
    print(f"  Domain:  {config['domain']}")
    print(f"  Blog ID: {config['blog_id']}")
    print(f"  AI:      {config['ai_provider']}/{config['ai_model']}")
    print()

if __name__ == "__main__":
    main()

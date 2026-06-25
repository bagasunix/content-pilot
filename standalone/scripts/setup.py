#!/usr/bin/env python3
"""
Blog Lifecycle Pro — Standalone Setup

Setup wizard untuk standalone version (tanpa Hermes).

Usage:
    python3 scripts/setup.py
"""

import os
import sys
import yaml
from pathlib import Path
from datetime import datetime

# ============================================================
# INTERACTIVE WIZARD
# ============================================================

def get_input(prompt, default="", required=True):
    """Get user input with default value."""
    while True:
        value = input(f"{prompt} [{default}]: ").strip()
        if not value and default:
            return default
        if not value and required:
            print("  ⚠️  Required field. Please enter a value.")
            continue
        return value

def setup():
    """Run setup wizard."""
    print("=" * 60)
    print("  Blog Lifecycle Pro — Standalone Setup")
    print("=" * 60)
    print()
    print("Setup blog automation tanpa Hermes dependency.")
    print()
    
    # Blog configuration
    print("📝 BLOG CONFIGURATION")
    print("-" * 40)
    domain = get_input("Domain blog (e.g., myblog.com)")
    blog_id = get_input("Blogger Blog ID (angka)")
    
    # AI provider
    print()
    print("🤖 AI PROVIDER")
    print("-" * 40)
    print("Pilih AI provider:")
    print("  1. OpenAI (GPT-4)")
    print("  2. DeepSeek")
    print("  3. Ollama (local)")
    print()
    
    provider_choice = get_input("Pilihan (1-3)", "1")
    
    provider_map = {"1": "openai", "2": "deepseek", "3": "ollama"}
    provider = provider_map.get(provider_choice, "openai")
    
    api_key = ""
    model = ""
    base_url = ""
    
    if provider == "openai":
        api_key = get_input("OpenAI API Key")
        model = get_input("Model", "gpt-4", required=False)
    elif provider == "deepseek":
        api_key = get_input("DeepSeek API Key")
        model = get_input("Model", "deepseek-chat", required=False)
    elif provider == "ollama":
        model = get_input("Model", "llama2", required=False)
        base_url = get_input("Ollama URL", "http://localhost:11434", required=False)
    
    # Generate config
    print()
    print("=" * 60)
    print("  Generating configuration...")
    print("=" * 60)
    print()
    
    config = {
        "domain": domain,
        "platform": "blogger",
        "blog_id": blog_id,
        "language": "id",
        "ai": {
            "provider": provider,
            "model": model,
            "api_key": api_key,
        },
        "pipeline": {
            "wip_limit": 3,
            "publish_mode": "draft",
            "autonomy": "gated",
        },
        "workspace": {
            "path": "workspace",
        }
    }
    
    if base_url:
        config["ai"]["base_url"] = base_url
    
    # Write config
    config_path = Path("config/config.yaml")
    config_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(config_path, 'w') as f:
        yaml.dump(config, f, default_flow_style=False)
    
    print(f"  ✅ Config saved: {config_path}")
    
    # Create workspace directories
    workspace = Path("workspace")
    (workspace / "drafts").mkdir(parents=True, exist_ok=True)
    (workspace / "published").mkdir(parents=True, exist_ok=True)
    (workspace / "research").mkdir(parents=True, exist_ok=True)
    
    print(f"  ✅ Workspace created: {workspace}")
    
    # Generate .env
    env_content = f"""# Blog Lifecycle Pro — Environment Variables
# Generated: {datetime.now().isoformat()}

# AI Provider API Keys
{"OPENAI_API_KEY=" + api_key if provider == "openai" else ""}
{"DEEPSEEK_API_KEY=" + api_key if provider == "deepseek" else ""}
"""
    
    env_path = Path(".env")
    env_path.write_text(env_content)
    print(f"  ✅ .env created: {env_path}")
    
    # Summary
    print()
    print("=" * 60)
    print("  ✅ Setup Complete!")
    print("=" * 60)
    print()
    print("📋 NEXT STEPS:")
    print()
    print("1. Install dependencies:")
    print("   pip install -r requirements.txt")
    print()
    print("2. Test pipeline:")
    print("   python3 -m blog.pipeline status")
    print()
    print("3. Start research:")
    print("   python3 -m blog.pipeline research 'topik anda'")
    print()
    print("📊 YOUR CONFIGURATION:")
    print(f"   Domain:     {domain}")
    print(f"   Blog ID:    {blog_id}")
    print(f"   AI Provider: {provider}")
    print(f"   Model:      {model}")
    print()

if __name__ == "__main__":
    setup()

from blog.license import check_license, require_license, track_usage, is_feature_available
"""
Blog Lifecycle Pro — Standalone Pipeline

Blog automation tanpa Hermes dependency.
Bisa jalan di Windows/Linux dengan Python 3.10+.

Usage:
    python3 -m blog.pipeline status
    python3 -m blog.pipeline research "topik"
    python3 -m blog.pipeline draft <idea_id>
"""

import os
import json
import yaml
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, Any

# ============================================================
# CONFIGURATION
# ============================================================

class Config:
    """Load configuration from config.yaml."""
    
    def __init__(self, config_path: str = "config/config.yaml"):
        self.config_path = Path(config_path)
        self.config = self._load()
    
    def _load(self) -> Dict[str, Any]:
        """Load config from YAML file."""
        if not self.config_path.exists():
            raise FileNotFoundError(f"Config not found: {self.config_path}")
        
        with open(self.config_path, 'r') as f:
            return yaml.safe_load(f)
    
    def get(self, key: str, default=None):
        """Get config value."""
        keys = key.split('.')
        value = self.config
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k, default)
            else:
                return default
        return value

# ============================================================
# AI PROVIDER ABSTRACTION
# ============================================================

class AIProvider:
    """Abstract AI provider interface."""
    
    def generate(self, prompt: str, system_prompt: str = "") -> str:
        """Generate text from prompt."""
        raise NotImplementedError

class OpenAIProvider(AIProvider):
    """OpenAI API provider."""
    
    def __init__(self, api_key: str, model: str = "gpt-4"):
        self.api_key = api_key
        self.model = model
        self.base_url = "https://api.openai.com/v1"
    
    def generate(self, prompt: str, system_prompt: str = "") -> str:
        """Generate text using OpenAI API."""
        import requests
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        
        data = {
            "model": self.model,
            "messages": messages,
            "temperature": 0.7
        }
        
        response = requests.post(
            f"{self.base_url}/chat/completions",
            headers=headers,
            json=data
        )
        response.raise_for_status()
        
        return response.json()["choices"][0]["message"]["content"]

class DeepSeekProvider(AIProvider):
    """DeepSeek API provider."""
    
    def __init__(self, api_key: str, model: str = "deepseek-chat"):
        self.api_key = api_key
        self.model = model
        self.base_url = "https://api.deepseek.com/v1"
    
    def generate(self, prompt: str, system_prompt: str = "") -> str:
        """Generate text using DeepSeek API."""
        import requests
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        
        data = {
            "model": self.model,
            "messages": messages,
            "temperature": 0.7
        }
        
        response = requests.post(
            f"{self.base_url}/chat/completions",
            headers=headers,
            json=data
        )
        response.raise_for_status()
        
        return response.json()["choices"][0]["message"]["content"]

class OllamaProvider(AIProvider):
    """Ollama local provider."""
    
    def __init__(self, model: str = "llama2", base_url: str = "http://localhost:11434"):
        self.model = model
        self.base_url = base_url
    
    def generate(self, prompt: str, system_prompt: str = "") -> str:
        """Generate text using Ollama API."""
        import requests
        
        data = {
            "model": self.model,
            "prompt": prompt,
            "system": system_prompt,
            "stream": False
        }
        
        response = requests.post(
            f"{self.base_url}/api/generate",
            json=data
        )
        response.raise_for_status()
        
        return response.json()["response"]

def create_provider(config: Config) -> AIProvider:
    """Create AI provider from config."""
    provider_type = config.get("ai.provider", "openai")
    
    if provider_type == "openai":
        api_key = os.getenv("OPENAI_API_KEY") or config.get("ai.api_key")
        model = config.get("ai.model", "gpt-4")
        return OpenAIProvider(api_key, model)
    
    elif provider_type == "deepseek":
        api_key = os.getenv("DEEPSEEK_API_KEY") or config.get("ai.api_key")
        model = config.get("ai.model", "deepseek-chat")
        return DeepSeekProvider(api_key, model)
    
    elif provider_type == "ollama":
        model = config.get("ai.model", "llama2")
        base_url = config.get("ai.base_url", "http://localhost:11434")
        return OllamaProvider(model, base_url)
    
    else:
        raise ValueError(f"Unknown AI provider: {provider_type}")

# ============================================================
# PIPELINE STAGES
# ============================================================

class Pipeline:
    """Blog lifecycle pipeline."""
    
    def __init__(self, config: Config, ai: AIProvider):
        self.config = config
        self.ai = ai
        self.workspace = Path(config.get("workspace.path", "workspace"))
        self.journal = self.workspace / "journal.jsonl"
    
    def status(self) -> Dict[str, Any]:
        """Get pipeline status."""
        # Read journal
        articles = []
        if self.journal.exists():
            with open(self.journal, 'r') as f:
                for line in f:
                    if line.strip():
                        articles.append(json.loads(line))
        
        return {
            "total_articles": len(articles),
            "stages": self._count_stages(articles),
            "wip_limit": self.config.get("pipeline.wip_limit", 3),
            "wip_current": sum(1 for a in articles if a.get("stage") in ["researching", "drafting", "reviewing"])
        }
    
    def _count_stages(self, articles: list) -> Dict[str, int]:
        """Count articles per stage."""
        stages = {}
        for article in articles:
            stage = article.get("stage", "unknown")
            stages[stage] = stages.get(stage, 0) + 1
        return stages
    
    def research(self, topic: str) -> str:
        """Start research for a topic."""
        idea_id = self._slugify(topic)
        
        # Check WIP limit
        status = self.status()
        if status["wip_current"] >= status["wip_limit"]:
            raise Exception(f"WIP limit reached ({status['wip_limit']}). Finish existing articles first.")
        
        # Create research brief using AI
        system_prompt = """Kamu adalah research analyst untuk blog. 
Buat research brief yang lengkap untuk topik yang diberikan.
Format:
- Keyword utama dan turunan
- Search volume estimate
- Kompetitor analysis
- Content angle yang unik
- Target audience"""
        
        prompt = f"Buat research brief untuk topik: {topic}"
        research_brief = self.ai.generate(prompt, system_prompt)
        
        # Save to journal
        self._log_event({
            "idea_id": idea_id,
            "topic": topic,
            "stage": "researching",
            "research_brief": research_brief,
            "timestamp": datetime.now().isoformat()
        })
        
        return idea_id
    
    def draft(self, idea_id: str) -> str:
        """Create draft from research."""
        # Load research from journal
        research = self._load_research(idea_id)
        if not research:
            raise Exception(f"Research not found for: {idea_id}")
        
        # Create draft using AI
        system_prompt = """Kamu adalah blog writer.
Buat artikel blog yang menarik dan informatif berdasarkan research brief.
Gunakan tone casual, hindari AI-tells, sertakan contoh nyata.
Minimal 600 kata."""
        
        prompt = f"Buat artikel blog berdasarkan research ini:\n\n{research['research_brief']}"
        draft = self.ai.generate(prompt, system_prompt)
        
        # Save draft
        draft_path = self.workspace / "drafts" / f"{idea_id}.md"
        draft_path.parent.mkdir(parents=True, exist_ok=True)
        draft_path.write_text(draft)
        
        # Update journal
        self._log_event({
            "idea_id": idea_id,
            "stage": "drafted",
            "draft_path": str(draft_path),
            "timestamp": datetime.now().isoformat()
        })
        
        return str(draft_path)
    
    def review(self, idea_id: str) -> Dict[str, Any]:
        """Review draft."""
        # Load draft
        draft_path = self.workspace / "drafts" / f"{idea_id}.md"
        if not draft_path.exists():
            raise Exception(f"Draft not found: {idea_id}")
        
        draft = draft_path.read_text()
        
        # Review using AI
        system_prompt = """Kamu adalah blog editor.
Review artikel dan berikan:
1. Verdict: PASS/FAIL
2. Issues yang ditemukan
3. Suggestions untuk perbaikan
4. SEO score (0-100)"""
        
        prompt = f"Review artikel ini:\n\n{draft}"
        review = self.ai.generate(prompt, system_prompt)
        
        # Update journal
        self._log_event({
            "idea_id": idea_id,
            "stage": "reviewed",
            "review": review,
            "timestamp": datetime.now().isoformat()
        })
        
        return {"idea_id": idea_id, "review": review}
    
    def gate(self, idea_id: str) -> bool:
        """Run quality gate checks."""
        # Load draft
        draft_path = self.workspace / "drafts" / f"{idea_id}.md"
        if not draft_path.exists():
            return False
        
        draft = draft_path.read_text()
        
        # Basic checks
        checks = {
            "word_count": len(draft.split()) >= 600,
            "has_title": draft.startswith("#"),
            "no_ai_tells": not any(phrase in draft.lower() for phrase in [
                "di era digital",
                "sangat penting",
                "tidak dapat dipungkiri"
            ])
        }
        
        passed = all(checks.values())
        
        # Update journal
        self._log_event({
            "idea_id": idea_id,
            "stage": "gated",
            "passed": passed,
            "checks": checks,
            "timestamp": datetime.now().isoformat()
        })
        
        return passed
    
    def approve(self, idea_id: str) -> bool:
        """Approve article for publishing."""
        # Check if gated
        status = self._get_article_status(idea_id)
        if status != "gated":
            raise Exception(f"Article must be gated before approval. Current status: {status}")
        
        # Update journal
        self._log_event({
            "idea_id": idea_id,
            "stage": "approved",
            "timestamp": datetime.now().isoformat()
        })
        
        return True
    
    def publish(self, idea_id: str) -> str:
        """Publish to Blogger."""
        # Load draft
        draft_path = self.workspace / "drafts" / f"{idea_id}.md"
        if not draft_path.exists():
            raise Exception(f"Draft not found: {idea_id}")
        
        # TODO: Implement Blogger API integration
        # For now, just mark as published
        self._log_event({
            "idea_id": idea_id,
            "stage": "published",
            "timestamp": datetime.now().isoformat()
        })
        
        return f"Published: {idea_id}"
    
    def _slugify(self, text: str) -> str:
        """Convert text to slug."""
        import re
        text = text.lower().strip()
        text = re.sub(r'[^\w\s-]', '', text)
        text = re.sub(r'[-\s]+', '-', text)
        return text
    
    def _log_event(self, event: Dict[str, Any]):
        """Log event to journal."""
        self.journal.parent.mkdir(parents=True, exist_ok=True)
        with open(self.journal, 'a') as f:
            f.write(json.dumps(event) + "\n")
    
    def _load_research(self, idea_id: str) -> Optional[Dict]:
        """Load research from journal."""
        if not self.journal.exists():
            return None
        
        with open(self.journal, 'r') as f:
            for line in f:
                if line.strip():
                    event = json.loads(line)
                    if event.get("idea_id") == idea_id and event.get("stage") == "researching":
                        return event
        return None
    
    def _get_article_status(self, idea_id: str) -> str:
        """Get current status of an article."""
        if not self.journal.exists():
            return "unknown"
        
        status = "unknown"
        with open(self.journal, 'r') as f:
            for line in f:
                if line.strip():
                    event = json.loads(line)
                    if event.get("idea_id") == idea_id:
                        status = event.get("stage", "unknown")
        
        return status

# ============================================================
# CLI INTERFACE
# ============================================================

def main():
    # Check license
    require_license()
    
    """Main CLI entry point."""
    import sys
    
    # Load config
    config = Config()
    
    # Create AI provider
    ai = create_provider(config)
    
    # Create pipeline
    pipeline = Pipeline(config, ai)
    
    # Parse command
    if len(sys.argv) < 2:
        print("Usage: python3 -m blog.pipeline <command> [args]")
        print("Commands: status, research, draft, review, gate, approve, publish")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "status":
        status = pipeline.status()
        print(f"Total articles: {status['total_articles']}")
        print(f"WIP: {status['wip_current']}/{status['wip_limit']}")
        print(f"Stages: {status['stages']}")
    
    elif command == "research":
        if len(sys.argv) < 3:
            print("Usage: python3 -m blog.pipeline research <topic>")
            sys.exit(1)
        topic = sys.argv[2]
        idea_id = pipeline.research(topic)
        print(f"Research started: {idea_id}")
    
    elif command == "draft":
        if len(sys.argv) < 3:
            print("Usage: python3 -m blog.pipeline draft <idea_id>")
            sys.exit(1)
        idea_id = sys.argv[2]
        draft_path = pipeline.draft(idea_id)
        print(f"Draft created: {draft_path}")
    
    elif command == "review":
        if len(sys.argv) < 3:
            print("Usage: python3 -m blog.pipeline review <idea_id>")
            sys.exit(1)
        idea_id = sys.argv[2]
        result = pipeline.review(idea_id)
        print(f"Review: {result['review']}")
    
    elif command == "gate":
        if len(sys.argv) < 3:
            print("Usage: python3 -m blog.pipeline gate <idea_id>")
            sys.exit(1)
        idea_id = sys.argv[2]
        passed = pipeline.gate(idea_id)
        print(f"Gate: {'PASS' if passed else 'FAIL'}")
    
    elif command == "approve":
        if len(sys.argv) < 3:
            print("Usage: python3 -m blog.pipeline approve <idea_id>")
            sys.exit(1)
        idea_id = sys.argv[2]
        approved = pipeline.approve(idea_id)
        print(f"Approved: {approved}")
    
    elif command == "publish":
        if len(sys.argv) < 3:
            print("Usage: python3 -m blog.pipeline publish <idea_id>")
            sys.exit(1)
        idea_id = sys.argv[2]
        result = pipeline.publish(idea_id)
        print(result)
    
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)

if __name__ == "__main__":
    main()

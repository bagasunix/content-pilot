"""
Telegram Notification for Blog Lifecycle Pro
Kirim notifikasi ke Telegram user
"""
import json
import urllib.request
import urllib.error
from typing import Optional, Dict, Any
from pathlib import Path

class TelegramNotifier:
    def __init__(self, bot_token: Optional[str] = None, chat_id: Optional[str] = None):
        self.bot_token = bot_token or ""
        self.chat_id = chat_id or ""
        self.enabled = bool(bot_token and chat_id)
    
    def send(self, message: str, parse_mode: str = "HTML") -> bool:
        """Kirim pesan ke Telegram"""
        if not self.enabled:
            return False
        
        url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"
        payload = {
            "chat_id": self.chat_id,
            "text": message,
            "parse_mode": parse_mode
        }
        
        try:
            data = json.dumps(payload).encode("utf-8")
            req = urllib.request.Request(
                url,
                data=data,
                headers={"Content-Type": "application/json"},
                method="POST"
            )
            with urllib.request.urlopen(req, timeout=10) as resp:
                return resp.status == 200
        except Exception:
            return False
    
    def send_article_ready(self, title: str, score: int, idea_id: str):
        """Notif artikel siap"""
        msg = (
            f"✅ <b>Artikel Siap</b>\n\n"
            f"📝 {title}\n"
            f"📊 Score: {score}/100\n"
            f"🆔 {idea_id}\n\n"
            f"Jalankan: python3 scripts/pipeline.py approve {idea_id}"
        )
        return self.send(msg)
    
    def send_draft_created(self, title: str, idea_id: str):
        """Notif draft dibuat"""
        msg = (
            f"✍️ <b>Draft Dibuat</b>\n\n"
            f"📝 {title}\n"
            f"🆔 {idea_id}\n\n"
            f"Menunggu review..."
        )
        return self.send(msg)
    
    def send_gate_result(self, title: str, passed: bool, issues: list):
        """Notif hasil quality gate"""
        status = "✅ PASS" if passed else "❌ FAIL"
        issues_text = "\n".join([f"• {i}" for i in issues]) if issues else "Tidak ada"
        
        msg = (
            f"{status} <b>Quality Gate</b>\n\n"
            f"📝 {title}\n"
            f"📋 Issues:\n{issues_text}"
        )
        return self.send(msg)
    
    def send_error(self, error: str, context: str = ""):
        """Notif error"""
        msg = (
            f"🚨 <b>Error</b>\n\n"
            f"❌ {error}\n"
        )
        if context:
            msg += f"📍 {context}\n"
        return self.send(msg)
    
    def send_daily_summary(self, stats: Dict[str, Any]):
        """Notif summary harian"""
        msg = (
            f"📊 <b>Daily Summary</b>\n\n"
            f"📝 WIP: {stats.get('wip', 0)}/{stats.get('limit', 3)}\n"
            f"✅ Published: {stats.get('published', 0)}\n"
            f"📈 Total: {stats.get('total', 0)}"
        )
        return self.send(msg)

def load_notifier(config_path: Optional[str] = None) -> TelegramNotifier:
    """Load notifier dari config"""
    if config_path is None:
        config_path = str(Path.home() / "Project/blog-lifecycle-pro/workspace/config.yaml")
    
    try:
        import yaml
        with open(config_path) as f:
            config = yaml.safe_load(f)
        
        tg = config.get("notifications", {}).get("telegram", {})
        return TelegramNotifier(
            bot_token=tg.get("bot_token"),
            chat_id=tg.get("chat_id")
        )
    except Exception:
        return TelegramNotifier()

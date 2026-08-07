import os
import feedparser
import requests
from datetime import datetime

FEEDS = {
    "🌍 Mundo": "https://g1.globo.com/rss/g1/mundo/",
    "🇧🇷 Brasil": "https://g1.globo.com/rss/g1/brasil/",
    "📍 Sudeste": "https://news.google.com/rss/search?q=Sudeste+Brasil&hl=pt-BR&gl=BR&ceid=BR:pt-419",
    "🏙️ São Paulo": "https://g1.globo.com/rss/g1/sao-paulo/"
}

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def buscar_noticias(limite_por_categoria=3):
    relatorio = f"📰 *RESUMO DIÁRIO DE NOTÍCIAS* - {datetime.now().strftime('%d/%m/%Y')}\n"
    relatorio += "=" * 35 + "\n\n"

    for categoria, url in FEEDS.items():
        relatorio += f"*{categoria}*\n"
        feed = feedparser.parse(url)
        
        if not feed.entries:
            relatorio += "• Nenhuma notícia encontrada.\n\n"
            continue

        for entry in feed.entries[:limite_por_categoria]:
            titulo = entry.title.strip()
            link = entry.link
            relatorio += f"• [{titulo}]({link})\n"
        
        relatorio += "\n"

    return relatorio

def enviar_telegram(mensagem):
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        print(mensagem)
        return

    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": mensagem,
        "parse_mode": "Markdown",
        "disable_web_page_preview": True
    }
    requests.post(url, data=payload)

if __name__ == "__main__":
    resumo = buscar_noticias(limite_por_categoria=4)
    enviar_telegram(resumo)

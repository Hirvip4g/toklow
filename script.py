import os
import re
import requests

# URL objetivo (la misma de tu script PHP)
url = 'https://telegratuita.st/token.php'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

try:
    # Realizar petición HTTP
    response = requests.get(url, headers=headers)
    html = response.text

    # Extraer token mediante expresión regular (idéntico al PHP)[cite: 1]
    token_match = re.search(r'token\s*:\s*["\']([^"\']+)["\']', html)
    token = token_match.group(1) if token_match else None

    if not token:
        print("Error: No se pudo encontrar el token.")
        exit(1)

    # Credenciales de Telegram (se leen de las variables de entorno de GitHub)
    BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
    CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID')

    # Mensaje a enviar
    mensaje = f"🔑 *Nuevo Token Extraído*\n\n`{token}`"

    # Enviar mensaje a Telegram
    telegram_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        'chat_id': CHAT_ID,
        'text': mensaje,
        'parse_mode': 'Markdown'
    }

    res = requests.post(telegram_url, data=payload)
    if res.status_code == 200:
        print("¡Token enviado a Telegram con éxito!")
    else:
        print(f"Error al enviar a Telegram: {res.text}")

except Exception as e:
    print(f"Ocurrió un error: {e}")
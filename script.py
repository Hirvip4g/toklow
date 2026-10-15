import os
import re
import time
import requests

BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
TELEGRAM_API = f"https://api.telegram.org/bot{BOT_TOKEN}"

def obtener_token_telegratuita():
    url = 'https://telegratuita.st/token.php'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    try:
        response = requests.get(url, headers=headers)
        token_match = re.search(r'token\s*:\s*["\']([^"\']+)["\']', response.text)
        return token_match.group(1) if token_match else None
    except:
        return None

def enviar_mensaje(chat_id, texto, reply_markup=None):
    payload = {
        'chat_id': chat_id,
        'text': texto,
        'parse_mode': 'Markdown'
    }
    if reply_markup:
        payload['reply_markup'] = reply_markup
    requests.post(f"{TELEGRAM_API}/sendMessage", json=payload)

# Bucle principal para escuchar mensajes/botones en Telegram (Long Polling)
print("Bot iniciado y escuchando comandos...")
offset = 0

while True:
    try:
        response = requests.get(f"{TELEGRAM_API}/getUpdates", params={'offset': offset, 'timeout': 30})
        data = response.json()
        
        if data.get("ok"):
            for result in data.get("result", []):
                offset = result["update_id"] + 1
                
                # Si el usuario presiona un botón o manda un mensaje
                if "message" in result:
                    chat_id = result["message"]["chat"]["id"]
                    text = result["message"].get("text", "")
                    
                    if text == "/start" or text == "/token":
                        # Crear un botón interactivo
                        teclado = {
                            "inline_keyboard": [[
                                {"text": "🔄 Obtener Token Ahora", "callback_data": "get_token"}
                            ]]
                        }
                        enviar_mensaje(chat_id, "Presiona el botón para extraer el token actualizado:", teclado)
                
                # Si el usuario hace clic en el botón inline
                elif "callback_query" in result:
                    chat_id = result["callback_query"]["message"]["chat"]["id"]
                    callback_data = result["callback_query"]["data"]
                    
                    if callback_data == "get_token":
                        enviar_mensaje(chat_id, "⏳ Extrayendo token...")
                        token = obtener_token_telegratuita()
                        
                        if token:
                            enviar_mensaje(chat_id, f"🔑 *Token Extraído Exitosamente*\n\n`{token}`")
                        else:
                            enviar_mensaje(chat_id, "❌ Error al extraer el token.")
                            
        time.sleep(1)
    except Exception as e:
        print(f"Error en el bucle: {e}")
        time.sleep(5)
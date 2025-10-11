import requests
import time
import json

BOT_TOKEN = "8227290006:AAHhQCs1KIrRiggUhNJ9hpWE-IVUH7OdLAU"
BASE_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"

def send_message(chat_id, text, reply_markup=None):
    """Отправка сообщения через API Telegram"""
    payload = {
        'chat_id': chat_id,
        'text': text
    }
    
    if reply_markup:
        payload['reply_markup'] = json.dumps(reply_markup)
    
    try:
        response = requests.post(f"{BASE_URL}/sendMessage", json=payload, timeout=10)
        return response.json()
    except Exception as e:
        print(f"❌ Ошибка отправки сообщения: {e}")
        return None

def get_updates(offset=None):
    """Получение обновлений"""
    params = {'timeout': 30}
    if offset:
        params['offset'] = offset
    
    try:
        response = requests.get(f"{BASE_URL}/getUpdates", params=params, timeout=35)
        return response.json()
    except Exception as e:
        print(f"❌ Ошибка получения обновлений: {e}")
        return {'ok': False, 'result': []}

def create_inline_keyboard():
    """Создание инлайн-клавиатуры с Web App кнопкой"""
    return {
        'inline_keyboard': [[{
            'text': 'ОТКРЫТЬ',
            'web_app': {'url': 'https://kupidones.github.io/market/'}
        }]]
    }

def main():
    """Основная функция бота"""
    print("=" * 50)
    print("🛍️ Market Bot запущен!")
    print("📱 Бот готов принимать команду /start")
    print("🔗 Ссылка на приложение: https://kupidones.github.io/market/")
    print("⏹️ Для остановки нажмите Ctrl+C")
    print("=" * 50)
    
    last_update_id = 0
    
    while True:
        try:
            # Получаем обновления
            updates = get_updates(last_update_id + 1)
            
            if updates.get('ok'):
                for update in updates['result']:
                    update_id = update['update_id']
                    
                    if 'message' in update and 'text' in update['message']:
                        message = update['message']
                        chat_id = message['chat']['id']
                        text = message['text']
                        user_name = message['chat'].get('first_name', 'Пользователь')
                        
                        if text == '/start':
                            # Отправляем сообщение с ИНЛАЙН-кнопкой
                            keyboard = create_inline_keyboard()
                            result = send_message(
                                chat_id,
                                f"Привет, {user_name}! 🛍️\n\n"
                                "2\n"
                                "4:",
                                keyboard
                            )
                            
                            if result and result.get('ok'):
                                print(f"✅ Отправлена инлайн-кнопка пользователю {user_name} (ID: {chat_id})")
                            else:
                                print(f"❌ Ошибка отправки пользователю {user_name}")
                    
                    last_update_id = max(last_update_id, update_id)
            
            time.sleep(1)
            
        except KeyboardInterrupt:
            print("\n🛑 Бот остановлен пользователем")
            break
        except Exception as e:
            print(f"⚠️ Ошибка: {e}")
            time.sleep(5)

if __name__ == "__main__":
    main()
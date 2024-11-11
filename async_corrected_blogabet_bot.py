import re
import time
import asyncio
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from telegram import Bot, error

# Настройка Telegram Bot
TELEGRAM_TOKEN = "7537676839:AAE3zmuL6ZWnZuNB43c4S8CqEkthOlWvALs"
bot = Bot(token=TELEGRAM_TOKEN)

# Список капперов и их телеграм-каналов
capper_channels = {
    "https://oskarok.blogabet.com/": "-1002358772434",
    # Добавляйте других капперов и их каналы здесь
    # 1 - страница каппера, 2 - id канала/чата, куда отправляем прогнозы
}

options = Options()
options.add_argument("--headless")  # Запускаем Firefox в безголовом режиме
options.add_argument("--no-sandbox")
options.add_argument("--disable-gpu")
options.add_argument("--disable-dev-shm-usage")

# Указываем путь к geckodriver
service = Service("/usr/local/bin/geckodriver")
driver = webdriver.Firefox(service=service, options=options)

# Авторизация
def login_to_blogabet():
    driver.get("https://blogabet.com/#login")
    time.sleep(2)

    # Тут данные от аккаунта blogabet.com // для проверки HTML кода
    driver.find_element("id", "email").send_keys("jasterelafis777@gmail.com")
    driver.find_element("id", "password").send_keys("Oz098a2HLp")
    driver.find_element("xpath", "//button[@type='submit']").click()

    time.sleep(5)

# Асинхронная функция для отправки сообщения в Телеграм с повторными попытками
async def send_message_with_retry(chat_id, message, retries=3, delay=5):
    for attempt in range(retries):
        try:
            await bot.send_message(chat_id=chat_id, text=message, parse_mode="Markdown")
            print(f"Сообщение отправлено в канал {chat_id}")
            return
        except error.TimedOut:
            print(f"Попытка {attempt + 1} не удалась. Повтор через {delay} секунд...")
            await asyncio.sleep(delay)
    print("Не удалось отправить сообщение после нескольких попыток.")

# Функция для парсинга последнего прогноза
async def get_latest_pick_and_send():
    last_sent_pick_id = None

    while True:
        for capper_url, chat_id in capper_channels.items():
            driver.get(capper_url)
            time.sleep(5)

            # Получаем HTML-код и используем BeautifulSoup для парсинга
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            pick_list = soup.find('ul', id='blogPickList')

            if not pick_list:
                print(f"Не удалось найти контейнер с id 'blogPickList' для {capper_url}.")
                continue

            # Берем самый верхний прогноз
            latest_bet = pick_list.find('li', class_='block media _feedPick feed-pick')
            if not latest_bet:
                print(f"Не удалось найти элемент последнего прогноза для {capper_url}.")
                continue

            # Проверяем, не отправляли ли мы этот прогноз ранее
            pick_id = latest_bet.get("id")
            if pick_id == last_sent_pick_id:
                print("Новых прогнозов нет. Проверка снова через 30 секунд.")
                continue

            last_sent_pick_id = pick_id  # Сохраняем ID последнего отправленного прогноза

            # Извлекаем данные о прогнозе
            title = latest_bet.find('h3').get_text(strip=True)
            bet_info = latest_bet.find('div', class_='pick-line').get_text(strip=True)
            odd = latest_bet.find('span', class_='feed-odd').get_text(strip=True)
            sport_info = latest_bet.find('div', class_='sport-line').get_text(strip=True)

            # Удаляем коэффициент из bet_info
            bet_info = re.sub(r"@\s*\d+(\.\d+)?", "", bet_info).strip()

            # Форматируем сообщение с эмодзи
            message = (
                f"📢 **Новая ставка**\n"
                f"🏆 **Матч**: {title}\n"
                f"💬 **Ставка**: {bet_info}\n"
                f"💰 **Коэффициент**: {odd}\n"
                f"⚽ **Спорт**: {sport_info}"
            )

            # Асинхронная отправка сообщения с повторной попыткой
            await send_message_with_retry(chat_id, message)

        # Ждем 30 сек перед следующей проверкой
        await asyncio.sleep(30)

# Основная функция для выполнения всего скрипта
async def main():
    login_to_blogabet()
    await get_latest_pick_and_send()

# Запуск асинхронной функции
asyncio.run(main())
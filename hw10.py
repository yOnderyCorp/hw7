import sqlite3
import requests
from bs4 import BeautifulSoup
import time
from datetime import datetime


class WeatherDB:
    def __init__(self, db_name="weather_data.db"):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self._create_table()

    def _create_table(self):
        """Создает таблицу, если она еще не существует"""
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS weather (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date_time TEXT,
                temperature TEXT
            )
        ''')
        self.conn.commit()

    def save_weather(self, temp):
        """Сохраняет дату и температуру в БД"""
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.cursor.execute('INSERT INTO weather (date_time, temperature) VALUES (?, ?)', (now, temp))
        self.conn.commit()
        print(f"[{now}] Данные сохранены: {temp}")


def get_weather():
    """Парсинг температуры с сайта Sinoptik"""
    url = "https://sinoptik.ua/погода-київ"
    headers = {'User-Agent': 'Mozilla/5.0'}

    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, 'lxml')

        # Ищем текущую температуру (класс .today-temp)
        temp_element = soup.select_one('.today-temp')

        if temp_element:
            return temp_element.get_text()
        else:
            # Запасной вариант поиска
            temp_element = soup.find('p', class_='today-temp')
            return temp_element.get_text() if temp_element else "Н/Д"

    except Exception as e:
        print(f"Ошибка парсинга: {e}")
        return None


def main():
    db = WeatherDB()
    print("Программа запущена. Обновление каждые 30 минут. Нажмите Ctrl+C для остановки.")

    try:
        while True:
            temp = get_weather()
            if temp:
                db.save_weather(temp)
            else:
                print("Не удалось получить данные о погоде.")

            # Ждем 30 минут (30 * 60 секунд)
            time.sleep(1800)

    except KeyboardInterrupt:
        print("\nПрограмма остановлена пользователем.")
    finally:
        db.conn.close()


if __name__ == "__main__":
    main()
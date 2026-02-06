import requests
from bs4 import BeautifulSoup
import tkinter as tk
from tkinter import messagebox


class CurrencyConverter:
    def __init__(self):
        # URL страницы курсов валют НБУ
        self.url = "https://bank.gov.ua/ua/markets/exchangerates"
        self.usd_rate = self._get_usd_rate()

    def _get_usd_rate(self):
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            response = requests.get(self.url, headers=headers, timeout=10)
            response.raise_for_status()  # Проверка на ошибки 404, 500 и т.д.
            soup = BeautifulSoup(response.content, 'html.parser'
            usd_cell = soup.find('td', string=lambda t: t and 'USD' in t)

            if not usd_cell:
                # Запасной вариант: поиск по тексту "Долар"
                usd_cell = soup.find('td', string=lambda t: t and 'Долар' in t)

            if usd_cell:
                usd_row = usd_cell.find_parent('tr')
                cells = usd_row.find_all('td')
                for cell in reversed(cells):
                    clean_text = cell.get_text(strip=True).replace(',', '.')
                    try:
                        rate = float(clean_text)
                        return rate
                    except ValueError:
                        continue

            return None
        except Exception as e:
            print(f"Критическая ошибка при парсинге: {e}")
            return None

    def convert(self, amount):
        if self.usd_rate and amount > 0:
            return amount / self.usd_rate
        return 0


# --- Графический интерфейс ---

class App:
    def __init__(self, root):
        self.converter = CurrencyConverter()

        self.root = root
        self.root.title("NBU Currency Converter")
        self.root.geometry("350x250")
        self.root.resizable(False, False)

        # Проверка, удалось ли получить курс при запуске
        rate_display = f"{self.converter.usd_rate} UAH" if self.converter.usd_rate else "Ошибка загрузки"

        # Заголовок
        tk.Label(root, text="Курс НБУ (USD/UAH):", font=("Arial", 10)).pack(pady=(20, 0))
        tk.Label(root, text=rate_display, font=("Arial", 14, "bold"), fg="blue").pack(pady=(0, 20))

        # Поле ввода
        tk.Label(root, text="Введите сумму в гривнах:").pack()
        self.entry = tk.Entry(root, justify='center', font=("Arial", 12))
        self.entry.pack(pady=5)
        self.entry.bind("<Return>", lambda e: self.calculate())  # Расчет по нажатию Enter

        # Кнопка
        self.btn = tk.Button(root, text="Конвертировать", command=self.calculate, bg="#4CAF50", fg="white", width=20)
        self.btn.pack(pady=10)

        # Результат
        self.result_label = tk.Label(root, text="", font=("Arial", 12, "bold"))
        self.result_label.pack(pady=10)

    def calculate(self):
        if not self.converter.usd_rate:
            messagebox.showerror("Ошибка", "Курс валют не загружен. Проверьте интернет.")
            return

        try:
            uah = float(self.entry.get().replace(',', '.'))
            usd = self.converter.convert(uah)
            self.result_label.config(text=f"{usd:.2f} USD", fg="black")
        except ValueError:
            messagebox.showwarning("Внимание", "Введите число (например: 100.50)")


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
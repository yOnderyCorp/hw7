def check_age(age):
    try:
        # assert проверяет условие. Если оно False, вызывается исключение с текстом после запятой.
        assert age >= 18, "Вам має бути 18 років або більше"
        print("Ви можете використовувати цей сервіс")
    except AssertionError as error:
        print(error)


if __name__ == "__main__":
    try:
        # Просим пользователя ввести данные
        user_input = input("Введіть свій вік: ")
        age = int(user_input)
        check_age(age)

    except ValueError:
        # если пользователь ввел не цифры, а буквы
        print("Помилка: будь ласка, введіть числове значення для віку.")
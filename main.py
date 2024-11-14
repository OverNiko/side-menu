import logging
import tkinter as tk
from tkinter import END, messagebox
import pyautogui
from email_module import EmailManager
from animation import animate_menu, animate_hide_menu
from styles import create_button

# Настройка логирования
logging.basicConfig(filename='application.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s', encoding='utf-8')


class Application:
    def __init__(self, root):
        self.root = root
        self.email_manager = EmailManager()
        self.current_email = ""
        self.output_text = None
        self.stop_button = None
        self.next_email = None
        self.check_email = None

        logging.info("Приложение инициализировано")
        self.setup_ui()
        self.check_mouse_position()

    def setup_ui(self):
        """Настройка основного интерфейса и меню."""
        self.root.withdraw()  # Скрываем основное окно
        self.root.geometry("400x300")  # Размер окна

        self.menu = tk.Toplevel(self.root)
        self.menu.withdraw()  # Скрываем окно меню изначально
        self.menu.overrideredirect(True)  # Убираем рамку окна
        self.menu.attributes("-topmost", True)  # Делаем окно поверх других

        self.menu.configure(bg="#2E2E2E")  # Темный фон
        self.menu.geometry(f"0x{self.root.winfo_screenheight()}+{self.root.winfo_screenwidth()}+0")  # Начальная позиция окна (вне экрана)

        self.create_buttons()
        logging.info("Интерфейс настроен")

    def create_buttons(self):
        """Создание кнопок в меню."""
        self.button1 = create_button(self.menu, "Показать сообщение", self.show_message, "#4CAF50", 10, 10)
        self.button2 = create_button(self.menu, "Временная почта", self.start_email, "#2196F3", 10, 50)
        self.button3 = create_button(self.menu, "Закрыть приложение", self.close_application, "#F44336", 10, 90)

    def show_menu(self):
        """Показать меню на всей правой стороне экрана."""
        self.reset_buttons()
        animate_menu(self.menu, self.root, 0)
        logging.info("Меню отображается")

    def reset_buttons(self):
        """Сбросить кнопки в начальное положение."""
        self.button1.place(x=10, y=10, width=250)
        self.button2.place(x=10, y=50, width=250)
        self.button3.place(x=10, y=90, width=250)
        logging.debug("Кнопки сброшены")

    def hide_menu(self):
        """Скрыть меню с анимацией."""
        animate_hide_menu(self.menu, self.root, 300, 
                        self.button1, self.button2, self.button3) 
                        # self.output_text, self.stop_button, 
                        # self.next_email, self.check_email)
        logging.info("Меню скрывается")


    def create_output_text(self):
        """Создание текстового поля для вывода."""
        self.output_text = tk.Text(self.menu, wrap='word', height=10, width=20)
        self.output_text.place(x=10, y=130, width=250)
        logging.debug("Создано текстовое поле для вывода")

    def start_email(self):
        """Запуск временной почты."""
        self.current_email = self.email_manager.main("start").split(": ")[-1].strip()
        logging.info(f"Текущий email: {self.current_email}")

        self.create_output_text()
        self.update_output_text(f"[+] Ваш почтовый адрес: {self.current_email}")

        self.create_action_buttons()

    def create_action_buttons(self):
        """Создание кнопок для управления почтой."""
        self.stop_button = create_button(self.menu, "Выключить почту", self.stop_code2, "#2196F3", 10, 50)
        self.next_email = create_button(self.menu, "Сменить Email", self.change_email_wrapper, "#2196F3", 10, 305)
        self.check_email = create_button(self.menu, "Проверить Email", self.check_mail_wrapper, "#2196F3", 10, 345)
        logging.debug("Созданы кнопки для управления почтой")

    def update_output_text(self, text):
        """Обновление текста в текстовом поле."""
        if self.output_text is not None:
            self.output_text.delete('1.0', END)
            self.output_text.insert(END, text)
        logging.debug("Обновлен текст в текстовом поле")

    def check_mail_wrapper(self):
        """Обертка для функции проверки почты."""
        result = self.email_manager.check_mail(mail=self.current_email)
        self.update_output_text(result)
        logging.info(f"Результат проверки почты: {result}")

    def change_email_wrapper(self):
        """Обертка для смены почты."""
        new_email = self.email_manager.main("change").split(": ")[-1].strip()
        self.current_email = new_email
        self.update_output_text(f"Ваш новый почтовый адрес: {self.current_email}")
        logging.info(f"Смена email на: {self.current_email}")

    def stop_code2(self):
        """Остановить работу с почтой и скрыть элементы."""
        self.stop_button.destroy()
        self.next_email.destroy()
        self.check_email.destroy()
        self.output_text.place_forget()
        self.email_manager.main("del")
        logging.info('Модуль временного Email прерван!')
        self.button2.place(x=10, y=50)

    def check_mouse_position(self):
        """Проверка положения курсора для отображения меню."""
        x, y = pyautogui.position()
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        if x > screen_width - 200 and y > screen_height - 200:
            if not self.menu.winfo_viewable():
                self.show_menu()
        else:
            if self.menu.winfo_viewable():
                menu_x = self.menu.winfo_x()
                menu_y = self.menu.winfo_y()
                menu_width = self.menu.winfo_width()
                menu_height = self.menu.winfo_height()

                if not (menu_x <= x <= menu_x + menu_width and menu_y <= y <= menu_y + menu_height):
                    self.hide_menu()

        self.root.after(100, self.check_mouse_position)

    def show_message(self):
        """Показать информационное сообщение."""
        messagebox.showinfo("Информация", "Это сообщение из выпадающего меню!")
        logging.info("Показано информационное сообщение")

    def close_application(self):
        """Закрыть приложение."""
        self.root.quit()
        logging.info("Приложение закрыто")

if __name__ == "__main__":
    root = tk.Tk()
    app = Application(root)
    root.mainloop()
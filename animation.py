import logging

def animate_menu(menu, root, current_width):
    """Плавное появление меню."""
    if current_width < 300:
        menu.geometry(f"{current_width}x{root.winfo_screenheight()}+{root.winfo_screenwidth() - current_width}+0")
        current_width += 30
        menu.after(10, lambda: animate_menu(menu, root, current_width))
    else:
        menu.deiconify()
        logging.info("Меню полностью отображается")

def animate_hide_menu(menu, root, current_width, button1, button2, button3): #, output_text, stop_button, next_email, check_email):
    """Плавное исчезновение меню с анимацией элементов."""
    if current_width > 0:
        menu.geometry(f"{current_width}x{root.winfo_screenheight()}+{root.winfo_screenwidth() - current_width}+0")

        # Перемещение кнопок меню
        button1.place(x=root.winfo_screenwidth() - 10, y=10, width=250)
        button2.place(x=root.winfo_screenwidth() - 10, y=50, width=250)
        button3.place(x=root.winfo_screenwidth() - 10, y=90, width=250)

        # # Проверка порога ширины меню для скрытия дополнительных элементов
        # if current_width > 0:
        #     # Удержание элементов в их текущем положении до скрытия
        #     if output_text is not None and output_text.winfo_ismapped():
        #         output_text.place(x=root.winfo_screenwidth() - 10, y=130, width=250)
        #         stop_button.place(x=root.winfo_screenwidth() - 10, y=50, width=250)
        #         next_email.place(x=root.winfo_screenwidth() - 10, y=305, width=250)
        #         check_email.place(x=root.winfo_screenwidth() - 10, y=345, width=250)

        # Уменьшение ширины меню
        current_width -= 30
        menu.after(10, lambda: animate_hide_menu(menu, root, current_width, button1, button2, button3)) #, output_text, stop_button, next_email, check_email))
    else:
        # Полностью скрываем меню
        menu.withdraw()
        logging.info("Меню скрыто")

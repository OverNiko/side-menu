import tkinter as tk  # Добавляем импорт tkinter

def darken_color(color, factor=0.7):
    """Функция для затемнения цвета."""
    # Конвертируем цвет из hex в RGB
    color = color.lstrip('#')
    rgb = tuple(int(color[i:i+2], 16) for i in (0, 2, 4))

    # Затемняем цвет
    dark_rgb = tuple(int(c * factor) for c in rgb)

    # Возвращаем затемненный цвет обратно в hex формат
    return '#%02x%02x%02x' % dark_rgb

def create_button(menu, text, command, bg_color, x, y, on_hover=True):
    """Создание кнопки с возможностью затемнения при наведении."""
    button = tk.Button(
        menu,
        text=text,
        command=command,
        bg=bg_color,
        fg="white",
        borderwidth=2,
        relief="raised"
    )
    button.place(x=x, y=y, width=250)
    button.configure(font=("Arial", 12), highlightbackground="#2E2E2E")

    if on_hover:
        # Применяем эффект затемнения
        button.bind("<Enter>", lambda e: button.configure(bg=darken_color(bg_color)))
        button.bind("<Leave>", lambda e: button.configure(bg=bg_color))

    return button

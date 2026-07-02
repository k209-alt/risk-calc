import flet as ft

def main(page: ft.Page):
    page.title = "Risk Calculator"
    page.theme_mode = ft.ThemeMode.DARK  # Минималистичный темный стиль
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.padding = 20

    # Выбор формулы
    dropdown_formula = ft.Dropdown(
        label="Выбор формулы",
        options=[
            ft.dropdown.Option("forex", "Forex (x100000)"),
            ft.dropdown.Option("futures_micro", "Futures Micro (M6E - $1/tick)"),
            ft.dropdown.Option("futures_std", "Futures Standard (6E - $12.5/tick)"),
        ],
        value="forex",
        width=300,
    )
    
    # Поля ввода
    input_r = ft.TextField(label="Риск (r)", keyboard_type=ft.KeyboardType.NUMBER, width=300)
    input_e = ft.TextField(label="Вход (e)", keyboard_type=ft.KeyboardType.NUMBER, width=300)
    input_s = ft.TextField(label="Стоп (s)", keyboard_type=ft.KeyboardType.NUMBER, width=300)
    
    # Поле вывода результата
    result_text = ft.Text(value="Результат: X = 0.00", size=22, weight=ft.FontWeight.BOLD, color=ft.Colors.GREEN_ACCENT)

    # Логика расчета
    def calculate(e):
        try:
            # Заменяем запятые на точки
            r = float(input_r.value.replace(",", "."))
            entry = float(input_e.value.replace(",", "."))
            stop = float(input_s.value.replace(",", "."))
            
            diff = abs(entry - stop)
            
            if diff == 0:
                result_text.value = "Ошибка: Вход и Стоп равны!"
                result_text.color = ft.Colors.RED_ACCENT
                page.update()
                return

            if dropdown_formula.value == "forex":
                # Стандартный форекс лот
                x = r / (diff * 100000)
                label = "лотов"
            
            elif dropdown_formula.value == "futures_micro":
                # Микро-фьючерс EUR (M6E): 1 тик = 0.0001, стоимость тика = $1.00
                ticks = diff / 0.0001
                x = r / (ticks * 1.00)
                label = "контр. (Micro)"
                
            elif dropdown_formula.value == "futures_std":
                # Полный фьючерс EUR (6E): 1 тик = 0.0001, стоимость тика = $12.50
                ticks = diff / 0.0001
                x = r / (ticks * 12.50)
                label = "контр. (Standard)"
            
            # Округление результатов
            # Для форекса до 0.01 лота, для фьючерсов контракты обычно округляют в меньшую сторону до целого,
            # но оставим 2 знака, чтобы ты видел точную математику позиции
            result_text.value = f"Результат: X = {round(x, 2):.2f} {label}"
            result_text.color = ft.Colors.GREEN_ACCENT
            
        except (ValueError, TypeError):
            result_text.value = "Заполните все поля числами!"
            result_text.color = ft.Colors.RED_ACCENT
            
        page.update()

    # Кнопка по стандартам Flet 0.85+
    btn_ok = ft.Button(
        content=ft.Text("OK"),
        on_click=calculate,
        width=300,
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=8),
        )
    )

    # Элементы интерфейса
    page.add(
        ft.Column(
            controls=[
                ft.Text("Калькулятор Риска", size=24, weight=ft.FontWeight.W_500),
                ft.Divider(height=10, color=ft.Colors.TRANSPARENT),
                dropdown_formula,
                input_r,
                input_e,
                input_s,
                ft.Divider(height=10, color=ft.Colors.TRANSPARENT),
                btn_ok,
                ft.Divider(height=10, color=ft.Colors.TRANSPARENT),
                result_text,
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
    )

# Новый метод запуска вместо ft.app()
ft.run(main)

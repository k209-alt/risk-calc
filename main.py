import flet as ft

def main(page: ft.Page):
    page.title = "calculator of risk"
    page.theme_mode = ft.ThemeMode.DARK
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.padding = 20

    # Выбор формулы рынка
    dropdown_formula = ft.Dropdown(
        label="Выбор формулы",
        options=[
            ft.dropdown.Option("forex", "Forex (x100000)"),
            ft.dropdown.Option("futures_micro", "Futures Micro"),
            ft.dropdown.Option("futures_std", "Futures Standard"),
        ],
        value="forex",
        width=300,
    )
    
    # Выбор конкретного контракта
    dropdown_pair = ft.Dropdown(
        label="Выбор контракта (для фьючерсов)",
        options=[
            ft.dropdown.Option("eur", "Euro (6E / M6E)"),
            ft.dropdown.Option("gbp", "GBP (6B / M6B)"),
        ],
        value="eur",
        width=300,
    )
    
    # Поля ввода
    input_r = ft.TextField(label="Риск (r)", keyboard_type=ft.KeyboardType.NUMBER, width=300)
    input_e = ft.TextField(label="Вход (e)", keyboard_type=ft.KeyboardType.NUMBER, width=300)
    input_s = ft.TextField(label="Стоп (s)", keyboard_type=ft.KeyboardType.NUMBER, width=300)
    
    # Поле вывода результата
    result_text = ft.Text(value="Результат: X = 0.00", size=22, weight=ft.FontWeight.BOLD)

    # Логика расчета
    def calculate(e):
        try:
            if not input_r.value or not input_e.value or not input_s.value:
                result_text.value = "Заполните все поля!"
                page.update()
                return
                
            r = float(input_r.value.replace(",", "."))
            entry = float(input_e.value.replace(",", "."))
            stop = float(input_s.value.replace(",", "."))
            
            diff = abs(entry - stop)
            
            if diff == 0:
                result_text.value = "Ошибка: Вход и Стоп равны!"
                page.update()
                return

            market = dropdown_formula.value
            pair = dropdown_pair.value

            # --- FOREX ---
            if market == "forex":
                x = r / (diff * 100000)
                label = "лотов"
            
            # --- FUTURES MICRO ---
            elif market == "futures_micro":
                label = "контр. (Micro)"
                if pair == "eur":
                    # M6E: тик 0.0001, стоимость $1.25
                    ticks = diff / 0.0001
                    tick_value = 1.25
                else:
                    # M6B: тик 0.0001, стоимость $0.625
                    ticks = diff / 0.0001
                    tick_value = 0.625
                x = r / (ticks * tick_value)
                
            # --- FUTURES STANDARD ---
            elif market == "futures_std":
                label = "контр. (Standard)"
                if pair == "eur":
                    # 6E: тик 0.00005, стоимость $6.25
                    ticks = diff / 0.00005
                    tick_value = 6.25
                else:
                    # 6B: тик 0.0001, стоимость $6.25
                    ticks = diff / 0.0001
                    tick_value = 6.25
                x = r / (ticks * tick_value)
            
            result_text.value = f"Результат: X = {round(x, 2):.2f} {label}"
            
        except (ValueError, TypeError):
            result_text.value = "Заполните все поля числами!"
            
        page.update()

    # Чтобы избежать багов обновления при кликах по дропдаунам,
    # расчет будет происходить строго по нажатию кнопки OK
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
                dropdown_pair,  
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

ft.run(main)

import flet as ft

def main(page: ft.Page):
    page.title = "calculator of risk"
    page.theme_mode = ft.ThemeMode.DARK
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.padding = 20

    # Выбор формулы
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
    
    # Выбор конкретного фьючерсного контракта
    dropdown_pair = ft.Dropdown(
        label="Выбор контракта",
        options=[
            ft.dropdown.Option("eur", "Euro (6E / M6E)"),
            ft.dropdown.Option("gbp", "GBP (6B / M6B)"),
        ],
        value="eur",
        width=300,
        visible=False,  # Скрыт по умолчанию
    )
    
    # Функция отслеживания смены формулы
    def formula_changed(e):
        if dropdown_formula.value == "forex":
            dropdown_pair.visible = False
        else:
            dropdown_pair.visible = True
        page.update()
        
    dropdown_formula.on_change = formula_changed
    
    # Поля ввода
    input_r = ft.TextField(label="Риск (r)", keyboard_type=ft.KeyboardType.NUMBER, width=300)
    input_e = ft.TextField(label="Вход (e)", keyboard_type=ft.KeyboardType.NUMBER, width=300)
    input_s = ft.TextField(label="Стоп (s)", keyboard_type=ft.KeyboardType.NUMBER, width=300)
    
    # Поле вывода результата
    result_text = ft.Text(value="Результат: X = 0.00", size=22, weight=ft.FontWeight.BOLD, color=ft.Colors.GREEN_ACCENT)

    # Логика расчета
    def calculate(e):
        try:
            r = float(input_r.value.replace(",", "."))
            entry = float(input_e.value.replace(",", "."))
            stop = float(input_s.value.replace(",", "."))
            
            diff = abs(entry - stop)
            
            if diff == 0:
                result_text.value = "Ошибка: Вход и Стоп равны!"
                result_text.color = ft.Colors.RED_ACCENT
                page.update()
                return

            # --- РАСЧЕТ ДЛЯ FOREX ---
            if dropdown_formula.value == "forex":
                x = r / (diff * 100000)
                label = "лотов"
            
            # --- РАСЧЕТ ДЛЯ MICRO FUTURES ---
            elif dropdown_formula.value == "futures_micro":
                label = "контр. (Micro)"
                if dropdown_pair.value == "eur":
                    # M6E: шаг 0.0001, стоимость $1.25
                    ticks = diff / 0.0001
                    tick_value = 1.25
                elif dropdown_pair.value == "gbp":
                    # M6B: шаг 0.0001, стоимость $1.25
                    ticks = diff / 0.0001
                    tick_value = 1.25
                x = r / (ticks * tick_value)
                
            # --- РАСЧЕТ ДЛЯ STANDARD FUTURES ---
            elif dropdown_formula.value == "futures_std":
                label = "контр. (Standard)"
                if dropdown_pair.value == "eur":
                    # 6E: шаг 0.00005, стоимость $6.25
                    ticks = diff / 0.00005
                    tick_value = 6.25
                elif dropdown_pair.value == "gbp":
                    # 6B: шаг 0.0001, стоимость $6.25
                    ticks = diff / 0.0001
                    tick_value = 6.25
                x = r / (ticks * tick_value)
            
            # Округление результатов до 2 знаков
            result_text.value = f"Результат: X = {round(x, 2):.2f} {label}"
            result_text.color = ft.Colors.GREEN_ACCENT
            
        except (ValueError, TypeError):
            result_text.value = "Заполните все поля числами!"
            result_text.color = ft.Colors.RED_ACCENT
            
        page.update()

    # Кнопка
    btn_ok = ft.ElevatedButton(
        text="OK",
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

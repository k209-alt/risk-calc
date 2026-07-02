import flet as ft

def main(page: ft.Page):
    page.title = "Calculator of Risk"
    page.theme_mode = ft.ThemeMode.DARK
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.padding = 20

    # Спецификации контрактов: (Стоимость шага, Размер шага)
    # Считаем через стандартный пункт 0.0001 для простоты ввода цен пользователем
    FUTURES_SPECS = {
        "futures_micro": {
            "eur": {"tick_value": 1.00, "tick_size": 0.0001},  # M6E
            "gbp": {"tick_value": 1.25, "tick_size": 0.0001},  # M6B
        },
        "futures_std": {
            "eur": {"tick_value": 12.50, "tick_size": 0.0001}, # 6E
            "gbp": {"tick_value": 12.50, "tick_size": 0.0001}, # 6B
        }
    }

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
        label="Выбор контракта",
        options=[
            ft.dropdown.Option("eur", "Euro (6E / M6E)"),
            ft.dropdown.Option("gbp", "GBP (6B / M6B)"),
        ],
        value="eur",
        width=300,
        visible=False,
    )
    
    def formula_changed(e):
        # Показываем выбор пары только если выбран фьючерс
        dropdown_pair.visible = dropdown_formula.value != "forex"
        page.update()
        
    dropdown_formula.on_change = formula_changed
    
    # Поля ввода
    input_r = ft.TextField(label="Риск ($)", keyboard_type=ft.KeyboardType.NUMBER, width=300)
    input_e = ft.TextField(label="Вход (Цена)", keyboard_type=ft.KeyboardType.NUMBER, width=300)
    input_s = ft.TextField(label="Стоп (Цена)", keyboard_type=ft.KeyboardType.NUMBER, width=300)
    
    result_text = ft.Text(value="Результат: X = 0.00", size=22, weight=ft.FontWeight.BOLD, color=ft.Colors.GREEN_ACCENT)

    def calculate(e):
        if not input_r.value or not input_e.value or not input_s.value:
            result_text.value = "Заполните все поля!"
            result_text.color = ft.Colors.RED_ACCENT
            page.update()
            return

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

            market = dropdown_formula.value
            pair = dropdown_pair.value

            if market == "forex":
                # Стандартная формула форекса (1 лот = 100,000 единиц)
                x = r / (diff * 100000)
                label = "лотов"
            else:
                # Извлекаем настройки конкретно для выбранного типа фьючерса и пары
                spec = FUTURES_SPECS[market][pair]
                
                ticks = diff / spec["tick_size"]
                x = r / (ticks * spec["tick_value"])
                
                label = "контр. (Micro)" if market == "futures_micro" else "контр. (Standard)"
            
            result_text.value = f"Результат: X = {round(x, 2):.2f} {label}"
            result_text.color = ft.Colors.GREEN_ACCENT
            
        except ValueError:
            result_text.value = "Используйте только числа!"
            result_text.color = ft.Colors.RED_ACCENT
            
        page.update()

    btn_ok = ft.ElevatedButton(
        text="Рассчитать объем",
        on_click=calculate,
        width=300,
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8))
    )

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

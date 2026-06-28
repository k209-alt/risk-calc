import flet as ft

def main(page: ft.Page):
    # Настройки окна/экрана
    page.title = "Risk Calculator"
    page.theme_mode = ft.ThemeMode.DARK  # Строгий темный дизайн
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.padding = 20

    # Поля ввода
    dropdown_formula = ft.Dropdown(
        label="Выбор формулы",
        options=[
            ft.dropdown.Option("forex", "Forex (x100000)"),
            ft.dropdown.Option("futures", "Futures (x10000 × 0.625)"),
        ],
        value="forex",
        width=300,
    )
    
    input_r = ft.TextField(label="Риск (r)", keyboard_type=ft.KeyboardType.NUMBER, width=300)
    input_e = ft.TextField(label="Вход (e)", keyboard_type=ft.KeyboardType.NUMBER, width=300)
    input_s = ft.TextField(label="Стоп (s)", keyboard_type=ft.KeyboardType.NUMBER, width=300)
    
    # Текст для вывода результата
    result_text = ft.Text(value="Результат: X = 0.00", size=24, weight=ft.FontWeight.BOLD, color=ft.Colors.GREEN_ACCENT)

    # Функция расчета
    def calculate(e):
        try:
            # Получаем значения и переводим в float
            r = float(input_r.value.replace(",", "."))
            entry = float(input_e.value.replace(",", "."))
            stop = float(input_s.value.replace(",", "."))
            
            # Модуль разницы |e - s|
            diff = abs(entry - stop)
            
            if diff == 0:
                result_text.value = "Ошибка: Вход и Стоп равны!"
                result_text.color = ft.Colors.RED_ACCENT
                page.update()
                return

            # Выбор формулы
            if dropdown_formula.value == "forex":
                # x = r ÷ ((|e-s|) × 100000)
                x = r / (diff * 100000)
            else:
                # x = r ÷ ((|e-s|) × 10000) × 0.625
                x = (r / (diff * 10000)) * 0.625
            
            # Округление до 0.01
            result_text.value = f"Результат: X = {round(x, 2):.2f}"
            result_text.color = ft.Colors.GREEN_ACCENT
            
        except ValueError:
            result_text.value = "Заполните все поля числами!"
            result_text.color = ft.Colors.RED_ACCENT
            
        page.update()

    # Кнопка ОК
    btn_ok = ft.ElevatedButton(
        text="OK",
        on_click=calculate,
        width=300,
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=8),
        )
    )

    # Добавляем элементы на экран (минималистичный B2B стиль)
    page.add(
        ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text("Калькулятор Риска", size=22, weight=ft.FontWeight.W_500),
                    ft.Divider(height=10, color=ft.Colors.TRANSPARENT),
                    dropdown_formula,
                    input_r,
                    input_e,
                    input_s,
                    ft.Divider(height=10, color=ft.Colors.TRANSPARENT),
                    btn_ok,
                    ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
                    result_text,
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            padding=24,
            border_radius=16,
            bgcolor=ft.Colors.SURFACE_VARIANT,
            elevation=2,
        )
    )

# Запуск приложения
ft.app(target=main)
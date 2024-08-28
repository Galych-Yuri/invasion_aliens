"""
settings. Кожного разу коли ми додаватимемо новий функціонал
простіше змінити певні налаштування ніж переписувати весь код
"""


class Settings:
    """Клас для збереження всіх налаштувань гри."""

    def __init__(self):
        """initialize game settings"""
        # Screen settings
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)

        # налаштування корабля
        self.ship_speed = 1.5

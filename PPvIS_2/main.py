from kivy import Config
Config.set("graphics", "resizable", "0")
Config.set("graphics", "width", "1000")
Config.set("graphics", "height", "600")
from kivymd.app import MDApp
from kivymd.uix.datatables import MDDataTable
from Controller.Vetscreen import VetScreenController
from Model.Vetscreen import VetScreenModel
from kivy.metrics import dp


class PassMVC(MDApp):
    date = ''

    def __init__(self):
        super().__init__()
        self.table = MDDataTable(
            pos_hint={'center_x': 0.5, 'center_y': 0.57},
            size_hint=(0.9, 0.8),
            use_pagination=True,
            elevation=2,
            rows_num=7,
            pagination_menu_height=240,
            background_color=(0, 1, 0, .10),
            column_data=[
                ("[color=#123487]Имя животного[/color]", dp(30)),
                ("[color=#123487]Дата рождения[/color]", dp(30)),
                ("[color=#123487]Дата последнего приема[/color]", dp(45)),
                ("[color=#123487]ФИО ветеринара[/color]", dp(40)),
                ("[color=#123487]Диагноз[/color]", dp(30)),
            ],
        )
        self.model = VetScreenModel(table=self.table)
        self.controller = VetScreenController(self.model)

    def build(self):
        return self.controller.get_screen()


PassMVC().run()

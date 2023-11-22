from kivy.uix.screenmanager import Screen
from kivymd.uix.relativelayout import MDRelativeLayout
from kivy.properties import StringProperty
from kivymd.uix.pickers import MDDatePicker
from kivymd.uix.menu import MDDropdownMenu


class RegistarScreen(Screen):
    def on_kv_post(self, base_widget):
        menu_items = [
            {
                "text": "Sim, na Esc. Sec. Ramada",
                "on_release": lambda x="Sim, na Esc. Sec. Ramada": self.set_item(x),
            },
            {
                "text": "Sim no Agrup. Vasco Santana",
                "on_release": lambda x="Sim no Agrup. Vasco Santana": self.set_item(x),
            },
            {
                "text": "Sim noutra escola",
                "on_release": lambda x="Sim noutra escola": self.set_item(x),
            },
            {
                "text": "Não",
                "on_release": lambda x="Não": self.set_item(x),
            },

        ]
        self.menu = MDDropdownMenu(
            caller=self.ids.drop_item,
            items=menu_items,
            position="center",
            width_mult=4,
        )

    def open_dropdown(self):
        self.menu.open()

    def set_item(self, text_item):
        self.ids.drop_item.set_item(text_item)
        self.menu.dismiss()


class ClickableTextFieldRound(MDRelativeLayout):
    text = StringProperty()
    hint_text = StringProperty()


class ClickableTextFieldRound2(MDRelativeLayout):
    text = StringProperty()
    hint_text = StringProperty()


class ClickableDateField(MDRelativeLayout):
    text = StringProperty()
    hint_text = StringProperty()

    def open_date_picker(self):
        date_dialog = MDDatePicker()
        date_dialog.bind(on_save=self.on_date_select)
        date_dialog.open()

    def on_date_select(self, instance, value, date_range):
        formated_date = value.strftime('%d/%m/%Y')
        self.text = formated_date

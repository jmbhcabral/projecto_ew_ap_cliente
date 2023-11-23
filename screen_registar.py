from kivy.uix.screenmanager import Screen
from kivymd.uix.relativelayout import MDRelativeLayout
from kivy.properties import StringProperty
from kivymd.uix.pickers import MDDatePicker
from kivymd.uix.menu import MDDropdownMenu
import requests


class RegistarScreen(Screen):
    def on_enter(self, *args):
        self.ids.nome_label.text = ""
        self.ids.apelido_label.text = ""
        self.ids.username_label.text = ""
        self.ids.email_label.text = ""
        self.ids.password_round.ids.password_label.text = ""
        self.ids.password2_round.ids.password2_label.text = ""
        self.ids.telemovel_label.text = ""
        self.ids.clickable_date.ids.data_nascimento_label.text = ""
        self.ids.drop_item.text = ""

    def menu_list(self):
        self.menu_items = [
            {
                "viewclass": "OneLineListItem",
                "text": "Sim, na Esc. Sec. Ramada",
                "on_release": lambda x="Sim, na Esc. Sec. Ramada": self.set_item(x),
            },
            {
                "viewclass": "OneLineListItem",
                "text": "Sim no Agrup. Vasco Santana",
                "on_release": lambda x="Sim no Agrup. Vasco Santana": self.set_item(x),
            },
            {
                "viewclass": "OneLineListItem",
                "text": "Sim noutra escola",
                "on_release": lambda x="Sim noutra escola": self.set_item(x),
            },
            {
                "viewclass": "OneLineListItem",
                "text": "Não",
                "on_release": lambda x="Não": self.set_item(x),
            },

        ]
        self.menu = MDDropdownMenu(
            caller=self.ids.drop_item,
            items=self.menu_items,
            position="center",
            width_mult=4,
        )

        self.menu.open()

    def set_item(self, text_item):
        self.ids.drop_item.text = text_item
        self.menu.dismiss()

    def register_user(self):
        nome = self.ids.nome_label.text
        apelido = self.ids.apelido_label.text
        username = self.ids.username_label.text
        email = self.ids.email_label.text
        password = self.ids.password_round.ids.password_label.text
        password2 = self.ids.password2_round.ids.password2_label.text
        telemovel = self.ids.telemovel_label.text
        data_nascimento = self.ids.clickable_date.ids.data_nascimento_label.text
        escola = self.ids.drop_item.text

        print('Nome: ', nome)
        print('Apelido: ', apelido)
        print('Username: ', username)
        print('Email: ', email)
        print('Password: ', password)
        print('Password2: ', password2)
        print('Telemovel: ', telemovel)
        print('Data de Nascimento: ', data_nascimento)
        print('Escola: ', escola)

        data = {
            'first_name': nome,
            'last_name': apelido,
            'username': username,
            'email': email,
            'password': password,
            # 'password2': password2,
            'perfil': {
                'telemovel': telemovel,
                'data_nascimento': data_nascimento,
                'estudante': escola
            }
        }
        print('Data: ', data)

        response = requests.post(
            'http://127.0.0.1:8000/users/api/v1/', json=data)

        if response:

            if response.status_code == 200:
                print('Utilizador registado com sucesso')
                self.manager.current = 'screen_login'

            else:
                try:
                    error_message = response.json()
                    print('Erro ao registar utilizador: ', error_message)
                except ValueError:
                    print('Erro ao registar utilizador: ', response.text)


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
        formated_date = value.strftime('%d-%m-%Y')
        self.text = formated_date

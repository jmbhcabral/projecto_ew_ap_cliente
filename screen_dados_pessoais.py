from kivy.uix.screenmanager import Screen
from utils.singleton import UserDataSingleton
from kivy.properties import StringProperty
from kivymd.uix.relativelayout import MDRelativeLayout
from kivymd.uix.pickers import MDDatePicker


class ScreenDadosPessoais(Screen):
    def on_enter(self):
        user_data_singleton = UserDataSingleton.get_instance()
        user_data = user_data_singleton.fetch_user_data()

        if user_data:
            self.update_ui_with_user_data(user_data)
        else:
            print('Nenhum dado do usuário encontrado!')

    def update_ui_with_user_data(self, user_data):
        first_name = user_data.get('first_name', 'N/A')
        last_name = user_data.get('last_name', 'N/A')
        username = user_data.get('username', 'N/A')
        email = user_data.get('email', 'N/A')
        telemovel = user_data['perfil'].get('telemovel', 'N/A')
        data_nascimento = user_data['perfil'].get('data_nascimento', 'N/A')

        self.ids.first_name_label.text = first_name
        self.ids.last_name_label.text = last_name
        self.ids.username_label.text = username
        self.ids.email_label.text = email
        self.ids.telemovel_label.text = telemovel
        self.ids.clickable_date.ids.data_nascimento_label.text = data_nascimento


class ClickableDateField(MDRelativeLayout):
    text = StringProperty()
    hint_text = StringProperty()

    def open_date_picker(self):
        date_dialog = MDDatePicker()
        date_dialog.bind(on_save=self.on_date_select)
        date_dialog.open()

    def on_date_select(self, instance, value, date_range):
        formated_date = value.strftime('%Y-%m-%d')
        self.text = formated_date

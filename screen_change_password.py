from kivy.uix.screenmanager import Screen
from kivymd.uix.snackbar import Snackbar
from utils.singleton import UserDataSingleton
import requests
import json


class ScreenChangePassword(Screen):

    def reset_field(self, field_id, default_helper_text):
        field = self.ids.get(field_id)
        if field:
            field.error = False
            field.helper_text = default_helper_text

    def on_enter(self, *args):
        self.ids.password_label.text = ''
        self.ids.password2_label.text = ''

    def toggle_password(self):
        password_label = self.ids.password_label
        toggle_icon = self.ids.toggle_icon

        password_label.password = not password_label.password

        if password_label.password:
            toggle_icon.icon = "eye-off"
        else:
            toggle_icon.icon = "eye"

    def toggle_password_confirmation(self):
        password2_label = self.ids.password2_label
        toggle_icon2 = self.ids.toggle_icon2

        password2_label.password = not password2_label.password

        if password2_label.password:
            toggle_icon2.icon = "eye-off"
        else:
            toggle_icon2.icon = "eye"

    def enviar_dados_servidor(self, user_id, data_actualizada):
        url = f'http://127.0.0.1:8000/users/api/v1/{user_id}/'
        headers = {'Content-Type': 'application/json'}
        data_json = json.dumps(data_actualizada)
        response = requests.patch(url, headers=headers, data=data_json)
        print('Data enviada para o servidor: ', data_json)
        if response.status_code == 200:
            print('Password alterada com sucesso')
            Snackbar(text='Password alterada com sucesso.').open()
            self.ids.password_label.error = False
            self.ids.password2_label.error = False
            self.manager.current = 'screen_utilizador_home'
        else:
            print('Erro ao alterar a password')
            Snackbar(text='Erro ao alterar a password.').open()

    def update_password(self):
        print("update_password")
        erro = False
        if not self.validar_password():
            return True
        if erro:
            return True

        user_data_singleton = UserDataSingleton.get_instance()
        user_data = user_data_singleton.fetch_user_data()

        if user_data:
            password = self.ids.password_label.text

            data = {
                'password': password
            }
            print('data', data)
            if password == '':
                Snackbar(text='Não alterou a Password.').open()
                return
            else:
                Snackbar(text='Password alterada com sucesso.').open()
                user_id = user_data.get('id', None)
                self.enviar_dados_servidor(user_id, data)

        self.manager.current = 'screen_utilizador_home'

    def validar_password(self):
        password_label = self.ids.password_label
        password2_label = self.ids.password2_label
        password = password_label.text
        password2 = password2_label.text
        if len(password) < 8:
            password_label.error = True
            password_label.helper_text = 'Deve ter pelo menos 8 caracteres'
            return False
        elif password != password2:
            password2_label.error = True
            password2_label.helper_text = 'Password não coincide'
            return False
        else:
            return True

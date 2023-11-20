# from kivy.uix.floatlayout import FloatLayout
import requests
import time
from requests.exceptions import ConnectionError, Timeout
from kivy.uix.screenmanager import Screen


class LoginScreen(Screen):
    def toggle_password(self):
        password_field = self.ids.password_field
        toggle_icon = self.ids.toggle_icon

        password_field.password = not password_field.password

        if password_field.password:
            toggle_icon.icon = "eye-off"
        else:
            toggle_icon.icon = "eye"

    def show_error_message(self, message):
        self.ids.error_label.text = message

    def on_username_or_password_change(self):
        self.show_error_message("")

    def login(self):
        self.show_error_message("")
        max_retries = 3
        for attempt in range(max_retries):
            try:
                url = "http://127.0.0.1:8000/api/token/"
                data = {
                    'username': self.ids.username_field.text,
                    'password': self.ids.password_field.text
                }

                response = requests.post(url, data=data)
                if response.status_code == 200:
                    data = response.json()
                    self.token = data.get('access')
                    self.user_id = data.get('user_id')

                    self.manager.current = 'screen_utilizador_home'

                    break
                if response.status_code == 400:
                    self.show_error_message(
                        "Username ou password incorretos.")
                    break

                if response.status_code == 401:
                    self.show_error_message(
                        "Username ou password incorretos.")
                    break

            except (ConnectionError, Timeout):
                if attempt == max_retries - 1:
                    self.show_error_message(
                        "Não foi possível conectar ao servidor.")
                time.sleep(2)

            except Exception as e:
                # Captura outras exceções genéricas
                print(f"Erro desconhecido: {e}")
                break

    def fetch_user_data(self, token):
        url = "http://127.0.0.1:8000/users/api/v1/"
        headers = {'Authorization': f'Bearer {token}'}
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            user_data = response.json()
            return user_data
        else:
            self.show_error_message(
                "Não foi possível obter os dados do utilizador.")
            return None

    def on_enter(self, *args):
        pass

    def logout(self):
        self.token = None
        self.manager.current = 'screen_login'

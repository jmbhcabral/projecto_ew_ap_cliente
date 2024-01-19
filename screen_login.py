# from kivy.uix.floatlayout import FloatLayout
import requests
import time
from utils.singleton import UserDataSingleton
from requests.exceptions import ConnectionError, Timeout
from kivy.uix.screenmanager import Screen
from kivy.app import App


class LoginScreen(Screen):
    def on_pre_enter(self, *args):
        self.ids.username_field.text = ""
        self.ids.password_field.text = ""
        self.ids.error_label.text = ""

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
                    token = data.get('access')
                    refresh_token = data.get('refresh')
                    user_id = data.get('user_id')

                    # configurar o singleton com o token e o user_id
                    user_data_singleton = UserDataSingleton.get_instance()
                    user_data_singleton.set_user_credentials(
                        token, refresh_token, user_id)

                    app_instance = App.get_running_app()
                    if app_instance:
                        print("Login: Obtendo a instância do aplicativo.")
                        app_instance.set_logged_in(True)
                    else:
                        print(
                            "Não foi possível obter a instância do aplicativo."
                        )

                    self.manager.current = 'screen_interface_utilizador'

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

    # def fetch_user_data(self, token):
    #     url = "http://127.0.0.1:8000/users/api/v1/"
    #     headers = {'Authorization': f'Bearer {token}'}
    #     response = requests.get(url, headers=headers)
    #     if response.status_code == 200:
    #         user_data = response.json()
    #         return user_data
    #     else:
    #         self.show_error_message(
    #             "Não foi possível obter os dados do utilizador.")
    #         return None

    def on_enter(self, *args):
        pass

    def logout(self):
        print("Iniciando o processo de logout.")
        self.manager.current = 'screen_clientes'

        # Limpar as credenciais do usuário
        user_data_singleton = UserDataSingleton.get_instance()
        user_data_singleton.clear_user_credentials()

        # Atualizar o ícone de login
        app_instance = App.get_running_app()
        if app_instance:
            print("Logout: Obtendo a instância do aplicativo.")
            # Isso atualizará o ícone para login
            app_instance.set_logged_in(False)
        else:
            print("Não foi possível obter a instância do aplicativo.")

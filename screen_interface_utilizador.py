from kivy.uix.screenmanager import Screen
from utils.singleton import UserDataSingleton
from kivy.properties import ObjectProperty, StringProperty, NumericProperty
from storage_manager import StorageManager
from kivy.network.urlrequest import UrlRequest


class ScreenInterfaceUtilizador(Screen):
    error_str = StringProperty('')

    def on_enter(self, *args):
        user_data_singleton = UserDataSingleton.get_instance()
        user_data = user_data_singleton.fetch_user_data()

        if user_data is None:
            return
        else:
            pontos_fidelidade = StorageManager()\
                .load('dados_pontos_fidelidade')
            print('pontos_fidelidade', pontos_fidelidade)
            if pontos_fidelidade is not None:
                print('pontos_fidelidade is not None')
                self.update_ui_with_data(pontos_fidelidade)
                user_id = user_data['id']
                self.get_pontos_fidelidade(user_id)
            else:
                print('pontos_fidelidade is None')
                user_id = user_data['id']
                self.get_pontos_fidelidade(user_id)

    def get_pontos_fidelidade(self, user_id, *args, **kwargs):
        user_data_singleton = UserDataSingleton.get_instance()
        headers = user_data_singleton._get_authorization_header()
        print('headers', headers)
        url = f'http://127.0.0.1:8000/fidelidade/api/v1/pontos/{user_id}/'

        def on_success(req, result):
            print('on_sucess: ', result)
            self.error_str = ''
            self.process_data(result)

        def on_failure(req, result):
            self.on_server_error('Falha no servidor: ' + str(req.resp_status))

        def on_error(req, error):
            self.on_server_error('Erro: ' + str(error))

        req = UrlRequest(url, on_success=on_success, on_error=on_error,
                         on_failure=on_failure, req_headers=headers)
        print('req', req)

    def on_server_error(self, error):
        self.error_str = "Error: " + error

    def process_data(self, data):
        print('Data: ------------', data)
        StorageManager().save_data('dados_pontos_fidelidade', data)
        self.update_ui_with_data(data)

    def update_ui_with_data(self, data):
        self.ids.pontos_label.text = f"{int(data['saldo_pontos'])}"
        print('pontos_label', self.ids.pontos_label.text)

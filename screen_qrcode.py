from kivy.uix.screenmanager import Screen
from utils.singleton import UserDataSingleton


class ScreenQRCode(Screen):
    def on_enter(self):
        user_data_singleton = UserDataSingleton.get_instance()
        user_data = user_data_singleton.fetch_user_data()

        if user_data:
            self.update_ui_with_user_data(user_data)
        else:
            print('Nenhum dado do usuário encontrado!')

    def update_ui_with_user_data(self, user_data):
        # Extraia os dados do usuário
        qrcode_url = user_data['perfil'].get('qrcode_url', '')

        # Atualize a interface do usuário com esses dados
        self.ids.image_qrcode.source = qrcode_url

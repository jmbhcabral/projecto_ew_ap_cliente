from kivymd.app import MDApp
# from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import (
    ObjectProperty, StringProperty, NumericProperty, BooleanProperty)
from kivy.uix.floatlayout import FloatLayout
from http_client import HttpClient
from storage_manager import StorageManager
from kivy.uix.behaviors import CoverBehavior
from kivy.uix.image import AsyncImage
from models import Produto
from screen_login import LoginScreen
from screen_utilizador_home import UtilizadorHomeScreen
from screen_registar import RegistarScreen
from screen_inicio import ScreenInicio
from screen_acerca_de import ScreenAcercaDe
from screen_programa_fidelidade import ScreenProgramaFidelidade
from screen_suporte import ScreenSuporte
from screen_qrcode import ScreenQRCode
from screen_dados_pessoais import ScreenDadosPessoais
from screen_change_password import ScreenChangePassword
from screen_ementa_utilizador import ScreenEmentaUtilizador
import time
from utils.singleton import UserDataSingleton


class Content(BoxLayout):
    manager = ObjectProperty()
    nav_drawer = ObjectProperty()

    def logout(self):
        login_screen = self.manager.get_screen('screen_clientes')
        login_screen.logout()


class MenuScreen(ScreenManager):
    pass


class ProdutoWidget(BoxLayout):
    nome = StringProperty()
    descricao_curta = StringProperty()
    imagem = StringProperty()
    preco_1 = NumericProperty()
    vegetariano = BooleanProperty()


class MainWidget(FloatLayout):
    recycleView = ObjectProperty(None)
    error_str = StringProperty('')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        HttpClient().get_produtos(self.on_server_data, self.on_server_error)

    def on_kv_post(self, base_widget):
        produtos_list = StorageManager().load('produtos')
        if produtos_list:
            self.recycleView.data = [{
                'nome': produto['nome'],
                'descricao_curta': produto['descricao_curta'],
                'imagem': produto['imagem'],
                'preco_1': produto['preco_1'],
                # Use .get para evitar KeyError
                'vegetariano': produto.get('vegetariano', False)
            } for produto in produtos_list]

    def on_server_data(self, produtos_list):
        self.recycleView.data = produtos_list
        StorageManager().save_data('produtos', produtos_list)

    def on_server_error(self, error):
        print('Erro: ' + error)
        self.error_str = "Error: " + error


class ExtremeWayApp(MDApp):
    is_logged_in = BooleanProperty(False)  # Rastreia o estado de login
    login_icon = StringProperty("login-variant")

    def set_logged_in(self, logged_in):
        self.is_logged_in = logged_in
        self.login_icon = "logout-variant" if logged_in else "login-variant"

    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Amber"

        # Tenta autenticar o usuário automaticamente
        self.auto_login()

        return MenuScreen()

    def auto_login(self):
        user_data = UserDataSingleton.get_instance().load_user_data()
        if user_data:
            current_time = int(time.time())
            token_expiration = user_data.get('token_expiration', 0)

            if current_time < token_expiration:
                # Token ainda valido, autenticar o usuário automaticamente
                self.set_logged_in(True)
            elif 'refresh_token' in user_data:
                # Tenta renovar o token de acesso
                if UserDataSingleton.get_instance().refresh_token(user_data):
                    self.set_logged_in(True)
                else:
                    self.set_logged_in(False)
            else:
                self.set_logged_in(False)

    def toggle_login(self):
        if self.is_logged_in:
            login_screen = self.root.ids.screen_manager.get_screen(
                'screen_clientes')
            login_screen.logout()
        else:
            # Lógica para mostrar a tela de login
            self.root.ids.screen_manager.current = 'screen_clientes'


if __name__ == '__main__':
    ExtremeWayApp().run()

from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.menu import MDDropdownMenu
from kivy.uix.screenmanager import ScreenManager
from storage_manager import StorageManager
from kivy.uix.image import AsyncImage
from kivy.properties import ObjectProperty, BooleanProperty, StringProperty
from screen_inicio import ScreenInicio
from screen_login import LoginScreen
from navigation_screen_manager import NavigationScreenManager
from screen_acerca_de import ScreenAcercaDe
from screen_programa_fidelidade import ScreenProgramaFidelidade
from screen_suporte import ScreenSuporte
from screen_interface_utilizador import ScreenInterfaceUtilizador
from screen_utilizador_home import UtilizadorHomeScreen
from screen_change_password import ScreenChangePassword
from screen_dados_pessoais import ScreenDadosPessoais
from screen_ementa_utilizador import ScreenEmentaUtilizador
from screen_movimentos_pontos import ScreenMovimentosPontos
from screen_pontos_oferta import ScreenPontosOferta
from screen_qrcode import ScreenQRCode
from screen_registar import RegistarScreen
import time


from utils.singleton import UserDataSingleton


class MainScreen(ScreenManager):
    nav_manager = ObjectProperty(None)


class ExtremeWayApp(MDApp):
    is_logged_in = BooleanProperty(False)  # Rastreia o estado de login
    login_icon = StringProperty("login-variant")  # Ícone de login
    menu = ObjectProperty()

    def set_logged_in(self, logged_in):
        self.is_logged_in = logged_in
        print("Logged in: {}".format(logged_in))
        self.login_icon = "logout-variant" if logged_in else "login-variant"
        self.build_menu()

    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Amber"

        # Tenta autenticar o usuário automaticamente
        self.auto_login()

        self.main_screen = MainScreen()
        # main_screen.ids.screen_manager.push("screen_inicio")
        return self.main_screen

    def build_menu(self):
        if self.is_logged_in:
            menu_items = [
                {"text": "Início", "viewclass": "OneLineListItem",
                    "on_release": lambda x='screen_inicio': self.menu_callback(x)},
                {"text": "Área Clientes", "viewclass": "OneLineListItem",
                    "on_release": lambda x='screen_interface_utilizador': self.menu_callback(x)},
                {"text": "Acerca de", "viewclass": "OneLineListItem",
                    "on_release": lambda x='screen_acerca_de': self.menu_callback(x)},
                {"text": "Programa Fidelidade", "viewclass": "OneLineListItem",
                    "on_release": lambda x='screen_programa_fidelidade': self.menu_callback(x)}
            ]
        else:
            menu_items = [
                {"text": "Início", "viewclass": "OneLineListItem",
                    "on_release": lambda x='screen_inicio': self.menu_callback(x)},
                {"text": "Clientes", "viewclass": "OneLineListItem",
                    "on_release": lambda x='screen_clientes': self.menu_callback(x)},
                {"text": "Acerca de", "viewclass": "OneLineListItem",
                    "on_release": lambda x='screen_acerca_de': self.menu_callback(x)},
                {"text": "Programa Fidelidade", "viewclass": "OneLineListItem",
                    "on_release": lambda x='screen_programa_fidelidade': self.menu_callback(x)}
            ]
        self.menu = MDDropdownMenu(
            items=menu_items,
            width_mult=4
        )

    def on_start(self):

        self.build_menu()

        # Define o screen inicial com base no estado de login
        if self.is_logged_in:
            self.root.ids\
                .screen_manager.current = 'screen_interface_utilizador'
        else:
            self.root.ids.screen_manager.current = 'screen_inicio'

    def open_menu(self, button):
        self.menu.caller = button
        self.menu.open()

    def menu_callback(self, screen_name):
        self.main_screen.ids.screen_manager.push(screen_name)
        self.menu.dismiss()

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
            self.logout_user()
        else:
            # Lógica para mostrar a tela de login
            self.root.ids.screen_manager.current = 'screen_clientes'

    def redirect_to_screen(self, screen_name):
        if self.is_logged_in:
            self.main_screen.ids.screen_manager.push(screen_name)
        else:
            self.root.ids.screen_manager.current = 'screen_clientes'

    def logout_user(self):
        # acessando o screen_manager e chamando o método logout
        navigation_manager = self.root.ids.screen_manager
        navigation_manager.logout()


if __name__ == '__main__':
    ExtremeWayApp().run()

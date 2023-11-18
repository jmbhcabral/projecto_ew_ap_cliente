from kivymd.app import MDApp
from kivy.lang import Builder
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


class Content(BoxLayout):
    manager = ObjectProperty()
    nav_drawer = ObjectProperty()


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


class LoginScreen(FloatLayout):

    def toggle_password(self):
        password_field = self.ids.password_field
        toggle_icon = self.ids.toggle_icon

        password_field.password = not password_field.password

        if password_field.password:
            toggle_icon.icon = "eye-off"
        else:
            toggle_icon.icon = "eye"


class MainApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Amber"
        Builder.load_file('ExtremeWay.kv')
        return MenuScreen()


if __name__ == '__main__':
    MainApp().run()

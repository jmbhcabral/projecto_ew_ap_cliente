from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import (
    ObjectProperty, StringProperty, NumericProperty, BooleanProperty
)
from models import Produto
from kivy.uix.behaviors import CoverBehavior  # usado em ExtremeWay.kv
from http_client import HttpClient
from storage_manager import StorageManager


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

    def on_parent(self, widget, parent):
        produtos_list = StorageManager().load('produtos')
        if produtos_list:
            self.recycleView.data = produtos_list

    def on_server_data(self, produtos_list):
        self.recycleView.data = produtos_list
        StorageManager().save_data('produtos', produtos_list)

    def on_server_error(self, error):
        print('Erro: ' + error)
        self.error_str = "Error: " + error


class ExtremeWayApp(App):
    pass


ExtremeWayApp().run()

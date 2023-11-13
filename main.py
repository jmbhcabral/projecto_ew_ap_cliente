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
from kivy.uix.image import AsyncImage


class ProdutoWidget(BoxLayout):
    nome = StringProperty()
    descricao_curta = StringProperty()
    imagem = StringProperty()
    preco_1 = NumericProperty()
    vegetariano = BooleanProperty()

    # def on_imagem(self, instance, value):
    #     print("URL da imagem para", self.nome, ":", value)


class MainWidget(FloatLayout):
    recycleView = ObjectProperty(None)
    error_str = StringProperty('')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        HttpClient().get_produtos(self.on_server_data, self.on_server_error)

    def on_parent(self, widget, parent):
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


class ExtremeWayApp(App):
    pass


ExtremeWayApp().run()

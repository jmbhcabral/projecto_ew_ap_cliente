from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import (
    ObjectProperty, StringProperty, NumericProperty, BooleanProperty
)
from models import Produto
from kivy.uix.behaviors import CoverBehavior  # usado em ExtremeWay.kv
from http_client import HttpClient


class ProdutoWidget(BoxLayout):
    nome = StringProperty()
    descricao_curta = StringProperty()
    preco_1 = NumericProperty()
    vegetariano = BooleanProperty()


class MainWidget(FloatLayout):
    recycleView = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # self.produtos = [
        #     Produto("Hamburguer", "Pão, carne e queijo", 15.0, False),
        #     Produto("X-Burguer", "Pão, carne, queijo e salada", 18.0, False),
        #     Produto(
        #         "X-Salada", "Pão, carne, queijo, salada e maionese", 20.0,
        #         False
        #     ),
        #     Produto("X-Veg", "Pão, queijo, salada e maionese", 20.0, True),
        # ]

        HttpClient().get_produtos(self.on_server_data)

    # def on_parent(self, widget, parent):
    #     self.recycleView.data = [produto.get_dictionary()
    #                              for produto in self.produtos]
    def on_server_data(self, produtos_list):
        data = [{'nome': produto['nome'],
                 'descricao_curta': produto['descricao_curta'],
                 'preco_1': produto['preco_1'],
                 } for produto in produtos_list]
        self.recycleView.data = data


class ExtremeWayApp(App):
    pass


ExtremeWayApp().run()

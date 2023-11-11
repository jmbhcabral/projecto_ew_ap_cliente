from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import (
    ObjectProperty, StringProperty, NumericProperty, BooleanProperty
)
from models import Produto
from kivy.uix.behaviors import CoverBehavior  # usado em ExtremeWay.kv


class ProdutoWidget(BoxLayout):
    nome = StringProperty()
    ingredientes = StringProperty()
    preco = NumericProperty()
    vegetariano = BooleanProperty()


class MainWidget(FloatLayout):
    recycleView = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.produtos = [
            Produto("Hamburguer", "Pão, carne e queijo", 15.0, False),
            Produto("X-Burguer", "Pão, carne, queijo e salada", 18.0, False),
            Produto(
                "X-Salada", "Pão, carne, queijo, salada e maionese", 20.0,
                False
            ),
            Produto("X-Veg", "Pão, queijo, salada e maionese", 20.0, True),
        ]

    def on_parent(self, widget, parent):
        self.recycleView.data = [produto.get_dictionary()
                                 for produto in self.produtos]


class ExtremeWayApp(App):
    pass


ExtremeWayApp().run()

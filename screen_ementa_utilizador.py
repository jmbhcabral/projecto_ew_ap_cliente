from kivy.uix.screenmanager import Screen
from utils.singleton import UserDataSingleton
from kivy.properties import ObjectProperty, StringProperty, NumericProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.network.urlrequest import UrlRequest
from storage_manager import StorageManager
from kivy.uix.recycleview import RecycleView


class ProdutoEmentaWidget(BoxLayout):
    nome = StringProperty()
    descricao_curta = StringProperty()
    imagem = StringProperty()
    preco = StringProperty()


class ScreenEmentaUtilizador(Screen):
    recycleView = ObjectProperty(None)
    error_str = StringProperty('')

    def on_enter(self, *args):
        user_data_singleton = UserDataSingleton.get_instance()
        user_data = user_data_singleton.fetch_user_data()

        if user_data is None:
            return
        else:
            ementa = StorageManager().load('dados_ementa')
            if ementa is not None:
                self.update_ui_with_data(ementa)
                user_id = user_data['id']
                self.get_ementa(user_id)
            else:
                user_id = user_data['id']
                self.get_ementa(user_id)

    def get_ementa(self, user_id, *args, **kwargs):
        user_data_singleton = UserDataSingleton.get_instance()
        headers = user_data_singleton._get_authorization_header()

        url = f'http://127.0.0.1:8000/ementa/api/v1/user/{user_id}/'

        def on_success(req, result):

            self.error_str = ''
            self.process_data(result)

        def on_failure(req, result):
            self.on_server_error('Falha no servidor: ' + str(req.resp_status))

        def on_error(req, error):
            self.on_server_error('Erro: ' + str(error))

        req = UrlRequest(url, on_success=on_success, on_error=on_error,
                         on_failure=on_failure, req_headers=headers)

    def on_server_error(self, error):
        self.error_str = "Error: " + error

    def process_data(self, result):
        # Supondo que result seja um dicionário ou lista de dicionários com os
        # dados desejados
        print('Result: ', result)
        StorageManager().save_data('dados_ementa', result)
        self.update_ui_with_data(result)

    def update_ui_with_data(self, data):
        if not data or not isinstance(data, list):

            self.error_str = 'Formato de dados invalido'
            return

        # Atualize a UI com os dados
        self.recycleView.data = []
        for menu in data:
            nome_campo_preco = menu.get(
                'nome_campo_preco_selecionado', 'preco_1')
            for categoria in menu['categorias']:
                for subcategoria in categoria['subcategorias']:
                    for produto in subcategoria['produtos']:
                        preco = produto.get(nome_campo_preco, '0.00')
                        if preco is None:
                            preco = '0.00'
                        self.recycleView.data.append({
                            'nome': produto['nome'],
                            'descricao_curta': produto['descricao_curta'],
                            'imagem': produto['imagem'],
                            'preco': f"{float(preco):.2f}"
                        })

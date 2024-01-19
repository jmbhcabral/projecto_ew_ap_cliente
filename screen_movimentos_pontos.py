from kivy.uix.screenmanager import Screen
from utils.singleton import UserDataSingleton
from storage_manager import StorageManager
from kivy.network.urlrequest import UrlRequest
from datetime import datetime
from kivymd.uix.label import MDLabel


class ScreenMovimentosPontos(Screen):
    def on_enter(self, *args):
        # Adicionar titulos das colunas
        self.add_column_titles()

        user_data_singleton = UserDataSingleton.get_instance()
        user_data = user_data_singleton.fetch_user_data()

        if user_data is None:
            return
        else:
            movimentos = StorageManager().load('dados_movimentos')
            if movimentos is not None:
                self.update_ui_with_data(movimentos)
                user_id = user_data['id']
                self.get_movimentos(user_id)
            else:
                user_id = user_data['id']
                self.get_movimentos(user_id)

    def add_column_titles(self):
        if len(self.ids.grid.children) <= 3:
            self.ids.grid.add_widget(MDLabel(text='Dia'))
            self.ids.grid.add_widget(MDLabel(text='Operação'))
            self.ids.grid.add_widget(MDLabel(text='Pontos'))

    def get_movimentos(self, user_id, *args, **kwargs):
        user_data_singleton = UserDataSingleton.get_instance()
        headers = user_data_singleton._get_authorization_header()

        url = f'http://127.0.0.1:8000/fidelidade/api/v1/pontos/{user_id}/'

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

    def process_data(self, data):
        StorageManager().save_data('dados_movimentos', data)
        self.update_ui_with_data(data)

    def update_ui_with_data(self, data):
        # Saldo de pontos
        self.ids.saldo_pontos.text = str(int(data['saldo_pontos']))
        for i in range(len(self.ids.grid.children) - 3):
            self.ids.grid.remove_widget(self.ids.grid.children[0])
        # Preparar e ordenar os dados
        movimentos = []

        for compra in data['detalhes_compras']:
            movimentos.append({
                'data': datetime.strptime(compra['criado_em'], "%Y-%m-%dT%H:%M:%S.%fZ"),
                'tipo': 'compra',
                'pontos': int(compra['pontos_adicionados']),
                'cor': (0, 1, 0, 1)  # Verde
            })

        for oferta in data['detalhes_ofertas']:
            movimentos.append({
                'data': datetime.strptime(oferta['criado_em'], "%Y-%m-%dT%H:%M:%S.%fZ"),
                'tipo': 'oferta',
                'pontos': int(oferta['pontos_gastos']),
                'cor': (1, 0, 0, 1)  # Vermelho
            })

        # Ordenar os movimentos por data
        movimentos.sort(key=lambda m: m['data'], reverse=True)

        # Adicionar á interface
        for movimento in movimentos:
            cor = movimento['cor']
            # Adicionar data

            label_data = MDLabel(
                text=movimento['data'].strftime("%d-%m-%y"),
                halign='left',
                theme_text_color='Custom',
                text_color=cor,
            )
            self.ids.grid.add_widget(label_data)

            # Adicionar tipo de operação com cor
            label_tipo = MDLabel(
                text=movimento['tipo'],
                halign='left',
                theme_text_color='Custom',
                text_color=cor,
            )

            self.ids.grid.add_widget(label_tipo)

            # Adicionar pontos

            label_pontos = MDLabel(
                text=str(movimento['pontos']),
                halign='right',
                text_size=(self.ids.grid.width / 3, None),
                theme_text_color='Custom',
                text_color=cor,
            )
            self.ids.grid.add_widget(label_pontos)

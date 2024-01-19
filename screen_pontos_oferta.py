from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty
from utils.singleton import UserDataSingleton
from kivy.network.urlrequest import UrlRequest
from storage_manager import StorageManager
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.accordion import Accordion, AccordionItem
from kivy.uix.label import Label


class ScreenPontosOferta(Screen):
    error_str = StringProperty('')

    def on_enter(self, *args):
        user_data_singleton = UserDataSingleton.get_instance()
        user_data = user_data_singleton.fetch_user_data()
        print('user_data', user_data)
        if user_data is None:
            return
        else:
            pontos_oferta = StorageManager().load('dados_pontos_oferta')
            print('pontos_oferta', pontos_oferta)
            if pontos_oferta is not None:
                self.update_ui_with_data(pontos_oferta)
                user_id = user_data['id']
                self.get_pontos_oferta(user_id)
            else:
                user_id = user_data['id']
                self.get_pontos_oferta(user_id)

    def get_pontos_oferta(self, user_id, *args, **kwargs):
        user_data_singleton = UserDataSingleton.get_instance()
        headers = user_data_singleton._get_authorization_header()

        url = f'http://127.0.0.1:8000/fidelidade/api/v1/produtos/{user_id}/'

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
        StorageManager().save_data('dados_pontos_oferta', data)
        self.update_ui_with_data(data)

    def update_ui_with_data(self, data):
        print('data', data)
        # Criação do accordion
        tipo_fidelidade = data['tipo_fidelidade']
        self.ids.tipo_fidelidade.text = tipo_fidelidade

        main_box = BoxLayout(orientation='vertical', size_hint_y=None)
        main_box.bind(minimum_height=main_box.setter('height'))

        for categoria in data['categorias']:
            cat_label = Label(
                text=categoria['categoria'],
                size_hint_y=None,
                height=30,
                bold=True,
                font_size=22,
                halign='left',
                valign='middle'
            )
            cat_label.bind(size=cat_label.setter('text_size'))
            main_box.add_widget(cat_label)

            for subcategoria in categoria['subcategorias']:
                subcat_label = Label(
                    text=subcategoria['subcategoria'],
                    size_hint_y=None,
                    height=30,
                    bold=True,
                    font_size=20,
                    halign='left',
                    valign='middle'
                )
                subcat_label.bind(size=subcat_label.setter('text_size'))
                main_box.add_widget(subcat_label)

                for produto in subcategoria['produtos']:
                    prod_box = BoxLayout(
                        orientation='horizontal',
                        size_hint_y=None,
                        height=30,

                    )

                    prod_label_nome = Label(
                        text=f"{produto['nome_produto']} ",
                        size_hint=(0.7, 1),
                        font_size=16,
                        halign='left',
                        valign='middle'
                    )
                    prod_label_nome.bind(
                        size=prod_label_nome.setter('text_size')
                    )
                    prod_label_pontos = Label(
                        text=f"Pts: {produto['pontos_para_oferta']}",
                        size_hint=(0.3, 1),
                        font_size=16,
                        halign='right',
                        valign='middle'
                    )
                    prod_label_pontos.bind(
                        size=prod_label_pontos.setter('text_size')
                    )
                    prod_box.add_widget(prod_label_nome)
                    prod_box.add_widget(prod_label_pontos)

                    main_box.add_widget(prod_box)
        # Limpe o layout atual e adicione o accordion
        self.ids.container_layout.clear_widgets()
        self.ids.container_layout.add_widget(main_box)

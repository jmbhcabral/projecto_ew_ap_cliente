from kivy.uix.screenmanager import Screen
from utils.singleton import UserDataSingleton
from kivy.properties import StringProperty
from kivymd.uix.relativelayout import MDRelativeLayout
from kivymd.uix.pickers import MDDatePicker
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.snackbar import Snackbar
import requests
import json


class ScreenDadosPessoais(Screen):
    def on_enter(self):
        user_data_singleton = UserDataSingleton.get_instance()
        user_data = user_data_singleton.fetch_user_data()

        if user_data:
            self.update_ui_with_user_data(user_data)
        else:
            print('Nenhum dado do usuário encontrado!')

    def update_ui_with_user_data(self, user_data):
        first_name = user_data.get('first_name', 'N/A')
        last_name = user_data.get('last_name', 'N/A')
        username = user_data.get('username', 'N/A')
        email = user_data.get('email', 'N/A')
        telemovel = user_data['perfil'].get('telemovel', 'N/A')
        data_nascimento = user_data['perfil'].get('data_nascimento', 'N/A')
        escola = user_data['perfil'].get('estudante', 'N/A')

        self.ids.first_name_label.text = first_name
        self.ids.last_name_label.text = last_name
        self.ids.username_label.text = username
        self.ids.email_label.text = email
        self.ids.telemovel_label.text = telemovel
        self.ids.clickable_date.ids.data_nascimento_label.text = data_nascimento
        self.ids.estudante_label.text = escola

    def menu_list(self):
        self.menu_items = [
            {
                "viewclass": "OneLineListItem",
                "text": "Sim, na Esc. Sec. Ramada",
                "on_release": lambda x="Sim, na Esc. Sec. Ramada": self.set_item(x),
            },
            {
                "viewclass": "OneLineListItem",
                "text": "Sim, no Agrup. Vasco Santana",
                "on_release": lambda x="Sim, no Agrup. Vasco Santana": self.set_item(x),
            },
            {
                "viewclass": "OneLineListItem",
                "text": "Sim, noutra escola",
                "on_release": lambda x="Sim, noutra escola": self.set_item(x),
            },
            {
                "viewclass": "OneLineListItem",
                "text": "Não",
                "on_release": lambda x="Não": self.set_item(x),
            },

        ]
        self.menu = MDDropdownMenu(
            caller=self.ids.estudante_label,
            items=self.menu_items,
            position="center",
            width_mult=4,
        )

        self.menu.open()

    def set_item(self, text_item):
        self.ids.estudante_label.text = text_item
        self.menu.dismiss()

    def enviar_dados_servidor(self, user_id, data_atualizada):
        print('Enviando dados para o servidor...')
        print('User id: ', user_id)
        print('Data atualizada: ', data_atualizada)

        url = f'http://127.0.0.1:8000/users/api/v1/{user_id}/'
        headers = {'Content-Type': 'application/json'}
        data_json = json.dumps(data_atualizada)
        response = requests.patch(url, headers=headers, data=data_json)

        if response.status_code == 200:
            print('Dados atualizados com sucesso!')
            Snackbar(text="Dados atualizados com sucesso.").open()
        else:
            print('Erro ao atualizar dados!')
            Snackbar(text="Erro ao atualizar dados.").open()

    def dados_iguais(self, data, user_data):
        print('Data dados pessoais: ', data)
        print('User data dados pessoais: ', user_data)
        campos_relevantes = user_data.copy()
        campos_relevantes.pop('id', None)
        campos_relevantes['perfil'].pop('qrcode_url', None)
        print('Campos relevantes: ', campos_relevantes)

        for key in data.keys():
            if key in campos_relevantes:
                print('Key: ', key)
                if isinstance(data[key], dict):
                    for sub_key in data[key]:
                        print('Sub key: ', sub_key)
                        if data[key][sub_key] != campos_relevantes[key]\
                                .get(sub_key, None):
                            return False
                else:
                    if data[key] != campos_relevantes.get(key, None):
                        return False
        return True

    def update_user(self):
        if not self.validar_nome() or \
                not self.validar_apelido() or \
                not self.validar_email() or \
                not self.validar_telemovel() or \
                not self.validar_data_nascimento() or \
                not self.validar_escola():
            return

        user_data_singleton = UserDataSingleton.get_instance()
        user_data = user_data_singleton.fetch_user_data()
        if user_data:
            username = user_data.get('username', 'N/A')
            nome = self.ids.first_name_label.text
            apelido = self.ids.last_name_label.text
            email = self.ids.email_label.text
            telemovel = self.ids.telemovel_label.text
            data_nascimento = self.ids.clickable_date.ids.data_nascimento_label.text
            estudante = self.ids.estudante_label.text

            if estudante == "Sim, na Esc. Sec. Ramada":
                estudante = "escola_sec_ramada"
            elif estudante == "Sim, no Agrup. Vasco Santana":
                estudante = "agrup_vasco_santana"
            elif estudante == "Sim, noutra escola":
                estudante = "outra_escola"
            elif estudante == "Não":
                estudante = "nao"

            data = {
                "username": username,
                "first_name": nome,
                "last_name": apelido,
                "email": email,
                "perfil": {
                    "telemovel": telemovel,
                    "data_nascimento": data_nascimento,
                    "estudante": estudante
                }
            }
            print('Data: ', data)
            print('User data: ', user_data)

            if self.dados_iguais(data, user_data):
                print('Nenhum dado foi alterado!')
                Snackbar(text="Nenhum dado foi alterado.").open()
                return
            else:
                print('Dados foram alterados!')
                user_id = user_data.get('id', None)
                self.enviar_dados_servidor(user_id, data)

    def validar_nome(self):
        nome = self.ids.first_name_label.text
        if not nome:
            self.ids.first_name_label.error = True
            Snackbar(text="O campo 'Nome' é obrigatório.").open()
            return False
        else:
            self.ids.first_name_label.error = False
            return True

    def validar_apelido(self):
        apelido = self.ids.last_name_label.text
        if not apelido:
            self.ids.last_name_label.error = True
            Snackbar(text="O campo 'Apelido' é obrigatório.").open()
            return False
        else:
            self.ids.last_name_label.error = False
            return True

    def validar_email(self):
        email = self.ids.email_label.text
        if not email:
            self.ids.email_label.error = True
            Snackbar(text="O campo 'Email' é obrigatório.").open()
            return False
        else:
            self.ids.email_label.error = False
            return True

    def validar_telemovel(self):
        telemovel = self.ids.telemovel_label.text
        if not telemovel:
            self.ids.telemovel_label.error = True
            Snackbar(text="O campo 'Telemóvel' é obrigatório.").open()
            return False
        else:
            self.ids.telemovel_label.error = False
            return True

    def validar_data_nascimento(self):
        data_nascimento = self.ids.clickable_date.ids.data_nascimento_label.text
        if not data_nascimento:
            self.ids.clickable_date.ids.data_nascimento_label.error = True
            Snackbar(text="O campo 'Data de nascimento' é obrigatório.").open()
            return False
        else:
            self.ids.clickable_date.ids.data_nascimento_label.error = False
            return True

    def validar_escola(self):
        escola = self.ids.estudante_label.text
        if not escola:
            self.ids.estudante_label.error = True
            Snackbar(text="O campo 'Escola' é obrigatório.").open()
            return False
        else:
            self.ids.estudante_label.error = False
            return True


class ClickableDateField(MDRelativeLayout):
    text = StringProperty()
    hint_text = StringProperty()

    def open_date_picker(self):
        date_dialog = MDDatePicker()
        date_dialog.bind(on_save=self.on_date_select)
        date_dialog.open()

    def on_date_select(self, instance, value, date_range):
        formated_date = value.strftime('%Y-%m-%d')
        self.text = formated_date

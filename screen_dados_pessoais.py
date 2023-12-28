from kivy.uix.screenmanager import Screen
from utils.singleton import UserDataSingleton
from kivymd.uix.pickers import MDDatePicker
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.snackbar import Snackbar
from datetime import datetime, timedelta
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

    def dez_anos_atras(self):
        agora = datetime.now()
        dez_anos_atras = agora - timedelta(days=365*10)
        return dez_anos_atras.strftime('%Y-%m-%d')

    def show_date_picker(self, text_field):
        # Armazena a referência do campo de texto
        self.target_text_field = text_field

        dez_anos_atras = self.dez_anos_atras()

        ano, mes, dia = map(int, dez_anos_atras.split('-'))
        # Cria e abre o MDDatePicker
        date_picker = MDDatePicker(year=ano, month=mes, day=dia)
        date_picker.bind(
            on_save=self.on_date_select)
        date_picker.open()

    def on_date_select(self, instance, value, date_range):
        # Atualiza o campo de texto com a data selecionada
        self.target_text_field.text = value.strftime('%Y-%m-%d')

    def update_ui_with_user_data(self, user_data):
        first_name = user_data.get('first_name', 'N/A')
        last_name = user_data.get('last_name', 'N/A')
        username = user_data.get('username', 'N/A')
        email = user_data.get('email', 'N/A')
        telemovel = user_data['perfil'].get('telemovel', 'N/A')
        data_nascimento = user_data['perfil'].get('data_nascimento', 'N/A')
        escola = user_data['perfil'].get('estudante', 'N/A')
        # fidelidade = user_data['perfil'].get('tipo_fidelidade', 'N/A')

        self.ids.first_name_label.text = first_name
        self.ids.last_name_label.text = last_name
        self.ids.username_label.text = username
        self.ids.email_label.text = email
        self.ids.telemovel_label.text = telemovel
        self.ids.data_nascimento_label.text = data_nascimento
        self.ids.estudante_label.text = escola
        # self.ids.fidelidade_label.text = fidelidade

    def menu_list(self):
        self.menu_items = [
            {
                "viewclass": "OneLineListItem",
                "text": "Sim, na Esc. Sec. Ramada",
                "on_release": lambda x="Sim, na Esc. Sec. Ramada": self
                .set_item(x),
            },
            {
                "viewclass": "OneLineListItem",
                "text": "Sim, no Agrup. Vasco Santana",
                "on_release": lambda x="Sim, no Agrup. Vasco Santana": self
                .set_item(x),
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
            self.ids.telemovel_label.error = False

        elif response.status_code > 200 and response.status_code < 500:
            print('Erro ao atualizar dados!')
            try:
                print('TRY')
                error_messages = response.json()
                print('Error messages: ', error_messages)
                for field, messages in error_messages.items():
                    if field == "email":
                        self.ids.email_label.error = True
                        self.ids.email_label.helper_text = messages[0]
                    elif field == "perfil":
                        # Acessa o dicionário aninhado 'perfil'
                        perfil_fields = messages
                        if "telemovel" in perfil_fields:
                            self.ids.telemovel_label.error = True
                            self.ids\
                                .telemovel_label\
                                .helper_text_mode = "on_error"
                            self.ids.telemovel_label.helper_text = \
                                perfil_fields["telemovel"][0]
                        elif "data_nascimento" in perfil_fields:
                            self.ids.data_nascimento_label.error = True
                            self.ids\
                                .data_nascimento_label\
                                .helper_text_mode = "on_error"
                            self.ids.data_nascimento_label.helper_text = \
                                perfil_fields["data_nascimento"][0]

                        elif "estudante" in perfil_fields:
                            self.ids.estudante_label.error = True
                            self.ids.estudante_label.helper_text = \
                                perfil_fields["estudante"][0]

            except ValueError:
                Snackbar(
                    text="Erro ao atualizar dados. Tente mais tarde.").open()
        else:
            print('Erro no servidor!')
            Snackbar(text="Erro no servidor. Tente mais tarde.").open()

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
        erro = False
        if not self.validar_nome():
            erro = True
        if not self.validar_apelido():
            erro = True
        if not self.validar_email():
            erro = True
        if not self.validar_telemovel():
            erro = True
        if not self.validar_data_nascimento():
            erro = True
        if not self.validar_escola():
            erro = True
        if erro:
            return  # Não atualiza os dados do usuário

        user_data_singleton = UserDataSingleton.get_instance()
        user_data = user_data_singleton.fetch_user_data()
        if user_data:
            username = user_data.get('username', 'N/A')
            nome = self.ids.first_name_label.text
            apelido = self.ids.last_name_label.text
            email = self.ids.email_label.text
            telemovel = self.ids.telemovel_label.text
            data_nascimento = self.ids.data_nascimento_label.text
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
            self.ids.first_name_label.helper_text_mode = "on_error"
            self.ids.first_name_label.helper_text = "Este campo é obrigatório."
            return False
        else:
            self.ids.first_name_label.error = False
            return True

    def validar_apelido(self):
        apelido = self.ids.last_name_label.text
        if not apelido:
            self.ids.last_name_label.error = True
            self.ids.last_name_label.helper_text_mode = "on_error"
            self.ids.last_name_label.helper_text = "Este campo é obrigatório."
            return False
        else:
            self.ids.last_name_label.error = False
            return True

    def validar_email(self):
        email = self.ids.email_label.text
        if not email:
            self.ids.email_label.error = True
            self.ids.email_label.helper_text_mode = "on_error"
            self.ids.email_label.helper_text = "Este campo é obrigatório."
            return False
        else:
            self.ids.email_label.error = False
            return True

    def validar_telemovel(self):
        telemovel = self.ids.telemovel_label.text
        if not telemovel:
            self.ids.telemovel_label.error = True
            self.ids.telemovel_label.helper_text_mode = "on_error"
            self.ids.telemovel_label.helper_text = "Este campo é obrigatório."
            return False
        elif len(self.ids.telemovel_label.text) != 9:
            self.ids.telemovel_label.error = True
            self.ids.telemovel_label.helper_text_mode = "on_error"
            self.ids.telemovel_label\
                .helper_text = "O campo 'Telemóvel' deve ter 9 dígitos."
            return False
        else:
            self.ids.telemovel_label.error = False
        return True

    def validar_data_nascimento(self):
        user_data_singleton = UserDataSingleton.get_instance()
        user_data = user_data_singleton.fetch_user_data()
        data_nascimento = self.ids\
            .data_nascimento_label.text
        if not data_nascimento:
            self.ids.data_nascimento_label.error = True
            self.ids.data_nascimento_label.helper_text_mode = "on_error"
            self.ids.data_nascimento_label\
                .helper_text = "Este campo é obrigatório."
            return False
        else:
            self.ids.data_nascimento_label.error = False
            return True

    def validar_escola(self):
        escola = self.ids.estudante_label.text
        if not escola:
            self.ids.estudante_label.error = True
            self.ids.estudante_label.helper_text_mode = "on_error"
            self.ids.estudante_label.helper_text = "Este campo é obrigatório."
            return False
        else:
            self.ids.estudante_label.error = False
            return True

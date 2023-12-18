from kivy.uix.screenmanager import Screen
from kivymd.uix.relativelayout import MDRelativeLayout
from kivy.properties import StringProperty, BooleanProperty
from kivymd.uix.pickers import MDDatePicker
from kivymd.uix.menu import MDDropdownMenu
import requests
import json
from kivymd.uix.snackbar import Snackbar


class RegistarScreen(Screen):
    def on_enter(self, *args):
        self.ids.nome_label.text = ""
        self.ids.apelido_label.text = ""
        self.ids.username_label.text = ""
        self.ids.email_label.text = ""
        self.ids.password_round.ids.password_label.text = ""
        self.ids.password2_round.ids.password2_label.text = ""
        self.ids.telemovel_label.text = ""
        self.ids.clickable_date.ids.data_nascimento_label.text = ""
        self.ids.drop_item.text = ""

        self.reset_field('email_label', 'user@gmail.com')
        self.reset_field('username_label', 'Escolha um nome de usuário')

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
            caller=self.ids.drop_item,
            items=self.menu_items,
            position="center",
            width_mult=4,
        )

        self.menu.open()

    def set_item(self, text_item):
        self.ids.drop_item.text = text_item
        self.menu.dismiss()

    def register_user(self):
        if not self.validar_nome() or \
                not self.validar_apelido() or \
                not self.validar_username() or \
                not self.validar_email() or \
                not self.validar_password() or \
                not self.validar_password2() or \
                not self.validar_telemovel() or \
                not self.validar_data_nascimento() or \
                not self.validar_escola():
            return

        nome = self.ids.nome_label.text
        apelido = self.ids.apelido_label.text
        username = self.ids.username_label.text
        email = self.ids.email_label.text
        password = self.ids.password_round.ids.password_label.text
        password2 = self.ids.password2_round.ids.password2_label.text
        telemovel = self.ids.telemovel_label.text
        data_nascimento = self.ids.clickable_date.ids.data_nascimento_label.text
        escola = self.ids.drop_item.text

        if escola == "Sim, na Esc. Sec. Ramada":
            escola = "escola_sec_ramada"
        elif escola == "Sim, no Agrup. Vasco Santana":
            escola = "agrup_vasco_santana"
        elif escola == "Sim, noutra escola":
            escola = "outra_escola"
        elif escola == "Não":
            escola = "nao"

        if password != password2:
            Snackbar(text="As senhas não coincidem.").open()
            return

        data = {
            "username": username,
            "password": password,
            "email": email,
            "first_name": nome,
            "last_name": apelido,
            # 'password2': password2,
            "perfil": {
                "data_nascimento": data_nascimento,
                "telemovel": telemovel,
                "estudante": escola
            }
        }
        print('Data: ', data)

        response = requests.post(
            'http://127.0.0.1:8000/users/api/v1/', json=data)

        # print('Response: ', response)
        print(json.dumps(response.json(), indent=4))

        # if response:
        print('Status Code: ', response.status_code)

        if response.status_code != 201:
            print('Status code diferente de 201')

            try:
                print('TRY')
                error_messages = response.json()
                print('Error messages: ', error_messages)
                for field, messages in error_messages.items():
                    if field == "username":
                        self.ids.username_label.error = True
                        self.ids.username_label.helper_text = messages[0]
                    elif field == "email":
                        self.ids.email_label.error = True
                        self.ids.email_label.helper_text = messages[0]
                    elif field == "password":
                        self.ids.password_round.ids.password_label.error = True
                        self.ids.password_round.ids.password_label.helper_text = messages[0]
                    elif field == "perfil":
                        # Acessa o dicionário aninhado 'perfil'
                        perfil_fields = messages
                        if "telemovel" in perfil_fields:
                            self.ids.telemovel_label.error = True
                            self.ids.telemovel_label.helper_text = \
                                perfil_fields["telemovel"][0]
                    # Adicione condições semelhantes para outros campos

            except ValueError:
                print('Erro ao registar utilizador(text): ', response.text)
                Snackbar(text=response.text).open()
            return

        print('Utilizador registado com sucesso')
        self.manager.current = 'screen_inicio'

    def validar_nome(self):
        nome = self.ids.nome_label.text
        if not nome:
            self.ids.nome_label.error = True  # Marca o campo como com erro
            Snackbar(text="O campo 'Nome' é obrigatório.").open()
            return False
        self.ids.nome_label.error = False  # Remove a marcação de erro
        return True

    def validar_apelido(self):
        apelido = self.ids.apelido_label.text
        if not apelido:
            self.ids.apelido_label.error = True  # Marca o campo como com erro
            Snackbar(text="O campo 'Apelido' é obrigatório.").open()
            return False
        self.ids.apelido_label.error = False
        return True

    def validar_username(self):
        username = self.ids.username_label.text
        if not username:
            self.ids.username_label.error = True
            Snackbar(text="O campo 'Username' é obrigatório.").open()
            return False
        self.ids.username_label.error = False
        return True

    def validar_email(self):
        email = self.ids.email_label.text
        if not email:
            self.ids.email_label.error = True
            Snackbar(text="O campo 'Email' é obrigatório.").open()
            return False
        self.ids.email_label.error = False
        return True

    def validar_password(self):
        password = self.ids.password_round.ids.password_label.text
        if not password:
            self.ids.password_round.ids.password_label.error = True
            Snackbar(text="O campo 'Senha' é obrigatório.").open()
            return False
        self.ids.password_round.ids.password_label.error = False
        return True

    def validar_password2(self):
        password2 = self.ids.password2_round.ids.password2_label.text
        if not password2:
            self.ids.password2_round.ids.password2_label.error = True
            Snackbar(text="O campo 'Confirmar Senha' é obrigatório.").open()
            return False
        self.ids.password2_round.ids.password2_label.error = False
        return True

    def validar_telemovel(self):
        telemovel = self.ids.telemovel_label.text
        if not telemovel:
            self.ids.telemovel_label.error = True
            Snackbar(text="O campo 'Telemóvel' é obrigatório.").open()
            return False
        self.ids.telemovel_label.error = False
        return True

    def validar_data_nascimento(self):
        data_nascimento = self.ids.clickable_date.ids.data_nascimento_label.text
        if not data_nascimento:
            self.ids.clickable_date.ids.data_nascimento_label.error = True
            Snackbar(text="O campo 'Data de Nascimento' é obrigatório.").open()
            return False
        self.ids.clickable_date.ids.data_nascimento_label.error = False
        return True

    def validar_escola(self):
        escola = self.ids.drop_item.text
        if not escola:
            self.ids.drop_item.error = True
            Snackbar(text="O campo 'Estudante' é obrigatório.").open()
            return False
        self.ids.drop_item.error = False
        return True

    def reset_field(self, field_id, default_helper_text):
        field = self.ids.get(field_id)
        if field:
            field.error = False
            field.helper_text = default_helper_text


class MDTextFieldError(BooleanProperty):
    error = BooleanProperty(False)


class ClickableTextFieldRound(MDRelativeLayout):
    text = StringProperty()
    hint_text = StringProperty()


class ClickableTextFieldRound2(MDRelativeLayout):
    text = StringProperty()
    hint_text = StringProperty()


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

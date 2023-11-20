from kivy.uix.screenmanager import Screen
import requests


class UtilizadorHomeScreen(Screen):

    def on_enter(self):
        # Isso mostrará todos os IDs disponíveis
        # Obter o token e o user_id
        login_screen = self.manager.get_screen('screen_clientes')
        token = login_screen.token
        user_id = login_screen.user_id

        # Buscar dados do usuário com o user_id
        self.fetch_user_data(token, user_id)

    def fetch_user_data(self, token, user_id):
        url = f"http://127.0.0.1:8000/users/api/v1/{user_id}"
        headers = {'Authorization': f'Bearer {token}'}
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            user_data = response.json()

            username = user_data.get('username')
            email = user_data.get('email')
            first_name = user_data.get('first_name')
            last_name = user_data.get('last_name')
            telefone = user_data['perfil'].get('telemovel')
            estudante = user_data['perfil'].get('estudante')
            qrcode_url = user_data['perfil'].get('qrcode_url')

            self.ids.label_boas_vindas.text = f"Bem-vindo, {first_name} {last_name}!"
            self.ids.label_username.text = f"Username: {username}"
            self.ids.label_email.text = f"Email: {email}"
            self.ids.label_nome_completo.text = f"Nome Completo: {first_name} {last_name}"
            self.ids.label_telefone.text = f"Telefone: {telefone}"
            self.ids.label_estudante.text = f"Estudante: {estudante}"
            self.ids.image_qrcode.source = qrcode_url

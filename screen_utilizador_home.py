from kivy.uix.screenmanager import Screen
from utils.singleton import UserDataSingleton
import requests


class UtilizadorHomeScreen(Screen):

    def on_enter(self):
        # Obter o token e o user_id
        user_data_singleton = UserDataSingleton.get_instance()
        user_data = user_data_singleton.fetch_user_data()

        if user_data:
            self.update_ui_with_user_data(user_data)
        else:
            print('Nenhum dado do usuário encontrado!')

    def update_ui_with_user_data(self, user_data):
        # Extraia os dados do usuário
        username = user_data.get('username', 'N/A')
        email = user_data.get('email', 'N/A')
        first_name = user_data.get('first_name', 'N/A')
        last_name = user_data.get('last_name', 'N/A')
        telefone = user_data['perfil'].get('telemovel', 'N/A')
        estudante = user_data['perfil'].get('estudante', 'N/A')
        qrcode_url = user_data['perfil'].get('qrcode_url', '')

        # Atualize a interface do usuário com esses dados
        self.ids.label_boas_vindas.text = f"Bem-vindo à Área do Cliente {first_name} {last_name}!\n\nAqui, você tem acesso a todos os benefícios e funcionalidades que a nossa aplicação oferece. Explore os diversos serviços e planos de fidelidade disponíveis, encontre as melhores ofertas perto de você e aproveite ofertas exclusivas para membros.\n\nNão se esqueça de atualizar o seu perfil para personalizar sua experiência e receber recomendações que correspondam aos seus interesses.\n\nSe precisar de ajuda ou tiver alguma dúvida, nossa equipe de suporte está sempre disponível para auxiliá-lo.\n\nAproveite ao máximo a sua experiência conosco!"
        # self.ids.label_username.text = f"Username: {username}"
        # self.ids.label_email.text = f"Email: {email}"
        # self.ids.label_nome_completo.text = f"Nome Completo: {first_name} {last_name}"
        # self.ids.label_telefone.text = f"Telefone: {telefone}"
        # self.ids.label_estudante.text = f"Estudante: {estudante}"
        # self.ids.image_qrcode.source = qrcode_url

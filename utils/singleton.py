import json
import os
import requests
from cryptography.fernet import Fernet
import time


class UserDataSingleton:
    _instance = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def __init__(self):
        if self._instance is not None:
            raise Exception("Esta classe é um singleton!")
        self.base_url = 'http://127.0.0.1:8000/'
        self._load_or_generate_key()

        self.user_data_file = 'user_data.json'
        self.load_user_data()

    def print_debug(self, message):
        # Implementação da função print_debug
        print(message)

    def _load_or_generate_key(self):
        key_file_path = 'secret.key'
        try:
            with open(key_file_path, 'rb') as key_file:
                self.key = key_file.read()
        except FileNotFoundError:
            self.key = Fernet.generate_key()
            with open(key_file_path, 'wb') as key_file:
                key_file.write(self.key)

    def save_user_data(self, user_data):
        user_data_json = json.dumps(user_data)
        encrypted_data = Fernet(self.key).encrypt(user_data_json.encode())
        with open(self.user_data_file, 'wb') as file:
            file.write(encrypted_data)

    def load_user_data(self):
        try:
            with open(self.user_data_file, 'rb') as file:
                encrypted_data = file.read()
                decrypted_data = Fernet(self.key).decrypt(encrypted_data)
                user_data = json.loads(decrypted_data.decode())
                print('----------DEBUGGING----------')
                print('-----------------------------')
                print('-----------------------------')
                print('Dados do usuário carregados - load_user_data: ', user_data)
                print('-----------------------------')
                print('-----------------------------')
                print('----------DEBUGGING----------')
                return user_data
        except FileNotFoundError:
            return None

    def clear_user_data(self):
        try:
            os.remove(self.user_data_file)
            print('Dados do usuário removidos.')
        except FileNotFoundError:
            pass

    def set_user_credentials(self, token, refresh_token, user_id):
        user_data = {'token': token,
                     'refresh_token': refresh_token, 'user_id': user_id}
        self.save_user_data(user_data)

    def clear_user_credentials(self):
        self.clear_user_data()

    def _get_authorization_header(self):
        user_data = self.load_user_data()
        if user_data and 'token' in user_data:
            print('----------DEBUGGING----------')
            print('-----------------------------')
            print('-----------------------------')
            print('User data get_authorization: ', user_data['token'])
            print('-----------------------------')
            print('-----------------------------')
            print('----------DEBUGGING----------')
            return {'Authorization': f'Bearer {user_data["token"]}'}
        else:
            return {}

    def is_user_data_valid(self):
        return bool(self.key) and self.load_user_data()

    def refresh_token(self, user_data):

        refresh_data = {
            'refresh': user_data.get('refresh_token') if user_data and 'refresh_token' in user_data else None
        }
        print('----------DEBUGGING----------')
        print('-----------------------------')
        print('-----------------------------')
        print('Refresh data: ', refresh_data)
        print('-----------------------------')
        print('-----------------------------')
        print('----------DEBUGGING----------')
        print('Refresh_token: ', user_data.get('refresh_token'))
        if user_data.get('new_token'):
            print('----------DEBUGGING----------')
            print('-----------------------------')
            print('-----------------------------')
            print('Refresh token: ', user_data.get('token'))
            print('-----------------------------')
            print('-----------------------------')
            print('----------DEBUGGING----------')
        else:
            print('Não há novo token.')

        # Adiciona o cabeçalho de tipo de conteúdo JSON
        headers = {'Content-Type': 'application/json'}
        print('----------DEBUGGING----------')
        print('-----------------------------')
        print('-----------------------------')
        print('Headers: ', headers)
        print('-----------------------------')
        print('-----------------------------')
        print('----------DEBUGGING----------')

        response = requests.post(
            self.base_url + '/api/token/refresh/',
            headers=headers,
            json=refresh_data,

        )
        print('----------DEBUGGING----------')
        print('-----------------------------')
        print('-----------------------------')
        print('Response: ', response)
        print('-----------------------------')
        print('-----------------------------')
        print('----------DEBUGGING----------')

        if response.status_code == 200:
            new_tokens = response.json()
            print('----------DEBUGGING----------')
            print('-----------------------------')
            print('-----------------------------')
            print('New tokens: ', new_tokens)
            print('-----------------------------')
            print('-----------------------------')
            print('----------DEBUGGING----------')
            # user_data.update(new_tokens)
            user_data['token'] = new_tokens.get('access')
            self.save_user_data(user_data)
            self.print_debug("Token atualizado com sucesso.")
            return True
        elif response.status_code == 400 and "refresh" in response.json():
            print('json response: ', response.json())
            error_message = response.json()["refresh"][0]
            self.print_debug(
                f"1-Falha ao atualizar o token. Código de status: {response.status_code}. Detalhes do erro: {error_message}")
            return False
        else:
            error_message = response.text if response.text else 'Erro desconhecido ao atualizar o token.'
            self.print_debug(
                f"2-Falha ao atualizar o token. Código de status: {response.status_code}. Detalhes do erro: {error_message}")

            return False

    def fetch_user_data(self):
        if not self.is_user_data_valid():
            print('Token inválido ou chave ausente.')
            return None

        user_data = self.load_user_data()

        # Verificar se os dados do usuário estão disponíveis
        if user_data is None:
            print('Dados do usuário não disponíveis.')
            return None

        # Verificar se o token de acesso expirou
        current_time = int(time.time())
        token_expiration = user_data.get('token_expiration', 0)

        if current_time >= token_expiration:
            print('Token de acesso expirado. Tentando atualizar o token...')
            if not self.refresh_token(user_data):
                print('Falha ao atualizar o token.')
                return None

            # Após a renovação bem-sucedida, atualize os dados do usuário
            user_data = self.load_user_data()

        # Verificar se a chave "user_id" existe em user_data antes de acessá-la
        if user_data is not None and isinstance(user_data, dict):
            user_id = user_data["user_id"]
            user_data_url = f'http://127.0.0.1:8000/users/api/v1/{user_id}'
            response = requests.get(
                user_data_url, headers=self._get_authorization_header())

            if response.status_code == 200:
                print('Dados do usuário fetch_user_data: ', response.json())
                return response.json()
            else:
                print('Não foi possível recuperar os dados do usuário.')
                return None
        else:
            print('user_data é None ou não é um dicionário.')

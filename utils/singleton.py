import requests


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
        self.token = None
        self.user_id = None

    def set_user_credentials(self, token, user_id):
        self.token = token
        self.user_id = user_id

    def clear_user_credentials(self):
        self.token = None
        self.user_id = None

    def fetch_user_data(self):
        if not self.token or not self.user_id:
            raise Exception("As credenciais do usuário não foram definidas!")

        url = f"http://127.0.0.1:8000/users/api/v1/{self.user_id}"
        headers = {'Authorization': f'Bearer {self.token}'}
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            print('Dados recebidos: ', response.json())
            return response.json()
        else:
            return None

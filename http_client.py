from kivy.network.urlrequest import UrlRequest
import json


class HttpClient:
    def get_produtos(self, on_complete):
        url = "http://127.0.0.1:8000/produtos/api/v1/"
        print('get_produtos', url)

        print(UrlRequest)

        def data_received(req, result):
            # produtos_dict = []
            # data = json.loads(result)
            produtos_dict = result['results']
            # for i in result:
            #     produtos_dict.append(i)
            # print('data_received', result)
            if on_complete:
                on_complete(produtos_dict)

        def on_success(req, result):
            print('Sucesso na requisição:', result)

        def on_error(req, error):
            print('Erro na requisição:', error)

        req = UrlRequest(url, on_success=data_received, on_error=on_error)

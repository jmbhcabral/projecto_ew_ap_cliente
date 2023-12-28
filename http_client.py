from kivy.network.urlrequest import UrlRequest
from utils.singleton import UserDataSingleton


class HttpClient:
    def get_produtos(self, on_complete, on_error):
        url = "http://127.0.0.1:8000/produtos/api/v1/"

        def data_received(req, result):
            produtos_dict = result['results']

            if on_complete:
                on_complete(produtos_dict)

        def data_error(req, error):
            if on_error:
                on_error(str(error))

        def data_failure(req, result):
            if on_error:
                on_error('Server Error: ' + str(req.resp_status))

        req = UrlRequest(url, on_success=data_received,
                         on_error=data_error, on_failure=data_failure)

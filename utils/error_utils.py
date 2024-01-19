from kivy.uix.popup import Popup
from kivy.uix.label import Label


def show_error_popup(message):
    popup = Popup(title='Erro',
                  content=Label(text=message),
                  size_hint=(0.8, 0.4)
                  )
    popup.open()

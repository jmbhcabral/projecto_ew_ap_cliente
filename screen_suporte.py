from kivy.uix.screenmanager import Screen
from kivy.utils import platform


class ScreenSuporte(Screen):
    def open_email(self):
        if platform == 'android':
            from jnius import autoclass
            Intent = autoclass('android.content.Intent')
            Uri = autoclass('android.net.Uri')
            intent = Intent(Intent.ACTION_SENDTO)
            intent.setData(Uri.parse("mailto:suporte@extremeway.pt"))
            autoclass('org.kivy.android.PythonActivity').mActivity.startActivity(
                intent)
        elif platform == 'ios':
            from pyobjus import autoclass
            from pyobjus.dylib_manager import load_framework
            load_framework('/System/Library/Frameworks/UIKit.framework')
            NSURL = autoclass('NSURL')
            UIApplication = autoclass('UIApplication')
            url = NSURL.URLWithString_("mailto:suporte@extremeway.pt")
            UIApplication.sharedApplication().openURL_(url)
        else:  # desktop
            import webbrowser
            webbrowser.open("mailto:suporte@extremeway.pt")

    def open_phone_dialer(self):
        if platform == 'android':
            from jnius import autoclass
            Intent = autoclass('android.content.Intent')
            Uri = autoclass('android.net.Uri')
            intent = Intent(Intent.ACTION_DIAL)
            intent.setData(Uri.parse("tel:309758819"))
            autoclass('org.kivy.android.PythonActivity').mActivity.startActivity(
                intent)
        elif platform == 'ios':
            from pyobjus import autoclass
            from pyobjus.dylib_manager import load_framework
            load_framework('/System/Library/Frameworks/UIKit.framework')
            NSURL = autoclass('NSURL')
            UIApplication = autoclass('UIApplication')
            url = NSURL.URLWithString_(f"tel:309758819")
            UIApplication.sharedApplication().openURL_(url)
        else:  # desktop
            print("Número de telefone: 309758819")
            # Não há discador no desktop

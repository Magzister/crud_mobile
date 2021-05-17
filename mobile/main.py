from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty
from kivy.uix.screenmanager import ScreenManager

from login.login import LoginScreen
from object_list.object_list import ObjectListScreen
from qr_code.qr_code import QRCodeScreen


class MainWindow(BoxLayout):

    login_screen = LoginScreen()
    object_list_screen = ObjectListScreen()
    qr_code_screen = QRCodeScreen()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.ids.main_screen_manager.add_widget(self.login_screen)
        self.ids.main_screen_manager.add_widget(self.object_list_screen)
        self.ids.main_screen_manager.add_widget(self.qr_code_screen)


class MainApp(App):

    def build(self):
        return MainWindow()


if __name__ == '__main__':
    MainApp().run()

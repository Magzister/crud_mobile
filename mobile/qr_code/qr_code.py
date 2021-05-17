from kivy.app import App
from kivy.uix.screenmanager import Screen
import requests

from kivy.lang import Builder


Builder.load_file('qr_code.kv')


class QRCodeScreen(Screen):

    def set_data(self, data):
        self.ids.qr.data = data

    def back(self):
        self.parent.current = 'object_list_screen'


class QRCodeApp(App):

    def build(self):
        return QRCodeScreen()


if __name__ == '__main__':
    QRCodeApp().run()

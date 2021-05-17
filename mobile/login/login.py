from kivy.app import App
from kivy.uix.screenmanager import Screen
import requests

from kivy.lang import Builder

LOGIN_URL = 'http://localhost:8000/auth/login/'

Builder.load_file('login.kv')


class LoginScreen(Screen):

    def login(self, username, password):
        data = {
            'username': username,
            'password': password,
        }
        response = requests.post(LOGIN_URL, data)
        if response.status_code == 200:
            refresh_token = response.json().get('refresh', None)
            access_token = response.json().get('access', None)
            object_list_screen = self.parent.get_screen('object_list_screen')
            object_list_screen.set_data(username, access_token, refresh_token)
            self.parent.current = 'object_list_screen'

    def clear(self):
        self.ids['username'].text = ""
        self.ids['password'].text = ""


class LoginApp(App):

    def build(self):
        return LoginScreen()


if __name__ == '__main__':
    LoginApp().run()

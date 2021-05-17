from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Rectangle, Color
import requests

import qr_code

OBJECTS_URL = 'http://localhost:8000/objects/'
ACCESSES_URL = 'http://localhost:8000/accesses/'
GET_CODE_URL = 'http://localhost:8000/accesses/get-access-key/{id}/'

refresh_token = None
access_token = None

Builder.load_file('object_list.kv')


class Object(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint_y = None
        self.height = 100
        self.owner_name = Label()
        self.object_name = Label()
        self.add_widget(self.owner_name)
        self.add_widget(self.object_name)
        self.object_id = None

    def set_data(self, owner_name, object_name, object_id):
        self.object_id = object_id
        self.owner_name.text = owner_name
        self.object_name.text = object_name

    def on_touch_up(self, touch):
        if self.collide_point(*touch.pos):
            headers = {'Authorization': f'Bearer {access_token}'}
            url = GET_CODE_URL.format(
                id=self.object_id
            )
            response = requests.get(url=url, headers=headers)
            data = response.json()['code']
            print(data)
            qr_code_screen = self.parent.parent.parent.parent.parent.parent.get_screen('qr_code_screen')
            qr_code_screen.set_data(data)
            self.parent.parent.parent.parent.parent.parent.current = 'qr_code_screen'


class ObjectListScreen(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.access_token = None
        self.refresh_token = None
        self.object_list = []

    def set_data(self, username, new_access_token, new_refresh_token):
        global access_token, refresh_token
        self.ids.username.text = username
        access_token = new_access_token
        refresh_token = new_refresh_token
        self.update_access_list()

    def update_access_list(self):
        self.object_list = []
        headers = {'Authorization': f'Bearer {access_token}'}
        response = requests.get(OBJECTS_URL, headers=headers)
        if response.status_code == 200:
            for el in response.json():
                self.object_list.append(el)
        #else
        response = requests.get(ACCESSES_URL, headers=headers)
        if response.status_code == 200:
            for el in response.json():
                self.object_list.append(el['object'])
        #else
        objects = self.ids.objects
        for obj in self.object_list:
            object = Object()
            object.set_data(
                obj['owner']['username'],
                obj['name'],
                obj['id']
            )
            objects.add_widget(object)

    def logout(self):
        objects = self.ids.objects
        print(objects.children)
        for child in [child for child in objects.children]:
            print(child)
            objects.remove_widget(child)
        login_screen = self.parent.get_screen('login_screen')
        login_screen.clear()
        self.parent.current = 'login_screen'


class ObjectListApp(App):

    def build(self):
        object_list = ObjectListScreen()
        return object_list


if __name__ == '__main__':
    ObjectListApp().run()

#test.py
from kivy.lang import Builder

import os
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image as KivyImage
from kivy.clock import Clock
import japanize_kivy
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
import sqlite3
from sql import create_table, insert_table_workbook, insert_table_question
from plyer import filechooser
from PIL import Image as PILImage
import cv2
from kivy.uix.camera import Camera
# 1ページ目のクラス定義
class CreateQuestionScreen(Screen):
    def __init__(self, **kwargs):
        super(CreateQuestionScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')

        layout.add_widget(Label(text='問題文'))
        layout.add_widget(TextInput(hint_text='問題文文字入力'))
        layout.add_widget(Button(text='問題文撮影ボタン'))

        # 画面遷移を行うメソッドを定義
        def switch_to_answer_screen(instance):
            self.manager.current = 'answer'

        next_page_button = Button(text='次のページへ')
        next_page_button.bind(on_press=switch_to_answer_screen)
        layout.add_widget(next_page_button)

        self.add_widget(layout)

# 2ページ目のクラスは同じままで問題ありません。

# 2ページ目のクラス定義
class AnswerScreen(Screen):
    def __init__(self, **kwargs):
        super(AnswerScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')

        layout.add_widget(Label(text='解答'))
        layout.add_widget(TextInput(hint_text='解答欄1入力'))

        layout.add_widget(Label(text='誤答'))
        layout.add_widget(TextInput(hint_text='誤答欄1入力'))

        layout.add_widget(Label(text='解説'))
        layout.add_widget(TextInput(hint_text='解説文入力'))
        layout.add_widget(Button(text='解説文撮影ボタン'))

        # 画面遷移を行うメソッドを定義
        def switch_to_question_screen(instance):
            self.manager.current = 'question'

        back_button = Button(text='戻る')
        back_button.bind(on_press=switch_to_question_screen)
        layout.add_widget(back_button)

        layout.add_widget(Button(text='登録ボタン'))

        self.add_widget(layout)


class MyApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(CreateQuestionScreen(name='question'))
        sm.add_widget(AnswerScreen(name='answer'))
        return sm

if __name__ == '__main__':
    MyApp().run()

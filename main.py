# main.py

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


con = sqlite3.connect("test.db")
cur = con.cursor()
con.execute("PRAGMA foreign_keys = true")

create_table()

class HomeScreen(Screen):
    def select_picture(self, instance):
        file_path = filechooser.open_file(title="画像を選択", filters=[("画像", "*.png", "*.jpg", "*.jpeg")])
        if file_path:
            selected_path = file_path[0]
            print("選択した画像:", selected_path)
        else:
            print("画像が選択されていません。")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = GridLayout(cols=1)
        label = Label(text="ホーム画面", font_size=20)
        layout.add_widget(label)
        
        button_select_picture = Button(text="写真を選択", size_hint=(None, None), size=(200, 50))
        button_select_picture.bind(on_press=self.select_picture)
        layout.add_widget(button_select_picture)
        
        self.add_widget(layout)

    def go_to_create_quiz_screen(self, instance):
        self.manager.current = "create_quiz_screen"

    def go_to_view_quiz_screen(self, instance):
        self.manager.current = "view_quiz_screen"

    def go_to_select_picture(self, instance):
        self.manager.current = "select_picture"


class QuestionScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = GridLayout(cols=1)
        self.add_widget(layout)
        label = Label(text="問題文＆解答追加画面", font_size=20)
        layout.add_widget(label)
        self.question_input = TextInput(multiline=False, hint_text="問題文を入力してください")
        layout.add_widget(self.question_input)
        self.answer_input = TextInput(multiline=False, hint_text="解答を入力してください")
        layout.add_widget(self.answer_input)
        button_add_question = Button(text="問題文と解答を追加する", size_hint=(None, None), size=(200, 50))
        button_add_question.bind(on_press=self.add_question_and_answer)
        layout.add_widget(button_add_question)
        button = Button(text="ホームへ", size_hint=(None, None), size=(200, 50))
        button.bind(on_press=self.go_to_home_screen)
        layout.add_widget(button)

    def go_to_home_screen(self, instance):
        self.manager.current = "home_screen"

    def add_question_and_answer(self, instance):
        question_text = self.question_input.text
        answer_text = self.answer_input.text
        quiz_name = self.quiz_name  # 問題集名を取得
        if question_text and answer_text and quiz_name:
            # 問題と解答を保存する処理
            insert_table_question(quiz_name, question_text, answer_text)
            print("問題と解答を追加しました")
        else:
            print("問題文と解答を入力してくださいまたは問題集名がありません")


class CreateQuizScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = GridLayout(cols=1)
        self.add_widget(layout)
        label = Label(text="問題集を作成", font_size=20)
        layout.add_widget(label)
        self.quiz_name_input = TextInput(multiline=False, hint_text="問題集の名前を入力してください")
        layout.add_widget(self.quiz_name_input)
        button_next = Button(text="次へ", size_hint=(None, None), size=(200, 50))
        button_next.bind(on_press=self.go_to_question_screen)
        layout.add_widget(button_next)
        button_home = Button(text="ホームへ", size_hint=(None, None), size=(200, 50))
        button_home.bind(on_press=self.go_to_home_screen)
        layout.add_widget(button_home)

    def go_to_home_screen(self, instance):
        self.manager.current = "home_screen"

    def go_to_question_screen(self, instance):
        quiz_name = self.quiz_name_input.text.strip()
        if not quiz_name:
            print("問題集の名前を入力してください")
            return
        insert_table_workbook(quiz_name)
        # Pass quiz name to the next screen
        question_screen = self.manager.get_screen("question_screen")
        question_screen.quiz_name = quiz_name  # 問題集名を渡す
        self.manager.current = "question_screen"


class ViewQuizScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = GridLayout(cols=1)
        self.add_widget(layout)
        label = Label(text="保存した問題集を見る", font_size=20)
        layout.add_widget(label)
        self.quiz_content_label = Label(text="", font_size=16, size_hint_y=None)
        self.quiz_content_label.bind(texture_size=self.quiz_content_label.setter('size'))
        scrollview = ScrollView(size_hint=(1, None), size=(Window.width, Window.height - 200))
        scrollview.add_widget(self.quiz_content_label)
        layout.add_widget(scrollview)
        # saved_quizzes ディレクトリが存在しない場合は作成する
        if not os.path.exists("saved_quizzes"):
            os.makedirs("saved_quizzes")
        saved_quizzes = os.listdir('saved_quizzes')
        for quiz_file in saved_quizzes:
            quiz_name = quiz_file[:-4]
            button_quiz = Button(text=quiz_name, size_hint=(None, None), size=(200, 50))
            button_quiz.bind(on_press=lambda instance, name=quiz_name: self.view_quiz(name))
            layout.add_widget(button_quiz)
        button_home = Button(text="ホームへ", size_hint=(None, None), size=(200, 50))
        button_home.bind(on_press=self.go_to_home_screen)
        layout.add_widget(button_home)

    def go_to_home_screen(self, instance):
        self.manager.current = "home_screen"

    def view_quiz(self, quiz_name):
        # Load and display the selected quiz
        with open(f"saved_quizzes/{quiz_name}.txt", "r") as f:
            quiz_content = f.read()
        self.quiz_content_label.text = quiz_content


class ExtractQuiz(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical')
        self.camera = Camera(play=True)
        self.add_widget(self.camera)
        self.camera.bind(on_texture=self.on_camera_texture)
        self.layout.add_widget(self.camera)

        button_capture = Button(text="写真を撮る")
        button_capture.bind(on_release=self.capture)
        self.layout.add_widget(button_capture)

        self.add_widget(self.layout)

    def on_camera_texture(self, *args):
        pass

    def capture(self, *args):
        Clock.schedule_once(self.save_picture, 0.1)

    def save_picture(self, *args):
        self.camera.export_to_png("captured_image.png")
        self.manager.current = "crop_picture"


class CropPicture(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical')
        self.img = Image(source='captured_image.png')
        self.layout.add_widget(self.img)
        button_crop = Button(text="画像を切り抜く")
        button_crop.bind(on_release=self.crop_image)
        self.layout.add_widget(button_crop)
        self.add_widget(self.layout)

    def crop_image(self, *args):
        # 画像を読み込む
        image_path = 'captured_image.png'  # このパスは、実際に存在する画像のパスであることを確認してください。
        img = cv2.imread(image_path)
        if img is not None:
            # 画像の切り取り処理をここで行う
            # 例: imgの中心部分を切り取る
            height, width, _ = img.shape
            center_x, center_y = width // 2, height // 2
            size = min(center_x, center_y)
            cropped_img = img[center_y-size:center_y+size, center_x-size:center_x+size]
            # 切り取った画像を保存
            cv2.imwrite('cropped_image.png', cropped_img)
            # 画像の更新
            self.img.source = 'cropped_image.png'
            self.img.reload()
        else:
            print("画像の読み込みに失敗しました。")
        self.manager.current = "extract_quiz"



class MainApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(HomeScreen(name="home_screen"))
        sm.add_widget(CreateQuizScreen(name="create_quiz_screen"))
        sm.add_widget(QuestionScreen(name="question_screen"))
        sm.add_widget(ViewQuizScreen(name="view_quiz_screen"))
        sm.add_widget(ExtractQuiz(name="extract_quiz"))
        sm.add_widget(CropPicture(name="crop_picture"))
        return sm


if __name__ == "__main__":
    MainApp().run()

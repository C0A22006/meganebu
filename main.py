# main.py 

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
from pytesseract import pytesseract
#SQL初期設定
import sqlite3
con = sqlite3.connect("test.db")
cur = con.cursor()
con.execute("PRAGMA foreign_keys = true")

#テーブル作成する関数
def create_table():
    try:
        cur.execute("CREATE TABLE workbook(workbook_id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT);")
    except sqlite3.OperationalError:
        pass
    try:
        cur.execute("CREATE TABLE question(workbook_id INTEGER, question_id INTEGER PRIMARY KEY AUTOINCREMENT, question TEXT, answer TEXT, explanation TEXT, choice1 TEXT, choice2 TEXT, choice3 TEXT, choice4 TEXT, choice5 TEXT, choice6 TEXT, choice7 TEXT, choice8 TEXT, choice9 TEXT, FOREIGN KEY(workbook_id) references workbook(workbook_id));")
    except sqlite3.OperationalError:
        pass

#workbookのテーブルに追加する関数
def insert_table_workbook(name):
    cur.execute("INSERT INTO workbook(name) values(:name);",{"name": name})
    con.commit()

#workbookのテーブルを参照する関数
def select_table_workbook():
    cur.execute("SELECT * FROM workbook;")
    ans = []
    for row in cur:
        ans.append((row))
    return tuple(ans)

#workbookの行を削除する関数
def delete_table_workbook(workbook_id):
    cur.execute("DELETE FROM question WHERE workbook_id = :workbook_id",{"workbook_id": workbook_id})
    cur.execute("DELETE FROM workbook WHERE workbook_id = :workbook_id",{"workbook_id": workbook_id})
    con.commit()

#questionのテーブルに追加する関数
def insert_table_question(workbook_id,question,answer,explanation=None,choice1=None,choice2=None,choice3=None,choice4=None,choice5=None,choice6=None,choice7=None,choice8=None,choice9=None):
    cur.execute("INSERT INTO question(workbook_id, question, answer, explanation, choice1, choice2, choice3, choice4, choice5, choice6, choice7, choice8, choice9) values(:workbook_id, :question, :answer, :explanation, :choice1, :choice2, :choice3, :choice4, :choice5, :choice6, :choice7, :choice8, :choice9);",{"workbook_id": workbook_id, "question": question, "answer": answer, "explanation": explanation, "choice1": choice1, "choice2": choice2, "choice3" : choice3, "choice4": choice4, "choice5": choice5, "choice6": choice6, "choice7": choice7, "choice8": choice8, "choice9": choice9})
    con.commit()

#questionのテーブルを参照する関数
def select_table_question(workbook_id = None):
    if workbook_id == None:
        cur.execute("SELECT * FROM question;") 
    else:
        cur.execute("SELECT * FROM question where workbook_id = :workbook_id;",{"workbook_id": workbook_id})
    ans = []
    for row in cur:
        ans.append((row))
    return tuple(ans)

#questionの行を削除する関数
def delete_table_question(question_id):
    cur.execute("DELETE FROM question WHERE question_id = :question_id",{"question_id": question_id})
    con.commit()

        
from kivy.uix.spinner import Spinner
from kivy.uix.widget import Widget
from kivy.core.window import Window

Window.size = (480, 720)


#from kivy.core.window import Window
#from kivy.uix.scrollview import ScrollView
#from kivymd.app import MDApp
#from kivymd.uix.list import OneLineListItem

class HomeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = GridLayout(cols=1)
        #self.layout.bind(minimum_height=self.layout.setter('height'))
        self.add_widget(self.layout)
        
        label = Label(text="ホーム", font_size=20, pos_hint=0.3, color=(0,0,0,1))
        self.layout.add_widget(label)
        workbook =  select_table_workbook()
        self.count = 1
        for i in range(len(workbook)):
            self.spinner = Spinner(
                text=workbook[i][1],
                values=('この問題集に問題を追加する', 'この問題集の問題を解く', 'この問題集の名前を変える','この問題集を削除する'),
                size_hint=(1, None),
                size=(200, 50),
                pos_hint={'center_x': .5, 'center_y': .5})
            self.spinner.bind(text=self.show_selected_value)
            self.layout.add_widget(self.spinner)
            self.count += 1

        self.button_add_question = Button(text="問題集を追加する", size_hint=(1, 0.3), size=(200, 50), background_color=(0.690, 0.878, 0.901, 1), background_normal='')
        self.button_add_question.bind(on_press=self.add_buttonClicked)
        self.layout.add_widget(self.button_add_question)
        #root = ScrollView(size_hint=(1, None), size=(Window.width, Window.height))
        #root.add_widget(self.layout) 

    def show_selected_value(self, spinner, choice):
        print(self.layout)
        if choice == '問題を追加する':
            self.manager.current = "question_screen"
        elif choice == '問題を解く':
            self.manager.current = "question_screen"
        elif choice == '名前を変える':
            print("変える")
        elif choice == '削除する':
            print("削除")
        elif choice == 'この問題集に問題を追加する':
            self.manager.current = 'create_question'
        else:
            print("eroor")

    def add_buttonClicked(self, instance):
        insert_table_workbook("問題集" + str(self.count))
        self.layout.remove_widget(self.button_add_question)
        self.spinner = Spinner(
                text="問題集" + str(self.count),
                values=('問題を追加する', '問題を解く', '名前を変える','削除する'),
                size_hint=(1, None),
                size=(200, 50),
                pos_hint={'center_x': .5, 'center_y': .5})
        self.spinner.bind(text=self.show_selected_value)
        self.layout.add_widget(self.spinner)
        self.count += 1
        try: 
            self.button_add_question = Button(text="問題集を追加する", size_hint=(1, 0.3), size=(200, 50))
            self.button_add_question.bind(on_press=self.add_buttonClicked)
            self.layout.add_widget(self.button_add_question)

        except AttributeError:
            pass

    def open_buttonClicked(self, instance):
        self.manager.current = "question_screen"
        
class QuestionScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = GridLayout(cols=1)
        self.add_widget(self.layout)
        self.button_home = Button(text="＞ホームにもどる", size_hint=(0.5, 0.1), size=(200, 50))
        self.button_home.bind(on_press=self.home_back_buttonClicked)
        self.layout.add_widget(self.button_home)
        label = Label(text="問題集１", font_size=20, pos_hint=0.3, color=(0,0,0,1))
        self.layout.add_widget(label)
        question = select_table_question()
        self.count = 1
        for i in range(len(question)):
            print(question[i][2])
            if len(question[i][2]) > 20:
                ans = str(question[i][2])[0:20] + "～"
            else:
                ans = question[i][3]
            self.spinner = Spinner(
                text=ans,
                values=('削除する'),
                size_hint=(1, None),
                size=(200, 50),
                pos_hint={'center_x': .5, 'center_y': .5})
            self.spinner.bind(text=self.show_selected_value)
            self.layout.add_widget(self.spinner)
            self.count += 1

        self.button_add_question = Button(text="新しい問題を作る", size_hint=(1, 0.3), size=(200, 50))
        self.button_add_question.bind(on_press=self.create_buttonClicked)
        self.layout.add_widget(self.button_add_question)
        self.button_add_question = Button(text="問題を解く", size_hint=(1, 0.3), size=(200, 50))
        self.button_add_question.bind(on_press=self.solve_buttonClicked)
        self.layout.add_widget(self.button_add_question)

    def show_selected_value(self, spinner, choice):
        print(self.layout)
        if choice == '削除する':
            print("削除") 
        else:
            print("eroor")

    

    def home_back_buttonClicked(self, instance):
        self.manager.current = "home_screen"
        print("home")

    def create_buttonClicked(self, instance):
        self.manager.current = "home_screen"
        print("create")

    def solve_buttonClicked(self, instance):
        self.manager.current = "home_screen"
        print("solve")

#追加ページ       
# 1ページ目のクラス定義
class CreateQuestionScreen(Screen):
    def __init__(self, **kwargs):
        super(CreateQuestionScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')

        self.question_input = TextInput(hint_text='問題文文字入力')
        layout.add_widget(Label(text='問題文'))
        layout.add_widget(self.question_input)
        photo_button = Button(text='問題文撮影ボタン')
        photo_button.bind(on_press=self.capture_and_recognize_text)
        layout.add_widget(photo_button)
        # 画面遷移を行うメソッドを定義
        def switch_to_answer_screen(instance):
            self.manager.current = 'answer'

        next_page_button = Button(text='次のページへ')
        next_page_button.bind(on_press=switch_to_answer_screen)
        layout.add_widget(next_page_button)

        self.add_widget(layout)

    def capture_and_recognize_text(self, instance):
        # 画像処理とOCRのコードをここに移植
        img_path = 'test2.png'  # 仮の画像パス
        img = cv2.imread(img_path, 0)
        img = cv2.fastNlMeansDenoising(img, None, 10, 7, 21)
        
        pytesseract.tesseract_cmd = "/usr/bin/tesseract"
        ocr_result = pytesseract.image_to_string(img, lang="eng+jpn")
        
        # OCR結果をTextInputに表示
        self.question_input.text = ocr_result

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
            self.manager.current = 'create_question'

        back_button = Button(text='戻る')
        back_button.bind(on_press=switch_to_question_screen)
        layout.add_widget(back_button)

        layout.add_widget(Button(text='登録ボタン'))

        self.add_widget(layout)


class MainApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(HomeScreen(name="home_screen"))
        sm.add_widget(QuestionScreen(name="question_screen"))
        sm.add_widget(CreateQuestionScreen(name='create_question'))
        sm.add_widget(AnswerScreen(name='answer'))
        return sm

    def on_stop(self):
        # アプリケーションが終了する際にデータベース接続を閉じる
        con.close()

if __name__ == "__main__":
    create_table()
    #insert_table_question("1", "16ビットの2進数nを16進数の各けたに分けて，下位のけたから順にスタックに格納するために，次の手順を4回", "答え", "解説", "選択肢1", "選択肢2", "選択肢3", "選択肢4", "選択肢5", "選択肢6", "選択肢7", "選択肢8")
    #insert_table_question("1", "コトラーの競争戦略によると，業界でのシェアは高くないが，特定の製品・サービスに経営資源を集中することで，収益を高め，独自の地位", "答え", "解説", "選択肢1", "選択肢2", "選択肢3", "選択肢4", "選択肢5", "選択肢6", "選択肢7", "選択肢8")
    #insert_table_question("2", "公開鍵暗号方式を用いて，図のようにAさんからBさんへ，他人に秘密にしておきたい文章を送るとき，暗号化に用いる鍵Kとして，適切", "答え", "解説", "選択肢1", "選択肢2", "選択肢3", "選択肢4", "選択肢5", "選択肢6", "選択肢7", "選択肢8")
    #insert_table_question("3", "ITサービスマネジメントにおけるインシデントの記録と問題の記録の関係についての記述のうち，適切なものはどれか。", "答え", "解説", "選択肢1", "選択肢2", "選択肢3", "選択肢4", "選択肢5", "選択肢6", "選択肢7", "選択肢8")
    MainApp().run()
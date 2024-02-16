import os
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput  # 追加
import japanize_kivy

class HomeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = GridLayout(cols=1)
        self.add_widget(layout)
        
        label = Label(text="ホーム画面", font_size=20)
        layout.add_widget(label)
        
        button_create_quiz = Button(text="問題集を作成", size_hint=(None, None), size=(200, 50))
        button_create_quiz.bind(on_press=self.go_to_create_quiz_screen)
        layout.add_widget(button_create_quiz)

        button_view_quiz = Button(text="保存した問題集を見る", size_hint=(None, None), size=(200, 50))
        button_view_quiz.bind(on_press=self.go_to_view_quiz_screen)
        layout.add_widget(button_view_quiz)
        
    def go_to_create_quiz_screen(self, instance):
        self.manager.current = "create_quiz_screen"
        
    def go_to_view_quiz_screen(self, instance):
        self.manager.current = "view_quiz_screen"


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
        if question_text and answer_text:
            # 問題と解答を保存する処理
            with open("question_bank.txt", "a") as f:
                f.write(f"Question: {question_text}\n")
                f.write(f"Answer: {answer_text}\n\n")
            print("問題と解答を追加しました")
        else:
            print("問題文と解答を入力してください")


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

        # Pass quiz name to the next screen
        self.manager.get_screen("question_screen").quiz_name = quiz_name
        self.manager.current = "question_screen"


class QuestionAddScreen(Screen):
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

        button_finish = Button(text="終了", size_hint=(None, None), size=(200, 50))
        button_finish.bind(on_press=self.finish_quiz_creation)
        layout.add_widget(button_finish)

        button_home = Button(text="ホームへ", size_hint=(None, None), size=(200, 50))
        button_home.bind(on_press=self.go_to_home_screen)
        layout.add_widget(button_home)

    def go_to_home_screen(self, instance):
        self.manager.current = "home_screen"

    def add_question_and_answer(self, instance):
        question_text = self.question_input.text
        answer_text = self.answer_input.text
        if question_text and answer_text:
            # 問題と解答を保存する処理
            quiz_name = self.manager.get_screen("create_quiz_screen").quiz_name
            with open(f"saved_quizzes/{quiz_name}.txt", "a") as f:
                f.write(f"Question: {question_text}\n")
                f.write(f"Answer: {answer_text}\n\n")
            print("問題と解答を追加しました")
        else:
            print("問題文と解答を入力してください")

    def finish_quiz_creation(self, instance):
        self.manager.current = "home_screen"


class ViewQuizScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = GridLayout(cols=1)
        self.add_widget(layout)

        label = Label(text="保存した問題集を見る", font_size=20)
        layout.add_widget(label)

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
        print(quiz_content)  # Display the quiz content (you may need to update this part)


class MainApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(HomeScreen(name="home_screen"))
        sm.add_widget(CreateQuizScreen(name="create_quiz_screen"))
        sm.add_widget(QuestionScreen(name="question_screen"))
        sm.add_widget(QuestionAddScreen(name="question_add_screen"))
        sm.add_widget(ViewQuizScreen(name="view_quiz_screen"))
        return sm

if __name__ == "__main__":
    MainApp().run()

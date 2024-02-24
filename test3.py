import tkinter as tk
from tkinter import filedialog
from kivy.app import App
from kivy.uix.button import Button

class TkinterFileChooserApp(App):
    def build(self):
        button = Button(text='ファイルを選択', on_press=self.open_file_dialog)
        return button

    def open_file_dialog(self, instance):
        root = tk.Tk()
        root.withdraw()  # Tkのメインウィンドウを表示しない
        file_path = filedialog.askopenfilename(filetypes=[('Image Files', '*.png;*.jpg;*.jpeg')])
        if file_path:
            print(f'選択されたファイル: {file_path}')
        root.destroy()

TkinterFileChooserApp().run()

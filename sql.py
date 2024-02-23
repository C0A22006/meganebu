# sql.py

#初期設定
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
        cur.execute("CREATE TABLE question(workbook_id INTEGER, question_id INTEGER PRIMARY KEY AUTOINCREMENT, question TEXT, answer TEXT, explanation TEXT, choise1 TEXT, choise2 TEXT, choise3 TEXT, choise4 TEXT, choise5 TEXT, choise6 TEXT, choise7 TEXT, choise8 TEXT, choise9 TEXT, FOREIGN KEY(workbook_id) references workbook(workbook_id));")
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
def insert_table_question(workbook_id,question,answer,explanation=None,choise1=None,choise2=None,choise3=None,choise4=None,choise5=None,choise6=None,choise7=None,choise8=None,choise9=None):
    cur.execute("INSERT INTO question(workbook_id, question, answer, explanation, choise1, choise2, choise3, choise4, choise5, choise6, choise7, choise8, choise9) values(:workbook_id, :question, :answer, :explanation, :choise1, :choise2, :choise3, :choise4, :choise5, :choise6, :choise7, :choise8, :choise9);",{"workbook_id": workbook_id, "question": question, "answer": answer, "explanation": explanation, "choise1": choise1, "choise2": choise2, "choise3" : choise3, "choise4": choise4, "choise5": choise5, "choise6": choise6, "choise7": choise7, "choise8": choise8, "choise9": choise9})
    con.commit()

#questionのテーブルを参照する関数
def select_table_question(workbook_id = None):
    row = ()
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

#最初に行うとテーブルを作ってくれる
#create_table()
#print("---workbook---")
#workbookの名前を入れる。worknook_idは自動で付与される
#insert_table_workbook("問題")
#workbook_idを入れるとその問題集を削除する
#delete_table_workbook(2)
#問題集が全部でてくる
#print(select_table_workbook())

#print("---question---")
#workbook_id,問題文、答え、解説、選択肢1~9をいれる。question_idは自動で付与される
#insert_table_question("3", "問題", "答え", "解説", "選択肢1", "選択肢2", "選択肢3", "選択肢4", "選択肢5", "選択肢6", "選択肢7", "選択肢8")
#question_idの値を入れればその問題が削除される。
#delete_table_question(6)
#workbook_iの値を入れればその問題集のやつだけでてくる。入れなければ問題が全部でてくる。何も入ってないとNoneとでる。
#print(select_table_question())

#データベースを閉じる
#cur.close()
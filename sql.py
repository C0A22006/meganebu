# sql.py

import sqlite3

# データベース接続を開く
con = sqlite3.connect("test.db")
con.execute("PRAGMA foreign_keys = true")

def create_table():
    # テーブルの作成
    cur = con.cursor()
    try:
        cur.execute("CREATE TABLE workbook(workbook_id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT);")
    except sqlite3.OperationalError as e:
        print("Error creating workbook table:", e)
    try:
        cur.execute(
            "CREATE TABLE question(workbook_id INTEGER, question_id INTEGER PRIMARY KEY AUTOINCREMENT, question TEXT, answer TEXT, explanation TEXT, choise1 TEXT, choise2 TEXT, choise3 TEXT, choise4 TEXT, choise5 TEXT, choise6 TEXT, choise7 TEXT, choise8 TEXT, choise9 TEXT, FOREIGN KEY(workbook_id) references workbook(workbook_id));")
    except sqlite3.OperationalError as e:
        print("Error creating question table:", e)
    cur.close()

def insert_table_workbook(name):
    # workbookへのデータ挿入
    cur = con.cursor()
    cur.execute("INSERT INTO workbook(name) VALUES (?);", (name,))
    con.commit()
    cur.close()

def select_table_workbook():
    # workbookのデータ選択
    cur = con.cursor()
    cur.execute("SELECT * FROM workbook;")
    rows = cur.fetchall()
    cur.close()
    return rows

def delete_table_workbook(workbook_id):
    # workbookからのデータ削除
    cur = con.cursor()
    cur.execute("DELETE FROM question WHERE workbook_id = ?;", (workbook_id,))
    cur.execute("DELETE FROM workbook WHERE workbook_id = ?;", (workbook_id,))
    con.commit()
    cur.close()

def insert_table_question(workbook_id, question, answer, explanation=None, choise1=None, choise2=None, choise3=None, choise4=None, choise5=None, choise6=None, choise7=None, choise8=None, choise9=None):
    # questionへのデータ挿入
    cur = con.cursor()
    cur.execute(
        "INSERT INTO question(workbook_id, question, answer, explanation, choise1, choise2, choise3, choise4, choise5, choise6, choise7, choise8, choise9) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);",
        (workbook_id, question, answer, explanation, choise1, choise2, choise3, choise4, choise5, choise6, choise7, choise8, choise9))
    con.commit()
    cur.close()


def select_table_question(workbook_id=None):
    # questionのデータ選択
    cur = con.cursor()
    if workbook_id:
        cur.execute("SELECT * FROM question WHERE workbook_id = ?;", (workbook_id,))
    else:
        cur.execute("SELECT * FROM question;")
    rows = cur.fetchall()
    cur.close()
    return rows

def delete_table_question(question_id):
    # questionからのデータ削除
    cur = con.cursor()
    cur.execute("DELETE FROM question WHERE question_id = ?;", (question_id,))
    con.commit()
    cur.close()

if __name__ == "__main__":
    # スクリプトが直接実行された場合、テーブルを作成する
    create_table()

#最初に行うとテーブルを作ってくれる
create_table()
print("---workbook---")
#workbookの名前を入れる。worknook_idは自動で付与される
insert_table_workbook("問題集")
#workbook_idを入れるとその問題集を削除する
delete_table_workbook(2)
#問題集が全部でてくる
select_table_workbook()

print("---question---")
#workbook_id,問題文、答え、解説、選択肢1~9をいれる。question_idは自動で付与される
insert_table_question("3", "問題", "答え", "解説", "選択肢1", "選択肢2", "選択肢3", "選択肢4", "選択肢5", "選択肢6", "選択肢7", "選択肢8")
#question_idの値を入れればその問題が削除される。
delete_table_question(6)
#workbook_iの値を入れればその問題集のやつだけでてくる。入れなければ問題が全部でてくる。何も入ってないとNoneとでる。
select_table_question(3)

#データベースを閉じる
#cur.close()


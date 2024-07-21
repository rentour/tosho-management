import os
import getpass
import hashlib
import sqlite3
import time
import datetime

# 認証関係
def authenticate_user(username, hashed_password):
    conn = sqlite3.connect("db/employee.db")
    cursor = conn.cursor()
    
    cursor.execute('SELECT name, password, isAdmin FROM users WHERE user_id = ?', (username,))
    user_data = cursor.fetchone()
    
    if user_data:
        stored_name, stored_password, is_admin = user_data
        if stored_password == hashed_password:
            cursor.close()
            conn.close()
            return "Success", stored_name, is_admin
        else:
            cursor.close()
            conn.close()
            return "Password", "NULL", False
    else:
        cursor.close()
        conn.close()
        return "USER", "NULL", False

def authenticate():
    os.system('cls' if os.name == 'nt' else 'clear')
    username = input("従業員ユーザーを入力してください:")
    password = getpass.getpass("パスワードを入力してください:")
    hashed_password = hashlib.sha512(password.encode()).hexdigest()
    
    authenticate_result, name, is_admin = authenticate_user(username, hashed_password)
    os.system('cls' if os.name == 'nt' else 'clear')
    if authenticate_result == "Success":
        print(f"認証に成功しました\n下記のユーザーでログインしました: {name}")
        display_menu(name, is_admin)
    elif authenticate_result == "Password":
        print("パスワードが正しくありません")
        time.sleep(2)
        authenticate()
    elif authenticate_result == "USER":
        print("ユーザーが存在しません")
        time.sleep(2)
        authenticate()
    else:
        print("例外的なエラーが発生しました。コードを確認してください。")
        time.sleep(2)
        authenticate()

# 業務関係

# 従業員管理
def EMPLOYEE_list():
    os.system('cls' if os.name == 'nt' else 'clear')
    conn = sqlite3.connect("db/employee.db")
    cursor = conn.cursor()
    cursor.execute('SELECT user_id, name FROM users')
    employee_list = cursor.fetchall()
    cursor.close()
    conn.close()
    print("現在の従業員リスト")
    print("--------------")
    for user_id, name in employee_list:
        print(f"ユーザーID: {user_id}, 名前: {name}")
    print("--------------")
    input("閲覧を終了する場合はEnterキーを押してください。")
    EMPLOYEE_Management()

def EMPLOYEE_CREATE():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("--------------")
    print("図書履歴管理システム\n©️Rentour")
    print("--------------")
    print("従業員新規登録システムへようこそ。")
    time.sleep(2)
    print("\n新規登録を開始します。\n")
    name = input("新規登録するユーザーの氏名を入力してください:")
    user_id = input("新規登録するユーザーのユーザーIDを入力してください:")
    password = getpass.getpass("新規登録するユーザーのパスワードを入力してください:")
    is_admin = input("このユーザーを管理者にしますか？ (y/n): ").strip().lower() == 'y'
    print("登録を行います。しばらくお待ち下さい。")
    
    # 登録処理を行う
    hashed_password = hashlib.sha512(password.encode()).hexdigest()
    conn = sqlite3.connect("db/employee.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (name, user_id, password, isAdmin) VALUES (?, ?, ?, ?)", (name, user_id, hashed_password, is_admin))
    conn.commit()
    cursor.close()
    conn.close()
    
    print("新規登録が完了しました。3秒後に従業員管理システムに戻ります")
    time.sleep(3)
    EMPLOYEE_Management()

def EMPLOYEE_EDIT():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("--------------")
    print("図書履歴管理システム\n©️Rentour")
    print("--------------")
    print("従業員編集システムへようこそ。")
    print("従業員編集を開始します。")
    time.sleep(2)
    user_id = input("編集する従業員のユーザーIDを入力してください: ")
    
    if user_id == "admin":
        print("adminの情報は変更できません。")
        time.sleep(2)
        return EMPLOYEE_Management()
    
    conn = sqlite3.connect("db/employee.db")
    cursor = conn.cursor()
    cursor.execute('SELECT name, isAdmin FROM users WHERE user_id = ?', (user_id,))
    user_data = cursor.fetchone()
    
    if not user_data:
        print("指定されたユーザーIDの従業員は存在しません。")
        cursor.close()
        conn.close()
        time.sleep(3)
        EMPLOYEE_Management()
        return
    
    current_name, current_is_admin = user_data
    print(f"現在の氏名: {current_name}")
    print(f"現在のユーザーID: {user_id}")
    print(f"現在の管理者権限: {'管理者' if current_is_admin else '一般従業員'}")
    
    new_name = input("新しい氏名を入力してください（変更しない場合はEnterキーを押してください）: ")
    new_user_id = input("新しいユーザーIDを入力してください（変更しない場合はEnterキーを押してください）: ")
    new_is_admin = input("管理者権限を変更しますか？ (y/n/Enterキーを押してスキップ): ").strip().lower()
    
    if new_name:
        cursor.execute('UPDATE users SET name = ? WHERE user_id = ?', (new_name, user_id))
    
    if new_user_id:
        cursor.execute('UPDATE users SET user_id = ? WHERE user_id = ?', (new_user_id, user_id))
    
    if new_is_admin in ('y', 'n'):
        new_is_admin_flag = new_is_admin == 'y'
        cursor.execute('UPDATE users SET isAdmin = ? WHERE user_id = ?', (new_is_admin_flag, user_id))
    
    conn.commit()
    cursor.close()
    conn.close()
    
    print("従業員情報の更新が完了しました。3秒後に従業員管理システムに戻ります")
    time.sleep(3)
    EMPLOYEE_Management()

def EMPLOYEE_DELETE():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("--------------")
    print("図書履歴管理システム\n©️Rentour")
    print("--------------")
    print("従業員登録削除システムへようこそ。")
    print("従業員登録削除を開始します。")
    time.sleep(2)
    user_id = input("削除する従業員のユーザーIDを入力してください: ")
    
    if user_id == "admin":
        print("adminは削除できません")
        time.sleep(2)
        return EMPLOYEE_Management()
    
    conn = sqlite3.connect("db/employee.db")
    cursor = conn.cursor()
    cursor.execute('SELECT name, isAdmin FROM users WHERE user_id = ?', (user_id,))
    user_data = cursor.fetchone()
    
    if not user_data:
        print("指定されたユーザーIDの従業員は存在しません。")
        cursor.close()
        conn.close()
        time.sleep(3)
        EMPLOYEE_Management()
        return
    
    current_name, current_is_admin = user_data
    print(f"現在の氏名: {current_name}")
    print(f"現在のユーザーID: {user_id}")
    print(f"現在の管理者権限: {'管理者' if current_is_admin else '一般従業員'}")
    
    agree = input("この従業員を削除してもよろしいですか？(y/n)")
    if agree == "y":
        final = input ("この操作は取り消せません。本当によろしいですか？(y/n)")
        if final == "y":
            print("削除処理を行います。")
            cursor.execute('DELETE FROM users WHERE user_id = ?', (user_id,))
            conn.commit()
            print("従業員情報の削除が完了しました。3秒後に従業員管理システムに移動します。")
            time.sleep(3)
            return EMPLOYEE_Management()
        else:
            EMPLOYEE_Management()
        return
    else:
        EMPLOYEE_Management()
        return

def EMPLOYEE_PASSWORD_RESET():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("--------------")
    print("図書履歴管理システム\n©️Rentour")
    print("--------------")
    print("従業員パスワードリセットシステムへようこそ。")
    print("従業員パスワードリセットを開始します。")
    time.sleep(2)
    user_id = input("パスワードリセットを行う従業員のユーザーIDを入力してください: ")
    
    conn = sqlite3.connect("db/employee.db")
    cursor = conn.cursor()
    cursor.execute('SELECT name FROM users WHERE user_id = ?', (user_id,))
    user_data = cursor.fetchone()
    
    if not user_data:
        print("指定されたユーザーIDの従業員は存在しません。")
        cursor.close()
        conn.close()
        time.sleep(3)
        EMPLOYEE_Management()
        return
    
    new_password = getpass.getpass("新しいパスワードを入力してください: ")
    hashed_password = hashlib.sha512(new_password.encode()).hexdigest()
    
    cursor.execute('UPDATE users SET password = ? WHERE user_id = ?', (hashed_password, user_id))
    conn.commit()
    
    print("パスワードがリセットされました。3秒後に従業員管理システムに移動します。")
    cursor.close()
    conn.close()
    time.sleep(3)
    EMPLOYEE_Management()

def EMPLOYEE_Management_SELECT(is_admin):
    if not is_admin:
        os.system("cls")
        print("管理者権限が必要です。管理者権限を持つアカウントで再度ログインし、実行してください。")
        time.sleep(2) 
        return display_menu_re(is_admin)
    
    os.system('cls' if os.name == 'nt' else 'clear')
    print("--------------")
    print("図書履歴管理システム\n©️Rentour")
    print("--------------")
    print("従業員管理システムへようこそ。")
    print("-----------------")
    print("1.従業員リスト\n2.従業員編集\n3.新規登録\n4.登録削除\n5.パスワードリセット\n6.ログアウト")
    print("-----------------")
    select = input("行う業務の番号を入力してください:")
    if select == "1":
        os.system('cls' if os.name == 'nt' else 'clear')
        print("従業員リストに接続します")
        EMPLOYEE_list()
    elif select == "2":
        os.system('cls' if os.name == 'nt' else 'clear')
        print("従業員編集システムへ接続します")
        EMPLOYEE_EDIT()
    elif select == "3":
        os.system('cls' if os.name == 'nt' else 'clear')
        print("従業員新規登録システムに接続します")
        EMPLOYEE_CREATE()
    elif select == "4":
        os.system('cls' if os.name == 'nt' else 'clear')
        print("従業員登録削除システムに接続します")
        EMPLOYEE_DELETE()
    elif select == "5":
        os.system('cls' if os.name == 'nt' else 'clear')
        print("従業員パスワードリセットシステムに接続します")
        EMPLOYEE_PASSWORD_RESET()
    elif select == "6":
        os.system('cls' if os.name == 'nt' else 'clear')
        print("ログアウトします")
        display_menu_re(is_admin)
    else:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("不正な番号です。")
        EMPLOYEE_Management_SELECT(is_admin)

def EMPLOYEE_Management():
    EMPLOYEE_Management_SELECT(True)

#利用者管理

def USER_list():
    os.system('cls' if os.name == 'nt' else 'clear')
    conn = sqlite3.connect("db/users.db")
    cursor = conn.cursor()
    cursor.execute('SELECT user_id, name FROM users')
    employee_list = cursor.fetchall()
    cursor.close()
    conn.close()
    print("現在の利用者リスト")
    print("--------------")
    for user_id, name in employee_list:
        print(f"ユーザーID: {user_id}, 名前: {name}")
    print("--------------")
    input("閲覧を終了する場合はEnterキーを押してください。")
    USER_Management()

def USER_EDIT():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("--------------")
    print("図書履歴管理システム\n©️Rentour")
    print("--------------")
    print("利用者編集システムへようこそ。")
    print("利用者編集を開始します。")
    time.sleep(2)
    user_id = input("編集する利用者のユーザーIDを入力してください: ")
    
    conn = sqlite3.connect("db/users.db")
    cursor = conn.cursor()
    cursor.execute('SELECT name FROM users WHERE user_id = ?', (user_id,))
    user_data = cursor.fetchone()
    
    if not user_data:
        print("指定されたユーザーIDの利用者は存在しません。")
        cursor.close()
        conn.close()
        time.sleep(3)
        USER_Management()
        return
    
    current_name, = user_data
    print(f"現在の氏名: {current_name}")
    print(f"現在のユーザーID: {user_id}")
    
    new_name = input("新しい氏名を入力してください（変更しない場合はEnterキーを押してください）: ")
    new_user_id = input("新しいユーザーIDを入力してください（変更しない場合はEnterキーを押してください）: ")
    
    if new_name:
        cursor.execute('UPDATE users SET name = ? WHERE user_id = ?', (new_name, user_id))
    
    if new_user_id:
        cursor.execute('UPDATE users SET user_id = ? WHERE user_id = ?', (new_user_id, user_id))
    
    conn.commit()
    cursor.close()
    conn.close()
    
    print("利用者情報の更新が完了しました。3秒後に利用者管理システムに戻ります")
    time.sleep(3)
    USER_Management()

def USER_CREATE():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("--------------")
    print("図書履歴管理システム\n©️Rentour")
    print("--------------")
    print("利用者新規登録システムへようこそ。")
    time.sleep(2)
    print("\n新規登録を開始します。\n")
    name = input("新規登録するユーザーの氏名を入力してください:")
    user_id = input("新規登録するユーザーのユーザーIDを入力してください:")
    print("登録を行います。しばらくお待ち下さい。")
    
    # 登録処理を行う
    conn = sqlite3.connect("db/users.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (name, user_id) VALUES (?, ?)", (name, user_id))
    conn.commit()
    cursor.close()
    conn.close()
    
    print("新規登録が完了しました。3秒後に利用者管理システムに戻ります")
    time.sleep(3)
    USER_Management()

def USER_DELETE():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("--------------")
    print("図書履歴管理システム\n©️Rentour")
    print("--------------")
    print("利用者登録削除システムへようこそ。")
    print("利用者登録削除を開始します。")
    time.sleep(2)
    user_id = input("削除する利用者のユーザーIDを入力してください: ")
    
    conn = sqlite3.connect("db/users.db")
    cursor = conn.cursor()
    cursor.execute('SELECT name FROM users WHERE user_id = ?', (user_id,))
    user_data = cursor.fetchone()
    
    if not user_data:
        print("指定されたユーザーIDの利用者は存在しません。")
        cursor.close()
        conn.close()
        time.sleep(3)
        USER_Management()
        return
    
    current_name = user_data
    print(f"現在の氏名: {current_name}")
    print(f"現在のユーザーID: {user_id}")
    
    agree = input("この利用者を削除してもよろしいですか？(y/n)")
    if agree == "y":
        final = input ("この操作は取り消せません。本当によろしいですか？(y/n)")
        if final == "y":
            print("削除処理を行います。")
            cursor.execute('DELETE FROM users WHERE user_id = ?', (user_id,))
            conn.commit()
            cursor.close()
            conn.close()
            print("利用者情報の削除が完了しました。3秒後に利用者管理システムに移動します。")
            time.sleep(3)
            return USER_Management()
        else:
            USER_Management()
        return
    else:
        USER_Management()
        return

def USER_Management_SELECT(is_admin):
    os.system('cls' if os.name == 'nt' else 'clear')
    print("--------------")
    print("図書履歴管理システム\n©️Rentour")
    print("--------------")
    print("利用者管理システムへようこそ。")
    print("-----------------")
    print("1.利用者リスト\n2.利用者編集\n3.新規登録\n4.登録削除\n5.ログアウト")
    print("-----------------")
    select = input("行う業務の番号を入力してください:")
    if select == "1":
        os.system('cls' if os.name == 'nt' else 'clear')
        print("利用者リストに接続します")
        USER_list()
    elif select == "2":
        os.system('cls' if os.name == 'nt' else 'clear')
        print("利用者編集システムに接続します")
        USER_EDIT()
    elif select == "3":
        os.system('cls' if os.name == 'nt' else 'clear')
        print("利用者新規登録システムに接続します")
        USER_CREATE()
    elif select == "4":
        os.system('cls' if os.name == 'nt' else 'clear')
        print("利用者新規削除システムに接続します")
        USER_DELETE()
    elif select == "5":
        os.system('cls' if os.name == 'nt' else 'clear')
        print("ログアウトします")
        display_menu_re(is_admin)
    else:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("不正な番号です。")
        USER_Management_SELECT(is_admin)

def USER_Management():
    USER_Management_SELECT(True)

#書籍管理

def BOOK_list():
    os.system('cls' if os.name == 'nt' else 'clear')
    conn = sqlite3.connect("db/books.db")
    cursor = conn.cursor()
    cursor.execute('SELECT id, title, isbn, isBorrow,borrow_user, borrow_date, return_date FROM books')
    book_list = cursor.fetchall()
    cursor.close()
    conn.close()
    print("現在の書籍リスト")
    print("--------------")
    for id, title, isbn,isBorrow,borrow_user, borrow_date, return_date in book_list:
        print(f"ID: {id}, 書籍名: {title}, ISBN: {isbn}, 貸出状況: {isBorrow}, 貸出者:{borrow_user}, 貸出日: {borrow_date}, 返却日: {return_date}")
    print("--------------")
    input("閲覧を終了する場合はEnterキーを押してください。")
    BOOK_Management()

def BOOK_EDIT():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("--------------")
    print("図書履歴管理システム\n©️Rentour")
    print("--------------")
    print("書籍編集システムへようこそ。")
    print("書籍編集を開始します。")
    time.sleep(2)
    id = input("編集する書籍のIDを入力してください: ")
    
    conn = sqlite3.connect("db/books.db")
    cursor = conn.cursor()
    cursor.execute('SELECT title,id,isbn FROM books WHERE id = ?', (id,))
    book_data = cursor.fetchone()
    
    if not book_data:
        print("指定されたIDのは存在しません。")
        cursor.close()
        conn.close()
        time.sleep(3)
        BOOK_Management()
        return
    
    title,id,isbn = book_data
    print(f"現在の書籍名: {title}")
    print(f"現在のID: {id}")
    print(f"現在のISBN: {isbn}")
    
    new_title = input("新しい書籍名を入力してください（変更しない場合はEnterキーを押してください）: ")
    new_id = input("新しいIDを入力してください（変更しない場合はEnterキーを押してください）: ")
    new_isbn = input("新しいISBNを入力してください（変更しない場合はEnterキーを押してください）: ")
    
    if new_title:
        cursor.execute('UPDATE books SET title = ? WHERE id = ?', (new_title, id))
    
    if new_id:
        cursor.execute('UPDATE books SET id = ? WHERE id = ?', (new_id, id))
        
    if new_isbn:
        cursor.execute('UPDATE books SET isbn = ? WHERE id = ?', (new_isbn, id))
    
    conn.commit()
    cursor.close()
    conn.close()
    
    print("書籍情報の更新が完了しました。3秒後に書籍管理システムに戻ります")
    time.sleep(3)
    BOOK_Management()

def BOOK_FORCE_RETURN():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("--------------")
    print("図書履歴管理システム\n©️Rentour")
    print("--------------")
    print("強制返却システムへようこそ。")
    print("強制返却を開始します。")
    time.sleep(2)
    id = input("強制返却する本のIDを入力してください: ")
    
    conn = sqlite3.connect("db/books.db")
    cursor = conn.cursor()
    cursor.execute('SELECT title,id,isbn,isBorrow,borrow_date,return_date,borrow_user FROM books WHERE id = ?', (id,))
    book_data = cursor.fetchone()
    
    if not book_data:
        print("指定されたIDの書籍は存在しません。")
        cursor.close()
        conn.close()
        time.sleep(3)
        BOOK_Management()
        return
    
    title,id,isbn,isBorrow,borrow_date,return_date,borrow_user = book_data
    
    if isBorrow == 1:
        print(f"書籍名: {title}")
        print(f"ID: {id}")
        print(f"ISBN: {isbn}")
        print(f"貸出状況: {isBorrow}(1=貸出中,0=貸出なし)")
        print(f"貸出者: {borrow_user}")
        print(f"貸出日: {borrow_date}")
        print(f"返却日: {return_date}")
        
        check = input("この書籍の本を強制返却してもよろしいですか?(y/n)")
        if check == "y":
            cursor.execute('UPDATE books SET isBorrow = ?, borrow_user = ?,borrow_date=?,return_date=? WHERE id =?', (False,"",None,None,id))
            conn.commit()
            cursor.close()
            conn.close()
            print("強制返却が完了しました。3秒後に書籍管理システムに戻ります")
            time.sleep(3)
            BOOK_Management()
        else:
            BOOK_Management()
    else:
        print("この書籍は貸出されていません。")
        time.sleep(2)
        BOOK_Management()

def BOOK_CREATE():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("--------------")
    print("図書履歴管理システム\n©️Rentour")
    print("--------------")
    print("書籍新規登録システムへようこそ。")
    print("新規登録を開始します。")
    time.sleep(2)
    book_id = input("新規登録する書籍のIDを入力してください:")
    title = input("新規登録する書籍のタイトルを入力してください:")
    isbn = input("新規登録する書籍のISBNを入力してください:")
    print("登録を行います。しばらくお待ち下さい。")
    
    # 登録処理を行う
    conn = sqlite3.connect("db/books.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO books (id, title,isbn) VALUES (?, ?,?)", (book_id,title,isbn))
    conn.commit()
    cursor.close()
    conn.close()
    
    print("新規登録が完了しました。3秒後に書籍管理システムに戻ります")
    time.sleep(3)
    BOOK_Management()

def BOOK_DELETE():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("--------------")
    print("図書履歴管理システム\n©️Rentour")
    print("--------------")
    print("書籍登録削除システムへようこそ。")
    print("登録削除を開始します。")
    time.sleep(2)
    book_id = input("登録削除する書籍のIDを入力してください:")
    
    conn = sqlite3.connect("db/books.db")
    cursor = conn.cursor()
    cursor.execute('SELECT title,isbn,isBorrow,id FROM books WHERE id = ?', (book_id,))
    book_data = cursor.fetchone()
    
    if not book_data:
        print("指定されたIDの書籍は存在しません。")
        cursor.close()
        conn.close()
        time.sleep(3)
        BOOK_Management()
        return
    
    id,title,isbn,isBorrow = book_data
    
    if isBorrow == True:
        print("貸出中の書籍のため、削除できません。")
        cursor.close()
        conn.close()
        time.sleep(3)
        BOOK_Management()
        return
    else:
        print(f"ID: {id}")
        print(f"書籍名: {title}")
        print(f"ISBN: {isbn}")
        
        agree = input("この書籍を削除してもよろしいですか？(y/n)")
        if agree == "y":
            final = input ("この操作は取り消せません。本当によろしいですか？(y/n)")
            if final == "y":
                print("削除処理を行います。")
                cursor.execute('DELETE FROM books WHERE id = ?', (id,))
                conn.commit()
                cursor.close()
                conn.close()
                print("書籍の削除が完了しました。3秒後に書籍管理システムに移動します。")
                time.sleep(3)
                return BOOK_Management()
            else:
                BOOK_Management()
            return
        else:
            BOOK_Management()
            return
    
def BOOK_Management_SELECT(is_admin):
    os.system('cls' if os.name == 'nt' else 'clear')
    print("--------------")
    print("図書履歴管理システム\n©️Rentour")
    print("--------------")
    print("書籍管理システムへようこそ。")
    print("-----------------")
    print("1.書籍リスト\n2.書籍編集\n3.強制返却\n4.新規登録\n5.登録削除\n6.ログアウト")
    print("-----------------")
    select = input("行う業務の番号を入力してください:")
    if select == "1":
        os.system('cls' if os.name == 'nt' else 'clear')
        print("書籍リストに接続します")
        BOOK_list()
    elif select == "2":
        os.system('cls' if os.name == 'nt' else 'clear')
        print("書籍編集システムに接続します")
        BOOK_EDIT()
    elif select == "3":
        os.system('cls' if os.name == 'nt' else 'clear')
        print("強制返却システムに接続します")
        BOOK_FORCE_RETURN()
    elif select == "4":
        os.system('cls' if os.name == 'nt' else 'clear')
        print("書籍新規登録システムに接続します")
        BOOK_CREATE()
    elif select == "5":
        os.system('cls' if os.name == 'nt' else 'clear')
        print("書籍登録削除システムに接続します")
        BOOK_DELETE()
    elif select == "6":
        os.system('cls' if os.name == 'nt' else 'clear')
        print("ログアウトします")
        display_menu_re(is_admin)
    else:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("不正な番号です。")
        BOOK_Management_SELECT(is_admin)

def BOOK_Management():
    BOOK_Management_SELECT(True)

#貸出業務
def BORROW_Management(is_admin):
    os.system('cls' if os.name == 'nt' else 'clear')
    print("--------------")
    print("図書履歴管理システム\n©️Rentour")
    print("--------------")
    print("貸出システムへようこそ。")
    os.system('cls' if os.name == 'nt' else 'clear')
    user = input("利用者ユーザーIDを入力してください:")
    conn = sqlite3.connect("db/users.db")
    cursor = conn.cursor()
    cursor.execute('SELECT Name FROM users WHERE user_id = ?', (user,))
    user_data = cursor.fetchone()
    
    if not user_data:
        print("指定されたユーザーIDの利用者は存在しません。")
        cursor.close()
        conn.close()
        time.sleep(3)
        BUSINESS_SELECT(is_admin)
        return
    
    Name = user_data
    print("--------------")
    print(f"氏名: {Name}")
    print(f"ユーザーID: {user}")
    print("--------------")
    cursor.close()
    conn.close()
    
    conn = sqlite3.connect("db/books.db")
    cursor = conn.cursor()
    cursor.execute('SELECT id, title, isbn, isBorrow,borrow_user, borrow_date, return_date FROM books')
    book_list = cursor.fetchall()
    cursor.close()
    conn.close()
    print("現在の書籍リスト")
    print("--------------")
    for id, title, isbn,isBorrow,borrow_user, borrow_date, return_date in book_list:
        print(f"ID: {id}, 書籍名: {title}, ISBN: {isbn}, 貸出状況: {isBorrow}, 貸出者:{borrow_user}, 貸出日: {borrow_date}, 返却日: {return_date}")
    print("--------------")
    book = input("貸出処理を行う書籍のIDを入力してください。")
    conn = sqlite3.connect("db/books.db")
    cursor = conn.cursor()
    cursor.execute('SELECT title,id,isbn,isBorrow FROM books WHERE id = ?', (book,))
    book_data = cursor.fetchone()
    
    if not book_data:
        print("指定されたIDの書籍は存在しません。")
        cursor.close()
        conn.close()
        time.sleep(3)
        BUSINESS_SELECT(is_admin)
        return
    
    title,id,isbn,isBorrow = book_data
    
    if isBorrow == False:
        user_id = user
        print("--------------")
        print(f"書籍名: {title}")
        print(f"ID: {id}")
        print(f"ISBN: {isbn}")
        print("--------------")
        check = input("上記の情報で貸出処理を行います。よろしいですか？(y/n)")
        if check == "y":
            print("貸出処理を行います。しばらくお待ち下さい:")
            today = datetime.date.today()
            day_after_week = datetime.timedelta(days=7)
            return_Date = today + day_after_week
            cursor.execute('UPDATE books SET isBorrow = ?, borrow_user = ?,borrow_date=?,return_date=? WHERE id =?', (True,user_id,today,return_Date,id))
            conn.commit()
            cursor.close()
            conn.close()
            print("貸出処理が完了しました。返却期限は"+ str(return_Date) + "です。")
            time.sleep(3)
            os.system('cls' if os.name == 'nt' else 'clear')
            BUSINESS_SELECT(is_admin)
            return
    else:
        print("貸出されている書籍のため、処理できません。")
        time.sleep(3)
        os.system('cls' if os.name == 'nt' else 'clear')
        BUSINESS_SELECT(is_admin)
        return

#返却業務
def RETURN_Management(is_admin):
    os.system('cls' if os.name == 'nt' else 'clear')
    print("--------------")
    print("図書履歴管理システム\n©️Rentour")
    print("--------------")
    print("返却システムへようこそ。")
    print("返却を開始します。")
    time.sleep(2)
    os.system('cls' if os.name == 'nt' else 'clear')
    conn = sqlite3.connect("db/books.db")
    cursor = conn.cursor()
    cursor.execute('SELECT id, title, isbn, isBorrow,borrow_user, borrow_date, return_date FROM books')
    book_list = cursor.fetchall()
    cursor.close()
    conn.close()
    print("現在の書籍リスト")
    print("--------------")
    for id, title, isbn,isBorrow,borrow_user, borrow_date, return_date in book_list:
        print(f"ID: {id}, 書籍名: {title}, ISBN: {isbn}, 貸出状況: {isBorrow}, 貸出者:{borrow_user}, 貸出日: {borrow_date}, 返却日: {return_date}")
    print("--------------")
    id = input("返却する本のIDを入力してください: ")
    
    conn = sqlite3.connect("db/books.db")
    cursor = conn.cursor()
    cursor.execute('SELECT title,id,isbn,isBorrow,borrow_date,return_date,borrow_user FROM books WHERE id = ?', (id,))
    book_data = cursor.fetchone()
    
    if not book_data:
        print("指定されたIDの書籍は存在しません。")
        cursor.close()
        conn.close()
        time.sleep(3)
        BOOK_Management()
        return
    
    title,id,isbn,isBorrow,borrow_date,return_date,borrow_user = book_data
    
    if isBorrow == 1:
        print(f"書籍名: {title}")
        print(f"ID: {id}")
        print(f"ISBN: {isbn}")
        print(f"貸出状況: {isBorrow}(1=貸出中,0=貸出なし)")
        print(f"貸出者: {borrow_user}")
        print(f"貸出日: {borrow_date}")
        print(f"返却日: {return_date}")
        
        check = input("この書籍の本を返却してもよろしいですか?(y/n)")
        if check == "y":
            cursor.execute('UPDATE books SET isBorrow = ?, borrow_user = ?,borrow_date=?,return_date=? WHERE id =?', (False,"",None,None,id))
            conn.commit()
            cursor.close()
            conn.close()
            print("返却が完了しました。3秒後に書籍管理システムに戻ります")
            time.sleep(3)
            BUSINESS_SELECT(is_admin)
        else:
            BUSINESS_SELECT(is_admin)
    else:
        print("この書籍は貸出されていません。")
        time.sleep(2)
        BUSINESS_SELECT(is_admin)

# 業務選択
def BUSINESS_SELECT(is_admin):
    print("-----------------")
    print("1.従業員管理\n2.利用者管理\n3.書籍管理\n4.貸出業務\n5.返却業務\n6.ログアウト\n7.別アカウントへ切り替える")
    print("-----------------")
    select = input("行う業務の番号を入力してください:")
    if select == "1":
        os.system('cls' if os.name == 'nt' else 'clear')
        print("従業員管理システムに接続します")
        EMPLOYEE_Management_SELECT(is_admin)
    elif select == "2":
        os.system('cls' if os.name == 'nt' else 'clear')
        print("利用者管理システムに接続します")
        USER_Management_SELECT(is_admin)
    elif select == "3":
        os.system('cls' if os.name == 'nt' else 'clear')
        print("書籍管理システムに接続します")
        BOOK_Management()
    elif select == "4":
        os.system('cls' if os.name == 'nt' else 'clear')
        print("貸出業務システムに接続します")
        BORROW_Management(is_admin)
    elif select == "5":
        os.system('cls' if os.name == 'nt' else 'clear')
        print("返却業務システムに接続します")
        RETURN_Management(is_admin)
    elif select == "6":
        os.system('cls' if os.name == 'nt' else 'clear')
        print("ログアウトします")
        exit()
    elif select == "7":
        os.system('cls' if os.name == 'nt' else 'clear')
        print("ログアウトし、ログイン画面に戻ります。")
        time.sleep(2)
        authenticate()
    else:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("不正な番号です。")
        BUSINESS_SELECT(is_admin)

# メインメニュー表示
def display_menu(user_name, is_admin):
    os.system('cls' if os.name == 'nt' else 'clear')
    print("--------------")
    print("図書履歴管理システム\n©️Rentour")
    print("--------------")
    print(f"ようこそ、{user_name}さん。\n業務を始めましょう。")
    BUSINESS_SELECT(is_admin)

# メインメニュー再表示
def display_menu_re(is_admin):
    os.system('cls' if os.name == 'nt' else 'clear')
    print("--------------")
    print("図書履歴管理システム\n©️Rentour")
    print("--------------")
    print("業務リスト")
    BUSINESS_SELECT(is_admin)

print("System is Starting")
authenticate()

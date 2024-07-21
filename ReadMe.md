# 書籍履歴管理システム

本を友達などに貸したときに、誰が借りているのか、またいつまでかを確認するための簡易版管理システムです。  
Python のコンソール上で利用できます

## Specification

- Python を利用しています。
- データベースには軽量な SQLite を採用し、複数の db ファイルを利用しています。
- パスワードを SHA-512 を利用してハッシュ化しています。

## How to use?

### 初期ログイン

- GitHub からダウンロードしてください。
- ダウンロードしたファイルの中にある「main.py」を起動してください。
  ![Start Login](/ReadMe/start.png)
- 上記の従業員ユーザーログイン画面が表示されますので、初期 ID でログインしてください。なお初期 ID とパスワード(管理者アカウント)は「admin」パスワードは「Admin」です。
- ログインに失敗する場合は employee.db に admin が登録されていない可能性があります。GitHub で再度ダウンロード願います。

### システムメインメニュー

![Main Menu](/ReadMe/menu.png)

- いくつものメニューから成り立っています
- 行いたい業務の番号を入力することによってその業務を行えます
- 1.従業員管理　は管理者権限を持つアカウント(デフォルトでは admin)でのみ変更できます。

## Warning

一部おかしな部分があります。

## Contact

自分で使い方を模索してみて、わからなければご連絡ください。

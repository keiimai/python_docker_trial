# Docker HubからPythonの公式イメージを取得します。
# これがコンテナのベースとなるOSとPython環境です。
FROM python:3.10-slim

# コンテナ内部の作業ディレクトリを設定します。
# 以降のコマンドは、このディレクトリ内で実行されます。
WORKDIR /app

# ローカルのrequirements.txtをコンテナの/appディレクトリにコピーします。
COPY requirements.txt .

# requirements.txtに記載されたライブラリをインストールします。
RUN pip install -r requirements.txt

# ローカルのmy_modules_environment_settingフォルダをコンテナにコピーします。
# これにより、コンテナ内であなたのモジュールが利用可能になります。
COPY my_modules_environment_setting my_modules_environment_setting

# コンテナが起動したときに実行されるデフォルトコマンドを設定します。
# ここではPythonの対話型シェルを起動するように設定しています。
CMD ["python"]

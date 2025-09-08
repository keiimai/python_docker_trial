# 【Python Docker Trial】
This repository created by Kei Imai, RN, MSN.

# 【格納されているファイルの説明】
requirements.txt
必要なライブラリを指定

# 【実行方法】
・クローンを作成
git clone URL_HERE
・ディレクトリへ移動
cd REPOSITORY
・Dockerイメージをビルドする
docker build -t my-project .
・Dockerコンテナを実行
docker run --rm -v "$(pwd)"/my_project:/data my-project python -c "
import os
from my_modules_environment_setting.create_project_folders import create_project_folders
base_path = '/data'
create_project_folders(base_path)
"

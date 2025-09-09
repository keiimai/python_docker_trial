# 【Python Docker Trial】
This repository created by Kei Imai, RN, MSN.

# 【格納されているファイルの説明】
python_docker_trial/

├── my_modules_environment_setting/

│   └── __init__.py

│   └── create_project_folders.py

├── my_modules_data_visualization/

│   └── __init__.py

│   └── data_visualization_tools.py

├── tests/

│   ├── __init__.py

│   └── test_project_folders.py

├── Dockerfile

├── .gitignore

├── README.md

└── requirements.txt

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

#【環境の削除】
・Dockerイメージを削除

docker rmi my-project

・ディレクトリから親ディレクトリに戻る

cd ..

・ディレクトリを強制的に再帰的に削除

rm -rf python_docker_trial


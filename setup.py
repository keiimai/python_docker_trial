from setuptools import setup, find_packages

# パッケージの依存関係をrequirements.txtから読み込む
with open('requirements.txt') as f:
    required_packages = f.read().splitlines()

setup(
    name='python_docker_trial',  # パッケージ名
    version='0.1.0',  # パッケージのバージョン
    author='kei-imai',  # あなたの名前
    author_email='keiimai1220@gmail.com',  # あなたのメールアドレス
    description='A project for data science and machine learning with Python and Docker.',  # パッケージの説明
    long_description=open('README.md').read(),  # 詳細な説明
    long_description_content_type='text/markdown',
    url='https://github.com/keiimai/python_docker_trial',  # GitHubリポジトリのURL
    packages=find_packages(),  # パッケージのフォルダを自動的に見つける
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
    ],
    install_requires=required_packages,  # requirements.txtから読み込んだ依存ライブラリ
    python_requires='>=3.8',  # 必要なPythonの最小バージョン
)

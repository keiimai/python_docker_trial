import os

def setup_project_directory(base_path):
    """
    指定されたパスにプロジェクトフォルダを作成し、作業ディレクトリを設定します。
    また、working directory、input path、output pathを明示します。

    Args:
        base_path (str): プロジェクトのルートとなるパス。
    """
    # フォルダの階層を定義
    folders_to_create = [
        '01_data',
        '02_document',
        '03_output',
        '04_script'
    ]

    # ベースパスが存在しない場合は作成
    os.makedirs(base_path, exist_ok=True)
    
    # 💡 ワーキングディレクトリを指定されたパスに設定
    os.chdir(base_path)

    # 各フォルダを作成
    for folder in folders_to_create:
        os.makedirs(folder, exist_ok=True)
        
    # 💡 01_data フォルダの中に original_data フォルダを作成
    os.makedirs(os.path.join('01_data', 'original_data'), exist_ok=True)

    # 💡 パスを変数に代入
    working_directory = os.getcwd()
    input_path = os.path.join(working_directory, '01_data')
    output_path = os.path.join(working_directory, '03_output')

    # 💡 最終的なパスを明示
    print("--- フォルダ設定完了 ---")
    print(f"ワーキングディレクトリ: {working_directory}")
    print(f"インプットパス: {input_path}")
    print(f"アウトプットパス: {output_path}")
    print("-----------------------")

    return working_directory, input_path, output_path

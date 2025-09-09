import polars as pl # pandasの進化版(こっちのほうが演算が早い)
import pandas as pd # DataFrameを操作するために活用されるもの
from typing import Optional, Tuple, Union, List

import matplotlib
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import matplotlib.gridspec as gridspec
from matplotlib.ticker import MaxNLocator, StrMethodFormatter
%matplotlib inline

import seaborn as sns
sns.set()
sns.set_style('dark')
sns.despine()
sns.set_context("poster", 1.0, {"lines.linewidth": 2})
sns.color_palette("Paired")

def eda_scatter_plot(
    df: pd.DataFrame,                 # 可視化するデータを含むDataFrame
    x_col: str,                       # X軸にプロットする連続変数の列名
    y_col: str,                       # Y軸にプロットする連続変数の列名
    hue_feature: str,                 # データを色分けするために使用するカテゴリ変数の列名
    kind: str = 'scatter',            # JointPlotのタイプ ('scatter', 'kde', 'hist', 'reg'など)。デフォルトは'scatter'
    palette: Optional[str] = None,    # 色のパレット。Noneの場合、Seabornのデフォルトパレットが使用されます。
                                      # (例: 'viridis', 'coolwarm', 'Paired'など)。
    reg_line: bool = True,            # メインプロットに回帰直線を表示するかどうか。デフォルトはTrue。
                                      # 注意: 'kind'が'reg'の場合、この設定は無視されます。
    title_fontsize: int = 8,          # 全体タイトル（suptitle）のフォントサイズ。デフォルトは8
    label_fontsize: int = 6,          # X軸とY軸ラベルのフォントサイズ。デフォルトは6
    tick_fontsize: int = 6,           # X軸とY軸の目盛りラベルのフォントサイズ。デフォルトは6
    variable_labels: Optional[dict] = None # 元の変数名を人間が読みやすいラベルにマッピングする辞書。
) -> None:
    """
    JointPlotを使用して、2つの連続変数間の関係を可視化します。
    散布図、KDE、ヒストグラムなどを表示し、指定されたカテゴリ変数で色分けが可能です。
    この関数は、単一の変数ペアに対して1つのプロットを生成します。

    Args:
        df (pd.DataFrame): 可視化するデータを含むDataFrame。
        x_col (str): X軸にプロットする連続変数の列名。
        y_col (str): Y軸にプロットする連続変数の列名。
        hue_feature (str): データを色分けするために使用するカテゴリ変数の列名。
        kind (str, optional): JointPlotのメインプロットのタイプ。
                              'scatter', 'kde', 'hist', 'reg' などが選択可能です。
                              詳細についてはSeabornのjointplotドキュメントを参照してください。
                              デフォルトは'scatter'です。
        palette (str, optional): プロットに使用する色のパレット。
                                 Seabornのパレット名 (例: 'viridis', 'coolwarm', 'Paired')
                                 または Matplotlib のカラーマップを指定できます。
                                 Noneの場合、Seabornのデフォルトパレットが使用されます。デフォルトはNone。
        reg_line (bool, optional): メインプロットに回帰直線を表示するかどうか。
                                   Trueの場合、回帰直線が描画されます。
                                   注意: 'kind'が'reg'の場合、この設定は無視されます。デフォルトはTrue。
        title_fontsize (int, optional): 全体タイトル（suptitle）のフォントサイズ。デフォルトは8。
        label_fontsize (int, optional): X軸とY軸ラベルのフォントサイズ。デフォルトは6。
        tick_fontsize (int, optional): X軸とY軸の目盛りラベルのフォントサイズ。デフォルトは6。
        variable_labels (dict, optional): 元の変数名を、プロットに表示する人間が読みやすいラベルに
                                         マッピングするための辞書。
                                         例: {'original_name': '表示名'}。デフォルトはNone。

    Returns:
        None: プロットを表示します。
    """
    # エラーハンドリング
    for col in [x_col, y_col]:
        if col not in df.columns:
            raise ValueError(f"指定された列 '{col}' がDataFrameに存在しません。")
    if hue_feature and hue_feature not in df.columns:
        raise ValueError(f"指定されたhue列 '{hue_feature}' がDataFrameに存在しません。")

    # 表示用ラベルを準備
    display_x_col = variable_labels.get(x_col, x_col) if variable_labels else x_col
    display_y_col = variable_labels.get(y_col, y_col) if variable_labels else y_col
    display_hue_feature = variable_labels.get(hue_feature, hue_feature) if variable_labels and hue_feature else hue_feature

    # Seabornのjointplot関数を使用してJointGridを作成
    g = sns.jointplot(
        data=df,
        x=x_col,
        y=y_col,
        hue=hue_feature,
        kind=kind,
        palette=palette,
    )

    # reg_lineがTrueで、かつkindが'reg'でない場合に回帰直線を追加
    if reg_line and kind != 'reg':
        sns.regplot(
            data=df,
            x=x_col,
            y=y_col,
            ax=g.ax_joint,
            scatter=False,
            color='red',
            line_kws={'alpha': 0.7, 'lw': 2}
        )

    # タイトルと軸ラベルを設定
    g.fig.suptitle(f'Joint Plot of {display_x_col} vs {display_y_col} (Hue by {display_hue_feature})',
                   y=1.02, fontsize=title_fontsize)
    # set_axis_labels に fontsize を直接渡すことはできないため、個別に設定
    g.ax_joint.set_xlabel(display_x_col, fontsize=label_fontsize)
    g.ax_joint.set_ylabel(display_y_col, fontsize=label_fontsize)
    # 目盛りラベルのフォントサイズを設定
    g.ax_joint.tick_params(axis='x', labelsize=tick_fontsize)
    g.ax_joint.tick_params(axis='y', labelsize=tick_fontsize)
    # 周辺プロットの目盛りも調整
    g.ax_marg_x.tick_params(axis='x', labelsize=tick_fontsize)
    g.ax_marg_y.tick_params(axis='y', labelsize=tick_fontsize)
    if g.ax_joint.legend_:
        # 凡例テキストのフォントサイズ
        plt.setp(g.ax_joint.get_legend().get_texts(), fontsize=tick_fontsize)
        # 凡例タイトルのフォントサイズ
        if g.ax_joint.get_legend().get_title():
            g.ax_joint.get_legend().get_title().set_fontsize(label_fontsize * 0.9) # 軸ラベルより少し小さめ

    # タイトルが被らないように調整
    plt.tight_layout(rect=[0, 0, 1, 0.98])
    plt.show()

def eda_violin_plot(
    df: pd.DataFrame,                 # 可視化するデータを含むDataFrame
    feature_col: str,                 # Y軸にプロットする連続変数の列名
    hue_feature: str = None,          # X軸にプロットするカテゴリ変数の列名。指定しない場合、単一のバイオリンプロット。
    palette: Optional[str] = None,    # 色のパレット。Noneの場合、Seabornのデフォルトパレットが使用されます。
                                      # (例: 'viridis', 'coolwarm', 'Paired'など)。
    title: str = None,                # プロットのタイトル。指定しない場合、自動生成されます。
    show_points: bool = True,         # バイオリン内に個々のデータポイント (または四分位点) を表示するかどうか。
    title_fontsize: int = 14,         # プロットのタイトルのフォントサイズ。デフォルトは14。
    label_fontsize: int = 12,         # X軸とY軸ラベルのフォントサイズ。デフォルトは12。
    tick_fontsize: int = 10,          # X軸とY軸の目盛りラベルのフォントサイズ。デフォルトは10。
    variable_labels: Optional[dict] = None # 元の変数名を人間が読みやすいラベルにマッピングする辞書。
) -> None:
    """
    Y軸に連続変数 (feature_col)、X軸にカテゴリ変数 (hue_feature) を取り、
    オプションで hue (色分け) も適用可能なバイオリンプロットを作成します。
    データの分布、中央値、四分位範囲などを視覚的に把握するのに役立ちます。
    画像のサイズはグローバル設定 (plt.rcParams["figure.figsize"]) に依存します。

    Args:
        df (pd.DataFrame): 可視化するデータを含むDataFrame。
        feature_col (str): Y軸にプロットする連続変数の列名。
        hue_feature (str, optional): X軸にプロットするカテゴリ変数の列名。
                                     指定した場合、そのカテゴリごとにバイオリンが分割されます。
                                     Noneの場合、単一のバイオリンプロットが描画されます。
                                     デフォルトはNone。
        palette (str, optional): プロットに使用する色のパレット。
                                 Seabornのパレット名 (例: 'viridis', 'coolwarm', 'Paired')
                                 または Matplotlib のカラーマップを指定できます。
                                 Noneの場合、Seabornのデフォルトパレットが使用されます。デフォルトはNone。
        title (str, optional): プロットのタイトル。指定しない場合、自動生成されます。
                               デフォルトはNone。
        show_points (bool, optional): バイオリンプロット内に個々のデータポイント (Trueの場合 'quartile'として描画)
                                       を表示するかどうか。
                                       Falseの場合、内側に何も表示されません。デフォルトはTrue。
        title_fontsize (int, optional): プロットのタイトルのフォントサイズ。デフォルトは14。
        label_fontsize (int, optional): X軸とY軸ラベルのフォントサイズ。デフォルトは12。
        tick_fontsize (int, optional): X軸とY軸の目盛りラベルのフォントサイズ。デフォルトは10。
        variable_labels (dict, optional): 元の変数名を、プロットに表示する人間が読みやすいラベルに
                                         マッピングするための辞書。
                                         例: {'original_name': '表示名'}。デフォルトはNone。

    Returns:
        None: プロットを表示します。
    """
    # エラーハンドリング
    if feature_col not in df.columns:
        raise ValueError(f"指定された列 '{feature_col}' がDataFrameに存在しません。")
    if hue_feature and hue_feature not in df.columns:
        raise ValueError(f"指定されたhue列 '{hue_feature}' がDataFrameに存在しません。")

    # figsize を削除し、グローバル設定に依存
    plt.figure()

    # 表示用のラベルを取得
    display_feature_col = variable_labels.get(feature_col, feature_col) if variable_labels else feature_col
    display_hue_feature = variable_labels.get(hue_feature, hue_feature) if variable_labels and hue_feature else hue_feature

    inner_setting = 'quartile' if show_points else None

    # hue_feature の有無でプロット方法を分岐
    if hue_feature:
        ax = sns.violinplot(
            data=df,
            x=hue_feature,  # hue_feature を X軸に割り当て
            y=feature_col,  # feature_col を Y軸に割り当て
            palette=palette,
            inner=inner_setting
        )
        # タイトルとX軸ラベルに表示用の名前を使用
        default_title = f'Violin Plot of {display_feature_col} by {display_hue_feature}'
        ax.set_xlabel(display_hue_feature, fontsize=label_fontsize)
    else:
        # hue_feature がNoneの場合、単一のバイオリンプロット
        ax = sns.violinplot(
            data=df,
            y=feature_col,  # feature_col を Y軸に割り当て
            x=None,         # X軸は使用しない (単一プロットの場合)
            palette=palette,
            inner=inner_setting
        )
        # タイトルとX軸ラベルに表示用の名前を使用
        default_title = f'Violin Plot of {display_feature_col}'
        ax.set_xlabel('', fontsize=label_fontsize) # X軸ラベルを空に設定

    # タイトル設定
    if title:
        ax.set_title(title, fontsize=title_fontsize)
    else:
        ax.set_title(default_title, fontsize=title_fontsize)

    ax.set_ylabel(display_feature_col, fontsize=label_fontsize) # Y軸ラベルに表示用の名前を使用

    # 目盛りラベルのフォントサイズを設定
    ax.tick_params(axis='x', labelsize=tick_fontsize)
    ax.tick_params(axis='y', labelsize=tick_fontsize)

    # 凡例のフォントサイズを設定 (hue_featureがある場合のみ凡例が生成される)
    if ax.legend_:
        plt.setp(ax.get_legend().get_texts(), fontsize=tick_fontsize)
        if ax.get_legend().get_title():
            ax.get_legend().get_title().set_fontsize(label_fontsize * 0.9)

    plt.tight_layout()
    plt.show()

def eda_bar_plot(
    df: pd.DataFrame,                 # 可視化するデータを含むDataFrame
    categorical_col: str,             # X軸となるカテゴリ変数の列名
    feature_col: str,                 # Y軸となる連続変数の列名（各カテゴリの平均などが計算される）
    hue_feature: Optional[str] = None,# 色分けに使用するカテゴリ変数の列名 (オプション)。デフォルトはNone。
    palette: Optional[str] = None,    # 色のパレット。Noneの場合、Seabornのデフォルトパレットが使用されます。
                                      # (例: 'viridis', 'coolwarm', 'Paired'など)。
    title: Optional[str] = None,      # プロットのタイトル。指定しない場合、自動生成されます。デフォルトはNone。
    title_fontsize: int = 14,         # プロットのタイトルのフォントサイズ。デフォルトは14。
    label_fontsize: int = 12,         # X軸とY軸ラベルのフォントサイズ。デフォルトは12。
    tick_fontsize: int = 10,          # X軸とY軸の目盛りラベルのフォントサイズ。デフォルトは10。
    show_error_bars: bool = True,     # 誤差棒 (信頼区間) を表示するかどうか。デフォルトはTrue。
    variable_labels: Optional[dict] = None # 元の変数名を人間が読みやすいラベルにマッピングする辞書。
                                          # 例: {'original_name': '表示名'}。
) -> None:
    """
    X軸にカテゴリ変数、Y軸に連続変数 (feature_col) を取り、
    オプションでhue引数による色分けが可能な棒グラフ (barplot) を作成します。
    棒の高さは各カテゴリグループにおける連続変数の平均値（デフォルト）を表し、
    オプションで誤差棒（95%信頼区間）も表示されます。
    画像のサイズはグローバル設定 (plt.rcParams["figure.figsize"]) に依存します。

    Args:
        df (pd.DataFrame): 可視化するデータを含むDataFrame。
        categorical_col (str): X軸にプロットするカテゴリ変数の列名。
        feature_col (str): Y軸にプロットする連続変数の列名。各カテゴリグループのこの列の平均値が棒の高さになります。
        hue_feature (Optional[str], optional): データを色分けするために使用するカテゴリ変数の列名。
                                               指定しない場合、hueによる色分けは行われません。デフォルトはNone。
        palette (str, optional): プロットに使用する色のパレット。
                                 Seabornのパレット名 (例: 'viridis', 'coolwarm', 'Paired')
                                 または Matplotlib のカラーマップを指定できます。
                                 Noneの場合、Seabornのデフォルトパレットが使用されます。デフォルトはNone。
        title (Optional[str], optional): プロットのタイトル。指定しない場合、内容に基づいて自動生成されます。
                                        デフォルトはNone。
        title_fontsize (int, optional): プロットのタイトルのフォントサイズ。デフォルトは14。
        label_fontsize (int, optional): X軸とY軸ラベルのフォントサイズ。デフォルトは12。
        tick_fontsize (int, optional): X軸とY軸の目盛りラベルのフォントサイズ。デフォルトは10。
        show_error_bars (bool, optional): 各棒の平均値に対する誤差棒 (95%信頼区間) を表示するかどうか。
                                         Trueの場合、誤差棒が表示されます。デフォルトはTrue。
        variable_labels (dict, optional): 元の変数名を、プロットに表示する人間が読みやすいラベルに
                                         マッピングするための辞書。
                                         例: {'original_name': '表示名'}。デフォルトはNone。

    Returns:
        None: プロットを表示します。
    """
    # エラーハンドリング
    if categorical_col not in df.columns:
        raise ValueError(f"指定されたカテゴリ列 '{categorical_col}' がDataFrameに存在しません。")
    if feature_col not in df.columns:
        raise ValueError(f"指定された特徴量列 '{feature_col}' がDataFrameに存在しません。")
    if hue_feature and hue_feature not in df.columns:
        raise ValueError(f"指定されたhue列 '{hue_feature}' がDataFrameに存在しません。")

    # figsize を削除し、グローバル設定に依存
    plt.figure()

    # 表示用のラベルを取得
    display_categorical_col = variable_labels.get(categorical_col, categorical_col) if variable_labels else categorical_col
    display_feature_col = variable_labels.get(feature_col, feature_col) if variable_labels else feature_col # feature_col に変更
    # hue_featureはOptionalなので、存在しない場合はNoneを返すように考慮
    display_hue_feature = variable_labels.get(hue_feature, hue_feature) if variable_labels and hue_feature else hue_feature

    # 誤差棒の表示設定
    errorbar_setting = ('ci', 95) if show_error_bars else None

    # barplot を作成
    ax = sns.barplot(
        data=df,
        x=categorical_col, # ここは元の列名を使用 (データアクセス用)
        y=feature_col,     # ★変更: y を feature_col に変更
        hue=hue_feature,   # ここは元の列名を使用 (データアクセス用)
        palette=palette,
        errorbar=errorbar_setting # 誤差棒の設定を適用
    )

    # タイトルを設定 (表示用のラベルを使用)
    if title:
        ax.set_title(title, fontsize=title_fontsize)
    else:
        default_title = f'Mean {display_feature_col} by {display_categorical_col}' # display_feature_col に変更
        if display_hue_feature:
            default_title += f' (Hue by {display_hue_feature})'
        ax.set_title(default_title, fontsize=title_fontsize)

    # 軸ラベルのフォントサイズを設定 (表示用のラベルを使用)
    ax.set_xlabel(display_categorical_col, fontsize=label_fontsize)
    ax.set_ylabel(display_feature_col, fontsize=label_fontsize) # display_feature_col に変更

    # 目盛りラベルのフォントサイズを設定
    ax.tick_params(axis='x', labelsize=tick_fontsize)
    ax.tick_params(axis='y', labelsize=tick_fontsize)

    # 凡例のフォントサイズを設定
    if ax.legend_:
        plt.setp(ax.get_legend().get_texts(), fontsize=tick_fontsize)
        if ax.get_legend().get_title():
            ax.get_legend().get_title().set_fontsize(label_fontsize * 0.9)

    plt.tight_layout()
    plt.show()

def eda_heatmap_crosstab(
    df: pd.DataFrame,                 # 可視化するデータを含むDataFrame
    categorical_col1: str,            # Y軸となるカテゴリ変数の列名 (pd.crosstabのindex)
    categorical_col2: str,            # X軸となるカテゴリ変数の列名 (pd.crosstabのcolumns)
    value_col: Optional[str] = None,  # クロス集計で集計する値の列名 (Noneの場合はカウント)。デフォルトはNone。
    agg_func: str = 'count',          # value_colが指定された場合の集計関数 ('count', 'mean', 'sum' など)。デフォルトは'count'。
    palette: Optional[str] = None,    # ヒートマップの色パレット。Noneの場合、Seabornのデフォルトが使用されます。
                                      # (例: 'viridis', 'coolwarm', 'Greens'など)。
    title: Optional[str] = None,      # プロットのタイトル。指定しない場合、自動生成されます。デフォルトはNone。
    title_fontsize: int = 14,         # プロットのタイトルのフォントサイズ。デフォルトは14。
    label_fontsize: int = 12,         # X軸とY軸ラベルのフォントサイズ。デフォルトは12。
    tick_fontsize: int = 10,          # X軸とY軸の目盛りラベルのフォントサイズ。デフォルトは10。
    cbar_label_fontsize: int = 12,    # カラーバーのラベルのフォントサイズ。デフォルトは12。
    annot: bool = True,               # セルの値にアノテーション（数値）を表示するかどうか。デフォルトはTrue。
    fmt: str = '.0f',                 # アノテーションの表示形式 (例: '.1f'は小数点以下1桁、'.0f'は整数)。デフォルトは'.0f'。
    linewidths: float = 0.5,          # セルの境界線の幅。デフォルトは0.5。
    linecolor: str = 'white',         # セルの境界線の色。デフォルトは'white'。
    variable_labels: Optional[dict] = None # 元の変数名を人間が読みやすいラベルにマッピングする辞書。
                                          # 例: {'original_name': '表示名'}。
) -> None:
    """
    2つのカテゴリ変数からクロス集計表（頻度または集計値）を作成し、その結果をヒートマップで可視化します。
    各セルの数値（カウントまたは集計された値）をカラーグラデーションとアノテーションで表示します。

    Args:
        df (pd.DataFrame): 可視化するデータを含むDataFrame。
        categorical_col1 (str): クロス集計のインデックス（Y軸）にするカテゴリ変数の列名。
        categorical_col2 (str): クロス集計のカラム（X軸）にするカテゴリ変数の列名。
        value_col (Optional[str], optional): クロス集計で集計する値の列名。
                                             指定しない場合、各カテゴリの組み合わせのカウントを計算します。
                                             デフォルトはNone。
        agg_func (str, optional): `value_col`が指定された場合の集計関数。
                                  'count', 'mean', 'sum' など、Pandasの`groupby().agg()`に渡せる文字列を指定します。
                                  デフォルトは'count'。
        palette (str, optional): ヒートマップの色パレット。
                                 Seabornのカラーマップ名 (例: 'viridis', 'coolwarm')
                                 または Matplotlib のカラーマップを指定できます。
                                 Noneの場合、Seabornのデフォルトカラーマップが使用されます。デフォルトはNone。
        title (Optional[str], optional): プロットのタイトル。指定しない場合、内容に基づいて自動生成されます。
                                        デフォルトはNone。
        title_fontsize (int, optional): プロットのタイトルのフォントサイズ。デフォルトは14。
        label_fontsize (int, optional): X軸とY軸ラベルのフォントサイズ。デフォルトは12。
        tick_fontsize (int, optional): X軸とY軸の目盛りラベルのフォントサイズ。デフォルトは10。
        cbar_label_fontsize (int, optional): カラーバーのラベルのフォントサイズ。デフォルトは12。
        annot (bool, optional): ヒートマップのセル内に数値（アノテーション）を表示するかどうか。デフォルトはTrue。
        fmt (str, optional): アノテーションの表示形式（フォーマット文字列）。
                             例: '.1f'は小数点以下1桁、'.0f'は整数。デフォルトは'.0f'。
        linewidths (float, optional): ヒートマップのセルの境界線の幅。デフォルトは0.5。
        linecolor (str, optional): ヒートマップのセルの境界線の色。デフォルトは'white'。
        variable_labels (dict, optional): 元の変数名を、プロットに表示する人間が読みやすいラベルに
                                         マッピングするための辞書。
                                         例: {'original_name': '表示名'}。デフォルトはNone。

    Returns:
        None: プロットを表示します。
    """
    # エラーハンドリング
    for col in [categorical_col1, categorical_col2]:
        if col not in df.columns:
            raise ValueError(f"指定されたカテゴリ列 '{col}' がDataFrameに存在しません。")
    if value_col and value_col not in df.columns:
        raise ValueError(f"指定された値の列 '{value_col}' がDataFrameに存在しません。")

    # figsize を削除し、グローバル設定に依存
    plt.figure()

    # 表示用のラベルを取得
    display_categorical_col1 = variable_labels.get(categorical_col1, categorical_col1) if variable_labels else categorical_col1
    display_categorical_col2 = variable_labels.get(categorical_col2, categorical_col2) if variable_labels else categorical_col2
    display_value_col = variable_labels.get(value_col, value_col) if variable_labels and value_col else value_col

    # クロス集計表を作成
    if value_col:
        # value_colが指定された場合は、指定された集計関数でクロス集計
        crosstab_df = pd.crosstab(
            df[categorical_col1],
            df[categorical_col2],
            values=df[value_col],
            aggfunc=agg_func
        )
    else:
        # value_colが指定されない場合は、カウントでクロス集計
        crosstab_df = pd.crosstab(
            df[categorical_col1],
            df[categorical_col2]
        )

    # ヒートマップを作成
    ax = sns.heatmap(
        crosstab_df,
        cmap=palette,
        annot=annot,
        fmt=fmt,
        linewidths=linewidths,
        linecolor=linecolor,
        cbar_kws={'label': f'{display_value_col if display_value_col else "Count"} ({agg_func})' if value_col else 'Count'}
    )

    # タイトルを設定 (表示用のラベルを使用)
    if title:
        ax.set_title(title, fontsize=title_fontsize)
    else:
        if value_col:
            default_title = f'{display_value_col} ({agg_func}) by {display_categorical_col1} and {display_categorical_col2}'
        else:
            default_title = f'Count by {display_categorical_col1} and {display_categorical_col2}'
        ax.set_title(default_title, fontsize=title_fontsize)

    # 軸ラベルのフォントサイズを設定 (表示用のラベルを使用)
    ax.set_xlabel(display_categorical_col2, fontsize=label_fontsize) # クロス集計のカラムがX軸になるので注意
    ax.set_ylabel(display_categorical_col1, fontsize=label_fontsize) # クロス集計のインデックスがY軸になるので注意

    # 目盛りラベルのフォントサイズを設定
    ax.tick_params(axis='x', labelsize=tick_fontsize)
    ax.tick_params(axis='y', labelsize=tick_fontsize)

    # カラーバーのラベルのフォントサイズを設定
    cbar = ax.collections[0].colorbar
    cbar.set_label('Count', fontsize=cbar_label_fontsize)
    cbar.ax.tick_params(labelsize=tick_fontsize)

    plt.tight_layout()
    plt.show()

#!/usr/bin/env python3
"""Tasks."""
from shlex import quote
import glob
import os
import re
import subprocess
import sys
import typing as t

tasks = {}


class SegziForcer(object):
    """Force 俗字 to 正字."""

    itaizi_selectors: t.List[str] = [
        "\U000E0100",
        "\U000E0101",
        "\U000E0102",
        "\U000E0103",
        "\U000E0104",
    ]

    table: t.Dict[str, str] = {
        "\u4E08": "\u4E08\U000E0101",  # 丈
        "\u4E0E": "\u8207",  # 与
        "\u4E3B": "\u4E3B\U000E0101",  # 主
        "\u4E73": "\u4E73\U000E0101",  # 乳
        "\u4EA1": "\u4EA1\U000E0101",  # 亡
        "\u4EA4": "\u4EA4\U000E0101",  # 交
        "\u4F4F": "\u4F4F\U000E0101",  # 住
        "\u4F75": "\u4F75\U000E0101",  # 併
        "\u4F7F": "\u4F7F\U000E0101",  # 使
        "\u4FBF": "\u4FBF\U000E0101",  # 便
        "\u5002": "\u4F75\U000E0101",  # 倂
        "\u5024": "\u5024\U000E0101",  # 値
        "\u5168": "\u5168\U000E0101",  # 全
        "\u516C": "\u516C\U000E0101",  # 公
        "\u5177": "\u5177\U000E0101",  # 具
        "\u5185": "\u5167",  # 内
        "\u518D": "\u518D\U000E0100",  # 再
        "\u51AC": "\U0002F81A",  # 冬
        "\u51E1": "\u51E1\U000E0101",  # 凡
        "\u5206": "\u5206\U000E0101",  # 分
        "\u5224": "\u5224\U000E0101",  # 判
        "\u524A": "\u524A\U000E0101",  # 削
        "\u524D": "\u524D\U000E0101",  # 前
        "\u5272": "\U0002F822",  # 割
        "\u5316": "\u5316\U000E0101",  # 化
        "\u533A": "\u5340\U000E0101",  # 区
        "\u533F": "\u533F\U000E0101",  # 匿
        "\u5340": "\u5340\U000E0101",  # 區
        "\u534A": "\u534A\U000E0101",  # 半
        "\u535A": "\u535A\U000E0101",  # 博
        "\u5373": "\u537d",  # 即
        "\u53CA": "\u53CA\U000E0101",  # 及
        "\u53F2": "\u53F2\U000E0101",  # 史
        "\u5438": "\u5438\U000E0101",  # 吸
        "\u5449": "\u5433",  # 呉
        "\u5468": "\u5468\U000E0100",  # 周
        "\u5510": "\u5510\U000E0101",  # 唐
        "\u5544": "\u5544\U000E0101",  # 啄
        "\u5546": "\u5546\U000E0101",  # 商
        "\u5618": "\u5653",  # 嘘
        "\u5668": "\u5668\U000E0101",  # 器
        "\u56DE": "\u56D8",  # 回
        "\u5897": "\u589E",  # 増
        "\u59FF": "\u59FF\U000E0101",  # 姿
        "\u5BD2": "\u5BD2\U000E0101",  # 寒
        "\u5C0B": "\u5C0B\U000E0101",  # 尋
        "\u5C0E": "\u5C0E\U000E0101",  # 導
        "\u5C1A": "\u5C19",  # 尚
        "\u5DE1": "\u5DE1\U000E0101",  # 巡
        "\u5DE8": "\u5DE8\U000E0101",  # 巨
        "\u5E1D": "\u5E1D\U000E0101",  # 帝
        "\u5E63": "\u5E63\U000E0101",  # 幣
        "\u5E73": "\u5E73\U000E0101",  # 平
        "\u5E7E": "\u5E7E\U000E0101",  # 幾
        "\u5E83": "\u5EE3",  # 広
        "\u5EFA": "\u5EFA\U000E0101",  # 建
        "\u5F62": "\u5F62\U000E0101",  # 形
        "\u5FB5": "\u5FB5\U000E0100",  # 徵
        "\u6025": "\u6025\U000E0101",  # 急
        "\u6050": "\u6050\U000E0101",  # 恐
        "\u610F": "\u610F\U000E0101",  # 意
        "\u6167": "\u6167\U000E0101",  # 慧
        "\u6210": "\U0002F8B2",  # 成
        "\u6238": "\u6236",  # 戸
        "\u623B": "\u623E",  # 戻
        "\u6240": "\u6240\U000E0101",  # 所
        "\u6271": "\u6271\U000E0101",  # 扱
        "\u62C5": "\u64D4",  # 担
        "\u6319": "\u64E7",  # 挙
        "\u63A1": "\u63A1\U000E0101",  # 採
        "\u6559": "\u654E",  # 教
        "\u6587": "\u6587\U000E0101",  # 文
        "\u65A7": "\u65A7\U000E0100",  # 斧
        "\u65E2": "\u65E3",  # 既
        "\u660E": "\u660E\U000E0101",  # 明
        "\u6696": "\u6696\U000E0101",  # 暖
        "\u66A6": "\u66C6",  # 暦
        "\u66DC": "\u66DC\U000E0101",  # 曜
        "\u66F8": "\u66F8\U000E0101",  # 書
        "\u6700": "\u6700\U000E0101",  # 最
        "\u6708": "\u6708\U000E0101",  # 月
        "\u671B": "\u671B\U000E0102",  # 望
        "\u671F": "\u671F\U000E0101",  # 期
        "\u6821": "\u6821\U000E0101",  # 校
        "\u690D": "\u690D\U000E0102",  # 植
        "\u6955": "\u6A62",  # 楕
        "\u6982": "\u69EA\U000E0101",  # 概
        "\u69CB": "\u69CB\U000E0101",  # 構
        "\u69EA": "\u69EA\U000E0101",  # 槪
        "\u6A5F": "\u6A5F\U000E0101",  # 機
        "\u6B21": "\u6B21\U000E0101",  # 次
        "\u6B69": "\u6B65",  # 歩
        "\u6B74": "\u6B77",  # 歴
        "\u6B96": "\u6B96\U000E0101",  # 殖
        "\u6BCE": "\u6BCF",  # 毎
        "\u6CA2": "\u6FA4",  # 沢
        "\u6CE8": "\u6CE8\U000E0101",  # 注
        "\u6D6E": "\u6D6E\U000E0101",  # 浮
        "\u6D77": "\u6D77\U000E0100",  # 海
        "\u6D88": "\u6D88\U000E0101",  # 消
        "\u6E09": "\u6D89",  # 渉
        "\u6E09": "\u6D89",  # 渉
        "\u6E29": "\u6EAB",  # 温
        "\u6F5B": "\u6F5B\U000E0100",  # 潛
        "\u70BA": "\u7232",  # 為
        "\u732B": "\u8C93",  # 猫
        "\u7387": "\u7387\U000E0101",  # 率
        "\u7523": "\u7522",  # 産
        "\u767A": "\u767C",  # 発
        "\u7684": "\u7684\U000E0101",  # 的
        "\u76DF": "\u76DF\U000E0101",  # 盟
        "\u76F4": "\u76F4\U000E0101",  # 直
        "\u77AC": "\u77AC\U000E0101",  # 瞬
        "\u7814": "\u784F",  # 研
        "\u793E": "\u793E\U000E0101",  # 社
        "\u7956": "\u7956\U000E0101",  # 祖
        "\u795D": "\u795D\U000E0100",  # 祝
        "\u795E": "\u795E\U000E0100",  # 神
        "\u7965": "\u7965\U000E0101",  # 祥
        "\u79D8": "\u7955",  # 秘
        "\u79F0": "\u7A31\U000E0101",  # 称
        "\u7A0B": "\u7A0B\U000E0101",  # 程
        "\u7A0E": "\u7A05",  # 税
        "\u7A31": "\u7A31\U000E0101",  # 稱
        "\u7A40": "\u7A40\U000E0100",  # 穀
        "\u7A74": "\u7A74\U000E0101",  # 穴
        "\u7A7A": "\u7A7A\U000E0101",  # 空
        "\u7A81": "\u7A81\U000E0101",  # 突
        "\u7A93": "\u7A97\U000E0101",  # 窓
        "\u7A97": "\u7A97\U000E0101",  # 窗
        "\u7ADC": "\u9F8D\U000E0102",  # 竜
        "\u7BC0": "\u7BC0\U000E0102",  # 節
        "\u7BC9": "\u7BC9\U000E0101",  # 築
        "\u7C89": "\u7C89\U000E0101",  # 粉
        "\u7CBE": "\u7CBE\U000E0100",  # 精
        "\u7D04": "\u7D04\U000E0101",  # 約
        "\u7D42": "\u7D42\U000E0101",  # 終
        "\u7D76": "\u7D55",  # 絶
        "\u7DB2": "\u7DB2\U000E0101",  # 網
        "\u7DE8": "\u7DE8\U000E0101",  # 編
        "\u7DE9": "\u7DE9\U000E0101",  # 緩
        "\u7DF4": "\u7DF4\U000E0100",  # 練
        "\u7E41": "\u7E41\U000E0101",  # 繁
        "\u7E41": "\u7E41\U000E0101",  # 繁
        "\u7F6E": "\u7F6E\U000E0101",  # 置
        "\u7FBD": "\u7FBD\U000E0100",  # 羽
        "\u7FCC": "\u7FCC\U000E0101",  # 翌
        "\u7FD2": "\u7FD2\U000E0101",  # 習
        "\u7FE0": "\u7FE0\U000E0101",  # 翠
        "\u7FE1": "\u7FE1\U000E0101",  # 翡
        "\u7FFC": "\u7FFC\U000E0102",  # 翼
        "\u8003": "\u8003\U000E0101",  # 考
        "\u8005": "\u8005\U000E0101",  # 者
        "\u8056": "\u8056\U000E0101",  # 聖
        "\u8089": "\u8089\U000E0101",  # 肉
        "\u80DE": "\u80DE\U000E0101",  # 胞
        "\u81ED": "\u81ED\U000E0101",  # 臭
        "\u8209": "\u64E7",  # 舉
        "\u8457": "\u8457\U000E0101",  # 著
        "\u8457": "\u8457\U000E0101",  # 著
        "\u8853": "\u8853\U000E0101",  # 術
        "\u8870": "\u8870\U000E0101",  # 衰
        "\u8877": "\u8877\U000E0101",  # 衷
        "\u8981": "\u8981\U000E0101",  # 要
        "\u8996": "\u8996\U000E0101",  # 視
        "\u8A8D": "\u8A8D\U000E0101",  # 認
        "\u8A95": "\u8A95\U000E0102",  # 誕
        "\u8AAC": "\u8AAA",  # 説
        "\u8ABF": "\u8ABF\U000E0101",  # 調
        "\u8AF8": "\u8AF8\U000E0100",  # 諸
        "\u8CA8": "\u8CA8\U000E0101",  # 貨
        "\u8D77": "\u8D77\U000E0101",  # 起
        "\u8F03": "\u8F03\U000E0101",  # 較
        "\u8F38": "\u8F38\U000E0101",  # 輸
        "\u8FBC": "\u8FBC\U000E0101",  # 込
        "\u8FC4": "\u8FC4\U000E0101",  # 迄
        "\u8FD1": "\u8FD1\U000E0101",  # 近
        "\u8FD1": "\u8FD1\U000E0101",  # 近
        "\u8FD4": "\u8FD4\U000E0101",  # 返
        "\u8FF0": "\u8FF0\U000E0101",  # 述
        "\u8FF7": "\u8FF7\U000E0101",  # 迷
        "\u8FF7": "\u8FF7\U000E0101",  # 迷
        "\u8FFD": "\u8FFD\U000E0101",  # 追
        "\u9000": "\u9000\U000E0101",  # 退
        "\u9001": "\u9001\U000E0101",  # 送
        "\u9003": "\u9003\U000E0102",  # 逃
        "\u9014": "\u9014\U000E0101",  # 途
        "\u9014": "\u9014\U000E0101",  # 途
        "\u901A": "\u901A\U000E0101",  # 通
        "\u901F": "\u901F\U000E0101",  # 速
        "\u9031": "\u9031\U000E0101",  # 週
        "\u9032": "\u9032\U000E0101",  # 進
        "\u9038": "\u9038\U000E0101",  # 逸
        "\u9042": "\u9042\U000E0102",  # 遂
        "\u904B": "\u904B\U000E0101",  # 運
        "\u904E": "\u904E\U000E0101",  # 過
        "\u9053": "\u9053\U000E0101",  # 道
        "\u9054": "\u9054\U000E0101",  # 達
        "\u9055": "\u9055\U000E0102",  # 違
        "\u9060": "\u9060\U000E0101",  # 遠
        "\u9069": "\u9069\U000E0101",  # 適
        "\u9078": "\u9078\U000E0101",  # 選
        "\u907A": "\u907A\U000E0101",  # 遺
        "\u90FD": "\u90FD\U000E0100",  # 都
        "\u9332": "\u9304",  # 録
        "\u9396": "\u9396\U000E0101",  # 鎖
        "\u9592": "\u9592\U000E0101",  # 閒
        "\u9593": "\u9592\U000E0101",  # 間
        "\u968A": "\u968A\U000E0101",  # 隊
        "\u9752": "\u9751",  # 青
        "\u97FF": "\u97FF\U000E0104",  # 響
        "\u983D": "\u9839",  # 頽
        "\u985E": "\u985E\U000E0100",  # 類
        "\u98DF": "\u98DF\U000E0101",  # 食
        "\u98FC": "\u98FC\U000E0101",  # 飼
        "\u98FE": "\u98FE\U000E0101",  # 飾
        "\u9A45": "\u9A45\U000E0101",  # 驅
        "\u9B2A": "\u9B2D\U000E0100",  # 鬪
        "\u9B2D": "\u9B2D\U000E0100",  # 鬭
        "\u9E97": "\u9E97\U000E0101",  # 麗
        "\u9EBB": "\u9EBB\U000E0101",  # 麻
        "\u9F8D": "\u9F8D\U000E0102",  # 龍
        "\uF9D0": "\u985E\U000E0100",  # 類
        "\uFA19": "\u795E\U000E0100",  # 神
        "\uFA38": "\u5668\U000E0101",  # 器
        "\uFA42": "\u65E3",  # 既
        "\uFA50": "\u7956\U000E0101",  # 祖
        "\uFA55": "\u7A81\U000E0101",  # 突
        "\uFA56": "\u7BC0\U000E0102",  # 節
        "\uFA59": "\u7E41\U000E0101",  # 繁
        "\uFA5B": "\u8005\U000E0101",  # 者
        "\uFA5C": "\u81ED\U000E0101",  # 臭
        "\uFA69": "\u97FF\U000E0104",  # 響
    }

    def force(self, filename: str) -> bool:
        """Force 俗字 to 正字. Return True if the file had some 俗字."""
        with open(filename, "r+") as f:
            original_content = content = f.read()
            for (zokuzi, segzi) in SegziForcer.table.items():
                # content = re.sub(
                #     "[{}]+".format("".join(SegziForcer.itaizi_selectors)), "", content,
                # )
                regex = "{}(?:[{}]?)".format(
                    zokuzi, "".join(SegziForcer.itaizi_selectors),
                )
                content = re.sub(regex, segzi, content)
            f.seek(0)
            f.truncate()
            f.write(content)
        return original_content != content


def run(command: str, capture_output=False, text=None) -> subprocess.CompletedProcess:
    """Run command."""
    command = command.strip()
    print("+ ", command)
    env = os.environ.copy()
    return subprocess.run(
        command,
        capture_output=capture_output,
        check=True,
        env=env,
        shell=True,
        text=text,
    )


def task(function):
    """Define a task."""
    if function.__doc__:
        tasks[function.__name__] = function.__doc__

    def wrapper():
        function()

    return wrapper


@task
def format():
    """Format all files."""
    run("poetry run black *.py")
    for filename in glob.glob("*.md"):
        # run(r"perl -i -pe 'use utf8; s/[\\x{E0100}\\x{E0101}]//g' " + quote(filename))
        # run("npx prettier --write {}".format(quote(filename)))
        if SegziForcer().force(filename):
            print(filename, " !")
        else:
            print(filename)


@task
def test():
    """Test."""
    run("poetry check")
    run("npm audit")


@task
def upgrade():
    """Upgrade dependencies."""
    run("npx npm-check-updates -u")
    run("npm install")
    run("npm audit fix")
    run("npm fund")
    run("poetry update")


if __name__ == "__main__":
    if len(sys.argv) == 1 or sys.argv[1] == "help":
        for task_name, describe in tasks.items():
            print(f"{task_name.ljust(16)}\t{describe}")
        exit(0)
    for task_name in sys.argv[1:]:
        locals()[task_name]()

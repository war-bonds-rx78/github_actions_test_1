# import os
import logging
from datetime import datetime
from logging.handlers import TimedRotatingFileHandler
# import psycopg2
import sqlite3
import click

@click.command()
@click.option("--target_file", "-s", default="select.sql", help="実行SQLファイル")
def main(target_file):

    ## ログ設定
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    log_file = "execute.log"
    # TimedRotatingFileHandlerの設定
    handler = TimedRotatingFileHandler(log_file, when="D", interval=1, backupCount=7)
    format_str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    handler.setFormatter(logging.Formatter(format_str))
    logger.addHandler(handler)

    logger.info("Start")
    # 環境変数の値を取得
    # hoge = os.getenv("HOGE")
    # logger.info(hoge)
    ## DB接続
    # DB_CONFIG = {
    #     "dbname": "your_database_name",
    #     "user": "your_username",
    #     "password": "your_password",
    #     "host": "localhost",  # データベースホスト名
    #     "port": 5432          # デフォルトのPostgreSQLポート
    # }
    
    ## 実行SQLファイルの読み込み
    ## パス直下
    # query_1 = ""
    sql_file = "sql/" + target_file
    now = datetime.now()
    formatted_now = now.strftime('%Y%m%d%H%M')
    file_name = "data" + formatted_now + ".csv"
    try:
        with open(sql_file, "r") as f:
            sql = f.read()
    except FileNotFoundError as e:
        logger.error(str(e))
        return
    except Exception as e:
        logger.error(str(e))
        return
    
    try:
        # with psycopg2.connect(**DB_CONFIG) as conn:
            # with conn.cursor() as cur:
        with sqlite3.connect("your_sqlite_file.db") as conn:
            cur = conn.cursor()
            ## SQL実行
            logger.info(f"実行SQL: {sql}")
            cur.execute(sql)
            # cur.execute(sql,(query_1,))
            # fetchone() を使って1行ずつ処理
            while True:
                result = cur.fetchone()
                if result is None:
                    break
                logger.info(f"連携失敗ユニークID: {result[0]}")
                _file_write(logger,file_name, result)
    except Exception as e:
        logger.error(str(e))
        return
    logger.info("End")

def _file_write(logger, file_path, data):
    try:
        with open(file_path, "a") as f :
            write_data = ",".join(map(str, data))
            f.write(write_data+"\n")
    except Exception as e:
        logger.error(str(e))
        return

# データ内容をslackに通知 ※　予定
def _slack_info(logger, data):

    # プロキシ設定
    # slackのBot tokenとチャンネルID
    # WebClientに設定
    # slackに通知
    # 通知成功
    # 通知失敗
    pass

if __name__ == "__main__":
    main()
import sys
import pytest
import sqlite3
import os
from unittest.mock import MagicMock, patch
from datetime import datetime
from click.testing import CliRunner


# プロジェクトのルートディレクトリをsys.pathに追加
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# テスト対象のモジュールをインポート
from sample import main, _file_write


# ログ出力のテスト
@pytest.fixture
def mock_logger():
    with patch('sample.logging.getLogger') as mock_get_logger:
        mock_logger = MagicMock()
        mock_get_logger.return_value = mock_logger
        yield mock_logger


# # DB接続とSQL実行のテスト
# @patch('main.sqlite3.connect')
# @patch('main.open', create=True)  # SQLファイルをモック
# def test_main(mock_open, mock_sqlite_connect, mock_logger):
#     # モックしたSQLファイルの内容
#     mock_open.return_value.__enter__.return_value.read.return_value = "SELECT * FROM some_table"
    
#     # SQLite3接続のモック
#     mock_conn = MagicMock()
#     mock_cursor = MagicMock()
#     mock_conn.cursor.return_value = mock_cursor
#     mock_sqlite_connect.return_value = mock_conn
    
#     # 実行時にファイル書き込み処理が行われることを確認
#     mock_cursor.fetchone.return_value = (1,)  # fetchone()で一行返す
#     mock_cursor.fetchone.return_value = None   # 2回目でNoneを返すことでループ終了
    
#     # 実行
#     main()

#     # ログ出力の確認
#     mock_logger.info.assert_any_call("Start")
#     mock_logger.info.assert_any_call("End")
#     mock_logger.info.assert_any_call("SELECT * FROM some_table")
    
#     # ファイル書き込みの確認
#     mock_open.assert_called_with("data" + datetime.now().strftime('%Y%m%d%H%M') + ".csv", "a")
#     mock_open.return_value.write.assert_called_with("1\n")
    

# ファイル書き込み処理のテスト
@patch('sample.open', create=True)  # ファイル操作をモック
def test_file_write(mock_open):
    mock_file = MagicMock()
    mock_open.return_value.__enter__.return_value = mock_file

    # データの書き込み
    _file_write(mock_file, 'test.csv', (1,'test_data'))

    # ファイル書き込みの確認
    mock_file.write.assert_called_with("1,test_data\n")


# エラーハンドリングのテスト (DB接続時)
@patch('sample.sqlite3.connect', side_effect=sqlite3.DatabaseError("DB Error"))
@patch('sample.logging.getLogger') 
def test_db_connection_error(mock_get_logger, mock_sqlite_connect):
    mock_logger = MagicMock()
    mock_get_logger.return_value = mock_logger
    # CliRunnerを使ってコマンドライン引数を渡す
    runner = CliRunner()
    runner.invoke(main, ["--target_file", "select.sql"])  # コマンドライン引数を渡

    # ロガーの呼び出しを確認
    mock_logger.error.assert_called_with('DB Error')


# エラーハンドリングのテスト (ファイル書き込み時)
@patch('sample.open', side_effect=OSError("File write error"))
@patch('sample.logging.getLogger')
def test_file_write_error(mock_get_logger, mock_open):
    mock_logger = MagicMock()
    mock_get_logger.return_value = mock_logger
    _file_write(mock_logger, 'test.csv', (1,'test_data'))
    # エラーメッセージがログに出力されることを確認
    mock_logger.error.assert_called_with('File write error')
DIALECT = 'mysql'  # 要用的什么数据库
DRIVER = 'pymysql'  # 连接数据库驱动
USERNAME = 'root'  # 用户名
PASSWORD = 'abc12356'  # 密码
HOST = '123.207.8.65'  # 服务器
PORT = '3306'  # 端口
DATABASE = 'chat'  # 数据库名

SQLALCHEMY_DATABASE_URI = '{}+{}://{}:{}@{}:{}/{}?charset=utf8'.format(DIALECT, DRIVER, USERNAME, PASSWORD, HOST, PORT, DATABASE)
SQLALCHEMY_TRACK_MODIFICATIONS = True

SECRET_KEY = 'your_secret_key_here'
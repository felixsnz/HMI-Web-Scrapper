import configparser
# Read database configuration
config = configparser.ConfigParser()
config.read('config.ini')

host = config['sql']['host']
database = config['sql']['database']
user = config['sql']['user']
password = config['sql']['password']
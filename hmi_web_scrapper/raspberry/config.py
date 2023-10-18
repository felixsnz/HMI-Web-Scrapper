import configparser
# Read database configuration
config = configparser.ConfigParser()
config.read('config.ini')

ip_address = config['raspberry']['ip']

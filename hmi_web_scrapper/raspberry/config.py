import configparser
# Read database configuration
config = configparser.ConfigParser()
config.read('/home/felix/projects/hmi_web_scrapper/config.ini')

ip_address = config['raspberry']['ip']

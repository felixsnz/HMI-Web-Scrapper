from utils.singleton import Singleton
import configparser
import threading

# Read database configuration
config = configparser.ConfigParser()
config.read('/home/felix/projects/hmi_web_scrapper/config.ini')

host = config['sql']['host']
database = config['sql']['database']
user = config['sql']['user']
password = config['sql']['password']

class ScrapperSingleton(Singleton):
    curr_e_standard = None
    lock = threading.Lock()
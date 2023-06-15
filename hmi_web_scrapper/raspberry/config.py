import socket
import netifaces as ni

ip_address = ni.ifaddresses('eth0')[ni.AF_INET][0]['addr']

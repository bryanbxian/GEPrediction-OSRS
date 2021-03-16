from bs4 import BeautifulSoup # BeautifulSoup is in bs4 package 
import requests

trade_url = 'https://secure.runescape.com/m=itemdb_oldschool/top100?list=0'
content = requests.get(trade_url)

print(content.text)

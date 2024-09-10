import sys
import requests

csv = {'data': ('my_table', open('/data/out/REG.txt', 'r'))}
host = 'http://localhost:9000'
csv1 = {'data': ('my_table', open('/data/out/RF.txt', 'r'))}
try:
    response = requests.post(host + '/imp', files=csv)
    print(response.text)
except requests.exceptions.RequestException as e:
    print(f'Error: {e}', file=sys.stderr)
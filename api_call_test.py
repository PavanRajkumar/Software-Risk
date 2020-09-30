# Author : Richard Delwin Myloth
import requests
from subprocess import check_output
from json import dumps

API_URL = "http://127.0.0.1:5000/"

Headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}

bash_cmd = 'git log -1 --pretty=format:"%an%n%s%n" --shortstat'
stdout = check_output(bash_cmd.split()).decode('utf-8').rstrip('\n')

content = dumps({"latest_commit": stdout})

response = requests.post(
    '{}/predict/'.format(API_URL),
    data=content,
    headers=Headers,
)

print(response.text)
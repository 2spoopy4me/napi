from flask import Flask
import psutil
from pprint import pprint as p
import json


app = Flask(__name__)

@app.route('/interfaces', methods=['GET'])

def get_interfaces():
    '''Returns JSON output of system's network interfaces'''
    interfaces = psutil.net_if_addrs()
    return json.dumps( list(interfaces.keys()) )


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=105)
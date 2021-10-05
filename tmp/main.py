from host import host
from client import client
import subprocess


subprocess.run('python3 host.py & python3 client.py', shell=True)
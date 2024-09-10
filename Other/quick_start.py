import subprocess
import time
import os

command = "start cmd /k python "
to_run = ["server.py", "client.py", "client.py"]
server : subprocess.Popen = None 

for app in to_run:
    path = os.path.join(os.getcwd(), app)
    
    full_command = command + "\"" + path + "\""
    print("running command", full_command)
    
    process = subprocess.Popen(full_command, shell=True)
    if app == "server.py":
        server = process
    # process.wait()

while(True):
    time.sleep(1)
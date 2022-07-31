import json
import time


print("ready")

while True:
    time.sleep(5)
    status = json.loads(input())
    if "start" in status["available_commands"]:
        print("start ironclad")
    else:
        print("state")

import requests
import json

if __name__ == '__main__':

    entries = []

    for i in range(4):
        #response = requests.get("http://6857simon.csail.mit.edu/?num=10000")
        response = requests.get("http://127.0.0.1:3000/?num=10000")
        print("Got response from {}".format(i))
        entries.extend(json.loads(response.content))

    with open("test_samples.json", "w") as f:
        f.write(json.dumps(entries))

    print(len(entries))

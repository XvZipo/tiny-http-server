import json
import sys
code = 200
status = "OK"

headers = {
    "Content-Type": "application/json;charset=utf-8"
}

# if POST method get body from argv
payload = ""
if len(sys.argv) > 1:
    payload = sys.argv[1]


data = {
    "key": payload
}

response = {
    "code": code,
    "status": status,
    "headers": headers,
    "data": json.dumps(data)
}


print(json.dumps(response))
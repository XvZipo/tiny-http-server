import json
import sys
code = 200
status = "OK"

headers = {
    "Content-Type": "application/json;charset=utf-8"
}

# if POST method get request body from argv
payload = "hello World!"
if len(sys.argv) > 1:
    payload = sys.argv[1]


msg = {
    "key": payload
}

response = {
    "code": code,
    "status": status,
    "headers": headers,
    "data": json.dumps(msg)
}

print(json.dumps(response))

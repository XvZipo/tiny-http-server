# coding:utf-8

import socket
from multiprocessing import Process
import subprocess
import sys
import json
import time


def implemented(client, request_data):
    request_method = method(request_data)
    if not request_method == 'GET':
        if not request_method == 'POST':
            message(client, '405', 'Method Not Allowed', "only GET and POST was permitted", headers={})
            return False
    return True


def method(request_data):
    data = str(request_data, encoding="utf-8").split(' ')
    return data[0]


def path(request_data):
    data = str(request_data, encoding="utf-8").split(' ')
    return data[1]


def body(request_data):
    data = str(request_data, encoding="utf-8").split('\r\n\r\n')
    data = data[-1]
    data = data.replace(" ", "").replace("\n", "").replace("\r", "")
    return json.dumps(data)


def message(client, status_code, status, msg, headers):
    # create response data
    response_start_line = "HTTP/1.1 "+str(status_code)+" "+str(status)+"\r\n"
    response_headers = "Server: mini server\r\n"
    for key in headers:
        response_headers = response_headers + key+":"+" "+headers[key]+"\r\n"
    response_body = msg
    response = str(response_start_line) + str(response_headers) + str("\r\n") + str(response_body) + str("\r\n")

    # send response data
    local_time = str(time.ctime())
    print(local_time + " response data:\n", response, "\n\n\n")
    client.sendall(bytes(response, "utf-8"))

    client.close()


def handle_client(client):
    request_data = client.recv(1024)
    request_method = method(request_data)
    request_payload = ""
    if request_method == "POST":
        request_body = body(request_data)
        request_payload = " " + request_body
    local_time = str(time.ctime())
    print(local_time + " request data:", request_data)
    if not implemented(client, request_data):
        return
    script = path(request_data)[1:]
    # execute python3 script
    res = subprocess.Popen(["python3 "+script+".py" + request_payload],
                           shell=True,
                           stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE)
    while res.poll() is None:
        msg = res.stdout.readlines()
        for i in range(len(msg)):
            msg[i] = str(msg[i], encoding="utf-8")
        try:
            response = json.loads(str(''.join(msg)))
        except:
            message(client, 500, "Internal Server Error", "script Error or Nothing was return from script",
                    headers={})
            return
    message(client, response["code"], response["status"], response["data"], response["headers"])
    return


if __name__ == "__main__":
    listen_address = str(sys.argv[1])
    port = int(sys.argv[2])
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((listen_address, port))
    server_socket.listen(128)
    print("start server...")
    while True:
        client_socket, client_address = server_socket.accept()
        print("[%s]request:", client_address)
        handle_client_process = Process(target=handle_client, args=(client_socket,))
        handle_client_process.start()
        client_socket.close()

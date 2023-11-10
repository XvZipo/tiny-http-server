# tiny-http-server
A mini HTTP server by python  



### Use Tips:


Run directly
```commandline
python3 tiny_server.py 0.0.0.0 9973
```


Run in the background

```commandline
nohup python3 tiny_server.py 0.0.0.0 9973 > tiny_server.log 2>&1 &
```


Client Test
```commandline
curl http://127.0.0.1:9973/api/helloWorld 
```



### Add script Tips

- create script in the api folder
- script name also is request path
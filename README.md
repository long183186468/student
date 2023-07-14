# student
用来自己学习
主要是研究使用chatglm-6b模型与群晖chat机器人之间的通讯，从而实现在群晖chat下使用本地化部署的chatglm-6b模型
2023-7-14测试实验后，在代码运行后的结果如下

Loading checkpoint shards: 100%|████████████████████████████████████████████████████████████████████████████████████| 8/8 [00:11<00:00,  1.38s/it]
INFO:     Started server process [25766]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://192.168.0.176:8000 (Press CTRL+C to quit)
INFO:     192.168.0.251:52406 - "POST / HTTP/1.1" 200 OK
INFO:     192.168.0.251:52414 - "POST / HTTP/1.1" 200 OK
INFO:     192.168.0.251:52424 - "POST / HTTP/1.1" 200 OK
INFO:     192.168.0.251:52446 - "POST / HTTP/1.1" 200 OK
INFO:     192.168.0.251:52452 - "POST / HTTP/1.1" 200 OK
INFO:     192.168.0.251:52454 - "POST / HTTP/1.1" 200 OK
INFO:     192.168.0.251:52460 - "POST / HTTP/1.1" 200 OK
INFO:     192.168.0.251:52462 - "POST / HTTP/1.1" 200 OK
INFO:     192.168.0.251:52470 - "POST / HTTP/1.1" 200 OK
INFO:     192.168.0.251:52472 - "POST / HTTP/1.1" 200 OK

但是在群晖chat中就是没有回复

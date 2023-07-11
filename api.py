import requests
import json
from fastapi import FastAPI, Request
from transformers import AutoTokenizer, AutoModel
import uvicorn
import datetime
import torch

DEVICE = "cuda"
DEVICE_ID = "0"
CUDA_DEVICE = f"{DEVICE}:{DEVICE_ID}" if DEVICE_ID else DEVICE

def torch_gc():
    if torch.cuda.is_available():
        with torch.cuda.device(CUDA_DEVICE):
            torch.cuda.empty_cache()
            torch.cuda.ipc_collect()

app = FastAPI()

API_URL = "https://192.168.0.251:5556/webapi/entry.cgi?api=SYNO.Chat.External&method=chatbot&version=2&token=%225nrlba3Ax7gffKX1c59D2zfnUSEAPA6t5Oi28ronYSJ0PfkCsBvrJl6nQemlmkD4%22"

@app.post("/")
async def create_item(request: Request):
    global model, tokenizer
    json_post_raw = await request.json()
    json_post = json.dumps(json_post_raw)
    json_post_list = json.loads(json_post)
    prompt = json_post_list.get('prompt')
    history = json_post_list.get('history')
    max_length = json_post_list.get('max_length')
    top_p = json_post_list.get('top_p')
    temperature = json_post_list.get('temperature')
    
    payload = {
        "text": prompt,
        "user_ids": [5]  # 根据需要指定要发送消息的用户ID
    }
    
    headers = {
        "Content-Type": "application/json"
    }
    
    response = requests.post(API_URL, data=json.dumps(payload), headers=headers)
    
    if response.status_code == 200:
        response_data = response.json()
        # 处理API的响应数据，根据需要提取相关信息
        response_text = response_data.get("text")
        history = response_data.get("history")
        
        now = datetime.datetime.now()
        time = now.strftime("%Y-%m-%d %H:%M:%S")
        answer = {
            "response": response_text,
            "history": history,
            "status": 200,
            "time": time
        }
        log = "[" + time + "] " + '", prompt:"' + prompt + '", response:"' + repr(response_text) + '"'
        print(log)
        torch_gc()
        return answer
    else:
        # 处理发送消息时的错误情况
        # 可以根据具体需求添加适当的错误处理逻辑
        return {"error": "发送消息时出错，错误代码：" + str(response.status_code)}

if __name__ == '__main__':
    tokenizer = AutoTokenizer.from_pretrained("THUDM/chatglm-6b", trust_remote_code=True)
    model = AutoModel.from_pretrained("THUDM/chatglm-6b", trust_remote_code=True).half().cuda()
    model.eval()
    uvicorn.run(app, host='0.0.0.0', port=8000, workers=1)

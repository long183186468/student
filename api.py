import requests
from fastapi import FastAPI, Request
from transformers import AutoTokenizer, AutoModel
import uvicorn
import torch
import json
import datetime

app = FastAPI()

DEVICE = "cpu"
tokenizer = AutoTokenizer.from_pretrained("/home/jianglong/chatglm2/chatglm_model/chatglm-6b", trust_remote_code=True)
model = AutoModel.from_pretrained("/home/jianglong/chatglm2/chatglm_model/chatglm-6b", trust_remote_code=True)
model.to(DEVICE)
model.eval()


def generate_gpt_response(prompt, history, max_length, top_p, temperature):
    response, history = model.chat(tokenizer,
                                   prompt,
                                   history=history,
                                   max_length=max_length if max_length else 2048,
                                   top_p=top_p if top_p else 0.7,
                                   temperature=temperature if temperature else 0.95)
    return response, history


def send_outgoing_message(user_id, message):
    url = "https://192.168.0.251:5556/webapi/entry.cgi"
    payload = {
        "api": "SYNO.Chat.External",
        "method": "chatbot",
        "version": "2",
        "token": "kuGsbHDhv2gjcuFeJ32DkKk6bMsLqY0bzpfYpx2jHsAaQsuw8w6CU59ri4Qhzhji",
        "user_id": user_id,
        "text": message
    }

    response = requests.post(url, params=payload, verify=False)

    # 检查响应状态码
    if response.status_code == 200:
        print("传出消息已成功发送")
    else:
        print("发送传出消息时出现错误")
        print(f"错误代码: {response.status_code}")


@app.post("/")
async def create_item(request: Request):
    global model, tokenizer
    try:
        json_post = await request.json()
        prompt = json_post.get('prompt')
        history = json_post.get('history')
        max_length = json_post.get('max_length')
        top_p = json_post.get('top_p')
        temperature = json_post.get('temperature')

        response, history = generate_gpt_response(prompt, history, max_length, top_p, temperature)

        now = datetime.datetime.now()
        time = now.strftime("%Y-%m-%d %H:%M:%S")

        answer = {
            "response": response,
            "history": history,
            "status": 200,
            "time": time
        }

        log = f"[{time}] prompt: {prompt}, response: {response}"
        print(log)

        # 发送传出消息
        user_id = json_post.get('user_id')
        send_outgoing_message(user_id, response)

        return answer

    except Exception as e:
        return {"error": str(e)}


if __name__ == '__main__':
    uvicorn.run(app, host='192.168.0.176', port=8000, workers=1)

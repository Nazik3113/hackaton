from fastapi import FastAPI
from pydantic import BaseModel
import requests
import json 
from random import choice

app = FastAPI()

# Константа с токенами chatgpt3
CHAT_GPT_TOKENS = ["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", "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"]

# Класс-форма json для Auto.ria
class AutoItem(BaseModel):
    gearbox: str
    drive: str
    isDamaged: bool
    isAbroad: bool
    price: int
    currency: str
    brand: str
    model: str
    year: int
    run: int
    engineType: str
    engineCP: int
    colour: str
    city: str
    isTradable: bool
    description: str

def getChatGptResponse(questionFilename:str, text:str) -> json:
    """ Функция принимающая название файла с запросом к chatgpt3 и текстом комментария с формы"""
    # Читаем запрос и заменяем {text} на комментарий
    with open(questionFilename) as file:
        question = file.read().replace("{text}", text.lower(), 1)
    
    # Отпраляем запрос и принимаем необработаный json ответ
    answer = requests.post("https://api.openai.com/v1/chat/completions",
                      headers ={"Content-Type":"application/json; charset=utf-8",
                                "Authorization":f"Bearer {choice(CHAT_GPT_TOKENS)}"},
                        json = {"model":"gpt-3.5-turbo",
                                "messages": [
                                    {"role":"user",
                                     "content":question}
                                     ],
                                     "temperature":0.2
                                     })
    return json.loads(json.loads(answer.text)["choices"][0]["message"]["content"])

@app.post("/auto/")
async def compareFieldsToDescription(item: AutoItem):
    item_json = json.loads(item.model_dump_json())
    answer_json = getChatGptResponse("auto_question.txt", item.description)
    compareResult = {"status":0, "errors": []}

    for key in item_json.keys():
        if type(item_json[key]) == str:
            item_json[key] = item_json[key].lower()
            
    for key in answer_json.keys():
        if type(answer_json[key]) == str:
            answer_json[key] = answer_json[key].lower() 

    for key in answer_json.keys():
        if answer_json[key] is not None and answer_json[key] != item_json[key]:
            compareResult["errors"].append(key)

    if len(compareResult["errors"]) == 0:
        compareResult.pop("errors")
        compareResult["status"] = 1

    return compareResult
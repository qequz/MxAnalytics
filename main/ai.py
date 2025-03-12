from openai import OpenAI
import os
from dotenv import load_dotenv, find_dotenv
import logging


logging.basicConfig(level = logging.INFO)

load_dotenv(find_dotenv())


"""14-33 строки взяты с https://openrouter.ai"""

client = OpenAI(
  base_url = "https://openrouter.ai/api/v1",
  api_key = os.getenv("AI_TOKEN"),
)


def gpt_verdict(*, chat_messages):
  attempt = 0
  while attempt < 5:
    prompt = f"Если человек в данном сообщении отказывается пойти с нами куда-нибудь, например, гулять, выведи True, во всех остальных случаях выведи False. Отвечать мне что-либо кроме True или False СТРОГО ЗАПРЕЩЕНО: {chat_messages}"
    completion = client.chat.completions.create(
      model="deepseek/deepseek-chat:free",
      messages=[
        {
          "role": "user",
          "content": prompt
        }
      ]
    )
    gpt_answer = completion.choices[0].message.content # получаем ответ из гпт (может нести чушь=невалидный ответ)

    if gpt_answer in ["True", "False"]:
      result_bool = gpt_answer == "True"

      logging.info("ответ валидный")

      return result_bool
    else:
      logging.info("ответ не валидный")
      attempt += 1
  else:
    logging.info("за 5 ретраев валидный ответ не получен - автоскип")


def vote(*, maks_messages_from_tg):
  result_list = []
  true_count = 0
  false_count = 0
  while len(result_list) < 3:
    a = gpt_verdict(chat_messages=maks_messages_from_tg)
    result_list.append(a)
    if len(result_list) == 2 and result_list[0] == result_list[1]:# чтобы не делать 3ий запрос
      logging.info("2 одинаковых ретрая")
      return result_list[0]
    if a:
      true_count += 1
    if a == False:#не юзаю else, неправильно с ним работает хз поч
      false_count += 1
  if true_count > false_count:
    return True
  else:
    return False


print(vote(maks_messages_from_tg = "Прохладно на улице"))
import os
from openai import AsyncOpenAI
from dotenv import load_dotenv


# load_dotenv()


# async def start_gpt(client):
    
    
    
    
    
#     ruls = 'Напиши благодарственный ответ на отзыв к покупке на маркетплейсе от имени продавца.Ответ должен соответствовать следующим критериям - ответ не должен содержать заполнители, параметры для вставки (наприер {имя клиента|компания} и т.п.); - клиент имеет женский пол; - не должен содержать информацию от кого этот ответ(например: "Команда продавцов" - такого не должно быть в ответе); - не должно быть предложение клиенту об обмене товара или какой-то компенсации. Пример ответа: Здравствуйте. Спасибо за то, что выбрали нас. Позвольте поблагодарить Вас за отзыв. Мы очень рады, что Вам подошел Наш товар, носите с удовольствием. Будем рады видеть Вас снова. Приятных покупок!  Дальше я передаю сам ответ покупателя:   '
#     user_question = ''
#     answer = ''
#     url = "https://feedbacks-api.wildberries.ru/api/v1/feedbacks"
#     headers = {
#         'Authorization': api_key,  
#     }
#     for key in massive:
#         user_question = key
#         try:
#             chat_completion = client.chat.completions.create(
#                     messages=[
#                         {
#                             "role": "user",
#                             "content": ruls + user_question,
#                         }
#                     ],
#                     model="gpt-3.5-turbo",
#                 )
            
#             answer = chat_completion.choices[0].message.content
#             data = {
#                 'id': massive[key],        
#                 'text': answer   
#             }
#             response = requests.patch(url, json=data, headers=headers)
#             if response.status_code == 200: return True
#         except Exception as e: print(1)

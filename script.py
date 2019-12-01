import requests  
import datetime

class BotHandler:

    def __init__(self, token):
        self.token = token
        self.api_url = "https://api.telegram.org/bot{}/".format(token)

    def get_updates(self, offset=None, timeout=5):
        method = 'getUpdates'
        params = {'timeout': timeout, 'offset': offset}
        resp = requests.get(self.api_url + method, params)
        result_json = resp.json()['result']
        return result_json

    def send_message(self, chat_id, text):
        params = {'chat_id': chat_id, 'text': text}
        method = 'sendMessage'
        resp = requests.post(self.api_url + method, params)
        return resp

    def get_last_update(self):
        get_result = self.get_updates()

        if len(get_result) > 0:
            last_update = get_result[-1]
        else:
            last_update = None

        return last_update

## TOKEN - INSERT YOUR TOKEN HERE
token = "967673574:AAGhnK76sG-yssLonUS6rVIKJCv-XeB8SKE"
greet_bot = BotHandler(token)  
greetings = ('здравствуй', 'привет', 'ку', 'здорово')  
now = datetime.datetime.now()
token1 = "c8aadb552db2d2c75bc938bd266daeea1f5262e25aaed8ba06895e2c427f4455"

def registration(user_id, full_name):
        api_url = 'http://jacob.slezins.ru/methods/index.php'
        params = {'id_telegram' : user_id, 'fullname' : full_name, 'token' : token1}
        resp = requests.get(api_url, params)
        result_json = resp.status_code
        return result_json
    
def signUp(user_id):
        api_url = 'http://jacob.slezins.ru/methods/index.php'
        params = {'id_telegram' : user_id, 'token' : token1}
        resp = requests.get(api_url, params)
        result_json = resp.status_code
        
        return result_json
    
def get_marks(user_id):
        api_url = 'http://jacob.slezins.ru/methods/index.php'
        params = {'id_telegram' : user_id, 'token' : token1}
        resp = requests.get(api_url, params)
        result_json = resp.json()['response']
        return result_json
    
def main():  
    new_offset = None
    today = now.day
    hour = now.hour

    flag_registration = False
    full_name = ""
    
    while True:
        greet_bot.get_updates(new_offset)
        
        last_update = greet_bot.get_last_update()
        if not last_update:
            continue
        last_update_id = last_update['update_id']
        last_chat_text = last_update['message']['text']
        last_chat_id = last_update['message']['chat']['id']
        last_chat_name = last_update['message']['chat']['first_name']
        last_chat_user_id = last_update['message']['from']['id']
        
        if flag_registration == True:
            code = registration(last_chat_user_id, last_chat_text)
            if code == 200:
                greet_bot.send_message(last_chat_id, 'Регистрация прошла успешно')
                flag_registration = False
            if code == 400:
                greet_bot.send_message(last_chat_id, 'ФИО не найдены, введите /sighUp, чтобы повторить')
                flag_registration = False
            if code == 500:
                greet_bot.send_message(last_chat_id, 'Ошибка сервера, введите /sighUp, чтобы повторить')
                flag_registration = False
        
        if last_chat_text == "/signUp":
            code = signUp(last_chat_user_id)
            if code == 401:
                greet_bot.send_message(last_chat_id, 'Введите ФИО в формате:\nФамилия Имя Отчество')
                flag_registration = True
            else:
                greet_bot.send_message(last_chat_id, 'Вы уже зарегистрированы')

                
        if last_chat_text.lower() == "/marks":
            marks = get_marks(last_chat_user_id)['marks']
            marks_string = ""
            for mark in marks:
                marks_string = marks_string + mark['task_name'] + ' - ' + mark['mark'] + '\n'
            greet_bot.send_message(last_chat_id, '{}'.format(last_chat_name) + ', твои оценки:\n' + marks_string)
        
        if last_chat_text.lower() in greetings and today == now.day and 6 <= hour < 12:
            greet_bot.send_message(last_chat_id, 'Доброе утро, {}'.format(last_chat_name))
##            today += 1

        elif last_chat_text.lower() in greetings and today == now.day and 12 <= hour < 17:
            greet_bot.send_message(last_chat_id, 'Добрый день, {}'.format(last_chat_name))
##            today += 1

        elif last_chat_text.lower() in greetings and today == now.day and 17 <= hour < 23:
            greet_bot.send_message(last_chat_id, 'Добрый вечер, {}'.format(last_chat_name))
##            today += 1

        new_offset = last_update_id + 1

if __name__ == '__main__':  
    try:
        main()
    except KeyboardInterrupt:
        exit()
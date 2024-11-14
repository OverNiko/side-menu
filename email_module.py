import logging
import requests
import random
import string
from bs4 import BeautifulSoup

# Настройка логирования
logging.basicConfig(filename='email_manager.log', level=logging.DEBUG, 
                    format='%(asctime)s - %(levelname)s - %(message)s', 
                    encoding='utf-8')

API = 'https://www.1secmail.com/api/v1/'
domain_list = ["1secmail.com", "1secmail.org", "1secmail.net"]
domain = random.choice(domain_list)


class EmailManager:
    def __init__(self):
        self.mail = ""
        self.seen_ids = set()
        logging.info("EmailManager инициализирован")

    def generate_username(self):
        """Генерация уникального имени пользователя."""
        name = string.ascii_lowercase + string.digits
        username = ''.join(random.choice(name) for _ in range(10))
        logging.debug(f"Сгенерированное имя пользователя: {username}")
        return username

    def check_mail(self, mail=''):
        """Проверка почты на наличие новых сообщений."""
        logging.info(f"Проверка почты для адреса: {mail}")
        req_link = f'{API}?action=getMessages&login={mail.split("@")[0]}&domain={mail.split("@")[1]}'
        logging.debug(f"Запрос к API: {req_link}")

        try:
            response = requests.get(req_link).json()
        except Exception as e:
            logging.error(f"Ошибка при запросе к API: {e}")
            return "Ошибка при проверке почты."

        if len(response) > 0:
            new_messages = []

            for message in response:
                message_id = message.get('id')
                if message_id not in self.seen_ids:
                    msg_data = self.get_message_data(mail, message_id)
                    if msg_data:
                        parsed_message = self.parse_message(msg_data)
                        new_messages.append(parsed_message)
                        self.seen_ids.add(message_id)

            result = "\n".join(new_messages)
            logging.info(f"Результат проверки почты: {result}")
            return result
        else:
            logging.info("Нет новых сообщений.")
            return "Нет новых сообщений."

    def get_message_data(self, mail, message_id):
        """Получение данных сообщения по ID."""
        read_msg = f'{API}?action=readMessage&login={mail.split("@")[0]}&domain={mail.split("@")[1]}&id={message_id}'
        logging.debug(f"Чтение сообщения с ID: {message_id} - запрос: {read_msg}")

        try:
            response = requests.get(read_msg).json()
            return response
        except Exception as e:
            logging.error(f"Ошибка при чтении сообщения: {e}")
            return None

    def parse_message(self, msg_data):
        """Парсинг сообщения."""
        text = msg_data.get('htmlBody', '')
        if not isinstance(text, str):
            text = ''
        soup = BeautifulSoup(text, 'html.parser')

        sender = msg_data.get('from', 'Неизвестно')
        subject = msg_data.get('subject', 'Без темы')
        content = soup.get_text(separator="\n", strip=True)

        confirm_link = soup.find('a', string="Подтвердить мою учетную запись")
        confirm_link = confirm_link['href'] if confirm_link else "Ссылка для подтверждения не найдена."

        parsed_message = f'От: {sender}\nТема: {subject}\nСодержание:\n{content}\nСсылка для подтверждения: {confirm_link}\n'
        logging.debug(f"Парсинг сообщения: {parsed_message}")
        return parsed_message

    def delete_mail(self, mail=''):
        url = 'https://www.1secmail.com/mailbox'
        data = {
            'action': 'deleteMailbox',
            'login': mail.split('@')[0],
            'domain': mail.split('@')[1]
        }
        r = requests.post(url, data=data)
        logging.info(f'[X] Почтовый адрес {mail} - удален!')

    def change_email(self):
        """Сменить адрес электронной почты."""
        username = self.generate_username()
        self.mail = f'{username}@{domain}'
        new_email_msg = f'[+] Новый почтовый адрес: {self.mail}'
        logging.info(new_email_msg)
        return new_email_msg

    def main(self, command):
        """Основная функция для управления почтой."""
        try:
            if not self.mail:
                username = self.generate_username()
                self.mail = f'{username}@{domain}'

            if command == "change":
                self.delete_mail(mail=self.mail)
                return self.change_email()
            elif command == "del":
                self.delete_mail(mail=self.mail)
            elif command == "check":
                return self.check_mail(mail=self.mail)
            elif command == "start":
                return f'{self.mail}'

        except KeyboardInterrupt:
            self.delete_mail(mail=self.mail)
            logging.warning('Программа прервана!')

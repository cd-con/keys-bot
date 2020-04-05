
import requests
import pyodbc
import random
import bs4 as bs4
print('Бот вот-вот будет готов...')
import settings as s
connStr = (s.connParm)
tables = 0
try:
    cnxn = pyodbc.connect(connStr)
except:
    exit('NullBase error: Base not found!')
crsr = cnxn.cursor()
cnxn.autocommit = True
key =''

class VkBot:

    def __init__(self, user_id):
        self._USER_ID = user_id
        self._USERNAME = self._get_user_name_from_vk_id(user_id)

        self._COMMANDS = ["ПРИВЕТ", "ХАЙ", "ПРИВ", "ПОКА", "КЛЮЧ", "КОМАНДЫ"]

    def _get_user_name_from_vk_id(self, user_id):
        request = requests.get("https://vk.com/id"+str(user_id))
        bs = bs4.BeautifulSoup(request.text, "html.parser")

        user_name = self._clean_all_tag_from_str(bs.findAll("title")[0])

        return user_name.split()[0]
    def new_message(self, message, userid):

        # Привет
        if message.upper() == self._COMMANDS[0] or  message.upper() == self._COMMANDS[1] or message.upper() == self._COMMANDS[2]:
            return s.welcomeMsg


        # Время
        elif message.upper() == self._COMMANDS[5]:
            return s.commandList

        # Пока
        elif message.upper() == self._COMMANDS[3]:
            return s.byeMsg
        #Уничтожение
        elif message.upper() == self._COMMANDS[4]:
                try:
                    ava = []
                    crsr.execute('SELECT user FROM got')
                    rows = crsr.fetchall()
                    for row in rows:
                        if str(userid) in row.user:
                            return s.gotKeyMsg
                            break
                    crsr.execute("""
                                   SELECT key, used
                                   FROM keys
                                   """)
                    rows = crsr.fetchall()
                    for row in rows:
                        if str(row.used) =='False':
                            ava = ava+[row.key]
                    crsr.execute("INSERT INTO got VALUES (%s ,'%s');" %((random.randint(0, 2048),userid)))
                    crsr.execute("UPDATE keys SET used = true WHERE key = ('%s') " % ava[len(ava)-(len(ava)-1)])
                    return s.giveKeyMsg+str(ava[len(ava) - (len(ava) - 1)])
                except:
                     return s.errMsg
        else:
           return "Беды с башкой? Введи 'команды' (без кавычек)"

    @staticmethod
    def _clean_all_tag_from_str(string_line):

        """
        Очистка строки stringLine от тэгов и их содержимых
        :param string_line: Очищаемая строка
        :return: очищенная строка
        """

        result = ""
        not_skip = True
        for i in list(string_line):
            if not_skip:
                if i == "<":
                    not_skip = False
                else:
                    result += i
            else:
                if i == ">":
                    not_skip = True

        return result


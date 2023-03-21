import pymysql
import re
from config import host, user, password, db_name

def isfloat(value:str):
    """Эта функция для определения типа float для метода insert_into
    value : str"""

    try:
        float(value)
        return True
    except ValueError:
        return False
class SQL():

    def __init__(self):
        try:
            connect = pymysql.connect(
                host=host,
                user=user,
                port=3306,
                password=password,
                database=db_name,
                cursorclass=pymysql.cursors.DictCursor)
            print('All Done!')

        except Exception as ex:
            print('[INFO] Error while working with MySQL', ex)


        self.connect = connect


    def select_version(self):
        """"Отображает текущую версию MySQL"""

        with self.connect.cursor() as cursor:

            cursor.execute("SELECT version();")
            print(f'Server version: {cursor.fetchone()}')

    def select_all(self, table: str):
        select = {}
        n = 1
        with self.connect.cursor() as cursor:

            cursor.execute('select * from {}'.format(table))
            rows = cursor.fetchall()

            for row in rows:
                select[n] = row
                n += 1
            n = 1

        return select

    def insert_into(self, table: str, columns: str, values: list):
        """"Вставляет значения (values) в колонки (columns) в таблице (table)
        table: str - название таблицы
        columns: str - название колонок через пробел
        values lists in list - каждая строка значений должна быть в отдельном списке"""
        self.table = table
        self.columns = columns
        self.values = values
        columns = columns.split()
        columns = ','.join(columns)
        lst_values = values

        with self.connect.cursor() as cursror:

            for element in lst_values:

                string = ''
                count = 0

                for i in element:
                    count += 1
                    if isfloat(i):
                        string += f'{i}'
                    elif len(i) == 0:
                        string += 'Null'
                    elif (len(i) == 11 and i.count('-') == 3) or not i.isdigit():
                        string += f'"{i}"'
                    else:
                        string += f'{i}'
                    if count != len(element):
                        string += ','



                insert_query = f'INSERT INTO {table} ({columns}) VALUES({string});'
                cursror.execute(insert_query)
                self.connect.commit()

                info_message = f'в таблицу {table} c колонками {columns} добавлены значения: {insert_query}\n'

                info_message += info_message

        return info_message


    def update(self,table: str):
        """""Функция для изменения значения в таблице

        table : str - название таблицы"""
        answer = ['y', 'n']
        check_where = ''

        print('Добавить условие для изменения? (Y/N)\n Внимание!! '
        '\n Если не добавить условие, будут изменены все значения в выбранной колонке')

        while check_where not in answer:
            check_where = input('Ответьте пожалуйста, "Y" или "N" ').lower()
        with self.connect.cursor() as cursor:

            cursor.execute(f'select * from {table};')
            row = cursor.fetchall()
            columns_list = row[2].items()

            print('Доступны колонки: ')
            for col, val in columns_list:
                print(f'{col} - {type(val)}')

        column =input('Введите название колонки для изменения: ')

        value = input('Введите значение\n'
                      '(Если это текст введите в двойных кавычках, например: "Это текст")\n'
                      '(Если это дата то в двойных кавычках в формате "гггг-мм-дд") ')


        with self.connect.cursor() as cursor:
            update_query = f'UPDATE {table} set {column}={value}'

            if check_where == 'y':

                update_where = f'WHERE {input("Введите название колонки или выражение для условия: ")}  {input("Введите условие: ")}'
                update_query += ' ' + update_where
            cursor.execute(update_query)
            self.connect.commit()
            print('Принято новое значение для значение: {} = {} '.format(column, value))
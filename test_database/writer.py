from database import DB
import json


class Writer:

    def __init__(self):
        self.db_writer = DB()

    def action(self):

        with open('data.json', 'r', encoding='utf-8') as file:
            data = json.load(file)

            for note in data:
                new_line = [str(note['tag']), str(note['brand']), str(note['name']), str(note['price']), str(note['specifications'])]
                self.db_writer.insert_into_db(new_line)

    def read_info(self):

        data = self.db_writer.read_db()

        for note in data:
            print(note)



if __name__ == '__main__':
    Banggood = Writer()
    Banggood.action()
    Banggood.read_info()

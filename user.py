# This Python file uses the following encoding: utf-8

class User:
    def __init__(self, email, password, first, last):
        self.email = email
        self.password = password
        self.first = first
        self.last = last
        with open('txt/user_count.txt', 'r+') as f:
            user_count = int(f.read())
            self.userID = user_count + 1
            f.seek(0)
            f.write(str(self.userID))
            f.truncate()
        print('{} nolu kullanici yaratildi'.format(self.userID))

    def printout(self):
        return '{} {} {} {} {}'.format(self.userID, self.first, self.last, self.email, self.password)



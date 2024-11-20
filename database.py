# database.py

class Database:
    def __init__(self):
        self.paiements = {}

    def add_payment(self, user, amount):
        if user not in self.paiements:
            self.paiements[user] = 0
        self.paiements[user] += amount

    def get_payments(self, user):
        return self.paiements.get(user, 0)

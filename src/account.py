from exceptions import NotEnoughBalanceError, FinanceOperationError

class Account:
    total_accounts = 0
    operation_tax = None

    def __init__(self, client, ag, number):
        self.__balance = 0
        self.__ag = 0
        self.__number = 0
        self.withdraws_blocked = 0
        self.transfers_blocked = 0
        self.client = client
        self.__set_ag(ag)
        self.__set_number(number)

        Account.total_accounts += 1
        Account.operation_tax = 30 / Account.total_accounts

    @property
    def ag(self):
        return self.__ag

    def __set_ag(self, ag):
        if (not isinstance(ag, int)):
            raise TypeError('Attribute must be an integer', ag)
        if (ag <=0):
            raise ValueError('Attribute must be greater than zero')

        self.__ag = ag

    @property
    def number(self):
        return self.__number

    def __set_number(self, number):
        if (not isinstance(number, int)):
            raise TypeError('Attribute must be an integer')
        if (number <=0):
            raise ValueError('Attribute must be greater than zero')

        self.__number = number

    @property
    def balance(self):
        return self.__balance
    @balance.setter
    def balance(self, balance):
        if (not isinstance(balance, int)):
            raise TypeError('Attribute must be an integer')
        if (balance <0):
            raise ValueError('Attribute must be positive')

        self.__balance = balance

    def transfer(self, value, dest):
        try:
            self.withdraw(value)
        except NotEnoughBalanceError as E:
            self.transfers_blocked += 1
            E.args = ()
            raise FinanceOperationError("Operation not executed") from E
        dest.deposit(value)

    def withdraw(self, value):
        if(value<0):
            raise ValueError('Value must be positive')
        if(self.balance < value):
            self.withdraws_blocked += 1
            raise NotEnoughBalanceError(balance=self.balance, value=value)
        self.balance -= value

    def deposit(self, value):
        if(value<0):
            raise ValueError('Value must be positive')
        self.__balance += value


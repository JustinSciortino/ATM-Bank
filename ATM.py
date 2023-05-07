#Justin Sciortino
#420-LCU Computer Programming, Section 01
#S. Hilal, instructor
#Assignment 4

import datetime
class BankAccount:
    Count = 0
    def __init__(self, CODE,NAME,BANK,ACC_TYPE,BALANCE = 0 ):
        self.code = int(CODE)
        self.name = NAME
        self.bank = BANK
        self.acc_type = ACC_TYPE
        self.balance = int(BALANCE)
        self.trans_type = 'type'   #Default value of the transaction type
        self.__password = '12345'
        self.__lastaccess = datetime.datetime.now()
        BankAccount.Count += 1
    def __del__(self):
        BankAccount.Count -= 1
    def __repr__(self):
        d = '{:<10} {:15s} {:10s} {:10s} {:<10d}'.format(self.code, self.name, self.bank, self.acc_type, self.balance)
        return d
    def withdraw (self, amount):
        self.balance -= amount
        self.__lastaccess = datetime.datetime.now()
        self.trans_type = 'Withdraw'          #Set transaction type to Withdraw
        self.amount = amount
    def deposit(self,amount):
        self.balance += amount
        self.__lastaccess = datetime.datetime.now()
        self.trans_type = 'Deposit'           #Set transaction type to deposit
        self.amount = amount
    def transfer(self, recip, amount):
        self.withdraw(amount)         #Code to withdraw an amount from the donor
        recip.deposit(amount)         #Code to deposit an amount for the recipient
        self.account_log()            #Update the AccountLogs.txt with the relevant information
        recip.account_log()
    def create_pwd(self, pwd):      #Create_pwd is the same as update_pwd in the assignment instructions
        
        slice=pwd [0: -1]
        if (slice.isalnum ()):
            if(pwd.endswith ("#")): #pwd[len(pwd) -1]=="#"
                if(8<=len(pwd ) <=15):
                    if(pwd [0]. isupper ()):#3
                        if (slice.isalpha ()==False):#4
                            if (slice.isupper () == False):
                                self.__password = pwd
                                self.__lastaccess = datetime.datetime.now()
                                self.trans_type = 'New pwd'     #Set transaction type to New password
                                self.amount = 0
                                print('Password accepted')
                                return True
                            else:
                                print("no small letters")
                        else:
                            print("no digits")
                    else:
                        print("does not start with a capital letter")
                else:
                    print("length does not satisfy requirements")
            else:
                print("does not end with #")
        else:
            print("all except last character not alphanumeris")
    def get_balance(self):
        self.__lastaccess = datetime.datetime.now()
        self.trans_type = 'Balance'             #Set transaction type to balance
        self.amount = 0
        return self.balance
    def admin_print(self):
        d = '{:<10} {:10s} {}'.format(self.code, self.__password, self.__lastaccess)    #Code for option 2, to admin print the relevant information
        return d
    def verify_pwd(self):
        return self.__password    #Returns the default password. Code is used to check the password before transactions are made 
    def account_log(self):        #Code to create or append a text file and add the relevant information for the log file
        flog = open('AccountsLog.txt', 'a')
        i = '{} {:10d}      {:15s}       {:<10d} {:<10d}'.format(self.__lastaccess, self.code, self.trans_type, self.amount,
                                                    self.balance)
        print(i, file=flog)
        flog.close()

MyAccounts = {}
fp = open('accounts.txt')
for line in fp.readlines():       
    line = line.strip('\n')
    myaccount_record = line.split(",")
    MyAccounts[int(myaccount_record[0])] = BankAccount(myaccount_record[0], myaccount_record[1], myaccount_record[2], myaccount_record[3], int(myaccount_record[4]))
fp.close()

menu = """
Welcome to the Bank Accounts Management App
1- Print All Accounts (tabular format) (prints code, name, bank, acc_type, balance, last_access)
2- Admin prints passwords and last_access of all accounts. (prints code, password, last_access)
3- Create an account (Enter code, client name, bank name, account type and balance)
4- Withdraw an amount from an account. (account code & amount)
5- Deposit an amount to an account (Enter account code & amount)
6- Transfer an amount between accounts (Enter from and to account codes and amount)
7- Get balance of a given account (Enter account code)
8- Update Password (request old , verify and then ask for new password)
9- Display the log file.
10- Exit
Enter your requested option:"""

option = 0
while option != 10:
    option = int(input(menu))

    if option == 1:
        for k in MyAccounts:                 #Prints all the accounts in tabular format
           print(MyAccounts[k].__repr__())

    if option == 2:
        for k in MyAccounts:
            print(MyAccounts[k].admin_print())

    if option == 3:
        account_info = input('Enter account info (account code, client name, bank name, account type, balance:')
        acc = account_info.split(',')
        account_code = int(acc[0])
        if 0<= int(acc[4])<= 10000:   #Code to make sure the balance is not below 0 and not above 10 000
            MyAccounts[account_code] = BankAccount(int(acc[0]),acc[1],acc[2],acc[3],int(acc[4]))    #Code to create the account
            MyAccounts[account_code].amount = 0      #Information for the log file
            MyAccounts[account_code].trans_type = 'New acc'
            MyAccounts[account_code].account_log()
            print('Account created')
        else:
            print('Balance must be between 0 and 10,000')

    if option == 4:
        account_code = int(input('Enter your account code:'))
        check_pwd = input('Enter your password:')
        if account_code in MyAccounts:                                      #Make sure the account entered is in MyAccounts
            if MyAccounts[account_code].verify_pwd() == check_pwd:          #Verifies that the user entered the right password
                amount = int(input('Enter the amount you would like to withdraw:')) #After all the information is verified, the user is then allowed to enter an amount to withdraw
                if amount > 0 and MyAccounts[int(account_code)].balance >= amount:  #Verifies that the user has sufficient funds to perform a transaction
                    MyAccounts[int(account_code)].withdraw(amount)
                    MyAccounts[account_code].account_log()
                    print('Withdrawal successful')
                else:
                    print('Insufficient funds')
            else:
                print('Incorrect password')
        else:
            print('Account code not in MyAccounts')

    if option == 5:
        account_code = int(input('Enter an account code:'))
        check_pwd = input('Enter your password:')
        if account_code in MyAccounts:                                  #Make sure the account entered is in MyAccounts
            if MyAccounts[account_code].verify_pwd() == check_pwd:      #Verifies that the user entered the right password
                amount = int(input('Enter an amount to deposit:'))      #After all the information is verified, the user is then allowed to enter an amount to deposit
                MyAccounts[account_code].deposit(amount)
                MyAccounts[account_code].account_log()
                print('Deposit successful')
            else:
                print('Incorrect password')
        else:
            print('Account code not in MyAccounts')

    if option == 6:
        donor_code = int(input('Enter an account code:')) #Donor account aka self in the class
        check_pwd_donor = input('Enter your password:')   
        if donor_code in MyAccounts:                                            #Make sure the account entered is in MyAccounts
            if MyAccounts[donor_code].verify_pwd() == check_pwd_donor:          #Verifies that the user entered the right password
                rec_code = int(input('Enter the account code that you wish to transfer the money to:'))   #Recipient accound aka recip in the class
                if rec_code in MyAccounts:
                    amount = int(input('Enter the amount you wish to transfer:'))   #After all the information is verified, the user is then allowed to enter an amount to transfer
                    donor_balance = (MyAccounts[int(donor_code)].get_balance())
                    if amount > 0 and donor_balance >= amount:                  #Verifies that the donor account has sufficient funds
                        MyAccounts[donor_code].transfer(MyAccounts[rec_code], amount)
                        print('Transfer succesful')
                    else:
                        print('Donor does not have enough funds')
                else:
                    print('Recipient account code not MyAccounts')
            else:
                print('Incorrect Donor account code password')
        else:
            print('Donor account code not in MyAccounts')

    if option == 7:
        account_code = int(input('Enter an account code:'))
        check_pwd = input('Enter your password:')
        if account_code in MyAccounts:                                  #Make sure the account entered is in MyAccounts
            if MyAccounts[account_code].verify_pwd() == check_pwd:      #Verifies that the user entered the right password
                account_code_balance = (MyAccounts[int(account_code)].get_balance())
                MyAccounts[account_code].account_log()
                print("Account code", account_code, 'balance:', account_code_balance)
            else:
                print('Incorrect password')
        else:
            print('Account code not in MyAccounts')

    if option == 8:
        account_code = int(input('Enter an account code:'))
        old_pwd = str(input('Enter your current password:'))
        if account_code in MyAccounts:                                  #Make sure the account entered is in MyAccounts
            if MyAccounts[account_code].verify_pwd() == old_pwd:        #Verifies that the user entered the right password
                new_pwd = input('Enter a new password:')
                if MyAccounts[account_code].create_pwd(new_pwd) is True:
                    MyAccounts[account_code].account_log()              #Append the information only if the new password meets all the conditions
            else:
                print('Password entered does not match current password')
        else:
            print('Account code not in MyAccounts')

    if option == 9:                  
        flog = open('AccountsLog.txt','r')  #Open the AccountsLog.txt and read it
        for line in flog.readlines():
            line = line.strip('\n')         #Print the lines in AccountsLog.txt
            print(line)
        flog.close()

    if option == 10:
        print('Exiting...')

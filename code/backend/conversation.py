from colorama import Fore, Style, init
init()


class Conversation():
    def __init__(self, username, friend):
        self.username = username
        self.conversation = []  # [sender, receiver, message]
        self.friend = friend

    def sendMessage(self, message):
        self.conversation.append([self.username, self.friend, message])

    def seeMessages(self):
        for i in range(len(self.conversation) - 1, -1, -1):
            message = self.conversation[i]
            if message[0] != self.username:
                print(Fore.GREEN + message[2])
            else:
                print(Fore.BLUE + message[2]) 


Con1 = Conversation("JoeHill", "MatthewHill")
while True:
    print("| 1. Send Message | 2. See Messages |")
    option = int(input(''))

    if option == 1:
        message = input(" Message: ")
        Con1.sendMessage(message)

    else:
        Con1.seeMessages()
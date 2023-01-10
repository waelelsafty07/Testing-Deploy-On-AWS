class unauthorizationSend():
    def __init__(self, checkauth, response):
        self.checkauth = checkauth
        self.response = response

    def check(self):
        if self.checkauth == True:
            return self.Send()

    def Send(self):
        return self.response

from discord.ui import View, Button

class HelpButtons(View):
    def __init__(self):
        super().__init__()
        self.add_item(Button(label="Invite", url="https://discord.com/oauth2/authorize/?permissions=19520&scope=bot&client_id=846899156673101854"))
        self.add_item(Button(label="Github", url="https://github.com/ahino6942/public-PogBot"))
        
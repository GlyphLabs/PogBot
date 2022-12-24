# So you wanna host PogBot eh?
Of course you do, thats why you are here right?

Anyways, its actually pretty simple, but you are going to need some stuff before you can actually host it:

* `Python 3.9+`
* `Statcord Token`
* `Discord Bot token`
* `Brainshop ID and Key`
* `PostgreSQL Database`

So you have these? Great! Now you can move on to the next step!

# Installing requirements.
So now that you have the stuff, you gonna need to install the stuff in the `requirements.txt` file.

For you people who don't know how to do this:

`pip install -r requirements.txt`

The stuff should begin installing.

# Applying your things.

So you are going to need to create `.env` file in the `src` directory. (keep in mind you mind need to add in some code for it to work on some hosts)

After you have done that, you are going to need to copy and paste this,

```
TOKEN=""
BRAINSHOP_ID=""
BRAINSHOP_KEY=""
STATCORD_TOKEN=""
DATABASE_URL=""
```

After that, you gotta fill in the values.

# Running the bot
Its surprisingly simple. You just need a bit of some basic python knowledge :D

Run these simple commands in that order:

```
cd src
python3 main.py
```

After that, your self hosted PogBot will be up and running!

Congratulations! You have successfully self hosted PogBot!

# Message Content Intent
For those who want the actual "pog" feature and the chatbot, you are gonna have to change this line to `True` near the intents section:

```py
i = Intents.all()
i.message_content = True # this is the line you want to change
i.typing = False
```

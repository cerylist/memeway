from flask import Flask, render_template, request, jsonify
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer, ListTrainer

from chatterbot.logic import LogicAdapter


class MyLogicAdapter(LogicAdapter):
    def __init__(self, **kwargs):
        super(MyLogicAdapter, self).__init__(**kwargs)

    def can_process(self, statement):
        if 'what is' in statement.text.lower() or 'who is' in statement.text.lower():
            return True
        else:
            return False

    def process(self, statement):
        from chatterbot.conversation import Statement
        import urllib.request as urllib
        import bs4

        text = statement.text.lower()

        compare = ""

        if "who is" in text:
            compare = text.split("who is")[1]
        elif "what is" in text:
            compare = text.split("what is")[1]

        if len(compare) < 0:
            return 0, Statement("I can't understand who/what you are trying to find!")

        url = "http://knowyourmeme.com/search?context=entries&sort=relevance&" + compare.replace(" ", "+")
        url_open = urllib.urlopen(url)

        search_soup = bs4.BeautifulSoup(url_open, "html.parser")

        table = search_soup.find("table", class_="entry_list")

        if table is None:
            return 0, Statement("I couldn't find a meme for that!")

        first_row = table.find("td")

        if first_row is None:
            return 0, Statement("I couldn't find a meme for that!")

        meme = first_row.find("td")

        if meme is None:
            return 0, Statement("I couldn't find a meme for that!")

        anchor = meme.find("h2").find("a")

        name = anchor.contents[0]

        link = anchor["href"]

        # Follow link to meme
        meme_url = "http://knowyourmeme.com%s" % link
        meme_page = bs4.BeautifulSoup(urllib.urlopen(meme_url).read(), "html.parser").find("section", class_="bodycopy")

        if meme_page is None:
            return 0, Statement("I couldn't find a meme for that!")

        image_list = meme_page.find_all("img")

        image = None

        if image_list:
            image= image_list[0]["href"]

        message = ""

        statement = Statement("I found a photo, '%s', a webiste, '%s' and this content:\n\n%s" % (image, meme_url, message))

        # Randomly select a confidence between 0 and 1
        confidence = 1

        # For this example, we will just return the input as output
        selected_statement = statement

        return confidence, selected_statement



app = Flask(__name__)

english_bot = ChatBot("English Bot", logic_adapters=(
    {
            'import_path': 'chat_bot.MyLogicAdapter'
    },
    {
        "import_path": "chatterbot.logic.MathematicalEvaluation"
    },
    {
        "import_path": "chatterbot.logic.MathematicalEvaluation"
    },
    {
        "import_path": "chatterbot.logic.LowConfidenceAdapter",
        'threshold': 0.2,
        'default_response': "Am I one of Hillary's emails because that response is missing, or you're just not making sense!"
    }
))
english_bot.set_trainer(ChatterBotCorpusTrainer)
english_bot.train("chatterbot.corpus.english")
# Train based on english greetings corpus
english_bot.train("chatterbot.corpus.english.greetings")
english_bot.train("chatterbot.corpus.english.conversations")

english_bot.set_trainer(ListTrainer)
english_bot.train(["What is your name?", "My name is memecat!", "Where do you live?", "I live on the interwebz!"])
english_bot.train(["What is a meme?", "Ur life is a meme.", "That's not nice!",
                   "This is you... http://www.relatably.com/m/img/sad-memes-about-life/a4b86fd5ac07c3445cc84325809856e213dcaa2c0c07ce1d620e4bfc9c88a325.jpg"])
english_bot.train(["What are memes?", "Memes are LYFE!"])
english_bot.train(["What is your favorite meme?",
                   "http://weknowmemes.com/wp-content/uploads/2011/12/say-ernie-would-you-like-some-ice-cream-sherbert.jpg"])
english_bot.train([""])


@app.route("/", methods=["POST"])
def home():
    json = request.get_json()
    query = json["message"]
    response = str(english_bot.get_response(query))
    d = {"response": response}
    return jsonify(**d)


if __name__ == "__main__":
    app.run()
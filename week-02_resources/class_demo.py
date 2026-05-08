class FlashCard:
    def __init__(self, question, answer):
        self.question = question
        self.answer = answer

    def review(self):
        print("Question", self.question)
        user = input("Your answer: ")
        if user.strip().lower() == self.answer.lower():
            print("Correct")
        else:
            print("Nope, answer is, ", self.answer)


# card1 = FlashCard("What is a venv?", "an isolated Python environment")
# card2 = FlashCard("What does pip do?", "installs Python packages")

# print(card1.review())


class Deck:
    def __init__(self):
        self.cards = []
    
    def add(self, card):
        self.cards.append(card)
        
    def study(self):
        for card in self.cards:
            card.review()

my_deck = Deck()

my_deck.add(FlashCard("What is a venv?", "an isolated Python environment"))
my_deck.add(FlashCard("What does pip do?", "installs Python packages"))
my_deck.add(FlashCard("What is JSON?", "a way to send data over the internet"))

my_deck.study()






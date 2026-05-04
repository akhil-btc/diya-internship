import random 
class Flashcard():
    def __init__(self, question, answer):
        self.question = question
        self.answer = answer
    def review(self):
        inp = input("Question: " + self.question + " ")

        inp = inp.strip()
        if inp.lower() == self.answer.lower():
            print("Correct!")
        else:
            print("Incorrect. Answer: ", self.answer)


class Deck():
    def __init__(self):
        self.lists = []
    
    def add_flashcard(self, card):
        self.lists.append(card)
    def shuffle(self):
        random.shuffle(self.lists)
    def study(self):
        for card in self.lists:
            card.review()

if __name__ == "__main__":
    deck = Deck()
    deck.add_flashcard(Flashcard("what is a method?", "a function located inside a class"))
    deck.add_flashcard(Flashcard("what does def __init__ do?", "sets up the class, giving it variables to use throughout the class methods"))
    deck.add_flashcard(Flashcard("what does a function do?", "it performs one task, and makes it easy to understand and organize in code"))
    deck.add_flashcard(Flashcard("what is a class?", "it creates a general shell to put specific information in "))
    deck.add_flashcard(Flashcard("what is a virtual environment?", "it is an online space so collaborators can run code on the same versions"))
    deck.add_flashcard(Flashcard("how do you define a function?", " use def."))
    deck.add_flashcard(Flashcard("how do you open a CSV file", "use with open()"))
    deck.add_flashcard(Flashcard("What does try/except do?", "it is a seatbelt for errors in the code so that it will run even with errors"))
    deck.add_flashcard(Flashcard("what happens if there is no csv file when trying to read one?", "you get a FileNotFoundError"))
    deck.add_flashcard(Flashcard("what are libraries?", "they are prewritten code that can be imported to do specific tasks"))
    deck.shuffle()
    deck.study()
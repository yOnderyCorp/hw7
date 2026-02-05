class WordLengthIterator:
    def __init__(self, words):
        self.words = words
        self.index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.index < len(self.words):
            word = self.words[self.index]
            self.index += 1
            return len(word)
        else:
            raise StopIteration


#Тест программы
if __name__ == "__main__":
    my_words = ["Python", "Iterator", "Homework", "AI"]
    length_iter = WordLengthIterator(my_words)
    print("Длины слов в списке:")
    for length in length_iter:
        print(length)
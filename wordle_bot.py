class WordleBot:

    def __init__(self):
        self.dictionary = []
        with open('wordle_dictionary.txt', "r") as words:
            for line in words:
                self.dictionary.append(line[:5])

        self.attempts = []
        self.results = []
    
    def attempt(self, attempt, result):
        self.attempts.append(attempt)
        self.results.append(result)
        count = {}
        for i in range(5):
            if attempt[i] not in count: count[attempt[i]] = 1
            else: count[attempt[i]] += 1
        seen = []
        for i in range(5):
            if result[i] == 'G':
                letter = attempt[i]
                ind = 0
                n = len(self.dictionary)
                while ind < n:
                    if self.dictionary[ind][i] != letter:
                        self.dictionary.pop(ind)
                        n -= 1
                    else: ind += 1
            elif result[i] == '_':
                letter = attempt[i]
                ind = 0
                n = len(self.dictionary)
                if count[letter] == 1:
                    while ind < n:
                        if letter in self.dictionary[ind]:
                            self.dictionary.pop(ind)
                            n -= 1
                        else: ind += 1
                elif count[letter] == 2:
                    if attempt[i] not in seen:
                        while ind < n:
                            if letter in self.dictionary[ind]:
                                self.dictionary.pop(ind)
                                n -= 1
                            else: ind += 1
                    else:
                        if self.results[seen.index(letter)] == '_': pass
                        elif self.results[seen.index(letter)] == 'G':
                            pass
                        else:
                            pass
            elif result[i] == 'Y':
                letter = attempt[i]
                ind = 0
                n = len(self.dictionary)
                while ind < n:
                    if letter not in self.dictionary[ind] or letter == self.dictionary[ind][i]:
                        self.dictionary.pop(ind)
                        n -= 1
                    else: ind += 1
            seen.append(attempt[i])
        print(f"{len(self.dictionary)} options remain")

    
    def suggestion(self):
        pass

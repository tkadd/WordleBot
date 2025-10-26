import numpy as np

class WordleBot:

    def __init__(self):
        self.dictionary = set()
        with open('wordle/dictionaries/wordle_dictionary.txt', "r") as words:
            for line in words:
                self.dictionary.add(line[:5])
    
    def play(self, attempt, result, update_dictionary=True, display=True, dictionary=None):
        if dictionary is None:
            dictionary = self.dictionary

        new_dictionary = set()
        for word in dictionary:
            temp_result = self.result(attempt, word)
            if temp_result == result: new_dictionary.add(word)

        n = len(new_dictionary)
        if update_dictionary:
            self.dictionary = new_dictionary
        if display:
            print(f"{len(self.dictionary)} option{'s' if n > 1 else ''} remain{'' if n > 1 else 's'}")
        return n, new_dictionary
    
    def word_entropy(self, dictionary=None):
        if dictionary is None: dictionary = self.dictionary
        word_entropy = {}
        n = len(dictionary)
        for guess in dictionary:
            result_counts = {}
            for target in dictionary:
                res = self.result(guess, target)
                if res in result_counts: result_counts[res] += 1
                else: result_counts[res] = 1
            entropy = -sum((count/n)*np.log2(count/n) for count in result_counts.values())
            word_entropy[guess] = entropy
        
        best_guess = max(word_entropy, key=word_entropy.get)
        return word_entropy

    def result(self, word, target):
        result = ['0','0','0','0','0']
        seen = {}
        for i, letter in enumerate(word):
            if letter == target[i]:
                result[i] = 'G'
                if letter not in seen: seen[letter] = 1
                else: seen[letter] += 1
        for i, letter in enumerate(word):
            if result[i] != 'G':
                target_count = target.count(letter)
                if letter in seen:
                    if seen[letter] < target_count:
                        result[i] = 'Y'
                    else:
                        result[i] = 'B'
                    seen[letter] += 1
                else:
                    if not target_count: result[i] = 'B'
                    else: result[i] = 'Y'
                    seen[letter] = 1

        return "".join(result)
    
    def predict(self):
        return None             

    def performance(self):
        scores = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0}
        for target in self.dictionary:
            dictionary = self.dictionary.copy()
            count = 1
            best_guess = 'raise'
            res = self.result(best_guess, target)
            n, dictionary = self.play(best_guess, res, update_dictionary=False, display=False, dictionary=dictionary)
            while best_guess != target:
                count += 1
                best_guess = self.suggestion(dictionary)[0]
                res = self.result(best_guess, target)
                n, dictionary = self.play(best_guess, res, update_dictionary=False, display=False, dictionary=dictionary)

            if count in scores:
                scores[count] += 1
            else:
                scores[count] = 1
        return scores

if __name__ == '__main__':
    pass

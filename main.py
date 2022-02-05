import random


def load_words():
    with open('words.txt') as word_file:
        words = list(word_file.read().split())

    five_letter_words = list(filter(lambda x: len(x) == 5, words))
    return five_letter_words


def get_word_result(input_word):
    result = ""
    for letter in input_word:
        correct = False
        while not correct:
            out = input(
                f'Enter result for {letter} (C)orrect, (M)issplaced, (W)rong: ').upper()
            if out in ['C', 'M', 'W']:
                result += out
                correct = True
    return result


def suggest_first_word(wordlist):
    sorted_by_vowels = sorted(wordlist, key=lambda x: sum(
        v in 'aeiou' for v in x), reverse=True)[:100]

    random.shuffle(sorted_by_vowels)
    for word in sorted_by_vowels:
        if len(set(word)) == 5:
            print(f'Try: \'{word}\'')
            return word


def suggest_word(wordlist):
    print(f'There are {len(wordlist)} possible words')
    word = random.choice(wordlist)
    print(f'Try: \'{word}\'')
    return word


def slim_down_words(input_word, letter_results, wordlist):
    for (i, letter) in enumerate(input_word):
        if letter_results[i] == 'W':
            already_confirmed = False
            for j, letter in enumerate(input_word):
                if letter == input_word[i] and i != j and letter_results[j] == "C":
                    already_confirmed = True
            if not already_confirmed:
                wordlist = wrong_letters(letter, wordlist)
        elif letter_results[i] == 'M':
            wordlist = missplaced_letters(letter, i, wordlist)
        elif letter_results[i] == 'C':
            wordlist = correct_letter(letter, i, wordlist)
    return wordlist


def wrong_letters(letter, wordlist):
    return list(filter(lambda x: letter not in x, wordlist))


def missplaced_letters(letter, index, wordlist):
    return [word for word in wordlist if letter in word and word[index] != letter]


def correct_letter(letter, index, wordlist):
    return [word for word in wordlist if word[index] == letter]


def mainloop(wordlist):
    suggested_word = suggest_first_word(wordlist)
    result = get_word_result(suggested_word)
    wordlist = slim_down_words(suggested_word, result, wordlist)
    while result != "CCCCC":
        suggested_word = suggest_word(wordlist)
        result = get_word_result(suggested_word)
        wordlist = slim_down_words(suggested_word, result, wordlist)


if __name__ == '__main__':
    words = load_words()
    mainloop(words)

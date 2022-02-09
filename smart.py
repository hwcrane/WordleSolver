import matplotlib.pyplot as plt
import math

from numpy.core.fromnumeric import mean


def load_words(filename):
    with open(filename) as word_file:
        words = word_file.read().split()

    five_letter_words = [word for word in words if len(word) == 5]
    return five_letter_words


def calculate_word_entropy(wordlist, word):
    options = {
        l1+l2+l3+l4+l5: 0 for l1 in 'CMW'for l2 in 'CMW'for l3 in 'CMW'for l4 in 'CMW'for l5 in 'CMW'}
    for w in wordlist:
        options[get_pattern_from_word(word, w)] += 1

    probabilites = [(v/len(wordlist)) * -math.log2(v/len(wordlist))
                    for v in options.values() if v > 0]

    return sum(probabilites)


def get_pattern_from_word(word_to_try, actual_word):
    pattern = ""
    for i, letter in enumerate(word_to_try):
        if letter == actual_word[i]:
            pattern += 'C'
        elif letter in actual_word:
            pattern += 'M'
        else:
            pattern += 'W'
    return pattern


def generate_default_letter_dict():
    # -1 = Confirmed incorrect
    # 0 = Unknown
    # 1 = Possible
    # 2 = Confirmed
    return {l: [0 for _ in range(5)] for l in 'abcdefghijklmnopqrstuvwxyz'}


def get_word_entropies(wordlist):
    return [(word, calculate_word_entropy(wordlist, word)) for word in wordlist]


def update_letter_dict(pattern, word, letter_dict):
    for i, pattern_part in enumerate(pattern):
        if pattern_part == "C":
            for l in letter_dict.keys():
                letter_dict[l][i] = -1
            arr = [-1, -1, -1, -1, -1]
            arr[i] = 2
            letter_dict[word[i]] = arr

        elif pattern_part == "W":
            letter_dict[word[i]] = [-1, -1, -1, -1, -1]

        elif pattern_part == "M":
            arr = letter_dict[word[i]]
            for j in range(len(arr)):
                arr[j] = 1 if j != i and arr[j] != -1 else -1
            letter_dict[word[i]] = arr

    return letter_dict


def update_wordlist(wordlist, letter_dict):
    return [word for word in wordlist if word_match_dict(word, letter_dict)]


def word_match_dict(word, letter_dict):
    for i, letter in enumerate(word):
        if letter_dict[letter][i] == -1:
            return False

    return True


if __name__ == '__main__':
    wordlist = load_words("words.txt")
    letter_dict = generate_default_letter_dict()

    print("Try 'crane'")

    # get pattern
    pattern = input("enter pattern").upper()

    # Filter out words that do not match pattern
    letter_dict = update_letter_dict(
        pattern, "crane", letter_dict)
    wordlist = update_wordlist(wordlist, letter_dict)

    while pattern != "CCCCC":

        # Calculate Word Entropies
        word_entropies = get_word_entropies(wordlist)

        # Sort Word entropies to find max
        sorted_word_entropies = sorted([(k, v)
                                        for (k, v) in word_entropies],
                                       key=lambda x: x[1], reverse=True)

        # Suggest word with max entropy
        print(f"Try \'{sorted_word_entropies[0][0]}\'")

        # get pattern
        pattern = input("enter pattern").upper()

        # Filter out words that do not match pattern
        letter_dict = update_letter_dict(
            pattern, sorted_word_entropies[0][0], letter_dict)
        wordlist = update_wordlist(wordlist, letter_dict)

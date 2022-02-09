import math


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


def get_word_entropies(wordlist):
    return [(word, calculate_word_entropy(wordlist, word)) for word in wordlist]


def is_word_valid(word, chosen_word, pattern):
    valid = True
    for i, pattern_part in enumerate(pattern):
        if pattern_part == "C":
            # Not valid if there if letters do not match at location i
            valid = False if word[i] != chosen_word[i] else valid

        elif pattern_part == "M":
            # Not valid if word[i] = chosen_word[i]
            valid = False if word[i] == chosen_word[i] else valid

            # Not valid if chosen_word[i] not in word
            valid = False if chosen_word[i] not in word else valid

        elif pattern_part == "W":
            # Not valid if chosen_word[i] is in word
            valid = False if chosen_word[i] in word else valid

    return valid


def update_wordlist(wordlist, chosen_word, pattern):
    return [word for word in wordlist if is_word_valid(word, chosen_word, pattern)]

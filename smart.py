def load_words(filename):
    with open(filename) as word_file:
        words = list(word_file.read().split())

    five_letter_words = list(filter(lambda x: len(x) == 5, words))
    return five_letter_words


def generate_default_letter_dict():
    # -1 = Confirmed incorrect
    # 0 = Unknown
    # 1 = Possible
    # 2 = Confirmed
    return {l: [0 for _ in range(5)] for l in 'abcdefghijklmnopqrstuvwxyz'}


def generate_word_options(letter_dict, word):
    # Generate all outcomes irrespective if posible
    # Options:
    #   C = Confirmed
    #   W = Wrong
    #   M = Missplaced

    options = [
        l1+l2+l3+l4+l5 for l1 in 'CWM' for l2 in 'CWM' for l3 in 'CWM' for l4 in 'CWM' for l5 in 'CWM']

    # Filter for only possible outcomes
    filtered_options = [
        x for x in options if is_option_possible(word, x, letter_dict)]

    return filtered_options


def is_option_possible(word, option, letter_dict):
    valid = True
    for i, letter in enumerate(word):
        if option[i] == 'C':
            # Valid if letter is not already confirmed incorrect
            valid = False if letter_dict[letter][i] == -1 else valid

            # Valid if position is not already confirmed to a differnt letter
            valid = False if any(
                letter_dict[l][i] == 2 and letter != l for l in "abcdefghijklmnopqrstuvwxyz") else valid

            # Valid if letter is not already confirmed in another position
            valid = False if any(
                letter_dict[letter][j] == 2 and i != j for j in range(5)) else valid

        elif option[i] == 'W':
            # Valid if letter is not already confirmed or possible in another position
            valid = False if any(
                letter_dict[letter][j] > 0 and i != j for j in range(5)) else valid

        elif option[i] == 'M':
            # Valid if letter is not already confirmed in another position
            valid = False if any(
                letter_dict[letter][j] == 2 and i != j for j in range(5)) else valid

            # Valid if letter is not already confirmed incorrect
            valid = False if letter_dict[letter][i] == -1 else valid

    return valid


if __name__ == '__main__':
    wordlist = load_words("words.txt")
    letter_dict = generate_default_letter_dict()
    filtered_wordlist = generate_word_options(letter_dict, wordlist[0])

from wordle import *

if __name__ == '__main__':
    wordlist = load_words("possible.txt")

    print("Try 'crane'")

    # get pattern
    pattern = input("enter pattern: ").upper()

    # Filter out words that do not match pattern
    wordlist = update_wordlist(wordlist, 'crane', pattern)

    while pattern != "CCCCC":

        # Calculate Word Entropies
        word_entropies = get_word_entropies(wordlist)

        # Sort Word entropies to find max
        sorted_word_entropies = sorted([(k, v)
                                        for (k, v) in word_entropies],
                                       key=lambda x: x[1], reverse=True)
        chosen_word = sorted_word_entropies[0][0]
        # Suggest word with max entropy
        print(f"Try \'{sorted_word_entropies[0][0]}\'")

        # get pattern
        pattern = input("enter pattern: ").upper()

        # Filter out words that do not match pattern
        wordlist = update_wordlist(wordlist, chosen_word, pattern)

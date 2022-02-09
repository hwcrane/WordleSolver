from wordle import *

if __name__ == "__main__":
    answers = load_words("possible.txt")
    data = []

    for answer in answers:
        attempts = 1
        wordlist = load_words("possible.txt")

        guess = "crane"

        pattern = get_pattern_from_word(guess, answer)

        # Filter out words that do not match pattern
        wordlist = update_wordlist(wordlist, 'crane', pattern)

        # print("Answer: " + answer)
        # print("Guess: " + guess)
        # print("Pattern Generated: " + pattern)

        while pattern != "CCCCC":
            attempts += 1
            # Calculate Word Entropies
            word_entropies = get_word_entropies(wordlist)

            # Sort Word entropies to find max
            sorted_word_entropies = sorted([(k, v)
                                            for (k, v) in word_entropies],
                                           key=lambda x: x[1], reverse=True)

            # print(sorted_word_entropies)
            guess = sorted_word_entropies[0][0]

            # get pattern
            pattern = get_pattern_from_word(guess, answer)

            # print("Guess: " + guess)
            # print("Pattern Generated: " + pattern)

            # Filter out words that do not match pattern
            wordlist = update_wordlist(wordlist, guess, pattern)

        while len(data) <= attempts:
            data.append(0)
        data[attempts] += 1
        print(f"{answer}: {attempts}")

    print(data)

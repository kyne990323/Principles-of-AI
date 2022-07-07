def read_text(path):
    with open("path", "r") as f:
        raw = f.read().replace("\n", " ")
    return raw


#########################
########FUCK YOU#########
#########################
def clean_text(raw) -> str:
    to_remove = [',', ';', ':', '.', '?', '!', '[', ']', '*', '(', ')', '-', "'", '"']
    char_arr = list(raw)
    for i in range(len(char_arr)):

        if char_arr[i] in to_remove:
            char_arr[i] = ''
        char_arr[i] = char_arr[i].lower()

    return ''.join(char_arr)


def get_word_frequencies(words) -> dict:
    res = {}
    for word in words:
        if word.lower() in res.keys():
            res[word.lower()] += 1
        else:
            res[word.lower()] = 1
    return res


def count_syllables(word) -> int:
    # same as provided
    return 0


def count_all_syllables(words):
    res = 0
    for word in words:
        res += count_syllables(word)
    return res


def main():
    print(clean_text("sda asxsa,,.ac''''' as.,lfl,., ."))
    # print("Welcome")
    # file_name = input("Name of file to analyze? ")
    # raw = read_text(file_name)
    # clean = clean_text(raw)
    # word_list = clean.split()
    # num_word = len(word_list)
    # print(f"Number of words: {num_word}")
    # num_sentence = 0
    # for char in list(raw):
    #     if char == '.' or char == '?' or char == '!':
    #         num_sentence += 1
    # print(f"Number of sentences: {num_sentence}")
    # unique = get_word_frequencies(word_list)
    # num_unique = len(unique)
    # print(f"Number of unique words: {num_unique}")
    # word_per_sentence = num_word // num_sentence
    # num_syllables = count_all_syllables(word_list)
    # syllable_per_word = num_syllables // num_word
    # print(f"Average words per sentence: {word_per_sentence}")
    # print(f"Average syllables per word: {syllable_per_word}")
    # re_score = 0
    # grade = 0
    # print(f"Reading-ease score: {re_score}")
    # print(f"U.S. grade level: {grade}")
    # print()
    # query = "Enter word to check "
    # while True:
    #     check = input('Enter word to check ("q" to quit): ')
    #     check = check.lower()
    #     if check == 'q':
    #         break
    #     if check not in unique:
    #         freq = 0
    #     freq = unique[check]
    #     print(f'The word "{check}" appears {freq} times.')
    # print("Thanks")


if __name__ == '__main__':
    main()

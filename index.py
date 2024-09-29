import json

soup = []
wordsToSearch = []

with open("soup.json", "r") as f:
    data = json.load(f)
    unformated_soup = data["soup"]
    unformated_wordsToSearch = data["words"]

# Format soup
for row in unformated_soup:
    soup.append(list(row))

# Format wordlist
for line in unformated_wordsToSearch:
    lineSplited = line.split(" ")
    for word in lineSplited:
        wordsToSearch.append(word.strip())

print("Sopa de letras:")
for row in soup:
    print(row)
print("Palabras a buscar:", wordsToSearch)

directions = [
    (0, 1),   # right
    (0, -1),  # left
    (1, 0),   # down
    (-1, 0),  # up
    (1, 1),   # down-right
    (-1, -1), # up-left
    (1, -1),  # down-left
    (-1, 1)   # up-right
]

directionsPlaintext = {
    (0, 1)    : "right",
    (0, -1)   : "left",
    (1, 0)    : "down",
    (-1, 0)   : "up",
    (1, 1)    : "down-right",
    (-1, -1)  : "up-left",
    (1, -1)   : "down-left",
    (-1, 1)   : "up-right"
}

def search_word(soup, word, start_row, start_col, direction):
    rows = len(soup)
    word_len = len(word)
    
    for k in range(word_len):
        new_row = start_row + direction[0] * k
        new_col = start_col + direction[1] * k

        # limit check
        if new_row < 0 or new_row >= rows or new_col < 0 or new_col >= len(soup[new_row]):
            return False
        
        if soup[new_row][new_col] != word[k]:
            return False
    return True

def find_words_in_soup(soup, wordsToSearch):
    found_words = []
    rows = len(soup)

    for word in wordsToSearch:
        word_found = False
        
        for i in range(rows):
            cols = len(soup[i])
            for j in range(cols):
                
                # check all directions if the first letter matches
                if soup[i][j] == word[0]:
                    for direction in directions:
                        if search_word(soup, word, i, j, direction):
                            found_words.append(word)
                            word_found = True
                            print(f'"{word}": ({j+1}, {i+1}, {directionsPlaintext[direction]})')
                            break
                
                if word_found:
                    break
            if word_found:
                break
    
    if not found_words:
        print("No se encontraron palabras.")
    
    return found_words

# Run the program
if __name__ == "__main__":
    find_words_in_soup(soup, wordsToSearch)

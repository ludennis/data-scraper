def ReadSearchPhrasesFromFile(filename):
    search_phrases = []
    with open(filename, 'r') as f:
        for line in f:
            search_phrases.append(line.replace('\n',''))

    return search_phrases

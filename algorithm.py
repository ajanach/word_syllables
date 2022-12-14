import re, string
from compound_split import doc_split

vowels = ["a", "e", "i", "o", "u", "ä", "ö", "ü", "ei", "ai", "ey", "ay", "eu", "äu", "ie", "au", "aa", "ee", "oo"]

consonants = ["b", "c", "d", "f", "g", "h", "j", "k", "l", "m", "n", "p", "q", "r", "s", "t", "v", "w", "x", "y", "z", "ß", "sch", "ch", "ck", "qu", "ph"]

prefixes = ["an", "ab", "auf", "aus", "dis", "ein", "fehl", "her", "hin", "haupt", "in", "dar", "durch", "los", "mit",
            "nach", "von", "vor", "weg", "um", "un", "ur", "ent", "er", "ver", "zer", "miss", "miß", "niss", "niß",
            "ex", "non", "super", "trans", "kon", "hoch", "stink", "stock", "tief", "tod", "erz", "unter", "über", "hinter", 
            "wider", "wieder", "weiter", "zurück", "zurecht", "zusammen", "hyper", "inter"]

splitting = ["VCCV", "VCCCV", "VCV", "VV"]

def syllables_rules_exceptions(input_sentence):
    global prefixes
    global vowels
    global consonants
    
    doc_split.MIDDLE_DOT = " "
    sentence_doc_split = doc_split.doc_split(input_sentence)
    sentence_exceptions_knie = sentence_doc_split.split(" ")
    regex_list_of_list = []
    for word in sentence_exceptions_knie:
        regex = re.findall(r'(?i)knie.*', word)
        if not regex:
            regex_list_of_list.append("X")
        else:
            regex_list_of_list.append(regex)
        regex_list = [val for sublist in regex_list_of_list for val in sublist]
        
        sentence_checksum = sentence_exceptions_knie
    if len(regex_list) == len(sentence_checksum):
        index = 0
        while index < len(sentence_checksum):
            if regex_list[index].lower() == sentence_exceptions_knie[index].lower():
                if index == 0 and sentence_exceptions_knie[index].lower() == "knie":
                    sentence_exceptions_knie[index] = sentence_exceptions_knie[index]
                elif sentence_exceptions_knie[index - 1][-1:] == "e" and sentence_exceptions_knie[index - 2] == "das" and sentence_exceptions_knie[index - 3][-1:] == "e":
                    sentence_exceptions_knie[index] == sentence_exceptions_knie[index]
                elif sentence_exceptions_knie[index - 1].lower() == "die" or sentence_exceptions_knie[index - 1].lower() == "der" or sentence_exceptions_knie[index - 1][-1:].lower() == "e":
                    letter_index = sentence_exceptions_knie[index].lower().find("knie")
                    word = sentence_exceptions_knie[index]
                    sentence_exceptions_knie[index] = word[:letter_index + 3] + " " + word[letter_index + 3:]
            index += 1
    
    sentence_knie = ' '.join(sentence_exceptions_knie)
    sentence_prefixes = sentence_knie.split(" ")
    
    for prefix in prefixes:
        prefix_length = len(prefix)
        for word in sentence_prefixes:
            if word[:prefix_length] == prefix:
                index = sentence_prefixes.index(word)
                sentence_prefixes[index] = word[:prefix_length] + " " + word[prefix_length:]
                
    sentence_split_prefixes = ' '.join(sentence_prefixes)
    sentence_vc = sentence_split_prefixes.split(" ")
    
    regex_list_of_list = []
    for word_vc in sentence_vc:
        regex = re.findall(r'.*tsch.*', word_vc)
        if not regex:
            regex_list_of_list.append("X")
        else:
            regex_list_of_list.append(regex)
    regex_list = [val for sublist in regex_list_of_list for val in sublist]
    
    if len(regex_list) == len(sentence_vc):
        index = 0
        while index < len(sentence_vc):
            if regex_list[index].lower() == sentence_vc[index].lower():
                sentence_length_01 = len(sentence_vc[index]) - 1
                sentence_length_02 = len(sentence_vc[index])
                tsch_length = len("tsch")
                letter_index = sentence_vc[index].find("tsch")
                
                if letter_index == 0:
                    word = sentence_vc[index]
                    sentence_vc[index] = "C" + word[tsch_length:]
                    
                if letter_index == sentence_length_01 - tsch_length or letter_index == sentence_length_02 - tsch_length:
                    word = sentence_vc[index]
                    sentence_vc[index] = word[:letter_index] + "C"
            index += 1
            
    sentence_join = ' '.join(sentence_vc)
    sentence_letters = list(sentence_join)
    
    counter = 0
    for letter in sentence_letters:
        for sign in consonants:
            if letter == sign.upper() or letter == sign.lower() and letter != string.punctuation:
                sentence_letters[counter] = "C"
        for sign in vowels:
            if letter == sign.upper() or letter == sign.lower() and letter != string.punctuation:
                sentence_letters[counter] = "V"
        counter += 1
    
    sentence_in_vc = ''.join(sentence_letters)
    sentence_vc = sentence_in_vc.split(" ")
    sentence = sentence_split_prefixes.split(" ")
    
    """
    In this moment we are using:
    sentence_split_prefixes - sentence as a normal input
    sentence_in_vc - sentence V and C type
    """

    regex_list_of_list = []  # kreiram prostor za praznu listu u koju će se pohraniti komadići lista jer regex vraća listu
    for word_vc in sentence:  # prolazim kroz sve riječi u obliku V i C
        regex = re.findall(r'.*tsch.*', word_vc)  # regeksom pretražujem koje su to riječi koje tražim
        if not regex:  # ako regeks nije pronašao match, vratit će praznu listu, ako vrati praznu listu onda će u regex_list_of_list na to mjesto upisati "X"
            regex_list_of_list.append("X")
        else:
            regex_list_of_list.append(regex)  # ako je regeks pronašao match, dodaj taj match na mjesto u regex_list_of_list
    regex_list = [val for sublist in regex_list_of_list for val in sublist]  # pošto imamo listu lista, smanjio sam ju za jedan level s ovim djelom koda

    if len(regex_list) == len(sentence):
        index = 0
        while index < len(sentence):
            if regex_list[index].lower() == sentence[index].lower():
                sentence_length_01 = len(sentence[index]) - 1
                sentence_length_02 = len(sentence[index])
                tsch_length = len("tsch")
                letter_index = sentence[index].find("tsch")
                
                if letter_index != 0 and letter_index != sentence_length_01 - tsch_length and letter_index != sentence_length_02 - tsch_length:
                    word = sentence[index]
                    #print(sentence[index], sentence_vc[index][letter_index - 1], sentence_vc[index][letter_index + tsch_length], sentence_vc[index][letter_index + tsch_length + 1])
                    if sentence_vc[index][letter_index - 1] == "V" and sentence_vc[index][letter_index + tsch_length] == "C" and sentence_vc[index][letter_index + tsch_length + 1] == "V":
                        sentence[index] = word[:letter_index + 4] + " " + word[letter_index + 4:]
                        #print(sentence[index], sentence_vc[index][letter_index - 1], sentence_vc[index][letter_index + tsch_length], sentence_vc[index][letter_index + tsch_length + 1])
                    if sentence_vc[index][letter_index - 1] == "V" and sentence_vc[index][letter_index + tsch_length] == "V":
                        sentence[index] = word[:letter_index + 1] + " " + word[letter_index + 1:]
                        #print(sentence[index])
            index += 1
            
    sentence_tsch = ' '.join(sentence)
    return sentence_tsch

def sentence_in_vc(input_sentence):
    global vowels
    global consonants
    
    sentence_letters = list(input_sentence)
    sentence = input_sentence.split(" ")

    regex_list_of_list = []  # kreiram prostor za praznu listu u koju će se pohraniti komadići lista jer regex vraća listu
    for word_vc in sentence:  # prolazim kroz sve riječi u obliku V i C
        regex = re.findall(r'.*tsch.*', word_vc)  # regeksom pretražujem koje su to riječi koje tražim
        if not regex:  # ako regeks nije pronašao match, vratit će praznu listu, ako vrati praznu listu onda će u regex_list_of_list na to mjesto upisati "X"
            regex_list_of_list.append("X")
        else:
            regex_list_of_list.append(regex)  # ako je regeks pronašao match, dodaj taj match na mjesto u regex_list_of_list
    regex_list = [val for sublist in regex_list_of_list for val in sublist]  # pošto imamo listu lista, smanjio sam ju za jedan level s ovim djelom koda
    if len(regex_list) == len(sentence):
        index = 0
        while index < len(sentence):
            if regex_list[index].lower() == sentence[index].lower():
                sentence_length_01 = len(sentence[index]) - 1
                sentence_length_02 = len(sentence[index])
                tsch_length = len("tsch")
                letter_index = sentence[index].find("tsch")

                if letter_index == 0:
                    word = sentence[index]
                    sentence[index] = "C" + word[tsch_length:]
                    
                if letter_index == sentence_length_01 - tsch_length or letter_index == sentence_length_02 - tsch_length:
                    word = sentence[index]
                    sentence[index] = word[:letter_index] + "C"
            index += 1
            
    sentence_join = ' '.join(sentence)
    sentence_letters = list(sentence_join)
    
    counter = 0
    for letter in sentence_letters:
        for sign in consonants:
            # ako se letter nalazi u sign (consonant) bez obzira na velika ili mala slova i ako nije interpunkcijski znak:
            if letter == sign.upper() or letter == sign.lower() and letter != string.punctuation:
                sentence_letters[counter] = "C"
        for sign in vowels:
            # ako se letter nalazi u sign(vowels) bez obzira na velika ili mala slova i ako nije interpunkcijski znak:
            if letter == sign.upper() or letter == sign.lower() and letter != string.punctuation:
                sentence_letters[counter] = "V"
        counter += 1
        
    sentence_vc = ''.join(sentence_letters)
    return sentence_vc

def syllables_rules(input_sentence):
    global splitting
    global vowels
    
    sentence = input_sentence.split(" ")
    sentence_vc = sentence_in_vc(input_sentence).split(" ")
    
    for split in splitting:
        if split == "VCCV":
            regex_list_of_list = []  # kreiram prostor za praznu listu u koju će se pohraniti komadići lista jer regex vraća listu
            for word_vc in sentence_vc:  # prolazim kroz sve riječi u obliku V i C
                regex = re.findall(r'.*{}.*'.format(split), word_vc)  # regeksom pretražujem koje su to riječi koje tražim
                if not regex:  # ako regeks nije pronašao match, vratit će praznu listu, ako vrati praznu listu onda će u regex_list_of_list na to mjesto upisati "X"
                    regex_list_of_list.append("X")
                else:
                    regex_list_of_list.append(regex)  # ako je regeks pronašao match, dodaj taj match na mjesto u regex_list_of_list
            regex_list = [val for sublist in regex_list_of_list for val in sublist]  # pošto imamo listu lista, smanjio sam ju za jedan level s ovim djelom koda
            if len(regex_list) == len(sentence_vc):
                index = 0
                while index < len(sentence_vc):
                    if regex_list[index] == sentence_vc[index]:
                        letter_index = sentence_vc[index].find(split)
                        word = sentence[index]
                        sentence[index] = word[:letter_index + 2] + " " + word[letter_index + 2:]
                        #print(sentence[index], sentence_vc[index], index)
                    index += 1
    
    sentence_splitting = ' '.join(sentence)
    sentence_splitting_vc = ' '.join(sentence)
    sentence = sentence_splitting.split(" ")
    sentence_vc = sentence_in_vc(sentence_splitting_vc).split(" ")
                    
    for split in splitting:                            
        if split == "VCCCV":
            regex_list_of_list = []  # kreiram prostor za praznu listu u koju će se pohraniti komadići lista jer regex vraća listu
            for word_vc in sentence_vc:  # prolazim kroz sve riječi u obliku V i C
                regex = re.findall(r'.*{}.*'.format(split), word_vc)  # regeksom pretražujem koje su to riječi koje tražim
                if not regex:  # ako regeks nije pronašao match, vratit će praznu listu, ako vrati praznu listu onda će u regex_list_of_list na to mjesto upisati "X"
                    regex_list_of_list.append("X")
                else:
                    regex_list_of_list.append(regex)  # ako je regeks pronašao match, dodaj taj match na mjesto u regex_list_of_list
            regex_list = [val for sublist in regex_list_of_list for val in sublist]  # pošto imamo listu lista, smanjio sam ju za jedan level s ovim djelom koda
            
            if len(regex_list) == len(sentence_vc):
                index = 0
                while index < len(sentence_vc):
                    if regex_list[index] == sentence_vc[index]:
                        difference_st = sentence[index].find("st") - sentence_vc[index].find("VCCCV")
                        difference_xt = sentence[index].find("xt") - sentence_vc[index].find("VCCCV")
                        
                        if difference_st == 1 or difference_xt == 1:
                            letter_index = sentence_vc[index].find(split)
                            word = sentence[index]
                            sentence[index] = word[:letter_index + 2] + " " + word[letter_index + 2:]
                            #print(sentence[index], sentence_vc[index], index)
                        else:
                            letter_index = sentence_vc[index].find(split)
                            word = sentence[index]
                            sentence[index] = word[:letter_index + 3] + " " + word[letter_index + 3:]
                            #print(sentence[index], sentence_vc[index], index)
                    index += 1
                    
                    
    sentence_splitting = ' '.join(sentence)
    sentence_splitting_vc = ' '.join(sentence)
    sentence = sentence_splitting.split(" ")
    sentence_vc = sentence_in_vc(sentence_splitting_vc).split(" ")
    
    for split in splitting:       
        if split == "VCV":
            regex_list_of_list = []  # kreiram prostor za praznu listu u koju će se pohraniti komadići lista jer regex vraća listu
            for word_vc in sentence_vc:  # prolazim kroz sve riječi u obliku V i C
                regex = re.findall(r'.*{}.*'.format(split), word_vc)  # regeksom pretražujem koje su to riječi koje tražim
                if not regex:  # ako regeks nije pronašao match, vratit će praznu listu, ako vrati praznu listu onda će u regex_list_of_list na to mjesto upisati "X"
                    regex_list_of_list.append("X")
                else:
                    regex_list_of_list.append(regex)  # ako je regeks pronašao match, dodaj taj match na mjesto u regex_list_of_list
            regex_list = [val for sublist in regex_list_of_list for val in sublist]  # pošto imamo listu lista, smanjio sam ju za jedan level s ovim djelom koda
            
            if len(regex_list) == len(sentence_vc):
                index = 0
                while index < len(sentence_vc):
                    if regex_list[index] == sentence_vc[index]:
                        letter_index = sentence_vc[index].find(split)
                        word = sentence[index]
                        sentence[index] = word[:letter_index + 1] + " " + word[letter_index + 1:]
                        #print(sentence[index], sentence_vc[index], index)
                    index += 1

    sentence_splitting = ' '.join(sentence)
    sentence_splitting_vc = ' '.join(sentence)
    sentence = sentence_splitting.split(" ")
    sentence_vc = sentence_in_vc(sentence_splitting_vc).split(" ")
                    
    for split in splitting:       
        if split == "VV":
            regex_list_of_list = []  # kreiram prostor za praznu listu u koju će se pohraniti komadići lista jer regex vraća listu
            for word_vc in sentence_vc:  # prolazim kroz sve riječi u obliku V i C
                regex = re.findall(r'.*{}.*'.format(split), word_vc)  # regeksom pretražujem koje su to riječi koje tražim
                if not regex:  # ako regeks nije pronašao match, vratit će praznu listu, ako vrati praznu listu onda će u regex_list_of_list na to mjesto upisati "X"
                    regex_list_of_list.append("X")
                else:
                    regex_list_of_list.append(regex)  # ako je regeks pronašao match, dodaj taj match na mjesto u regex_list_of_list
            regex_list = [val for sublist in regex_list_of_list for val in sublist]  # pošto imamo listu lista, smanjio sam ju za jedan level s ovim djelom koda
            #print(regex_list)

            index = 0
            if len(regex_list) == len(sentence_vc):
                index = 0
                while index < len(sentence_vc):
                    if regex_list[index] == sentence_vc[index]:
                        letter_index = sentence_vc[index].find(split)
                        word = sentence[index]
                        vowels_check = word[letter_index] + word[letter_index + 1]
                        if vowels_check.lower() not in vowels:
                            sentence[index] = word[:letter_index + 1] + " " + word[letter_index + 1:]
                            #print(sentence[index], sentence_vc[index], index)
                    index += 1

    sentence_splitting = ' '.join(sentence)  # join and remove duplicated spaces in word
    return re.sub(' +', ' ', sentence_splitting)

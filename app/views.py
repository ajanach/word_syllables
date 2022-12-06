from app import app
from flask import render_template, request, redirect, send_from_directory, abort
import re
from compound_split import doc_split
import string
from datetime import datetime
import os
from werkzeug.utils import secure_filename

app.config["TXT_UPLOADS"] = "C:/Users/antonio/Desktop/app/app/static/files"
app.config["ALLOW_TXT_EXTENSIONS"] = "TXT"
app.config["MAX_IMAGE_FILESIZE"] = 4 * 1024 * 1024

def verify_txt(filename):
    if not "." in filename:
        return False
    ext = filename.rsplit(".", 1)[1]
    
    if ext.upper() in app.config["ALLOW_TXT_EXTENSIONS"]:
        return True
    else:
        return False
    
def allowed_image_filesize(filesize):
    if int(filesize) >= app.config["MAX_IMAGE_FILESIZE"]:
        return True
    else:
        return False

def clear_result():
    if request.method == "POST":
        sentence = ""
        entry = ""
        error = ""
        return render_template("public/upload_txt.html", entry=entry, sentence=sentence, error=error)

@app.route("/")
def home():
    return render_template("public/index.html")

@app.route("/text-input", methods=["GET", "POST"])
def text_input():
    if request.method == "POST":
        sentence = request.form.get('sentence', type=str)
        print(sentence)
        # samoglasnici:
        vowels = ["a", "e", "i", "o", "u", "ä", "ö", "ü", "ei", "ai", "ey", "ay", "eu", "äu", "ie", "au", "aa", "ee", "oo"]

        # suglasnici
        consonants = ["b", "c", "d", "f", "g", "h", "j", "k", "l", "m", "n", "p", "q", "r", "s", "t", "v", "w", "x", "y", "z",
                    "ß", "sch", "ch", "ck", "qu", "ph"]
        # prefiksi:
        prefixes = ["an", "ab", "auf", "aus", "dis", "ein", "fehl", "her", "hin", "haupt", "in", "dar", "durch", "los", "mit",
                    "nach", "von", "vor", "weg", "um", "un", "ur", "ent", "er", "ver", "zer", "miss", "miß", "niss", "niß",
                    "ex", "non", "super", "trans", "kon", "hoch", "stink", "stock", "tief", "tod", "erz"]

        # rastavljanje na slogove:
        splitting = ["VCCV", "VCCCV", "VCV"]

        # rastavljanje na slogove u sredini
        splitting_in_middle = ["st", "tz", "pf"]

        # rečenica za testiranje 3. i 4. zadatka:
        # sentence = "kastrat, foxtrott, muster, hamster, fenster, hinstellen, katze, TROPFNASS, witzlos, krapfen, Guten, " \
        #           "Auf Wiedersehen, ABSTAMMEN, HARTZEN, KARPFEN, die knie, der knie"

        # sentence = "Gibt es ein Restaurant in der Nähe?"

        # doc_split.MIDDLE_DOT promijenjen tako da koristi razmak i u rečenici su rastavljene sve složenice:
        doc_split.MIDDLE_DOT = " "
        sentence_split = doc_split.doc_split(sentence)  # doc_split lista

        # u rečenici su uklonjene sve interpunkcije radi lakšeg rada nad riječima i svaka riječ je pospremljena u listu:
        # sentence_split_punctuation = re.sub(r'[^\w\s]', '', sentence_split)

        sentence_split_list = sentence_split.split(" ")  # svaka riječ je pospremljena u listu

        # prolazim po svim njemačkim prefiksima:
        for prefix in prefixes:
            # u varijablu pohranjujem koliko je dugačak prefix, vraća int
            prefix_length = len(prefix)
            # pretrčavam kroz listu:
            for word in sentence_split_list:
                # u listi tražim riječ koja se podudara sa prefikom
                if word[:prefix_length] == prefix:
                    # kad je pronađena podudarnost tada želim znati mjesto gdje se nalazi taj element
                    index = sentence_split_list.index(word)
                    # print(index, word) # test
                    # u varijablu x pohranjujem tu riječ odvojenu od prefiksa, gdje zapravo dobivam dvije riječi
                    x = word[:prefix_length] + " " + word[prefix_length:]
                    # te dvije riječi pohranjujem na mjesto gdje se ta riječ nalazila prije odvajanja prefiksa:
                    sentence_split_list[index] = x

        # spajam listu i ispisujem je:
        prefix_split = " ".join(sentence_split_list)

        # 3 i 4. dio zadatka:
        # kreiram listu iz stringa prefix_split i postavljam counter kako bi znao na kojem indexu se nalazi traženo slovo: - napravi funkciju za čitkost
        prefix_split_letter_list = list(prefix_split)
        counter = 0
        for letter in prefix_split_letter_list:
            for sign in consonants:
                # ako se letter nalazi u sign (consonant) bez obzira na velika ili mala slova i ako nije interpunkcijski znak:
                if letter == sign.upper() or letter == sign.lower() and letter != string.punctuation:
                    prefix_split_letter_list[counter] = "C"
                    # print(letter, counter, end=" ")
            for sign in vowels:
                # ako se letter nalazi u sign(vowels) bez obzira na velika ili mala slova i ako nije interpunkcijski znak:
                if letter == sign.upper() or letter == sign.lower() and letter != string.punctuation:
                    prefix_split_letter_list[counter] = "V"
                    # print(letter, counter, end=" ")
            counter += 1

        convert_in_consonant_vowels = ''.join(prefix_split_letter_list)

        # sada ću koristiti jednu i drugu listu kako bi pronašao match pravila i dodao razmak originalnoj listi sa riječima
        convert_in_consonant_vowels_list = convert_in_consonant_vowels.split(" ")  # kreirana lista koja sadrži C i V
        prefix_split_list = prefix_split.split(" ")  # kreirana lista koja sadrži riječi

        for split in splitting:
            if split == "VCCV":
                regex_list_of_list = []  # kreiram prostor za praznu listu u koju će se pohraniti komadići lista jer regex vraća listu
                for word_VC in convert_in_consonant_vowels_list:  # prolazim kroz sve riječi u obliku V i C
                    regex = re.findall(r".*{}.*".format(split), word_VC)  # regeksom pretražujem koje su to riječi koje tražim
                    if not regex:  # ako regeks nije pronašao match, vratit će praznu listu, ako vrati praznu listu onda će u regex_list_of_list na to mjesto upisati "X"
                        regex_list_of_list.append("X")
                    else:
                        regex_list_of_list.append(
                            regex)  # ako je regeks pronašao match, dodaj taj match na mjesto u regex_list_of_list
                regex_list = [val for sublist in regex_list_of_list for val in
                            sublist]  # pošto imamo listu lista, smanjio sam ju za jedan level s ovim djelom koda
                # print(regex_list)  # za provjeru
                if len(regex_list) == len(
                        convert_in_consonant_vowels_list):  # checksum provjera istih duljina regex_liste i liste koja sadrži V i C, da ne bi došlo do krivog rastavljanja
                    index_location = 0  # postavljen brojač koji se koristi za pozicioniranje lista indeksa
                    while index_location < len(
                            convert_in_consonant_vowels_list):  # svejedno da li stavljam duljinu V i C rečenice ili regex liste
                        if regex_list[index_location] == convert_in_consonant_vowels_list[index_location]:  # jako bitan dio
                            x = convert_in_consonant_vowels_list[index_location].find(
                                split)  # index koji govori na kojem mjestu u riječi počinje pattern VCCCV
                            word = prefix_split_list[
                                index_location]  # moram pospremiti tu riječ koju treba rastaviti u varijablu
                            prefix_split_list[index_location] = word[:x + 2] + " " + word[
                                                                                    x + 2:]  # iz riječi koja se nalazi na indexu zapisujemo novu riječ sa razmakom gdje treba biti
                            # print(index_location, x, prefix_split_list[index_location])
                        index_location += 1

            if split == "VCCCV":
                regex_list_of_list = []  # kreiram prostor za praznu listu u koju će se pohraniti komadići lista jer regex vraća listu
                for word_VC in convert_in_consonant_vowels_list:  # prolazim kroz sve riječi u obliku V i C
                    regex = re.findall(r".*{}.*".format(split), word_VC)  # regeksom pretražujem koje su to riječi koje tražim
                    if not regex:  # ako regeks nije pronašao match, vratit će praznu listu, ako vrati praznu listu onda će u regex_list_of_list na to mjesto upisati "X"
                        regex_list_of_list.append("X")
                    else:
                        regex_list_of_list.append(
                            regex)  # ako je regeks pronašao match, dodaj taj match na mjesto u regex_list_of_list
                regex_list = [val for sublist in regex_list_of_list for val in
                            sublist]  # pošto imamo listu lista, smanjio sam ju za jedan level s ovim djelom koda
                # print(regex_list)  # za provjeru
                if len(regex_list) == len(convert_in_consonant_vowels_list):
                    index_location = 0
                    while index_location < len(
                            convert_in_consonant_vowels_list):  # svejedno da li stavljam duljinu V i C rečenice ili regex liste
                        if regex_list[index_location] == convert_in_consonant_vowels_list[index_location]:
                            difference_st = prefix_split_list[index_location].find("st") - convert_in_consonant_vowels_list[
                                index_location].find("VCCCV")
                            difference_xt = prefix_split_list[index_location].find("xt") - convert_in_consonant_vowels_list[
                                index_location].find("VCCCV")

                            # 4.3 pravilo, razlika patterna VCCCV i na kojem indeksu se nalazi st u riječi mora biti točno 1:
                            # 4.4 pravilo, razlika patterna VCCCV i na kojem indeksu se nalazi xt u riječi isto mora biti točno 1:
                            if difference_st == 1 or difference_xt == 1:
                                x = convert_in_consonant_vowels_list[index_location].find(split)
                                word = prefix_split_list[index_location]
                                prefix_split_list[index_location] = word[:x + 2] + " " + word[x + 2:]
                                # print(index_location, x, prefix_split_list[index_location])

                            else:
                                x = convert_in_consonant_vowels_list[index_location].find(split)
                                word = prefix_split_list[index_location]
                                prefix_split_list[index_location] = word[:x + 3] + " " + word[x + 3:]
                                # print(index_location, x, prefix_split_list[index_location])
                        index_location += 1

            if split == "VCV":
                regex_list_of_list = []
                for word_VC in convert_in_consonant_vowels_list:
                    regex = re.findall(r".*{}.*".format(split), word_VC)
                    if not regex:
                        regex_list_of_list.append("X")
                    else:
                        regex_list_of_list.append(regex)
                regex_list = [val for sublist in regex_list_of_list for val in sublist]
                # print(regex_list)
                if len(regex_list) == len(convert_in_consonant_vowels_list):
                    index_location = 0
                    while index_location < len(
                            convert_in_consonant_vowels_list):  # svejedno da li stavljam duljinu V i C rečenice ili regex liste
                        if regex_list[index_location] == convert_in_consonant_vowels_list[index_location]:
                            x = convert_in_consonant_vowels_list[index_location].find(
                                split)  # index koji govori na kojem mjestu u riječi počinje pattern VCCCV
                            word = prefix_split_list[index_location]
                            prefix_split_list[index_location] = word[:x + 1] + " " + word[
                                                                                    x + 1:]  # iz riječi koja se nalazi na indexu zapisujemo novu riječ sa razmakom gdje treba biti
                            # print(index_location, x, prefix_split_list[index_location])
                        index_location += 1

        # 4. dio zadatka:
        prefix_split_list_join = ' '.join(prefix_split_list)
        prefix_split_letter_list = list(prefix_split_list_join)
        # kreiram listu iz stringa prefix_split i postavljam counter kako bi znao na kojem indexu se nalazi traženo slovo: - treba napisati funkciju za ovo:
        counter = 0
        for letter in prefix_split_letter_list:
            for sign in consonants:
                # ako se letter nalazi u sign (consonant) bez obzira na velika ili mala slova i ako nije interpunkcijski znak:
                if letter == sign.upper() or letter == sign.lower() and letter != string.punctuation:
                    prefix_split_letter_list[counter] = "C"
                    # print(letter, counter, end=" ")
            for sign in vowels:
                # ako se letter nalazi u sign(vowels) bez obzira na velika ili mala slova i ako nije interpunkcijski znak:
                if letter == sign.upper() or letter == sign.lower() and letter != string.punctuation:
                    prefix_split_letter_list[counter] = "V"
                    # print(letter, counter, end=" ")
            counter += 1

        convert_in_consonant_vowels = ''.join(prefix_split_letter_list)

        # ostatak 4. zadatka da pokupi još one koji nisu rastavljeni u prvom koraku:
        prefix_split_list = prefix_split_list_join.split(" ")
        convert_in_consonant_vowels_list = convert_in_consonant_vowels.split(" ")  # kreirana lista koja sadrži C i V ----- vjerojatno ne potrebno, ali za svaki slučaj

        for split in splitting:
            if split == "VCCV":
                regex_list_of_list = []  # kreiram prostor za praznu listu u koju će se pohraniti komadići lista jer regex vraća listu
                for word_VC in convert_in_consonant_vowels_list:  # prolazim kroz sve riječi u obliku V i C
                    regex = re.findall(r".*{}.*".format(split), word_VC)  # regeksom pretražujem koje su to riječi koje tražim
                    if not regex:  # ako regeks nije pronašao match, vratit će praznu listu, ako vrati praznu listu onda će u regex_list_of_list na to mjesto upisati "X"
                        regex_list_of_list.append("X")
                    else:
                        regex_list_of_list.append(
                            regex)  # ako je regeks pronašao match, dodaj taj match na mjesto u regex_list_of_list
                regex_list = [val for sublist in regex_list_of_list for val in
                            sublist]  # pošto imamo listu lista, smanjio sam ju za jedan level s ovim djelom koda
                # print(regex_list)  # za provjeru
                if len(regex_list) == len(
                        convert_in_consonant_vowels_list):  # checksum provjera istih duljina regex_liste i liste koja sadrži V i C, da ne bi došlo do krivog rastavljanja
                    index_location = 0  # postavljen brojač koji se koristi za pozicioniranje lista indeksa
                    while index_location < len(
                            convert_in_consonant_vowels_list):  # svejedno da li stavljam duljinu V i C rečenice ili regex liste
                        if regex_list[index_location] == convert_in_consonant_vowels_list[index_location]:  # jako bitan dio
                            x = convert_in_consonant_vowels_list[index_location].find(
                                split)  # index koji govori na kojem mjestu u riječi počinje pattern VCCCV
                            word = prefix_split_list[
                                index_location]  # moram pospremiti tu riječ koju treba rastaviti u varijablu
                            prefix_split_list[index_location] = word[:x + 2] + " " + word[
                                                                                    x + 2:]  # iz riječi koja se nalazi na indexu zapisujemo novu riječ sa razmakom gdje treba biti
                            # print(index_location, x, prefix_split_list[index_location])
                        index_location += 1

            if split == "VCCCV":
                regex_list_of_list = []  # kreiram prostor za praznu listu u koju će se pohraniti komadići lista jer regex vraća listu
                for word_VC in convert_in_consonant_vowels_list:  # prolazim kroz sve riječi u obliku V i C
                    regex = re.findall(r".*{}.*".format(split), word_VC)  # regeksom pretražujem koje su to riječi koje tražim
                    if not regex:  # ako regeks nije pronašao match, vratit će praznu listu, ako vrati praznu listu onda će u regex_list_of_list na to mjesto upisati "X"
                        regex_list_of_list.append("X")
                    else:
                        regex_list_of_list.append(
                            regex)  # ako je regeks pronašao match, dodaj taj match na mjesto u regex_list_of_list
                regex_list = [val for sublist in regex_list_of_list for val in
                            sublist]  # pošto imamo listu lista, smanjio sam ju za jedan level s ovim djelom koda
                # print(regex_list)  # za provjeru
                if len(regex_list) == len(convert_in_consonant_vowels_list):
                    index_location = 0
                    while index_location < len(
                            convert_in_consonant_vowels_list):  # svejedno da li stavljam duljinu V i C rečenice ili regex liste
                        if regex_list[index_location] == convert_in_consonant_vowels_list[index_location]:
                            difference_st = prefix_split_list[index_location].find("st") - convert_in_consonant_vowels_list[
                                index_location].find("VCCCV")
                            difference_xt = prefix_split_list[index_location].find("xt") - convert_in_consonant_vowels_list[
                                index_location].find("VCCCV")

                            # 4.3 pravilo, razlika patterna VCCCV i na kojem indeksu se nalazi st u riječi mora biti točno 1:
                            # 4.4 pravilo, razlika patterna VCCCV i na kojem indeksu se nalazi xt u riječi isto mora biti točno 1:
                            if difference_st == 1 or difference_xt == 1:
                                x = convert_in_consonant_vowels_list[index_location].find(split)
                                word = prefix_split_list[index_location]
                                prefix_split_list[index_location] = word[:x + 2] + " " + word[x + 2:]
                                # print(index_location, x, prefix_split_list[index_location])

                            else:
                                x = convert_in_consonant_vowels_list[index_location].find(split)
                                word = prefix_split_list[index_location]
                                prefix_split_list[index_location] = word[:x + 3] + " " + word[x + 3:]
                                # print(index_location, x, prefix_split_list[index_location])
                        index_location += 1

            if split == "VCV":
                regex_list_of_list = []
                for word_VC in convert_in_consonant_vowels_list:
                    regex = re.findall(r".*{}.*".format(split), word_VC)
                    if not regex:
                        regex_list_of_list.append("X")
                    else:
                        regex_list_of_list.append(regex)
                regex_list = [val for sublist in regex_list_of_list for val in sublist]
                # print(regex_list)
                if len(regex_list) == len(convert_in_consonant_vowels_list):
                    index_location = 0
                    while index_location < len(
                            convert_in_consonant_vowels_list):  # svejedno da li stavljam duljinu V i C rečenice ili regex liste
                        if regex_list[index_location] == convert_in_consonant_vowels_list[index_location]:
                            x = convert_in_consonant_vowels_list[index_location].find(split)  # index koji govori na kojem mjestu u riječi počinje pattern VCCCV
                            word = prefix_split_list[index_location]
                            prefix_split_list[index_location] = word[:x + 1] + " " + word[x + 1:]  # iz riječi koja se nalazi na indexu zapisujemo novu riječ sa razmakom gdje treba biti
                            # print(index_location, x, word, prefix_split_list[index_location])
                        index_location += 1

        prefix_split_list_join = ' '.join(prefix_split_list)
        prefix_split_letter_list = list(prefix_split_list_join)
        convert_in_consonant_vowels = ''.join(prefix_split_letter_list)

        # 5. zadatak:
        prefix_split_list = prefix_split_list_join.split(" ")

        regex_list_of_list = []
        for word in prefix_split_list:  # prolazim kroz sve riječi u obliku V i C
            regex = re.findall(r'(?i)knie.*', word)  # regeksom pretražujem koje su to riječi koje tražim
            if not regex:  # ako regeks nije pronašao match, vratit će praznu listu, ako vrati praznu listu onda će u regex_list_of_list na to mjesto upisati "X"
                regex_list_of_list.append("X")
            else:
                regex_list_of_list.append(regex)  # ako je regeks pronašao match, dodaj taj match na mjesto u regex_list_of_list
        regex_list = [val for sublist in regex_list_of_list for val in
                    sublist]  # pošto imamo listu lista, smanjio sam ju za jedan level s ovim djelom koda
        prefix_split_list_checksum = prefix_split_list

        if len(regex_list) == len(prefix_split_list_checksum):
            index_location = 0
            while index_location < len(prefix_split_list_checksum):
                if regex_list[index_location] == prefix_split_list_checksum[index_location]:
                    if prefix_split_list[index_location - 1].lower() == "die" or prefix_split_list[
                        index_location - 1].lower() == "der":
                        x = prefix_split_list[index_location].lower().find("knie")
                        word = prefix_split_list[index_location]
                        prefix_split_list[index_location] = word[:x + 3] + " " + word[x + 3:]
                    if ((prefix_split_list[index_location - 1][-1:] == "e" and prefix_split_list[index_location - 2] != "das") or prefix_split_list[index_location - 3][-1:] != "e")  or prefix_split_list[index_location - 1][-2:] == "er":
                        x = prefix_split_list[index_location].lower().find("knie")
                        word = prefix_split_list[index_location]
                        prefix_split_list[index_location] = word[:x + 3] + " " + word[x + 3:]
                index_location += 1

        splitted_sentence = ' '.join(prefix_split_list)
        entry = splitted_sentence
        return render_template("public/text_input.html", sentence=sentence, entry=entry)
    return render_template("public/text_input.html")

@app.route("/upload-txt", methods=["GET", "POST"])  
def upload_txt():
    if request.method == "POST":
        
        error = ""
        if allowed_image_filesize(request.cookies.get("filesize")):
            error = "File exceeded maximum size"
            return redirect("public/upload_txt.html", error=error)
        
        if request.files:
            txtfile = request.files["txt"]
             
            if txtfile.filename == "":
                error = "You need to browse your .txt file."
                return render_template("public/upload_txt.html", error=error)
                
            if txtfile.filename == ".txt":
                error = "Textual file must have a filename"
                return render_template("public/upload_txt.html", error=error)
            
            if not verify_txt(txtfile.filename):
                error = "Only .txt extension is allowed"
                return render_template("public/upload_txt.html", error=error)
            else:
                filename = secure_filename(txtfile.filename)
                
            txtfile.save(os.path.join(app.config["TXT_UPLOADS"], txtfile.filename))
            
        
            f = open("C:/Users/antonio/Desktop/app/app/static/files/" + filename)
            sentence = f.read()
            f.close()
            
            # samoglasnici:
            vowels = ["a", "e", "i", "o", "u", "ä", "ö", "ü", "ei", "ai", "ey", "ay", "eu", "äu", "ie", "au", "aa", "ee", "oo"]

            # suglasnici
            consonants = ["b", "c", "d", "f", "g", "h", "j", "k", "l", "m", "n", "p", "q", "r", "s", "t", "v", "w", "x", "y", "z",
                        "ß", "sch", "ch", "ck", "qu", "ph"]
            # prefiksi:
            prefixes = ["an", "ab", "auf", "aus", "dis", "ein", "fehl", "her", "hin", "haupt", "in", "dar", "durch", "los", "mit",
                        "nach", "von", "vor", "weg", "um", "un", "ur", "ent", "er", "ver", "zer", "miss", "miß", "niss", "niß",
                        "ex", "non", "super", "trans", "kon", "hoch", "stink", "stock", "tief", "tod", "erz"]

            # rastavljanje na slogove:
            splitting = ["VCCV", "VCCCV", "VCV"]

            # rečenica za testiranje 3. i 4. zadatka:
            # sentence = "kastrat, foxtrott, muster, hamster, fenster, hinstellen, katze, TROPFNASS, witzlos, krapfen, Guten, " \
            #           "Auf Wiedersehen, ABSTAMMEN, HARTZEN, KARPFEN, die knie, der knie"

            # doc_split.MIDDLE_DOT promijenjen tako da koristi razmak i u rečenici su rastavljene sve složenice:
            doc_split.MIDDLE_DOT = " "
            sentence_split = doc_split.doc_split(sentence)  # doc_split lista

            # u rečenici su uklonjene sve interpunkcije radi lakšeg rada nad riječima i svaka riječ je pospremljena u listu:
            # sentence_split_punctuation = re.sub(r'[^\w\s]', '', sentence_split)

            sentence_split_list = sentence_split.split(" ")  # svaka riječ je pospremljena u listu

            # prolazim po svim njemačkim prefiksima:
            for prefix in prefixes:
                # u varijablu pohranjujem koliko je dugačak prefix, vraća int
                prefix_length = len(prefix)
                # pretrčavam kroz listu:
                for word in sentence_split_list:
                    # u listi tražim riječ koja se podudara sa prefikom
                    if word[:prefix_length] == prefix:
                        # kad je pronađena podudarnost tada želim znati mjesto gdje se nalazi taj element
                        index = sentence_split_list.index(word)
                        # print(index, word) # test
                        # u varijablu x pohranjujem tu riječ odvojenu od prefiksa, gdje zapravo dobivam dvije riječi
                        x = word[:prefix_length] + " " + word[prefix_length:]
                        # te dvije riječi pohranjujem na mjesto gdje se ta riječ nalazila prije odvajanja prefiksa:
                        sentence_split_list[index] = x

            # spajam listu i ispisujem je:
            prefix_split = " ".join(sentence_split_list)

            # 3 i 4. dio zadatka:
            # kreiram listu iz stringa prefix_split i postavljam counter kako bi znao na kojem indexu se nalazi traženo slovo: - napravi funkciju za čitkost
            prefix_split_letter_list = list(prefix_split)
            counter = 0
            for letter in prefix_split_letter_list:
                for sign in consonants:
                    # ako se letter nalazi u sign (consonant) bez obzira na velika ili mala slova i ako nije interpunkcijski znak:
                    if letter == sign.upper() or letter == sign.lower() and letter != string.punctuation:
                        prefix_split_letter_list[counter] = "C"
                        # print(letter, counter, end=" ")
                for sign in vowels:
                    # ako se letter nalazi u sign(vowels) bez obzira na velika ili mala slova i ako nije interpunkcijski znak:
                    if letter == sign.upper() or letter == sign.lower() and letter != string.punctuation:
                        prefix_split_letter_list[counter] = "V"
                        # print(letter, counter, end=" ")
                counter += 1

            convert_in_consonant_vowels = ''.join(prefix_split_letter_list)

            # sada ću koristiti jednu i drugu listu kako bi pronašao match pravila i dodao razmak originalnoj listi sa riječima
            convert_in_consonant_vowels_list = convert_in_consonant_vowels.split(" ")  # kreirana lista koja sadrži C i V
            prefix_split_list = prefix_split.split(" ")  # kreirana lista koja sadrži riječi

            for split in splitting:
                if split == "VCCV":
                    regex_list_of_list = []  # kreiram prostor za praznu listu u koju će se pohraniti komadići lista jer regex vraća listu
                    for word_VC in convert_in_consonant_vowels_list:  # prolazim kroz sve riječi u obliku V i C
                        regex = re.findall(r".*{}.*".format(split), word_VC)  # regeksom pretražujem koje su to riječi koje tražim
                        if not regex:  # ako regeks nije pronašao match, vratit će praznu listu, ako vrati praznu listu onda će u regex_list_of_list na to mjesto upisati "X"
                            regex_list_of_list.append("X")
                        else:
                            regex_list_of_list.append(
                                regex)  # ako je regeks pronašao match, dodaj taj match na mjesto u regex_list_of_list
                    regex_list = [val for sublist in regex_list_of_list for val in
                                sublist]  # pošto imamo listu lista, smanjio sam ju za jedan level s ovim djelom koda
                    # print(regex_list)  # za provjeru
                    if len(regex_list) == len(
                            convert_in_consonant_vowels_list):  # checksum provjera istih duljina regex_liste i liste koja sadrži V i C, da ne bi došlo do krivog rastavljanja
                        index_location = 0  # postavljen brojač koji se koristi za pozicioniranje lista indeksa
                        while index_location < len(
                                convert_in_consonant_vowels_list):  # svejedno da li stavljam duljinu V i C rečenice ili regex liste
                            if regex_list[index_location] == convert_in_consonant_vowels_list[index_location]:  # jako bitan dio
                                x = convert_in_consonant_vowels_list[index_location].find(
                                    split)  # index koji govori na kojem mjestu u riječi počinje pattern VCCCV
                                word = prefix_split_list[
                                    index_location]  # moram pospremiti tu riječ koju treba rastaviti u varijablu
                                prefix_split_list[index_location] = word[:x + 2] + " " + word[
                                                                                        x + 2:]  # iz riječi koja se nalazi na indexu zapisujemo novu riječ sa razmakom gdje treba biti
                                # print(index_location, x, prefix_split_list[index_location])
                            index_location += 1

                if split == "VCCCV":
                    regex_list_of_list = []  # kreiram prostor za praznu listu u koju će se pohraniti komadići lista jer regex vraća listu
                    for word_VC in convert_in_consonant_vowels_list:  # prolazim kroz sve riječi u obliku V i C
                        regex = re.findall(r".*{}.*".format(split), word_VC)  # regeksom pretražujem koje su to riječi koje tražim
                        if not regex:  # ako regeks nije pronašao match, vratit će praznu listu, ako vrati praznu listu onda će u regex_list_of_list na to mjesto upisati "X"
                            regex_list_of_list.append("X")
                        else:
                            regex_list_of_list.append(
                                regex)  # ako je regeks pronašao match, dodaj taj match na mjesto u regex_list_of_list
                    regex_list = [val for sublist in regex_list_of_list for val in
                                sublist]  # pošto imamo listu lista, smanjio sam ju za jedan level s ovim djelom koda
                    # print(regex_list)  # za provjeru
                    if len(regex_list) == len(convert_in_consonant_vowels_list):
                        index_location = 0
                        while index_location < len(
                                convert_in_consonant_vowels_list):  # svejedno da li stavljam duljinu V i C rečenice ili regex liste
                            if regex_list[index_location] == convert_in_consonant_vowels_list[index_location]:
                                difference_st = prefix_split_list[index_location].find("st") - convert_in_consonant_vowels_list[
                                    index_location].find("VCCCV")
                                difference_xt = prefix_split_list[index_location].find("xt") - convert_in_consonant_vowels_list[
                                    index_location].find("VCCCV")

                                # 4.3 pravilo, razlika patterna VCCCV i na kojem indeksu se nalazi st u riječi mora biti točno 1:
                                # 4.4 pravilo, razlika patterna VCCCV i na kojem indeksu se nalazi xt u riječi isto mora biti točno 1:
                                if difference_st == 1 or difference_xt == 1:
                                    x = convert_in_consonant_vowels_list[index_location].find(split)
                                    word = prefix_split_list[index_location]
                                    prefix_split_list[index_location] = word[:x + 2] + " " + word[x + 2:]
                                    # print(index_location, x, prefix_split_list[index_location])

                                else:
                                    x = convert_in_consonant_vowels_list[index_location].find(split)
                                    word = prefix_split_list[index_location]
                                    prefix_split_list[index_location] = word[:x + 3] + " " + word[x + 3:]
                                    # print(index_location, x, prefix_split_list[index_location])
                            index_location += 1

                if split == "VCV":
                    regex_list_of_list = []
                    for word_VC in convert_in_consonant_vowels_list:
                        regex = re.findall(r".*{}.*".format(split), word_VC)
                        if not regex:
                            regex_list_of_list.append("X")
                        else:
                            regex_list_of_list.append(regex)
                    regex_list = [val for sublist in regex_list_of_list for val in sublist]
                    # print(regex_list)
                    if len(regex_list) == len(convert_in_consonant_vowels_list):
                        index_location = 0
                        while index_location < len(
                                convert_in_consonant_vowels_list):  # svejedno da li stavljam duljinu V i C rečenice ili regex liste
                            if regex_list[index_location] == convert_in_consonant_vowels_list[index_location]:
                                x = convert_in_consonant_vowels_list[index_location].find(
                                    split)  # index koji govori na kojem mjestu u riječi počinje pattern VCCCV
                                word = prefix_split_list[index_location]
                                prefix_split_list[index_location] = word[:x + 1] + " " + word[
                                                                                        x + 1:]  # iz riječi koja se nalazi na indexu zapisujemo novu riječ sa razmakom gdje treba biti
                                # print(index_location, x, prefix_split_list[index_location])
                            index_location += 1

            # 4. dio zadatka:
            prefix_split_list_join = ' '.join(prefix_split_list)
            prefix_split_letter_list = list(prefix_split_list_join)
            # kreiram listu iz stringa prefix_split i postavljam counter kako bi znao na kojem indexu se nalazi traženo slovo: - treba napisati funkciju za ovo:
            counter = 0
            for letter in prefix_split_letter_list:
                for sign in consonants:
                    # ako se letter nalazi u sign (consonant) bez obzira na velika ili mala slova i ako nije interpunkcijski znak:
                    if letter == sign.upper() or letter == sign.lower() and letter != string.punctuation:
                        prefix_split_letter_list[counter] = "C"
                        # print(letter, counter, end=" ")
                for sign in vowels:
                    # ako se letter nalazi u sign(vowels) bez obzira na velika ili mala slova i ako nije interpunkcijski znak:
                    if letter == sign.upper() or letter == sign.lower() and letter != string.punctuation:
                        prefix_split_letter_list[counter] = "V"
                        # print(letter, counter, end=" ")
                counter += 1

            convert_in_consonant_vowels = ''.join(prefix_split_letter_list)

            # ostatak 4. zadatka da pokupi još one koji nisu rastavljeni u prvom koraku:
            prefix_split_list = prefix_split_list_join.split(" ")
            convert_in_consonant_vowels_list = convert_in_consonant_vowels.split(" ")  # kreirana lista koja sadrži C i V ----- vjerojatno ne potrebno, ali za svaki slučaj

            for split in splitting:
                if split == "VCCV":
                    regex_list_of_list = []  # kreiram prostor za praznu listu u koju će se pohraniti komadići lista jer regex vraća listu
                    for word_VC in convert_in_consonant_vowels_list:  # prolazim kroz sve riječi u obliku V i C
                        regex = re.findall(r".*{}.*".format(split), word_VC)  # regeksom pretražujem koje su to riječi koje tražim
                        if not regex:  # ako regeks nije pronašao match, vratit će praznu listu, ako vrati praznu listu onda će u regex_list_of_list na to mjesto upisati "X"
                            regex_list_of_list.append("X")
                        else:
                            regex_list_of_list.append(
                                regex)  # ako je regeks pronašao match, dodaj taj match na mjesto u regex_list_of_list
                    regex_list = [val for sublist in regex_list_of_list for val in
                                sublist]  # pošto imamo listu lista, smanjio sam ju za jedan level s ovim djelom koda
                    # print(regex_list)  # za provjeru
                    if len(regex_list) == len(
                            convert_in_consonant_vowels_list):  # checksum provjera istih duljina regex_liste i liste koja sadrži V i C, da ne bi došlo do krivog rastavljanja
                        index_location = 0  # postavljen brojač koji se koristi za pozicioniranje lista indeksa
                        while index_location < len(
                                convert_in_consonant_vowels_list):  # svejedno da li stavljam duljinu V i C rečenice ili regex liste
                            if regex_list[index_location] == convert_in_consonant_vowels_list[index_location]:  # jako bitan dio
                                x = convert_in_consonant_vowels_list[index_location].find(
                                    split)  # index koji govori na kojem mjestu u riječi počinje pattern VCCCV
                                word = prefix_split_list[
                                    index_location]  # moram pospremiti tu riječ koju treba rastaviti u varijablu
                                prefix_split_list[index_location] = word[:x + 2] + " " + word[
                                                                                        x + 2:]  # iz riječi koja se nalazi na indexu zapisujemo novu riječ sa razmakom gdje treba biti
                                # print(index_location, x, prefix_split_list[index_location])
                            index_location += 1

                if split == "VCCCV":
                    regex_list_of_list = []  # kreiram prostor za praznu listu u koju će se pohraniti komadići lista jer regex vraća listu
                    for word_VC in convert_in_consonant_vowels_list:  # prolazim kroz sve riječi u obliku V i C
                        regex = re.findall(r".*{}.*".format(split), word_VC)  # regeksom pretražujem koje su to riječi koje tražim
                        if not regex:  # ako regeks nije pronašao match, vratit će praznu listu, ako vrati praznu listu onda će u regex_list_of_list na to mjesto upisati "X"
                            regex_list_of_list.append("X")
                        else:
                            regex_list_of_list.append(
                                regex)  # ako je regeks pronašao match, dodaj taj match na mjesto u regex_list_of_list
                    regex_list = [val for sublist in regex_list_of_list for val in
                                sublist]  # pošto imamo listu lista, smanjio sam ju za jedan level s ovim djelom koda
                    # print(regex_list)  # za provjeru
                    if len(regex_list) == len(convert_in_consonant_vowels_list):
                        index_location = 0
                        while index_location < len(
                                convert_in_consonant_vowels_list):  # svejedno da li stavljam duljinu V i C rečenice ili regex liste
                            if regex_list[index_location] == convert_in_consonant_vowels_list[index_location]:
                                difference_st = prefix_split_list[index_location].find("st") - convert_in_consonant_vowels_list[
                                    index_location].find("VCCCV")
                                difference_xt = prefix_split_list[index_location].find("xt") - convert_in_consonant_vowels_list[
                                    index_location].find("VCCCV")

                                # 4.3 pravilo, razlika patterna VCCCV i na kojem indeksu se nalazi st u riječi mora biti točno 1:
                                # 4.4 pravilo, razlika patterna VCCCV i na kojem indeksu se nalazi xt u riječi isto mora biti točno 1:
                                if difference_st == 1 or difference_xt == 1:
                                    x = convert_in_consonant_vowels_list[index_location].find(split)
                                    word = prefix_split_list[index_location]
                                    prefix_split_list[index_location] = word[:x + 2] + " " + word[x + 2:]
                                    # print(index_location, x, prefix_split_list[index_location])

                                else:
                                    x = convert_in_consonant_vowels_list[index_location].find(split)
                                    word = prefix_split_list[index_location]
                                    prefix_split_list[index_location] = word[:x + 3] + " " + word[x + 3:]
                                    # print(index_location, x, prefix_split_list[index_location])
                            index_location += 1

                if split == "VCV":
                    regex_list_of_list = []
                    for word_VC in convert_in_consonant_vowels_list:
                        regex = re.findall(r".*{}.*".format(split), word_VC)
                        if not regex:
                            regex_list_of_list.append("X")
                        else:
                            regex_list_of_list.append(regex)
                    regex_list = [val for sublist in regex_list_of_list for val in sublist]
                    # print(regex_list)
                    if len(regex_list) == len(convert_in_consonant_vowels_list):
                        index_location = 0
                        while index_location < len(
                                convert_in_consonant_vowels_list):  # svejedno da li stavljam duljinu V i C rečenice ili regex liste
                            if regex_list[index_location] == convert_in_consonant_vowels_list[index_location]:
                                x = convert_in_consonant_vowels_list[index_location].find(split)  # index koji govori na kojem mjestu u riječi počinje pattern VCCCV
                                word = prefix_split_list[index_location]
                                prefix_split_list[index_location] = word[:x + 1] + " " + word[x + 1:]  # iz riječi koja se nalazi na indexu zapisujemo novu riječ sa razmakom gdje treba biti
                                # print(index_location, x, word, prefix_split_list[index_location])
                            index_location += 1

            prefix_split_list_join = ' '.join(prefix_split_list)
            prefix_split_letter_list = list(prefix_split_list_join)
            convert_in_consonant_vowels = ''.join(prefix_split_letter_list)

            # 5. zadatak:
            prefix_split_list = prefix_split_list_join.split(" ")

            regex_list_of_list = []
            for word in prefix_split_list:  # prolazim kroz sve riječi u obliku V i C
                regex = re.findall(r'(?i)knie.*', word)  # regeksom pretražujem koje su to riječi koje tražim
                if not regex:  # ako regeks nije pronašao match, vratit će praznu listu, ako vrati praznu listu onda će u regex_list_of_list na to mjesto upisati "X"
                    regex_list_of_list.append("X")
                else:
                    regex_list_of_list.append(regex)  # ako je regeks pronašao match, dodaj taj match na mjesto u regex_list_of_list
            regex_list = [val for sublist in regex_list_of_list for val in
                        sublist]  # pošto imamo listu lista, smanjio sam ju za jedan level s ovim djelom koda
            prefix_split_list_checksum = prefix_split_list

            if len(regex_list) == len(prefix_split_list_checksum):
                index_location = 0
                while index_location < len(prefix_split_list_checksum):
                    if regex_list[index_location] == prefix_split_list_checksum[index_location]:
                        if prefix_split_list[index_location - 1].lower() == "die" or prefix_split_list[
                            index_location - 1].lower() == "der":
                            x = prefix_split_list[index_location].lower().find("knie")
                            word = prefix_split_list[index_location]
                            prefix_split_list[index_location] = word[:x + 3] + " " + word[x + 3:]
                        if ((prefix_split_list[index_location - 1][-1:] == "e" and prefix_split_list[index_location - 2] != "das") or prefix_split_list[index_location - 3][-1:] != "e")  or prefix_split_list[index_location - 1][-2:] == "er":
                            x = prefix_split_list[index_location].lower().find("knie")
                            word = prefix_split_list[index_location]
                            prefix_split_list[index_location] = word[:x + 3] + " " + word[x + 3:]
                    index_location += 1

            splitted_sentence = ' '.join(prefix_split_list)

            entry = splitted_sentence
            txtfile = "File name: " + txtfile.filename 
                        
            return render_template("public/upload_txt.html", entry=entry, sentence=sentence, error=error, txtfile=txtfile)
            
    return render_template("public/upload_txt.html")
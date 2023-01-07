from app import app
import os, algorithm, test_accuracy
from flask import render_template, request, redirect, send_from_directory, abort
from datetime import datetime
from werkzeug.utils import secure_filename

vowels = ["a", "e", "i", "o", "u", "ä", "ö", "ü", "ei", "ai", "ey", "ay", "eu", "äu", "ie", "au", "aa", "ee", "oo"]

consonants = ["b", "c", "d", "f", "g", "h", "j", "k", "l", "m", "n", "p", "q", "r", "s", "t", "v", "w", "x", "y", "z", "ß", "sch", "ch", "ck", "qu", "ph"]

prefixes = ["an", "ab", "auf", "aus", "dis", "ein", "fehl", "her", "hin", "haupt", "in", "dar", "durch", "los", "mit",
            "nach", "von", "vor", "weg", "um", "un", "ur", "ent", "er", "ver", "zer", "miss", "miß", "niss", "niß",
            "ex", "non", "super", "trans", "kon", "hoch", "stink", "stock", "tief", "tod", "erz"]

splitting = ["VCCV", "VCCCV", "VCV", "VV"]

app.config["TXT_UPLOADS"] = "D:/GitHub/word_syllables/app/static/files"
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
        txtfile = ""
        return render_template("public/upload_txt.html", entry=entry, sentence=sentence, error=error, txtfile=txtfile)

@app.route("/")
def home():
    return render_template("public/index.html")

@app.route("/text-input", methods=["GET", "POST"])
def text_input():
    if request.method == "POST":
        sentence = request.form.get('sentence', type=str)
        print(sentence)

        prvi_krug = algorithm.syllables_rules(algorithm.syllables_rules_exceptions(sentence))
        drugi_krug = algorithm.syllables_rules(algorithm.syllables_rules_exceptions(prvi_krug))
        treci_krug = algorithm.syllables_rules(algorithm.syllables_rules_exceptions(drugi_krug))
        sentence_vc = algorithm.sentence_in_vc(treci_krug)

        entry = treci_krug
        return render_template("public/text_input.html", sentence=sentence, entry=entry, sentence_vc=sentence_vc)
    return render_template("public/text_input.html")

@app.route("/upload-txt", methods=["GET", "POST"])  
def upload_txt():
    if request.method == "POST":
        
        error = ""
        entry = ""
        sentence = ""
        txtfile = ""
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
        
            f = open("D:/GitHub/word_syllables/app/static/files/" + filename)
            sentence = f.read()
            f.close()

            prvi_krug = algorithm.syllables_rules(algorithm.syllables_rules_exceptions(sentence))
            drugi_krug = algorithm.syllables_rules(algorithm.syllables_rules_exceptions(prvi_krug))
            treci_krug = algorithm.syllables_rules(algorithm.syllables_rules_exceptions(drugi_krug))
            #sentence_vc = algorithm.sentence_in_vc(treci_krug)

            entry = treci_krug 
            txtfile = "File name: " + txtfile.filename
        return render_template("public/upload_txt.html", entry=entry, sentence=sentence, error=error, txtfile=txtfile)
            
    return render_template("public/upload_txt.html")

@app.route("/accuracy", methods=["GET", "POST"])
def accuracy():
    entry = test_accuracy.accuracy()
    return render_template("public/accuracy.html", entry = entry)
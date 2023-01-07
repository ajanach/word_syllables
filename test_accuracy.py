import algorithm
from prettytable import PrettyTable
from termcolor import colored
import csv

test_words = ["Diät", "Knie", "die knie", "der knie", "reise knie", "Auto", "Seeufer", "Katze", "Tatze", "Pfütze", "putzen", "platzen", "Bürste", "Kiste", "Hamster", "Fenster", "hinstellen", "darstellen", "erstarren", "plötzlich", 
              "Postauto", "Kratzbaum", "boxen", "heben", "rodeln", "Schifffahrt", "Mussspiel", "wichtigsten", "besuchen", "gewinnen", "vergessen", "abangeln", "Kreuzotter", "poetisch", "Nationen", "aber", "über", "Kreuzklemme", 
              "Foxtrott", "witzlos", "witzig", "wegschmeißen", "Bettüberzug", "wirtschaft", "Beziehungsknatsch", "Gletscher", "Wurstscheibe", "Borretschgewächs", "Bodden", "Handball", "Neubau", "Stalltür", "Autobahnanschlussstelle",
              "Laufschuhe", "Baustelle", "Lebkuchen", "Himbeere", "Klassenzimmer", "Hubbleteleskop", "Botschaft", "Schokoladenfabrik", "Hühnersuppe", "Schweinebraten", "Halsschmerzen", "Weltanschauung", "Weltschmerz", "Weihnachtsbaum",
              "Kugelschreiber", "Bohnensalat", "Freundschaftsbezeigung", "Weihnachtsmannfigur", "Glasflächenreinigung"]

verify_words = ["Di ät", "Knie", "die kni e", "der kni e", "rei se kni e", "Au to", "See ufer", "Kat ze", "Tat ze", "Pfüt ze", "put zen", "plat zen", "Bürs te", "Kis te", "Hams ter", "Fens ter", "hin stel len", "dar stel len",
                "er star ren", "plötz lich", "Post au to", "Kratz baum", "bo xen", "he ben", "ro deln", "Schiff fahrt", "Muss spiel", "wich tigs ten", "be su chen", "ge win nen", "ver ges sen", "ab an geln", "Kreuz ot ter", 
                "po e tisch", "Na ti o nen", "a ber", "ü ber", "Kreuz klem me", "Fox trott", "witz los ", "wit zig", "weg schmei ßen", "Bett ü ber zug", "wirt schaft", "Be zieh ungs knatsch", "Glet scher", "Wurst schei be", 
                "Bor retsch ge wächs", "Bod den", "Hand ball", "Neu bau", "Stall tür", "Au to bahn an schluss stel le", "Lauf schu he", "Bau stel le", "Leb ku chen", "Him bee re", "Klas sen zim mer", "Hub ble te le skop",
                "Bot schaft", "Scho ko la den fa brik", "Hüh ner sup pe", "Schwei ne bra ten", "Hals schmer zen", "Welt an schau ung", "Welt schmerz", "Weih nachts baum", "Ku gel schrei ber", "Boh nen sa lat", "Freund schafts be zei gung",
                "Weih nachts mann fi gur", "Glas fläch en rei ni gung"]

correct_words = []

partial_correct_words = []

table = PrettyTable()
table.field_names = ['Test word', 'Verify word', 'Algorithm output', 'Partial correct word', 'Partial uncorrect word', 'Percent of partial word accuracy']

def accuracy():
    global test_words
    global verify_words
    global correct_words
    global partial_correct_words
    counter = 0
    for word in test_words:
        prvi_krug = algorithm.syllables_rules(algorithm.syllables_rules_exceptions(word))
        drugi_krug = algorithm.syllables_rules(algorithm.syllables_rules_exceptions(prvi_krug))
        treci_krug = algorithm.syllables_rules(algorithm.syllables_rules_exceptions(drugi_krug))
        
        algorithm_output = treci_krug
        
        if algorithm_output == verify_words[counter]:
            correct_words.append(1)
            partial_correct_words.append(1)
            table.add_row([word, verify_words[counter], algorithm_output, "yes", "no", format(1, ".2f")])
        else:
            correct_words.append(0)
            word_split = algorithm_output.split()
            verify_words_split = verify_words[counter].split()
            
            part_number = len(verify_words_split)
            part_correct = 0
            for part_vws in verify_words_split:
                for part_ws in word_split: 
                    if part_ws == part_vws:
                        part_correct += 1
            
            
            #print(algorithm_output + " | ", verify_words[counter], part_correct, part_number)
            partial_accuracy = part_correct / part_number
            partial_correct_words.append(partial_accuracy)
            table.add_row([word, verify_words[counter], algorithm_output, "no", "yes", format(partial_accuracy, ".2f")])
            
        counter += 1

    table.add_row([colored("---", "yellow"), colored("---", "yellow"), colored("---", "yellow"), colored(format(sum(partial_correct_words), ".2f"), "yellow"), colored(format(len(partial_correct_words) - sum(partial_correct_words), ".2f"), "yellow"), colored(format(sum(partial_correct_words) / len(partial_correct_words), ".2f"), "yellow")])

    print(table)

    entry = f"Full measure of accuracy: {sum(correct_words) / len(correct_words):.2f}\n"\
            f"Correct words: {sum(correct_words)}\n"\
            f"Uncorrect words: {len(correct_words) - sum(correct_words)}\n"\
            f"Number of words: {len(correct_words)}\n"\
            f"Partial measure of accuracy: {sum(partial_correct_words) / len(partial_correct_words):.2f}\n"\
            f"Partial correct words: {sum(partial_correct_words):.2f}\n"\
            f"Partial uncorrect words: {len(partial_correct_words) - sum(partial_correct_words):.2f}\n"\
            f"Number of words: {len(partial_correct_words)}\n"\

    return entry
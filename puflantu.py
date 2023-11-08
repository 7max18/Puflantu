import csv, argparse, re
from itertools import chain, combinations
from modifiers import prefixes, suffixes, pronouns, all_pronouns, pronoun_meanings
import colorama
from colorama import Fore, Style

colorama.init()

def search_dict(nested_dict, value, prepath=()):
    for k, v in nested_dict.items():
        path = prepath + (k,)
        if v == value: # found value
            return path
        elif hasattr(v, 'items'): # v is a dict
            p = search_dict(v, value, path) # recursive call
            if p is not None:
                return p

def get_dictionary():
    with open('root_words.csv') as dictionary_csv:
        reader = csv.DictReader(dictionary_csv, fieldnames=('puflantu', 'english'))
        dictionary = { rows['puflantu']:rows['english'] for rows in reader }
    return dictionary

def translate(sentence):
    dictionary = get_dictionary()
    full_translation = list()
    combined_prefixes = "((" + ")|(".join(prefixes.keys()) + "))*"
    combined_suffixes = "((" + ")|(".join(suffixes.keys()) + "))*"
    combined_pronouns = "((" + ")|(".join(pronouns.keys()) + "))*"
    regex_prefixes = [(pattern, re.compile(combined_prefixes+pattern+r'\w+')) for pattern in prefixes.keys()]
    regex_suffixes = [(pattern, re.compile(r'\w+'+pattern+combined_suffixes+r'\b')) for pattern in suffixes.keys()]
    regex_pronouns = [(pattern, re.compile(r'\w+'+combined_pronouns+pattern+r'[aeiouw][^aeiouw]{1,2}')) for pattern in all_pronouns]
    regex_light = re.compile(r'([aeiouw])[^aeiouw]\1\w*')
    regex_fluid = re.compile(r'\w*[aeiouw]\w*u?r[aeiouw]')
    regex_physical_activity = re.compile(r'([^aeiouw][^aeiouw])w\1[aeiouw]{0,2}$')
    regex_n_negation = re.compile(r'ay[aeiouw]{0,2}$')
    regex_v_negation = re.compile(combined_pronouns+r'?ey'+combined_pronouns+r'?')
    for word in sentence:
        if word in dictionary:
            full_translation.append(dictionary[word])
            continue
        pre_translated = ''
        post_translated = ''
        enclitic_translated = ''
        #check for enclitics
        if '-' in word:
            enclitic = word[word.find('-')+1:]
            if enclitic in dictionary:
                if enclitic == 'ro':
                    enclitic_translated = '\'s'
                else:
                    enclitic_translated = '-' + dictionary[enclitic]
            elif enclitic[-1] == 's':
                enclitic_translated = '-' + dictionary[enclitic:-1]
            word = word[:word.find('-')]
        negation_match = regex_n_negation.search(word)
        if negation_match:
            pre_translated += "not-"
            word = word[:negation_match.start()]+word[negation_match.start()+2:]
        #check for prefixes, suffixes, and infixes
        present_prefixes = [exp[0] for exp in regex_prefixes if exp[1].match(word)]
        present_suffixes = [exp[0] for exp in regex_suffixes if exp[1].match(word)]
        present_pronouns = [exp[0] for exp in regex_pronouns if exp[1].match(word)]
        light_match = regex_light.match(word)
        fluid_match = regex_fluid.match(word)
        physical_match = regex_physical_activity.search(word)
        v_negation_match = regex_v_negation.search(word)
        all_candidates = set([x for x in chain(present_prefixes, present_suffixes, present_pronouns) if x])
        if light_match:
            all_candidates.add(light_match.group()[0])
        if fluid_match:
            if "ur" in fluid_match.group():
                all_candidates.add(fluid_match.group()[-3:-1])
            else:
                all_candidates.add(fluid_match.group()[-2:-1])
        if physical_match:
            all_candidates.add(physical_match.group()[:physical_match.group().find("w")+1])
        if v_negation_match:
            all_candidates.add("ey")
        potential_roots = list()
        for candidate in chain.from_iterable(combinations(all_candidates, r) for r in range(len(all_candidates)+1)):
            root = word
            for substr in candidate:
                if substr in present_suffixes:
                    i = root.rfind(substr)
                else:
                    i = root.find(substr)
                root = root[:i] + root[i+len(substr):]
            if root in dictionary:
                potential_roots.append((root, candidate))
        if potential_roots:
            root, candidate = min(potential_roots, key=lambda x:len(x[0]))
            for prefix in present_prefixes:
                if prefix in candidate:
                    pre_translated += prefixes[prefix] + '-'
            for suffix in present_suffixes:
                if suffix in candidate:
                    post_translated += suffixes[suffix]
            for pronoun in present_pronouns:
                if pronoun in candidate:
                    path = search_dict(pronouns, pronoun)
                    if path:
                        if 'REL' in path[0]:
                            pre_translated = pronoun_meanings[path[0]][path[1]] + '-' + pre_translated
                        else:
                            if 'SUBJ' in path[1]:
                                pre_translated += pronoun_meanings[path[0]][path[1]] + '-'
                            elif 'OBJ' in path[1]:
                                post_translated += '-' + pronoun_meanings[path[0]][path[1]]
            if light_match:
                if light_match.group()[0] in candidate:
                    post_translated += "&light-source"
            if fluid_match:
                if fluid_match.group()[-3:-1] in candidate:
                    post_translated += "&fluid"
            if physical_match:
                if physical_match.group()[:physical_match.group().find("w")+1] in candidate:
                    post_translated += "&bodily-action"
            if v_negation_match:
                if "ey" in candidate:
                    pre_translated += "not-"
            word = root
        #check for dual/pluralization
        if word[-1] == "w":
            p = re.compile(word[:-1]+r'[aeiouw]')
            for check in dictionary.keys():
                if p.match(check):
                    word = check
                    post_translated = "-dual" + post_translated
                    break
        elif word[-2:] == "we":
            p = re.compile(word[:-2]+r'[aeiouw]')
            for check in dictionary.keys():
                if p.match(check):
                    word = check
                    if dictionary[check][-1] != "s":
                        post_translated = "s" + post_translated
                    else:
                        post_translated = "es" + post_translated
                    break
        if word in dictionary:
            if post_translated or enclitic_translated:
                full_translation.append(pre_translated+dictionary[word].split()[0]+post_translated+enclitic_translated)
            else:
                full_translation.append(pre_translated+dictionary[word]+post_translated+enclitic_translated)
        else:
            full_translation.append(pre_translated+"UNKNOWN"+post_translated+enclitic_translated)
    return full_translation

parser = argparse.ArgumentParser(
    prog='puflantu',
    description='Puflantu translation utility'
)

parser.add_argument("text", help="text to be translated from puflantu")
parser.add_argument('-N', '-natural', help='Translate into proper English', dest='natural', action='store_true')

if __name__ == '__main__':
    args = parser.parse_args()
    if args.text:
        sentence = args.text.lower()
        p = re.compile(" ")
        if not p.search(sentence):
            sentence = [''.join([x for x in sentence if x in "\'abcdefghijklmnopqrstuvwxyz-"])]
        else:
            sentence = sentence.split()
            sentence = [''.join([x for x in word if x in "\'abcdefghijklmnopqrstuvwxyz-"]) for word in sentence]
        translation = translate(sentence)
        if args.natural:
            pass
        else:
            for i, v in enumerate(sentence):
                spacing = max(len(v), len(translation[i]))
                print(Fore.LIGHTBLUE_EX+f"{v:{spacing}}", end="  ")
            print(Style.RESET_ALL)
            for i, v in enumerate(translation):
                spacing = max(len(v), len(sentence[i]))
                print(f"{v:{spacing}}", end="  ")
            


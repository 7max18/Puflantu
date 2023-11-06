import csv, argparse, re
from itertools import chain, combinations
from modifiers import prefixes, suffixes, pronouns, all_pronouns, pronoun_meanings

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
    regex_suffixes = [(pattern, re.compile(r"\w+"+pattern+combined_suffixes+r'\b')) for pattern in suffixes.keys()]
    regex_pronouns = [(pattern, re.compile(r"\w+"+combined_pronouns+pattern+r'[aeiouw][^aeiouw]{1,2}')) for pattern in all_pronouns]
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
            if enclitic in dictionary and enclitic != 'ro':
                enclitic_translated = '-' + dictionary[enclitic]
            elif enclitic[-1] == 's':
                enclitic_translated = '-' + dictionary[enclitic:-1]
            word = word[:word.find('-')]
        #check for pluralization
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
        #check for prefixes, suffixes, and infixes
        present_prefixes = [exp[0] for exp in regex_prefixes if exp[1].match(word)]
        present_suffixes = [exp[0] for exp in regex_suffixes if exp[1].match(word)]
        present_pronouns = [exp[0] for exp in regex_pronouns if exp[1].match(word)]
        all_candidates = set([x for x in chain(present_prefixes, present_suffixes, present_pronouns)])
        for candidate in chain.from_iterable(combinations(all_candidates, r) for r in range(len(all_candidates)+1)):
            root = word
            for substr in candidate:
                if substr in present_suffixes:
                    i = root.rfind(substr)
                else:
                    i = root.find(substr)
                root = root[:i] + root[i+len(substr):]
            if root in dictionary:
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
                word = root
                break
            if word in dictionary:
                break
        if word in dictionary:
            if post_translated or enclitic_translated:
                full_translation.append(pre_translated+dictionary[word].split()[0]+post_translated+enclitic_translated)
            else:
                full_translation.append(pre_translated+dictionary[word]+post_translated+enclitic_translated)
        else:
            full_translation.append('UNKNOWN')
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
            sentence = [sentence]
        else:
            sentence = sentence.split()
            sentence = [''.join([x for x in word if x in "\'abcdefghijklmnopqrstuvwxyz-"]) for word in sentence]
        translation = translate(sentence)
        if args.natural:
            pass
        else:
            for i, v in enumerate(sentence):
                spacing = max(len(v), len(translation[i]))
                print(f"{v:{spacing}}", end="  ")
            print()
            for i, v in enumerate(translation):
                spacing = max(len(v), len(sentence[i]))
                print(f"{v:{spacing}}", end="  ")
            


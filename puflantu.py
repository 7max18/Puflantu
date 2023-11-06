import csv, argparse, re
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
    regex_prefixes = [re.compile(pattern+r'\w+') for pattern in prefixes.keys()]
    regex_suffixes = [(pattern, re.compile(r"\w+"+pattern+r'\b')) for pattern in suffixes.keys()]
    regex_pronouns = [(pattern, re.compile(r"\w+"+pattern+r'[aeiouw][^aeiouw]{1,2}')) for pattern in all_pronouns]
    for word in sentence:
        pre_translated = ''
        post_translated = '' 
        present_suffixes = [exp[0] for exp in regex_suffixes if exp[1].match(word)]
        present_pronouns = [exp[0] for exp in regex_pronouns if exp[1].match(word)]
        if any(present_suffixes):
            suffix = present_suffixes[0]
            word = word.removesuffix(suffix)
            post_translated += suffixes[suffix]
        if any(present_pronouns):
            for pronoun in present_pronouns:
                path = search_dict(pronouns, pronoun)
                if path:
                    if 'SUBJ' in path[1]:
                        pre_translated += pronoun_meanings[path[0]][path[1]]
                    elif 'OBJ' in path[1]:
                        post_translated += pronoun_meanings[path[0]][path[1]]
                    i = word.find(pronoun)
                    word = word[:i] + word[i+len(pronoun):]
        if word in dictionary:
            full_translation.append(pre_translated+dictionary[word]+post_translated)
        else:
            full_translation.append('UNKNOWN')
    return full_translation

parser = argparse.ArgumentParser(
    prog='puflantu',
    description='Puflantu translation utility'
)

parser.add_argument("text", help="text to be translated from puflantu")
parser.add_argument('-N', '-natural', help="Translate into proper English", dest="natural", action='store_true')

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
            


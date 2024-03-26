prefixes = {
    'ag': 'big/very',
    'sa': 'small/slightly',
    'vo': 'anti',
    '\'': '!'
}

suffixes = {
    's': '-adverb',
    'l': '-verb',
    '\'fi': 'er',
    '\'': 'est',
    'a': 'ing',
    'afe': '-performer',
    'who': '-recipient',
    'wmi': 'ed',
    'aqo': '-instrument',
    'ice': '-location',
    'ede': '-cause',
    'oda': '-result'
    ''
}

pronouns = {
    '1ST': {
        'SG-SUBJ': 'wm',
        'SG-OBJ': 'um',
        'DU-SUBJ': 'wn',
        'DU-OBJ': 'un',
        'PL-SUBJ': 'wy',
        'PL-OBJ': 'uy'
    },
    '2ND': {
        'SG-SUBJ': 'iz',
        'SG-OBJ': 'ez',
        'DU-SUBJ': 'ij',
        'DU-OBJ': 'ej',
        'PL-SUBJ': 'ix',
        'PL-OBJ': 'ex'
    },
    '3RD': {
        'SG-SUBJ': 'at',
        'SG-OBJ': 'ot',
        'DU-SUBJ': 'ab',
        'DU-OBJ': 'ob',
        'PL-SUBJ': 'ad',
        'PL-OBJ': 'od'
    },
    'THIS': {
        'SG-SUBJ': 'ita',
        'SG-OBJ': 'eta',
        'DU-SUBJ': 'itw',
        'DU-OBJ': 'etw',
        'PL-SUBJ': 'itwe',
        'PL-OBJ': 'etwe'
    },
    'THAT': {
        'SG-SUBJ': 'iqa',
        'SG-OBJ': 'eqa',
        'DU-SUBJ': 'iqw',
        'DU-OBJ': 'eqw',
        'PL-SUBJ': 'iqwe',
        'PL-OBJ': 'eqwe'
    },
    'REL': {
        'SG-SUBJ': 'al',
        'SG-OBJ': 'ol',
        'DU-SUBJ': 'an',
        'DU-OBJ': 'on',
        'PL-SUBJ': 'ary',
        'PL-OBJ': 'ory'
    }
}

pronoun_meanings = {
    '1ST': {
        'SG-SUBJ': 'I',
        'SG-OBJ': 'me',
        'DU-SUBJ': 'we-two',
        'DU-OBJ': 'us-two',
        'PL-SUBJ': 'we',
        'PL-OBJ': 'us'
    },
    '2ND': {
        'SG-SUBJ': 'you',
        'SG-OBJ': 'you',
        'DU-SUBJ': 'you-two',
        'DU-OBJ': 'you-two',
        'PL-SUBJ': 'you-all',
        'PL-OBJ': 'you-all'
    },
    '3RD': {
        'SG-SUBJ': 'it',
        'SG-OBJ': 'it',
        'DU-SUBJ': 'those-two',
        'DU-OBJ': 'those-two',
        'PL-SUBJ': 'they',
        'PL-OBJ': 'they'
    },
    'THIS': {
        'SG-SUBJ': 'this',
        'SG-OBJ': 'this',
        'DU-SUBJ': 'these-two',
        'DU-OBJ': 'these-two',
        'PL-SUBJ': 'these',
        'PL-OBJ': 'these'
    },
    'THAT': {
        'SG-SUBJ': 'that',
        'SG-OBJ': 'that',
        'DU-SUBJ': 'those-two',
        'DU-OBJ': 'those-two',
        'PL-SUBJ': 'those',
        'PL-OBJ': 'those'
    },
    'REL': {
        'SG-SUBJ': 'that',
        'SG-OBJ': 'that',
        'DU-SUBJ': 'that',
        'DU-OBJ': 'that',
        'PL-SUBJ': 'that',
        'PL-OBJ': 'that'
    }
}

all_pronouns = ['wm', 'um', 'wn', 'un', 'wy', 'uy', 
                'iz', 'ez', 'ij', 'ej', 'ix', 'ex',
                'at', 'ot', 'ab', 'ob', 'ad', 'od',
                'ita', 'eta', 'itw', 'etw', 'itwe', 'etwe',
                'iqa', 'eqa', 'iqw', 'eqw', 'iqwe', 'eqwe',
                'al', 'ol', 'an', 'on', 'ary', 'ory']
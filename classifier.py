ANIMAL_TERMS = [
    'animal experiment',
    "animal model",
    "mouse",
    "mice",
    "rat",
    "rats"
]

ANTIOXIDANT_TERMS = [
    "antioxidant",
    "n-acetylcysteine",
    "acetylcysteine",
    "curcumin",
    "quercetin",
    "resveratrol",
    "vitamin c"
]

OXIDATIVE_TERMS = [
    "reactive oxygen species",
    "ros",
    "oxidative stress",
    "oxidation reduction"
]

COCHLEA_TERMS = [
    "cochlea",
    "cochlear",
    "hair cell",
    "hearing loss",
    "ototoxicity",
    "auditory"
]

def find_terms(text, terms):
    text = text.lower()
    return [term for term in terms if term.lower() in text]

def classify(text):
    findings = []

    findings.extend(find_terms(text, ANIMAL_TERMS))
    findings.extend(find_terms(text, ANTIOXIDANT_TERMS))
    findings.extend(find_terms(text, OXIDATIVE_TERMS))
    findings.extend(find_terms(text, COCHLEA_TERMS))

    return {
        'decision': 'INCLUDE' if findings else 'EXCLUDE',
        'findings': list(set(findings))
    }
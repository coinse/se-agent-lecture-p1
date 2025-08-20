

def remove_vowels(text):
    """
    remove_vowels is a function that takes string and returns string without vowels.
    """
    return "".join([s for s in text if s.lower() not in ["a", "e", "i", "o", "u"]])

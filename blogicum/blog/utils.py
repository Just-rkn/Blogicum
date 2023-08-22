def get_short_string(full_string: str, max_words: int = 5) -> str:
    """
    Takes in a string full_string and int optional argument max_words,
    max_words defaults to 5.
    returns a string with the number of words equal to max_words,
    """

    string_words = full_string.split()
    if len(string_words) > max_words:
        return ' '.join(string_words[:max_words])
    return full_string

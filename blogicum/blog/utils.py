def get_short_string(full_string: str, max_words: int = 5) -> str:
    """
    Takes in a string full_string and int optional argument max_words,
    max_words defaults to 5,
<<<<<<< HEAD
    returns a string with the number of words equal to max_words or less.
=======
    returns a string with the number of words equal to max_words.
>>>>>>> 8c3a7546af5c84b5effb472d2dce7f63f892bcb1
    """

    string_words = full_string.split()
    if len(string_words) > max_words:
        return ' '.join(string_words[:max_words])
    return full_string

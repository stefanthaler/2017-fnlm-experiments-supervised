import re
# use existing split function
def split_logline(line):
    """
        WARNING - this is very crucial point for the success of the model; check here if your loglines are split correctly

        in our synthetic logfile we have the following special characters
        \t \n \s ! " # % & ' ( ) * + , - . / : ; < = > ? @ [ \ ] _ ` { }
    """
    special_chars = [
        '!', '"', '#', '%', '&', "'", '(', ')',
        '*', '+', ',', '-', '.', '/', ':', ';', '<', '=', '>',
        '?', '@', '[', '\\', ']', '_', '`', '{', '}'
    ]
    escaped_chars = map(re.escape, special_chars) + ['\t', '\n', '\s'] # should not be escaped
    special_char_slit_regex = r"(" + r"|".join(escaped_chars) + r")" # looks like r(\t|\s|... )
    tokens = re.split(special_char_slit_regex, line)
    filtered_tokens = [t for t in tokens if len(t)>0 ] # filter out empty tokens
    # print(filtered_tokens)
    return filtered_tokens

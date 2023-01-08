from F import LIST
import re

def remove_special_characters(text):
    """ DEPRECATED """
    newText = re.sub('[^a-zA-Z0-9]', ' ', text)
    return newText

def remove_empty_strings(list_of_strs: []):
    newS = []
    for word in list_of_strs:
        if word == '':
            continue
        newS.append(word)
    return newS

def replace(content, *args):
    for arg in args:
        content = content.replace(arg, " ")
    return content

def combine_args_str(*content: str) -> str:
    temp = ""
    content = LIST.flatten(content)
    for item in content:
        temp += " " + str(item)
    return str(temp).strip()


def to_paragraphs(body: str) -> [str]:
    """ -> Separates text based on "\n" <- """
    paragraph_list = []
    i = 0
    temp_body = body
    for char in body:
        if char == "\n":
            new_body = temp_body[:i]
            paragraph_list.append(new_body)
            temp_body = temp_body[i+1:]
            i = 0
            continue
        i += 1
    return paragraph_list
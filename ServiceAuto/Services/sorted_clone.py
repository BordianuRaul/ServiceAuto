
def sorted_clone(random_list: list, key, reverse: bool):

    """
    Functie care inlocuieste functia sorted din python.
    :param random_list:lista cu elemente intr-o ordine random
    :param key:functia dupa care se sorteaza
    :param reverse:parametrul in funcie de care lista se ordoneaza crescator
    sau descrescator
    :return:lista sortata
    """

    for i in range(len(random_list)):
        for j in range(i+1, len(random_list)):
            if key(random_list[i]) > key(random_list[j]):
                random_list[i], random_list[j] = random_list[j], random_list[i]

    if reverse is True:
        return random_list[::-1]
    else:
        return random_list

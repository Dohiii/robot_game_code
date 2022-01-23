

def presses(phrase):
    list = [
        ['1', 'A', 'D', 'G', 'J', 'M', 'P', 'T', 'W', ' ', "*", '#'],
        ['B', 'E', 'H', 'K', 'N', 'Q', 'U', 'X'],
        ['C', 'F', 'I', 'L', 'O', 'R', 'V', 'Y'],
        ['S', 'Z', '2', '3', '4', '5', '6', '8', ],
        ['7',  '9', '0'],
    ]
    # your code here
    result = 0
    phrase.lower()
    for letter in phrase:
        letter.lower()
        if letter in list[0]:
            result += 1
        if letter in list[1]:
            result += 2
        if letter in list[2]:
            result += 3
        if letter in list[3]:
            result += 4
        if letter in list[4]:
            result += 5
    return result


print(presses('WBHSW12'))

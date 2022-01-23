

def double_letters(str):
    for index, character in enumerate(str[:-1]):
        if str[index + 1] == character:
            return True
        else:
            return False


print(double_letters('hello'))



test = [1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0]


def data_reverse(data, n):
    list = [data[i:i + n] for i in range(0, len(data), n)]
    reversed = list[::-1]
    return sum(reversed, [])


print(data_reverse(test, 8))

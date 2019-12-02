
def add(*args):
    a, *b = args
    if len(b) > 1:
        b = add(*b)
    else:
        b = b[0]
    if len(a) != len(b):
        raise ValueError("Given matrices are not the same size.")
    result = []
    for i in range(len(a)):
        if type(a[i]) is list:
            result.append(add(a[i],b[i]))
        else:
            result.append(a[i]+b[i])
    return result

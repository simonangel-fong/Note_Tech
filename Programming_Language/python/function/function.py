print("\n--------Recursion--------\n")


def sumInteger(num):
    if num > 0:
        result = num + sumInteger(num-1)
        print(result)
    else:
        result = 0
    return result


num = 4
print(f"Sum of 1-{num}: ", sumInteger(num))

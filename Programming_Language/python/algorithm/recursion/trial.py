# def permute(s, output=None):

#     if (len(s) <= 1):
#         return []

#     if output == None:
#         output = []

#     if s in output:
#         return output
#     else:
#         output.append(s)
#         return permute(s[1:]+s[0], output)


# print(permute('abc'))  # 'abc', 'acb', 'bac', 'bca', 'cab', 'cba'

# '''
# 0<1<2

# s   r
# a   a
# ab  ab, ba
# abc ab c, ab c,

# '''

def rec_coin(target, coins, output=None):

    # base case
    if target % coins[-1] == 0:
        return target // coins[-1]
    # recursive case
    else:
        return target // coins[-1] + rec_coin(target % coins[-1], coins[:-1])


coins = [1, 5, 10, 25]
print(rec_coin(10, [1, 5]))  # 2
print(rec_coin(45, coins))  # 3
print(rec_coin(23, coins))  # 5
print(rec_coin(74, coins))  # 8

print(coins[:-1])

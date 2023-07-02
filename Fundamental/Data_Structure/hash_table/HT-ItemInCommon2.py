# method using hash table
def item_in_common(list1, list2):
    my_dict = {}
    for i in list1:
        my_dict[i] = True

    for j in list2:
        if j in my_dict:
            return True

    return False


# method using set()
def item_in_common(list1, list2):
    s1 = set(list1)
    s2 = set(list2)

    return len(s1.intersection(s2)) > 0


list1 = [1, 3, 5]
list2 = [2, 4, 5]


print(item_in_common(list1, list2))

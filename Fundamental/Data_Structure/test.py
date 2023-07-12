def longest_consecutive_sequence(nums):

    num_set = set(nums)     # 之所以使用set, 是因为set本身也是hash, lookup的效率是O(1)
    max_len = 0

    for num in nums:
        if num - 1 not in num_set:  # 保证最小开始
            current_num = num
            current_len = 1

            while current_num + 1 in num_set:
                current_len += 1
                current_num += 1
            max_len = max(current_len, max_len)

    return max_len


print(longest_consecutive_sequence([100, 4, 200, 1, 3, 2]))


"""
    EXPECTED OUTPUT:
    ----------------
    4

"""

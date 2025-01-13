class Solution:
    def mergeAlternately(self, word1: str, word2: str) -> str:
        min_len = min(len(word1), len(word2))
        result = []
        for i in range(0, min_len):
            result.append(word1[i])
            result.append(word2[i])

        result += word1[i+1:]
        result += word2[i+1:]
        return "".join(result)


s = Solution()

word1 = "abc"
word2 = "pqr"
print(s.mergeAlternately(word1, word2))

word1 = "ab"
word2 = "pqrs"
print(s.mergeAlternately(word1, word2))

word1 = "abcd"
word2 = "pq"
print(s.mergeAlternately(word1, word2))

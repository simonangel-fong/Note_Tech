class Solution:
    def maxVowels(self, s: str, k: int) -> int:
        dum = ["z"]*(k-1)
        dumStr = "".join(dum) + s
        vowl = set('aeiou')
        maxCount = currentCount = 0

        for i in range(0, len(dumStr)):
            if dumStr[i] in vowl and currentCount < k:
                currentCount += 1

            if dumStr[i] not in vowl and 0 < currentCount:
                currentCount -= 1

            maxCount = max(maxCount, currentCount)
        return maxCount


S = Solution()
# s = "zzzabciiidef"
# k = 3
# print(S.maxVowels(s, k))

# s = "aeiou"
# k = 2
# print(S.maxVowels(s, k))

# s = "leetcode"
# k = 3
# print(S.maxVowels(s, k))

s = "weallloveyou"
k = 7
print(S.maxVowels(s, k))
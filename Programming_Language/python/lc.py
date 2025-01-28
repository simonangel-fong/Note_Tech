from typing import List


class Solution:
    def isSubsequence(self, s: str, t: str) -> bool:
        # 2 pointers: spointer, tpointer
        # each t: match; if match spointer+1
        # return: if spointer == len

        spointer = tpointer = 0

        while spointer < len(s) and tpointer < len(t):
            # match
            if t[tpointer] == s[spointer]:
                spointer += 1
            tpointer += 1
        return spointer == len(s)


sol = Solution()

s = "abc"
t = "ahbgdc"
print(sol.isSubsequence(s, t))

s = "axc"
t = "ahbgdc"
print(sol.isSubsequence(s, t))

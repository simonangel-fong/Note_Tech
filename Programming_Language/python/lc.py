from typing import List


class Solution:
    def kidsWithCandies(self, candies: List[int], extraCandies: int) -> List[bool]:
        # get the max of the candies
        maxCount = max(candies)
        # create output result array
        result = [True]*len(candies)
        # loop candies
        for i in range(len(candies)):
            # check if < maxCount
            if candies[i] + extraCandies < maxCount:
                result[i] = False
        return result


s = Solution()
candies = [2, 3, 5, 1, 3]
extraCandies = 3
print(s.kidsWithCandies(candies, extraCandies))


candies = [4, 2, 1, 1, 2]
extraCandies = 1
print(s.kidsWithCandies(candies, extraCandies))

candies = [12, 1, 12]
extraCandies = 10
print(s.kidsWithCandies(candies, extraCandies))

from typing import List


class Solution:
    def findMaxAverage(self, nums: List[int], k: int) -> float:
        currentSum = maxSum = sum(nums[:k])
        for i in range(len(nums)-k):
            currentSum -= nums[i]
            currentSum += nums[k+i]
            maxSum = max(currentSum, maxSum)

        return maxSum / k


S = Solution()

# nums = [1, 12, -5, -6, 50, 3]
# k = 4
# print(S.findMaxAverage(nums, k))
# 12.75000

# nums = [5]
# k = 1
# print(S.findMaxAverage(nums, k))
# # 5.00000

nums = [-1]
k = 1
print(S.findMaxAverage(nums, k))

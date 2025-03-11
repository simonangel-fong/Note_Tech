from typing import List


class Solution:
    def maxArea(self, height: List[int]) -> int:
        left = 0
        right = len(height)-1
        maxArea = 0
        while left < right:
            min_height = min(height[left], height[right])
            maxArea = max(maxArea, min_height*(right-left))
            if height[left] <= height[right]:
                left += 1
                # continuely moving to the next higher height
                while height[left] < min_height:
                    left += 1
            else:
                right -= 1
                while height[right] < min_height:
                    right -= 1
        return maxArea


S = Solution()
height = [1, 8, 6, 2, 5, 4, 8, 3, 7]
print(S.maxArea(height))

height = [1, 1]
print(S.maxArea(height))

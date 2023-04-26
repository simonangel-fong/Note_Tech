/**
 * @param {number[]} nums
 * @return {number}
 */
var pivotIndex = function (nums) {
  let leftSum = 0;

  let rightSum = nums.reduce((acc, row) => {
    acc += row;
    return acc;
  }, 0);

  for (let i = 0; i < nums.length; i++) {
    rightSum -= nums[i];
    if (rightSum == leftSum) {
      return i;
    }
    leftSum += nums[i];
  }
  return -1;
};

nums = [1, 7, 3, 6, 5, 6];

console.log(pivotIndex(nums));

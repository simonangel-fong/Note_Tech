package Leetcode;

public class Leetcode724 {
    public static void main(String[] args) {
        int[] nums = { 1, 7, 3, 6, 5, 6 };
        Leetcode724 s = new Leetcode724();
        System.out.println(s.pivotIndex(nums));
    }

    public int pivotIndex(int[] nums) {
        int rightSum = 0;
        int leftSum = 0;

        for (int i = 0; i < nums.length; i++) {
            rightSum += nums[i];
        }

        for (int i = 0; i < nums.length; i++) {
            rightSum -= nums[i];
            if (leftSum == rightSum) {
                return i;
            }
            leftSum += nums[i];
        }

        return -1;
    }
}
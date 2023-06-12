package Array;

import java.util.*;

public class ArrayListDemo_Size {
    public static void main(String[] args) throws Exception {

        ArrayList<Integer> listStr01 = new ArrayList<Integer>();

        System.out.println("The size of the array is: " + listStr01.size()); // 0

        ArrayList<Integer> listStr02 = new ArrayList<Integer>(10);

        System.out.println("The size of the array is: " + listStr02.size());// 0
    }
}

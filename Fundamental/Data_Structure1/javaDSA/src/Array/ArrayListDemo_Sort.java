package Array;

import java.util.*;

public class ArrayListDemo_Sort {
    public static void main(String[] args) {
        ArrayList<String> listStr = new ArrayList<String>();
        listStr.add("Mango");
        listStr.add("Apple");
        listStr.add("Banana");
        listStr.add("Grapes");
        // Sorting the list
        Collections.sort(listStr);
        // Traversing list through the for-each loop
        for (String fruit : listStr) {
            System.out.println(fruit);
            // Apple
            // Banana
            // Grapes
            // Mango
        }

        ArrayList<Integer> listNum = new ArrayList<Integer>();
        listNum.add(21);
        listNum.add(11);
        listNum.add(51);
        listNum.add(1);

        // Sorting the list
        Collections.sort(listNum);

        // Traversing list through the for-each loop
        for (int num : listNum) {
            System.out.println(num);
            // 1
            // 11
            // 21
            // 51
        }
    }
}

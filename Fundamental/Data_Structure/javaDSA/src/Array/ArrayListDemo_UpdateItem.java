package Array;

import java.util.*;

public class ArrayListDemo_UpdateItem {
    public static void main(String[] args) {
        ArrayList<String> list = new ArrayList<String>();
        list.add("Mango");
        list.add("Apple");
        list.add("Banana");
        list.add("Grapes");

        // accessing the element
        System.out.println("Returning element: " + list.get(1));// it will return the 2nd element, because index starts
                                                                // from 0
        // changing the element
        list.set(1, "Dates");
        // Traversing list
        for (String fruit : list) {
            System.out.println(fruit);
            // Mango
            // Dates
            // Banana
            // Grapes
        }

    }
}

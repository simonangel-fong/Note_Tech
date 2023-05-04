package Array;

import java.util.*;

public class ArrayListDemo_Loop_ForEach {
    public static void main(String args[]) {
        ArrayList<String> list = new ArrayList<String>();// Creating arraylist
        list.add("Mango");// Adding object in arraylist
        list.add("Apple");
        list.add("Banana");
        list.add("Grapes");

        System.out.println("Traversing list through forEach() method:");
        // The forEach() method is a new feature, introduced in Java 8.
        list.forEach(a -> { // Here, we are using lambda expression
            System.out.println(a);
            // Mango
            // Apple
            // Banana
            // Grapes
        });

    }
}
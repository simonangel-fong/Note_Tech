package Array;

import java.util.*;

public class ArrayListDemo_Loop_Iterator {
    public static void main(String args[]) {
        ArrayList<String> list = new ArrayList<String>();// Creating arraylist
        list.add("Mango");// Adding object in arraylist
        list.add("Apple");
        list.add("Banana");
        list.add("Grapes");

        System.out.println("Traversing list through Iterator");
        Iterator<String> itr01 = list.iterator();// getting the Iterator
        while (itr01.hasNext()) {// check if iterator has the elements
            System.out.println(itr01.next());// printing the element and move to next
            // Mango
            // Apple
            // Banana
            // Grapes
        }

        System.out.println("Traversing list through forEachRemaining() method:");
        Iterator<String> itr02 = list.iterator();
        itr02.forEachRemaining(a -> // Here, we are using lambda expression
        {
            System.out.println(a);
            // Mango
            // Apple
            // Banana
            // Grapes
        });
    }
}
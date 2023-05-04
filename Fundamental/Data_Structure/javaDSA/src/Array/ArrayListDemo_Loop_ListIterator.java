package Array;

import java.util.*;

public class ArrayListDemo_Loop_ListIterator {
    public static void main(String[] args) {
        ArrayList<String> list = new ArrayList<String>();// Creating arraylist
        list.add("Ravi");// Adding object in arraylist
        list.add("Vijay");
        list.add("Ravi");
        list.add("Ajay");

        System.out.println("Traversing list through List Iterator:");
        // Here, element iterates in reverse order
        ListIterator<String> listIterator = list.listIterator(list.size());
        while (listIterator.hasPrevious()) {
            String str = listIterator.previous();
            System.out.println(str);
            // Ajay
            // Ravi
            // Vijay
            // Ravi
        }
    }
}

package Array;

import java.util.*;

public class ArrayListDemo_Add {
    public static void main(String[] args) {
        ArrayList<String> listStr = new ArrayList<String>();
        System.out.println("Initial list of elements: " + listStr);
        // Adding elements to the end of the list
        listStr.add("Ravi");
        listStr.add("Vijay");
        listStr.add("Ajay");
        System.out.println("After invoking add(E e) method: " + listStr);
        // [Ravi, Vijay, Ajay]

        // Adding an element at the specific position
        listStr.add(1, "Gaurav");
        System.out.println("After invoking add(int index, E element) method: " + listStr);
        // [Ravi, Gaurav, Vijay, Ajay]

        ArrayList<String> listStr2 = new ArrayList<String>();
        listStr2.add("Sonoo");
        listStr2.add("Hanumat");

        // Adding second list elements to the first list
        listStr.addAll(listStr2);
        System.out.println("After invoking addlistStrl(Collection<? extends E> c) method: " + listStr);
        // [Ravi, Gaurav, Vijay, Ajay, Sonoo, Hanumat]

        ArrayList<String> listStr3 = new ArrayList<String>();
        listStr3.add("John");
        listStr3.add("Rahul");

        // Adding second list elements to the first list at specific position
        listStr.addAll(1, listStr3);
        System.out.println("After invoking addAll(int index, Collection<? extends E> c) method: " + listStr);
        // [Ravi, John, Rahul, Gaurav, Vijay, Ajay, Sonoo, Hanumat]
    }
}
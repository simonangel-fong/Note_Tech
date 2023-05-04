package Array;

import java.util.*;

public class ArrayListDemo_Remove {
    public static void main(String[] args) {
        ArrayList<String> listStr = new ArrayList<String>();
        listStr.add("Ravi");
        listStr.add("Vijay");
        listStr.add("Ajay");
        listStr.add("Anuj");
        listStr.add("Gaurav");
        System.out.println("An initial list of elements: " + listStr);
        // [Ravi, Vijay, Ajay, Anuj, Gaurav]

        // Removing specific element from arraylist
        listStr.remove("Vijay");
        System.out.println("After invoking remove(object) method: " + listStr);
        // [Ravi, Ajay, Anuj, Gaurav]

        // Removing element on the basis of specific position
        listStr.remove(0);
        System.out.println("After invoking remove(index) method: " + listStr);
        // [Ajay, Anuj, Gaurav]

        // Creating another arraylist
        ArrayList<String> listStr2 = new ArrayList<String>();
        listStr2.add("Ravi");
        listStr2.add("Hanumat");

        // Adding new elements to arraylist
        listStr.addAll(listStr2);
        System.out.println("Updated list : " + listStr);
        // [Ajay, Anuj, Gaurav, Ravi, Hanumat]

        // Removing all the new elements from arraylist
        listStr.removeAll(listStr2);
        System.out.println("After invoking removeAll() method: " + listStr);
        // [Ajay, Anuj, Gaurav]

        // Removing elements on the basis of specified condition
        listStr.removeIf(str -> str.contains("Ajay")); // Here, we are using Lambda expression
        System.out.println("After invoking removeIf() method: " + listStr);
        // [Anuj, Gaurav]

        // Removing all the elements available in the list
        listStr.clear();
        System.out.println("After invoking clear() method: " + listStr);
        // []
    }
}
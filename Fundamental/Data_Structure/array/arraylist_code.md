# Java - ArrayList<> Code

[Back to ArrayList](./arraylist.md)

[Back to Data Structure](../index.md)

---

- [Java - ArrayList\<\> Code](#java---arraylist-code)
  - [Add new Item](#add-new-item)
  - [Add User Defined Class](#add-user-defined-class)
  - [Update Item](#update-item)
  - [Remove Item](#remove-item)
  - [Loop](#loop)
    - [Using .forEach()](#using-foreach)
    - [Using Iterator](#using-iterator)
    - [Using ListIterator](#using-listiterator)
  - [Size](#size)
  - [Sort](#sort)
  - [Serialization and Deserialization](#serialization-and-deserialization)

---

## Add new Item

```java

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
```

---

## Add User Defined Class

```java

import java.util.*;

public class ArrayListDemo_User_Define_Object {

    public static void main(String[] args) {
        // Creating user-defined class objects
        Student s1 = new Student(101, "Sonoo", 23);
        Student s2 = new Student(102, "Ravi", 21);
        Student s3 = new Student(103, "Hanumat", 25);

        // creating arraylist
        ArrayList<Student> listStu = new ArrayList<Student>();
        listStu.add(s1);// adding Student class object
        listStu.add(s2);
        listStu.add(s3);

        // Getting Iterator
        Iterator<Student> itr = listStu.iterator();
        // traversing elements of ArrayList object
        while (itr.hasNext()) {
            Student st = (Student) itr.next();
            System.out.println(st.rollno + " " + st.name + " " + st.age);
            // 101 Sonoo 23
            // 102 Ravi 21
            // 103 Hanumat 25
        }
    }

}

class Student {
    int rollno;
    String name;
    int age;

    Student(int rollno, String name, int age) {
        this.rollno = rollno;
        this.name = name;
        this.age = age;
    }
}
```

---

## Update Item

```java

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

```

---

## Remove Item

```java

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
```

---

## Loop

### Using .forEach()

```java

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
```

---

### Using Iterator

```java

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
```

---

### Using ListIterator

```java

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
```

---

## Size

```java

import java.util.*;

public class ArrayListDemo_Size {
    public static void main(String[] args) throws Exception {

        ArrayList<Integer> listStr01 = new ArrayList<Integer>();

        System.out.println("The size of the array is: " + listStr01.size()); // 0

        ArrayList<Integer> listStr02 = new ArrayList<Integer>(10);

        System.out.println("The size of the array is: " + listStr02.size());// 0
    }
}

```

---

## Sort

```java
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

```

---

## Serialization and Deserialization

```java

import java.io.*;
import java.util.*;

public class ArrayListDemo_Serialization_Deserialization {
    public static void main(String[] args) {
        ArrayList<String> al = new ArrayList<String>();
        al.add("Ravi");
        al.add("Vijay");
        al.add("Ajay");

        try {
            // Serialization
            FileOutputStream fos = new FileOutputStream("file");
            ObjectOutputStream oos = new ObjectOutputStream(fos);
            oos.writeObject(al);
            fos.close();
            oos.close();

            // Deserialization
            FileInputStream fis = new FileInputStream("file");
            ObjectInputStream ois = new ObjectInputStream(fis);
            ArrayList<String> list = (ArrayList<String>) ois.readObject();
            System.out.println(list);
        } catch (Exception e) {
            System.out.println(e); // [Ravi, Vijay, Ajay]
        }
    }
}

```

---

[TOP](#java---arraylist-code)

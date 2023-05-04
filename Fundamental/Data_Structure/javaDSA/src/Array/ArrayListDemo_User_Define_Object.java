package Array;

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
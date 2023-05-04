package Array;

import java.util.*;

public class DynamicArrayDemo {
    public static void main(String[] args) {

        System.out.println("\n--------Test DynamicArray--------\n");

        DynamicArray<Integer> arrInt = new DynamicArray<Integer>();
        System.out.println(arrInt.size());

        System.out.println(arrInt.isEmpty());

        arrInt.add(0);
        arrInt.add(1);
        arrInt.add(2);
        arrInt.add(3);
        arrInt.add(4);

        System.out.println("\n--------create-------");

        System.out.println("isEmpty():\t" + arrInt.isEmpty());
        System.out.println("size():\t\t" + arrInt.size());
        System.out.println("toString():\t" + arrInt);
        System.out.println("get():\t\t" + arrInt.get(4));
        System.out.println("indexOf():\t" + arrInt.indexOf(5));
        System.out.println("contain():\t" + arrInt.contain(4));

        System.out.println("\n--------update--------");
        arrInt.set(4, 5);
        System.out.println("Ater set():\t" + arrInt);

        System.out.println("\n--------clear--------");
        arrInt.clear();
        System.out.println("isEmpty():\t" + arrInt.isEmpty());
        System.out.println("size():\t\t" + arrInt.size());
        System.out.println("toString():\t" + arrInt);

        System.out.println("\n--------add--------");
        arrInt.add(10);
        arrInt.add(20);
        arrInt.add(30);
        arrInt.add(40);
        arrInt.add(50);
        System.out.println("isEmpty():\t" + arrInt.isEmpty());
        System.out.println("size():\t\t" + arrInt.size());
        System.out.println("new add():\t" + arrInt);

        System.out.println("\n--------removeAt--------");
        System.out.println("removeAt():\t" + arrInt.removeAt(0));
        System.out.println("toString():\t" + arrInt);
        System.out.println("size():\t\t" + arrInt.size());

        System.out.println("\n--------remove--------");
        System.out.println("remove():\t" + arrInt.remove(10));
        System.out.println("remove():\t" + arrInt.remove(40));
        System.out.println("toString():\t" + arrInt);
        System.out.println("size():\t\t" + arrInt.size());

        System.out.println("\n--------iterator--------");
        Iterator<Integer> itr = arrInt.iterator();
        while (itr.hasNext()) {
            System.out.println(itr.next());
        }

    }
}

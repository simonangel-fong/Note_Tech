
public class DynamicArraySim<T> implements Iterable<T> {

    private T[] arr;
    private int capacity; // internal array size
    private int size; // external array size

    public DynamicArraySim() {
        this(16);
    }

    public DynamicArraySim(int initSize) {
        //check if the initial size is less than zero
        if(initSize<0 ){
            throw IllegalArgumentException("Illegal Capacity: " + initSize);
        }
        this.size = initSize;
        arr[] = (T[]) Object[initSize];//create a emprty static array with given size
    }

    public int size() {
        return this.size;
    }

    public isEmpty(){
        return this.size==0;
    }

    public T get(int index) {
        if (index > this.size) {
            throw new IndexOutOfBoundsException();
        } else {
            return arr[index];
        }
    }

    public void set(int index, T element) {
        arr[index] = element;
    }

    public void clear(){
        for(int i=0; i<)
    }
}
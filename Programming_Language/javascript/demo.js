const obj = {
  name: "John",
  call: () => {
    console.log(this); //{}
    return this.name;
  },
  yell: function () {
    console.log(this); //{ name: 'John', call: [Function: call], yell: [Function: yell] }
    return this.name;
  },
};

console.log(obj.call()); //undefined
console.log(obj.yell()); //John

let arr = [1, 2, 3, 4];
console.log(arr[length-1]);

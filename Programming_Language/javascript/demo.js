console.log("\n-------- in Operator --------\n");

const person = { firstName: "John", lastName: "Doe", age: 50 };

console.log("firstName" in person); //true
console.log("age" in person); //true
console.log("address" in person); //false

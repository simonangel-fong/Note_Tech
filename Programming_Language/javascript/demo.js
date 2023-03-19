var text = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";

// slice(start, [end])
console.log("\n--- slice(start, [end]) ---\n");

//slice out the rest of the string
console.log(text.slice(2)); //CDEFGHIJKLMNOPQRSTUVWXYZ
//If a parameter is negative, the position is counted from the end of the string.
console.log(text.slice(-2)); //YZ
console.log(text.slice(1, 2)); //B
console.log(text.slice(1, 3)); //BC
console.log(text.slice(-3, -1)); //XY

// substring(start, end)
console.log("\n--- substring(start, end) ---\n");

//substring out the rest of the string
console.log(text.substring(2)); //CDEFGHIJKLMNOPQRSTUVWXYZ
// substring cannot be negative
console.log(text.substring(-2)); //ABCDEFGHIJKLMNOPQRSTUVWXYZ
console.log(text.substring(1, 2)); //B
console.log(text.substring(1, 3)); //BC
// substring cannot be negative
console.log(text.substring(-3, -1)); //""

// replace(matched, target)
console.log("\n--- replace(matched, target) ---\n");

var text = "Microsoft, Microsoft, Microsoft";

//replace the first matched
console.log(text.replace("Microsoft", "W3Schools")); //W3Schools, Microsoft, Microsoft
//replace the all matched
console.log(text.replace(/Microsoft/g, "W3Schools")); //W3Schools, W3Schools, W3Schools

//replace() method is case sensitive
console.log(text.replace("MICROSOFT", "W3Schools")); //Microsoft, Microsoft, Microsoft
// To replace case insensitive, use a regular expression with an /i flag (insensitive)
console.log(text.replace(/MICROSOFT/i, "W3Schools")); //W3Schools, Microsoft, Microsoft
console.log(text.replace(/MICROSOFT/gi, "W3Schools")); //W3Schools, W3Schools, W3Schools

// replaceAll(matched, target)
// replaceAll() does not work in Internet Explorer.
console.log("\n--- replaceAll(matched, target) ---\n");

var text = "Microsoft, Microsoft, Microsoft";
//replace the all matched
console.log(text.replaceAll("Microsoft", "W3Schools")); //W3Schools, W3Schools, W3Schools
// If the parameter is a regular expression, the global flag (g) must be set set, otherwise a TypeError is thrown.
console.log(text.replaceAll(/MICROSOFT/gi, "W3Schools")); //W3Schools, W3Schools, W3Schools
// console.log(text.replaceAll(/MICROSOFT/i, "W3Schools")); //TypeError: String.prototype.replaceAll called with a non-global RegExp argument

// toLowerCase(), toUpperCase()
console.log("\n--- toLowerCase(), toUpperCase() ---\n");

var text = "Microsoft, Microsoft, Microsoft";
console.log(text.toLowerCase()); //microsoft, microsoft, microsoft
console.log(text.toUpperCase()); //MICROSOFT, MICROSOFT, MICROSOFT

// concat([str])
console.log("\n--- concat([str]) ---\n");

var text1 = "Microsoft, Microsoft, Microsoft";
var text2 = "Google, Google, Google";
var text3 = "Apple, Apple, Apple";
console.log(text1.concat(text2, text3)); //Microsoft, Microsoft, MicrosoftGoogle, Google, GoogleApple, Apple, Apple
console.log(text1.concat(", ", text2, ", ", text3)); //Microsoft, Microsoft, Microsoft, Google, Google, Google, Apple, Apple, Apple
console.log(text1.concat(" ", text2)); //Microsoft, Microsoft, Microsoft Google, Google, Google

// trim(), trimStart(), trimEnd()
console.log("\n--- trim(), trimStart(), trimEnd() ---\n");

var text1 = "       Microsoft          ";

console.log(text1.trim() + ";"); //Microsoft;
console.log(text1.trimStart() + ";"); //Microsoft          ;
console.log(text1.trimEnd() + ";"); //       Microsoft;

// padStart(), padEnd()
console.log("\n--- padStart(), padEnd() ---\n");

var text1 = "Microsoft";

console.log(text1.padStart(5, "*")); //Microsoft;
console.log(text1.padStart(15, "*")); //******Microsoft
console.log(text1.padStart(15, "word")); //wordwoMicrosof
console.log(text1.padEnd(5, "*")); //Microsoft;
console.log(text1.padEnd(15, "*")); //Microsoft******
console.log(text1.padEnd(15, "word")); //Microsoftwordwo

// padStart(), padEnd()
console.log("\n--- padStart(), padEnd() ---\n");

var text1 = "Microsoft";

console.log(text1.padStart(5, "*")); //Microsoft;
console.log(text1.padStart(15, "*")); //******Microsoft
console.log(text1.padStart(15, "word")); //wordwoMicrosof
console.log(text1.padEnd(5, "*")); //Microsoft;
console.log(text1.padEnd(15, "*")); //Microsoft******
console.log(text1.padEnd(15, "word")); //Microsoftwordwo

// charAt(), charCodeAt(), Property Access
console.log("\n--- charAt(), charCodeAt(), Property Access ---\n");

var text1 = "Microsoft";

console.log(text1.charAt(0)); //M
console.log(text1.charAt(1)); //i
console.log(text1.charAt(-1)); //""

console.log(text1.charCodeAt(0)); //77
console.log(text1.charCodeAt(1)); //105
console.log(text1.charCodeAt(-1)); //NaN

console.log(text1[0]); //M
console.log(text1[1]); //i
console.log(text1[-1]); //undefined

// split()
console.log("\n--- split() ---\n");

var text1 = "Microsoft,Google,Apple";

console.log(text1.split(",")); //[ 'Microsoft', 'Google', 'Apple' ]
console.log(text1.split("|")); //[ 'Microsoft,Google,Apple' ]
// If the separator is "", the returned array will be an array of single characters:
console.log(text1.split(""));
//[
// 'M', 'i', 'c', 'r', 'o',
// 's', 'o', 'f', 't', ',',
// 'G', 'o', 'o', 'g', 'l',
// 'e', ',', 'A', 'p', 'p',
// 'l', 'e'
//   ]

// valueOf()
console.log("\n--- valueOf() ---\n");

var text = new String("Hello World!");
console.log(text.valueOf()); //Hello World!

// indexOf(), lastIndexOf()
console.log("\n--- indexOf(), lastIndexOf ---\n");

var text = "Please locate where 'locate' occurs!";
console.log(text.indexOf()); //-1
console.log(text.indexOf("")); //0
console.log(text.indexOf("locate")); //7
console.log(text.indexOf("locate", 8)); //21

console.log(text.lastIndexOf()); //-1
console.log(text.length); //0
console.log(text.lastIndexOf("")); //36, the length of the string
console.log(text.lastIndexOf("locate")); //21
console.log(text.lastIndexOf("locate", 8)); //8

// search()
console.log("\n--- search() ---\n");

// The search() method cannot take a second start position argument.
// The indexOf() method cannot take powerful search values (regular expressions).

var text = "Please locate where 'locate' occurs!";
console.log(text.search()); //0
console.log(text.search("locate")); //7
console.log(text.search("Locate")); //-1
console.log(text.search(/locate/)); //7
console.log(text.search(/Locate/)); //-1
console.log(text.search(/Locate/i)); //7
console.log(text.search(/locate/g)); //7
console.log(text.search(/Locate/g)); //-1
console.log(text.search(/Locate/gi)); //7

// match()
console.log("\n--- match() ---\n");

// If a regular expression does not include the g modifier (global search), match() will return only the first match in the string.
var text = "Please locate where 'locate' occurs!";
console.log(text.match());
// [
//     '',
//     index: 0,
//     input: "Please locate where 'locate' occurs!",
//     groups: undefined
//   ]
console.log(text.match("locate"));
// [
//     'locate',
//     index: 7,
//     input: "Please locate where 'locate' occurs!",
//     groups: undefined
//   ]
console.log(text.match(/locate/));
// [
//     'locate',
//     index: 7,
//     input: "Please locate where 'locate' occurs!",
//     groups: undefined
//   ]
console.log(text.match(/locate/g)); //[ 'locate', 'locate' ]
console.log(text.match(/Locate/gi)); //[ 'locate', 'locate' ]

// matchAll()
console.log("\n--- matchAll() ---\n");

var text = "Please locate where 'locate' occurs!";

console.log(text.matchAll("locate")); //Object [RegExp String Iterator] {}
console.log(Array.from(text.matchAll("locate")));
//[
// [
//     'locate',
//     index: 7,
//     input: "Please locate where 'locate' occurs!",
//     groups: undefined
//   ],
//   [
//     'locate',
//     index: 21,
//     input: "Please locate where 'locate' occurs!",
//     groups: undefined
//   ]
// ]
// If the parameter is a regular expression, the global flag (g) must be set, otherwise a TypeError is thrown.
console.log(Array.from(text.matchAll(/locate/g)));
// [
//     [
//       'locate',
//       index: 7,
//       input: "Please locate where 'locate' occurs!",
//       groups: undefined
//     ],
//     [
//       'locate',
//       index: 21,
//       input: "Please locate where 'locate' occurs!",
//       groups: undefined
//     ]
//   ]

// includes()
console.log("\n--- includes() ---\n");

var text = "Please locate where 'locate' occurs!";

console.log(text.includes()); //false
console.log(text.includes("")); //true
console.log(text.includes("locate")); //true
console.log(text.includes("locate", 32)); //false
console.log(text.includes("Locate")); //false

// startsWith()
console.log("\n--- startsWith() ---\n");

var text = "Please locate where 'locate' occurs!";

console.log(text.startsWith()); //false
console.log(text.startsWith("")); //true
console.log(text.startsWith("Please")); //true
console.log(text.startsWith("please")); //false
console.log(text.startsWith("locate", 7)); //true

// endsWith()
console.log("\n--- endsWith() ---\n");

var text = "Please locate where 'locate' occurs!";

console.log(text.endsWith()); //false
console.log(text.endsWith("")); //true
console.log(text.endsWith("occurs!")); //true
console.log(text.endsWith("occurS!")); //false
console.log(text.endsWith("locate", 13)); //true
console.log(text.endsWith("locate", 27)); //true

var x = 100 / "Apple";
console.log(x); //NaN
console.log(isNaN(x)); //true

var x = 100 / "10";
console.log(x); //10
console.log(isNaN(x)); //false

var x = NaN;
var y = 5;
console.log(x + y); //NaN

var x = NaN;
var y = "5";
console.log(x + y); //NaN5

console.log(typeof x);

var x = 2;
while (x != Infinity) {
  // while (isFinite(x)) {
  console.log(x);
  x **= 2;
}
// 2
// 4
// 16
// 256
// 65536
// 4294967296
// 18446744073709552000
// 3.402823669209385e+38
// 1.157920892373162e+77
// 1.3407807929942597e+154

var y = 2 / 0;

console.log(isFinite(y)); //false
console.log(y == Infinity); //true
console.log(y); //Infinity

console.log(typeof Infinity); //number

var x = 0xff;

console.log(x); //255
console.log(x.toString(2)); //11111111
console.log(x.toString(8)); //377
console.log(x.toString(10)); //255
console.log(x.toString(16)); //ff
console.log(x.toString(32)); //7v

var x = 500;
var y = new Number(500);
var z = new Number(500);

console.log(x == y); //true
console.log(x === y); //false

console.log(y == z); //false
console.log(y === z); //false

var x = 9999999999999999n;
var y = BigInt(1234567890123456789012345);

console.log(typeof x); //bigint
console.log(typeof y); //bigint

var x = 5n;
// var y = x / 2; // Error: Cannot mix BigInt and other types, use explicit conversion.

var y = Number(x) / 2;
console.log(y); //2.5

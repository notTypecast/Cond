# Cond - Numeric data type  

**Cond** is a custom numeric data type for Python 3. It supports most operations that are legal on a regular data type, while adding some new properties.  

***The idea***  

The basic idea of a Cond object, is that it can hold various options at once, but only represent one of them. That option is called the main option.  

***Importing***  

The module is called cond, so it can be imported using `import cond`. The only two, public members of the module that are available are `Cond`, which is the class that is used to instantiate objects, and `require`, which is the function used to set "limitations" for Cond objects. Some other functions will also be imported, but these are implementation functions (indicated with a trailing underscore). All the following code assumes that the line `from cond import Cond, require` has been called.  

***Initializing***
* Arguments  

	To initialize a Cond object, simply use the syntax `x = Cond(*args)`. In this case, `args` is a list that contains an arbitrary amount of elements, all of the same numeric, built-in data type (e.g. integer). Of course, the arguments can also be passed as numeric literals, `x = Cond(1, 5, 10)`. Whenever a Cond object is created in this manner, the main option of the object, which essentially represents it, will always be chosen to be the first passed argument, unless otherwise specified. At least one argument must be passed when a Cond object is created, unless the `range` keyword is included (discussed below). Cond objects do not accept duplicate arguments.
* Keyword arguments  

	There are currently two optional keyword arguments that can be used for the initialization of a Cond object. These are `mainpos` and `range`. The former is used to specify the index of the main option of the object. For example, `x = Cond(1, 5, 10, mainpos = 1)` will initialize a Cond object with the options 1, 5 and 10, but the option that initially represents the object will be the second one (5). The latter is used to specify a range, which the Cond object will use to generate options. The `range` keyword argument has to either be a single positive integer (in which case all the numbers from 0 to it will be included), or a tuple, where the first argument specifies the start, the second argument specifies the end, and the (optional) third argument specifies the step. If this keyword argument is included, it is optional to also include arguments.  

***Basic Operations***  

A Cond object will operate just like the numeric type that it represents in basic operations. The value that will be used for any actual operation will be the main value of the object. For instance:
```Python
x = Cond(5, 17)
y = x + 3
print(y)
```
OUTPUT:
```
8
```
The reason the above output is 8 for this, is that the main option of x is 5 (because it was passed first, and no `mainpos` was specified), so that value will be used for any operations. If, in the above code, the line where the Cond object is initialized was replaced with `x = Cond(17, 5)`, or even, `x = Cond(5, 17, mainpos = 1)`, the resulting value of y would be 20, because in both cases the main option of x would be 17. This works similarly for all other operations, including subtraction, multiplication, division, exponentiation, bitwise operations, etc.  

***Basic Evaluation***
Just like in basic operations, a Cond object will also act in the same way as the numeric type that it represents in evaluation statements. For example:
```Python
x = Cond(11.5, 20.3)
y = 11.5
z = 20.3
print(x == y)
print(x == z)
```
OUTPUT:
```
True
False
```
As expected, the above code yields `True` and `False`. This is because, as stated before, x here is represented by the float 11.5, whereas 20.3 is just an option. So when x is evaluated to be equal to y, which is also 11.5, that yields 1, whereas when it is evaluated to be equal to z, which is 20.3, that yields 0.  

***Incrementing & Decrementing***  

A Cond object also has the ability to be incremented, decremented, or have any other syntax of the type `[operation_sign]=` be used on it. For example, dividing a Cond object's main option by 2 can be done using `x /= 2`, or for an integer, `x >>= 1`. Note that the former will only work if the options of x are of type float. If they are not, and in general, whenever an operation attempts  to change the main option of a Cond object to a different type, `TypeChangeError` is thrown. The latter is a right shift by 1 bit and therefore equivalent to `x //= 2` for an integer number. Here, it is also important to note that, while for a regular number, `x += 1` is completely equivalent to `x = x + 1`, for a Cond object, these are two completely different statements. In fact, the latter should be used with caution. The reason for this, is that stating `x += 1`, is essentially saying "increment the main option of x by 1", whereas stating `x = x + 1` is saying "take 1, add it to the main value of the Cond object x and store the result in x". However, since the resulting value (x + 1) will be an numeric type, by default, x will also be set to be a numeric type. Therefore, the Cond object x will be overwritten by an integer, which will use the name, x, after the statement, and will have the final value that the Cond object would have had. This is demonstrated by this example:
```Python
x = Cond(5)
x += 1
print(x, type(x))
x = x + 1
print(x, type(x))
```
OUTPUT:
```
6 <class 'cond.Cond'>
7 <class 'int'>
```  

***Iterable Properties***  

A Cond object, even though it is represented by one main option, can hold many options at one time. This allows it to have properties that are usually found in iterables, such as lists and tuples. Firstly, calling `len(x)` will return the amount of options that the Cond object currently holds. Using bracket syntax, it is possible to view the option at a specific index; in addition to that, assigning and deleting options is possible, unless the given index corresponds to the main option. A Cond object can be used just like any other iterable in a for loop, looping through its options. The `in` syntax can also be used to check whether a given value is inside the list of options of the Cond object. Adding a new option to a Cond object can be achieved by using the `x.append(value)` syntax, just like one would use in a list. Similarly, `x.remove(value)` and `x.index(value)` are also valid expressions. Finally, calling `x.all()` will return a list of all the options that x currently holds. The below code snippet demonstrates the usage of all of these properties.
```Python
x = Cond(-8, 14, 3)
print("x length: ", len(x))
print("Third option: ", x[2])
x[2] = -x[2]
print("Third option: ", x[2])
del x[2]

print("All x options using for loop:")
for option in x:
	print(option)

print(5 in x)

x.append(5)
x.remove(14)
print("Index of 5 in x: ", x.index(5))

print("All x options: ", x.all())
print("Main x option: ", x)
```
OUTPUT:
```
x length: 3
Third option: 3
Third option: -3
All x options using for loop:
-8
14
False
Index of 5 in x: 1
All x options: [-8, 5]
Main x option: -8
```  

***The require function***  

As mentioned above, the require function is the function which applies "limitations" to Cond objects and changes their main options, based on those limitations. In reality, the require function does nothing more than brute-forcing solutions until it potentially gets a correct one. More specifically, the syntax is: `require(expression, cond_objects, eval_sign, eval_number)`. Following is the explanation for each of these arguments.
* expression: the expression is actually a string representation of an algebraic expression. In essence, it is the "left part" of the equation. Each Cond object that is part of the expression must be represented with a single-digit letter. Just as in regular Python, addition is represented by the "+" symbol, subtraction by the "-" symbol, multiplication by the "\*" symbol, division by the "\\" symbol and modulo by the "%" symbol. Contrary to how it works in regular Python, exponentiation is represented by the "^" symbol (though "\*\*" can also be used). In addition to this, the multiplication symbol can be skipped in cases where algebra allows it (between single-letter variables, numbers or variables followed by parenthesis, numbers followed by variables, etc).
* cond_objects: this argument can either be a single Cond object, or a tuple containing multiple of them. However, the amount of Cond objects passed through this argument must be exactly equal to the amount of variables that the expression contains. The correspondence between variables and Cond objects is 1-1, meaning the first variable is paired with the first object, the second with the second, and so on. This means that, if the expression was `"x - y"` and the tuple was `(y, x)`, the actual operation that the function would attempt to satisfy would be `y - x` and not `x - y`, because the object y was written first, so it corresponds to the first available variable, x. In essence, variable names inside the expression are no more than conventions -they don't represent any actual variable names.
* eval_sign: this argument is a string of the evaluation sign. This can be either one of: "=", ">", ">=", "<", "<=".
* eval_number: this argument is a numeric value, representing the "right side" of the equation. This can be any built-in numeric value, or it can be of type Cond. However, note that if type Cond is used, it will not be edited in any way. It will simply be used for its value and not take part in the actual expression.
The full equation can be recreated by substituting the variable names with the Cond object names, with the correct correlation and then appending the sign and the evaluation number at the end.
The require function will return `True` if any combination of existing options for each included Cond object is found, which satisfies the given equation and will change the main value of the object to that which was found. If no combination of values that satisfy the equation are found, `False` is returned and no changes are made onto the Cond objects.
Following are some examples of the require function's use.
* Example 1:
```Python
	x = Cond(1, 5, 10, 25)
	res = require("x", x, ">", 5)
	print(res)
	print(x)
```
	OUTPUT:
```
	True
	10
```
In this example, it is essentially requested that x be greater than 5. The function searched through the values, found that the value 10, which is the third option of the object, is greater than 10 and set that option to be the main option of the object. Because it was successful in satisfying the equation, it returned `True`.
* Example 2:
```Python
	x = Cond(-5, 10, 102, 54)
	y = Cond(4, 12, 66)
	z = Cond(3, 0, -1)
	res = require(r"xy/(2z) + 15%x - 3y", (x, y, z), "=", 8)
	print(res)
	print(x, y, z)
```
	OUTPUT:
```
	False
	-5 4 3
```
In this example, no combination is found that satisfies the expression. Therefore, the function returned `False` and the Cond objects passed kept their initial main options.
*Note: raw string was used instead of skipping the `%` character.*
* Example 3 (`x`, `y` used from Example 2):
```Python
	res = require(r"15a - a^2  - b", (x, y), ">", 1)
	print(res)
	print(x, y)
```
	OUTPUT:
```
	True
	10 4
```
In this example, notice that x is not passed twice. Even though the variable a appears twice before the variable b, once the object x is mapped to the variable a, whenever a is found again, it is dismissed. Therefore, it is safe to pass y afterwards, so it is mapped to b, without worrying about passing x twice.
*Note: passing x twice would actually cause an error*  

***Future additions***  

A not-equals sign is planned for the `eval_sign`.  

Must test behavior for when same Cond object is passed more than once inside a single expression more extensively.  

Further bug testing.

***Credit***  

The inspiration for this project was solely taken from a lightning talk by Jason Orendorff, [on Youtube.](https://www.youtube.com/watch?v=iOJD7nd7cyY)  

His github profile can be found [here](https://github.com/jorendorff).  

[This description](https://wiki.c2.com/?QuantumBogoSort) on "Quantum Bogosort" also helped.
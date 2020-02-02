# Cond - Numeric data type  

**Cond** is a custom numeric data type for Python 3. It supports most operations that are legal on a regular data type, while adding some new properties. It can be installed using `pip3 install cond`.  

***The idea***  

The basic idea of a Cond object, is that it can hold various options at once, but only represent one of them. That option is called the main option.  

***Importing***  

The module is called cond, so it can be imported using `import cond`. The only three, public members of the module that are available are `Cond`, which is the class that is used to instantiate objects, `LinkedCond`, which is a modified version of the `Cond` class, and `require`, which is the function used to set "limitations" for Cond objects. Some other functions will also be imported, but these are implementation functions (indicated with a trailing underscore). All the following code assumes that the line `from cond import Cond, LinkedCond, require` has been called.  

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

A Cond object also has the ability to be incremented, decremented, or have any other syntax of the type `[operation_sign]=` be used on it. For example, dividing a Cond object's main option by 2 can be done using `x /= 2`, or for an integer, `x >>= 1`. Note that the former will only work if the options of x are of type float. If they are not, and in general, whenever an operation attempts  to change the main option of a Cond object to a different type, `TypeChangeError` is thrown. The latter is a right shift by 1 bit and therefore, equivalent to `x //= 2`, for an integer number. Here, it is also important to note that, while for a regular number, `x += 1` is completely equivalent to `x = x + 1`, for a Cond object, these are two completely different statements. In fact, the latter should be used with caution. The reason for this, is that stating `x += 1`, is essentially saying "increment the main option of x by 1", whereas stating `x = x + 1` is saying "take 1, add it to the main value of the Cond object x and store the result in x". However, since the resulting value (x + 1) will be a numeric type, by default, x will also be set to be a numeric type. Therefore, the Cond object x will be overwritten by an integer, which will use the name, x, after the statement, and will have the final value that the Cond object would have had. This is demonstrated by this example:
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

***LinkedCond objects***  

LinkedCond objects can be instantiated just like Cond objects. The only difference between them and Cond objects, is that they have a "history"; in other words, they "remember" the limitations that are applied on them. An implication of this, is that they can be linked to each other; this is why they are called LinkedCond objects. LinkedCond objects, and their differences with Cond objects, are discussed later.  

***The require function***  

* Cond objects

	As mentioned above, the require function is the function which applies "limitations" to Cond objects and changes their main options, based on those limitations. In reality, the require function does nothing more than brute-forcing solutions until it potentially gets a correct one. More specifically, the syntax is: `require(expression, cond_objects, eval_sign, eval_number)`. Following is the explanation for each of these arguments.
	* expression: the expression is actually a string representation of an algebraic expression. In essence, it is the "left part" of the equation. Each Cond object that is part of the expression must be represented with a single-digit letter. Just as in regular Python, addition is represented by the "+" symbol, subtraction by the "-" symbol, multiplication by the "\*" symbol, division by the "\\" symbol and modulo by the "%" symbol. Contrary to how it works in regular Python, exponentiation is represented by the "^" symbol (though "\*\*" can also be used). In addition to this, the multiplication symbol can be skipped in cases where algebra allows it (between single-letter variables, numbers or variables followed by parenthesis, numbers followed by variables, etc).
	* cond_objects: this argument can either be a single Cond object, or a tuple containing multiple of them. However, the amount of Cond objects passed through this argument must be exactly equal to the amount of variables that the expression contains. The correspondence between variables and Cond objects is 1-1, meaning the first variable is paired with the first object, the second with the second, and so on. This means that, if the expression was `"x - y"` and the tuple was `(y, x)`, the actual operation that the function would attempt to satisfy would be `y - x` and not `x - y`, because the object y was written first, so it corresponds to the first available variable, x. In essence, variable names inside the expression are no more than conventions -they don't represent any actual variable names.
	* eval_sign: this argument is a string of the evaluation sign. This can be either one of: "=", ">", ">=", "<", "<=", "!=".
	* eval_number: this argument is a numeric value, representing the "right side" of the equation. This can be any built-in numeric value, or it can be of type Cond. However, note that if type Cond is used, it will not be edited in any way. It will simply be used for its value and not take part in the actual expression. An expression cannot be used for this argument, therefore any equation should be solved so that there is only a single numeric value on the right side of it before using the function. This argument can also be a tuple of multiple numeric types, but only if the eval_sign argument is "!=".
	The full equation can be recreated by substituting the variable names with the Cond object names, with the correct correlation and then appending the sign and the evaluation number at the end.
	The require function will return `True` if any combination of existing options for each included Cond object is found, which satisfies the given equation and will change the main value of the object to that which was found. If no combination of values that satisfy the equation are found, `False` is returned and no changes are made onto the Cond objects.
	Following are some examples of the require function's use.
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
	In this example, it is essentially requested that x be greater than 5. The function searched through the values, found that the value 10, which is the third option of the object, is greater than 5 and set that option to be the main option of the object. Because it was successful in satisfying the equation, it returned `True`.
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
	(`x`, `y` used from Example 2): In this example, notice that x is not passed twice. Even though the variable a appears twice before the variable b, once the object x is mapped to the variable a, whenever a is found again, it is dismissed. Therefore, it is safe to pass y afterwards, so it is mapped to b, without worrying about passing x twice.
	*Note: passing x twice would actually cause an error.*  

* LinkedCond objects

	The require function can take LinkedCond objects instead of Cond objects as arguments. However, note that both LinkedCond and Cond objects cannot be passed as arguments in a single require call. This is explained further later on. The syntax for the require function, when it is run with LinkedCond objects, is exactly the same as that for when it is run with Cond objects. For example:
	```Python
	a = LinkedCond(1, 2, 3)
	res = require("x", a, ">", 2)
	print(res)
	print(a)
	```
	OUTPUT:
	```
	True
	3
	```
	Here, the LinkedCond object will act exactly like a Cond object. However, consider that the following code was run after the above code:
	```Python
	res = require("x", a, "<", 2)
	print(res)
	print(a)
	```
	OUTPUT:
	```
	False
	3
	```
	If we had initially made `a` be an instance of the Cond class, the above code would have printed out `True` and `1`. For LinkedCond objects, this is not the case; because a LinkedCond object will remember previous require calls onto it, it is impossible to have `a` be smaller than 2, when `a` must already be greater than `2`. In other words, after the first require call, `a` cannot ever be smaller than or equal to 2. Since that is what we request with the second require call, `False` will be returned.
	Multiple LinkedCond objects can also be passed to a single require call. This will, in a way, link them. What this actually means, is that the main option of each of these objects will not only depend on require calls onto them, but also on require calls onto the objects that they are linked with. A big difference between Cond and LinkedCond objects, is that a Cond object can never have its main option altered, unless it is directly passed to require, using the `cond_objects` argument; this is untrue for LinkedCond objects. It is possible for their main option to change *indirectly*. This would have to occur via a require call, to which a LinkedCond object, that is linked to them, is passed. An example of this follows.
	```Python
	a = LinkedCond(range = 10)
	b = LinkedCond(range = 10)
	res = require("xy", (a, b), "=", 24) #a*b = 24
	print(res)
	print(a, b)
	res = require("x", b, "<", 6)
	print(res)
	print(a, b)
	```
	OUTPUT:
	```
	True
	3 8
	True
	8 3
	```
	In the above example, notice that even though the second require call only contained `b` in the passed objects, `a` was also altered. This is the reason why `b` is considered linked to `a`: it can be indirectly affected. When a require call attempts to change `a`, it will also attempt to change `b` so that the new limitation for `a` is satisfied, whereas the previous limitations, which included `b`, are also satisfied.
	Consider a situation where we wanted, just like before, the product of `a` and `b` to be 24, however we also needed `a` to be greater than `b`. As shown, `a` is not greater than `b` when the initial require call, for the product, is made. Even though it *could* be, if we really wanted to ensure that it is, we could do the following:

	```Python
	a = LinkedCond(range = 10)
	b = LinkedCond(range = 10)
	res = require("xy", (a, b), "=", 24) #a*b = 24
	print(res)
	print(a, b)
	res = require("x - y", (a, b), ">", 0) #x-y > 0 => x > y
	print(res)
	print(a, b)
	```
	OUTPUT:
	```
	True
	3 8
	True
	8 3
	```
	Here, just like before, it is first requested that the product of the two LinkedCond objects be equal to 24. Since the options for both objects are the digits, it is found that, if `a` becomes 3 and `b` becomes 8, the product will be 24. The second require call makes sure that the difference of `a` with `b` is greater than 0. This is the correct way to require that `a` be greater than `b`. If that require call was replaced with `require("x", a, ">", b)`, it would return `False`. This is because, as stated before, object `b` was passed as a final argument, meaning it is the evaluation number. For this reason, it will only be used for its value and will not take part in the expression. The function will attempt to make `a` greater than the value of `b`, which is 8. In other words, it will attempt to make `a` be 9; this won't work, since it must also be true that the product of `a` with `b` is 24, which is impossible for `a = 9`, no matter what the main option `b` is. Nevertheless, when the require call is written as it was in the code snippet, it makes sure that both the values of `a` and `b` can be re-evaluated, so matching values can be found. The second solution, `a = 8` and `b = 3` satisfies both equations; the function might also, in this case, pick the values `a = 6` and `b = 4`. This would also be correct in this case.  

***Additional LinkedCond properties***  

LinkedCond objects share all their methods with Cond objects, except for two extra ones:
* The first new method is `getlims()`. This method will return a set, containing all the limitations that currently apply for the object. As for the names that will be used in place of the single-letter variables, it will be attempted to replicate the variable names that have been used. For example:
	```Python
	obj = LinkedCond(range = 20)
	require("x", obj, ">", 11)
	print(obj.getlims())
	```
	OUTPUT:
	```
	{"obj > 11"}
	```
	In place of `x`, `obj`, which is the variable name of the object, was used. This is done so that it is easier to see which objects the limitation is really referring to. Nevertheless, above, it was stated that it will be *attempted* to replicate the variable names. This is because, in some cases, it will be impossible to replicate those names. Consider the following:
	```Python
	def func():
		obj = LinkedCond(range = 20)
		require("x", obj, ">", 11)
		return [obj]
	obj_list = func()
	print(obj_list[0].getlims())
	for v in obj_list:
		print(v.getlims())
	```
	OUTPUT:
	```
	{"obj_list[0] > 11"}
	{"v > 11"}
	```
	Here, after the function `func` quits, all the variables declared in its scope are destroyed; it is impossible to get the variable name `obj` after that. However, since the object is saved inside of the list named `obj_list`, when using the `getlims` method on it, the name of the list that contains it followed by brackets and the index will be used instead. When iterating through the list, the name of the temporary variable will be used.
	The only case in which the single-letter variable names will be used, is when it is impossible to find variable names for all the included objects. For example, consider the following:
	```Python
	def func():
		obj = LinkedCond(range = 10)
		obj2 = LinkedCond(range = 20)
		require("xy", (obj, obj2), ">", 10)
		return {obj: "Hello", obj2: "World"}
	thedict = func()
	for key in thedict:
		print key.getlims()
	```
	OUTPUT:
	```
	{"x*y > 10"}
	{"x*y > 10"}
	```
	Here, the objects are used as dictionary keys (note: **almost never do this**). This means that *no* variable names, at all, exist for these objects. Because they are the dictionary keys, meaning that they are the ones used to refer to the dictionary values, there is no real way to refer to them. For this reason, the only thing that the `getlims` function can do is use the single-letter variables, passed when require was called, instead.
	The reason using Cond or LinkedCond objects as dictionary keys should be avoided, is because the dictionary will represent the object by its main option. This means that if two objects have the same main option, there cannot be two dictionary entries for both of them; when it is attempted to set a new value for the second object, the first object and its value will be overwritten.
* The second method is `clearlims()`. As would be expected, this method will clear all the limitations for a LinkedCond object. The only thing that needs to be noted here, is that `clearlims` will not only clear the limitations for the object it is called on, but also for linked objects, that link the object to them. Consider the example where the product of two LinkedCond objects is 24 and one of them is smaller than 6.
	```Python
	a = LinkedCond(range = 10)
	b = LinkedCond(range = 10)
	require("ab", (a, b), "=", 24)
	require("b", b, "<", 6)
	print(b.getlims())
	a.clearlims()
	print(b.getlims())
	```
	OUTPUT:
	```
	{'b < 6', 'a*b = 24'}
	{'b < 6'}
	```
	In this case, when `clearlims` was called on `a`, the limitation `a*b = 24` was also removed from `b`. However, the limitation of `b` that didn't include `a`, `b < 6`, did not change.

***Credit***  

The inspiration for this project was solely taken from a lightning talk by Jason Orendorff, [on Youtube.](https://www.youtube.com/watch?v=iOJD7nd7cyY)  

His github profile can be found [here](https://github.com/jorendorff).  

[This description](https://wiki.c2.com/?QuantumBogoSort) on "Quantum Bogosort" also helped.
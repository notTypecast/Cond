#!/usr/bin/python3
import math
import operator
from parser import expr
from string import ascii_uppercase, ascii_lowercase, digits

class Cond:

	'''
	Cond class
	Creates a Cond object, whose options are passed as unnamed arguments
	All options must be of the same built-in numeric type (int, float or complex)
	Main option is chosen to be the first passed argument, unless otherwise specified by the "mainpos" keyword argument
	
	A Cond object acts just like a numeric type in most cases, however it has some additional methods
	Calling len() on a Cond object will return the amount of options that it currently holds
	The options of a Cond object can be accessed, reassigned or deleted using the [] syntax, with the exception of the main option
	Using the "in" keyword on a Cond object will return True if the given value is in the options, otherwise False
	A Cond object can be used as an iterable, which is equivalent to using the list of options in place of the Cond object
	Using the append() method on a Cond object will add a new option to that object, so long it doesn't already exist
	Using the remove() method on a Cond object will remove an existing option from that object, so long it isn't the main option
	Using the index(value) method on a Cond object will return an integer representing the index of that value in the Cond object's options

	Cond objects can be passed to the require function, which will edit their main option based on the given expression
	The require function cannot affect the options of a Cond object, it can only change its main option to a different one from
	the available options
	'''

	def __init__(self, *args, **kwargs):

		#check if kwargs are correct
		for kwarg in kwargs:
			if kwarg not in {"mainpos", "range"}:
				raise ValueError("Cond: unknown keyword argument {}".format(kwarg))

		#raise error if no arguments were given
		if len(args) == 0 and "range" not in kwargs:
			raise ValueError("Cond: need at least one argument at initialization")

		#setup mainpos kwarg
		if "mainpos" in kwargs:
			self.__MAINPOS = kwargs["mainpos"]
		else:
			self.__MAINPOS = 0

		#error check range kwarg if it's tuple (if it is int, it's ready to use in range() function)
		if "range" in kwargs and type(kwargs["range"]) is not int:
			if type(kwargs["range"]) is not tuple or not len(kwargs["range"]) or len(kwargs["range"]) > 3:
				raise ValueError("Cond: keyword argument \"range\" must be int, or tuple of length 1-3")

			for num in kwargs["range"]:
				if type(num) is not int:
					raise ValueError("Cond: keyword argument \"range\" can only include numbers of type int, not {}".format(type(num)))

		#error check regular numeric arguments
		if "range" in kwargs:
			argtype = int
		else:
			argtype = type(args[self.__MAINPOS])

		if argtype not in {int, float, complex}:
			raise TypeError("Cond: arguments must all be numeric types")

		for arg in args:

			if type(arg) is not argtype:
				raise TypeError("Cond: arguments must all be of the same type")

			elif args.count(arg) != 1:
				raise ValueError("Cond: object cannot have duplicate values")

		#save the option type in __TYPE, the values in __VALS and the main option in __MAIN
		self.__TYPE = argtype
		self.__VALS = []

		#if range keyword was provided, add the specified range to __VALS
		if "range" in kwargs:
			if type(kwargs["range"]) is int and kwargs["range"] <= 0:
				raise ValueError("Cond: bad keyword argument \"range\"")
			elif type(kwargs["range"]) is int:
				kwargs["range"] = (kwargs["range"],)

			if len(kwargs["range"]) == 1:
				self.__VALS.extend(range(kwargs["range"][0]))
			elif len(kwargs["range"]) == 2:
				self.__VALS.extend(range(kwargs["range"][0], kwargs["range"][1]))
			else:
				self.__VALS.extend(range(kwargs["range"][0], kwargs["range"][1], kwargs["range"][2]))

		for arg in args:
			if arg not in self.__VALS:
				self.__VALS.append(arg)

		if self.__MAINPOS >= len(self.__VALS):
			raise ValueError("Cond: keyword argument \"mainpos\" out of range")

		self.__MAIN = self.__VALS[self.__MAINPOS]

	def all(self):
		return self.__VALS

	def _setmain(self, op_index):
		self.__MAIN = self.__VALS[op_index]
		self.__MAINPOS = op_index

	def __get__(self):
		return self.__MAIN

	def __eq__(self, other):
		if type(other) is type(self):
			return self.__MAIN == other.__MAIN
		else:
			return self.__MAIN == other

	def __ne__(self, other):
		if type(other) is type(self):
			return self.__MAIN != other.__MAIN
		else:
			return self.__MAIN != other

	def __lt__(self, other):
		if type(other) is type(self):
			return self.__MAIN < other.__MAIN
		else:
			return self.__MAIN < other

	def __gt__(self, other):
		if type(other) is type(self):
			return self.__MAIN > other.__MAIN
		else:
			return self.__MAIN > other

	def __le__(self, other):
		if type(other) is type(self):
			return self.__MAIN <= other.__MAIN
		else:
			return self.__MAIN <= other

	def __ge__(self, other):
		if type(other) is type(self):
			return self.__MAIN >= other.__MAIN
		else:
			return self.__MAIN >= other

	def __pos__(self):
		return self.__MAIN

	def __neg__(self):
		return -self.__MAIN

	def __abs__(self):
		return abs(self.__MAIN)

	def __invert__(self):
		return ~self.__MAIN

	def __round__(self):
		return round(self.__MAIN)

	def __floor__(self):
		return math.floor(self.__MAIN)

	def __ceil__(self):
		return math.ceil(self.__MAIN)

	def __trunc__(self):
		return math.trunc(self.__MAIN)

	def __add__(self, other):
		if type(other) is type(self):
			return self.__MAIN + other.__MAIN
		else:
			return self.__MAIN + other

	def __sub__(self, other):
		if type(other) is type(self):
			return self.__MAIN - other.__MAIN
		else:
			return self.__MAIN - other

	def __mul__(self, other):
		if type(other) is type(self):
			return self.__MAIN * other.__MAIN
		else:
			return self.__MAIN * other

	def __floordiv__(self, other):
		if type(other) is type(self):
			return self.__MAIN // other.__MAIN
		else:
			return self.__MAIN // other

	def __truediv__(self, other):
		if type(other) is type(self):
			return self.__MAIN / other.__MAIN
		else:
			return self.__MAIN / other

	def __mod__(self, other):
		if type(other) is type(self):
			return self.__MAIN % other.__MAIN
		else:
			return self.__MAIN % other

	def __divmod__(self, other):
		if type(other) is type(self):
			return divmod(self.__MAIN, other.__MAIN)
		else:
			return divmod(self.__MAIN, other)

	def __pow__(self, other):
		if type(other) is type(self):
			return self.__MAIN ** other.__MAIN
		else:
			return self.__MAIN ** other

	def __lshift__(self, other):
		if type(other) is type(self):
			return self.__MAIN << other.__MAIN
		else:
			return self.__MAIN << other

	def __rshift__(self, other):
		if type(other) is type(self):
			return self.__MAIN >> other.__MAIN
		else:
			return self.__MAIN >> other

	def __and__(self, other):
		if type(other) is type(self):
			return self.__MAIN & other.__MAIN
		else:
			return self.__MAIN & other

	def __or__(self, other):
		if type(other) is type(self):
			return self.__MAIN | other.__MAIN
		else:
			return self.__MAIN | other

	def __xor__(self, other):
		if type(other) is type(self):
			return self.__MAIN ^ other.__MAIN
		else:
			return self.__MAIN ^ other

	def __radd__(self, other):
		return self + other

	def __rsub__(self, other):
		if type(other) is type(self):
			return other.__MAIN - self.__MAIN
		else:
			return other - self.__MAIN

	def __rmul__(self, other):
		return self * other

	def __rfloordiv__(self, other):
		if type(other) is type(self):
			return other.__MAIN // self.__MAIN
		else:
			return other // self.__MAIN

	def __rtruediv__(self, other):
		if type(other) is type(self):
			return other.__MAIN / self.__MAIN
		else:
			return other / self.__MAIN

	def __rmod__(self, other):
		if type(other) is type(self):
			return other.__MAIN % self.__MAIN
		else:
			return other % self.__MAIN

	def __rdivmod__(self, other):
		if type(other) is type(self):
			return divmod(other, self)
		else:
			return divmod(other, self.__MAIN)

	def __rpow__(self, other):
		if type(other) is type(self):
			return other ** self
		else:
			return other ** self.__MAIN

	def __rlshift__(self, other):
		if type(other) is type(self):
			return other << self
		else:
			return other << self.__MAIN

	def __rrshift__(self, other):
		if type(other) is type(self):
			return other >> self
		else:
			return other >> self.__MAIN

	def __rand__(self, other):
		return self & other

	def __ror__(self, other):
		return self | other

	def __rxor__(self, other):
		return self ^ other

	def __iadd__(self, other):
		if type(other) is type(self):
			result = self.__MAIN + other.__MAIN
		else:
			result = self.__MAIN + other

		if not type(result) is self.__TYPE:
			raise TypeChangeError("Cond: operation would change main option type")

		self.__MAIN = result		
		self.__VALS[self.__MAINPOS] = self.__MAIN
		return self

	def __isub__(self, other):
		if type(other) is type(self):
			result = self.__MAIN - other.__MAIN
		else:
			result = self.__MAIN - other

		if not type(result) is self.__TYPE:
			raise TypeChangeError("Cond: operation would change main option type")

		self.__MAIN = result		
		self.__VALS[self.__MAINPOS] = self.__MAIN
		return self

	def __imul__(self, other):
		if type(other) is type(self):
			result = self.__MAIN * other.__MAIN
		else:
			result = self.__MAIN * other

		if not type(result) is self.__TYPE:
			raise TypeChangeError("Cond: operation would change main option type")

		self.__MAIN = result		
		self.__VALS[self.__MAINPOS] = self.__MAIN
		return self

	def __ifloordiv__(self, other):
		if type(other) is type(self):
			result = self.__MAIN // other.__MAIN
		else:
			result = self.__MAIN // other

		if not type(result) is self.__TYPE:
			raise TypeChangeError("Cond: operation would change main option type")

		self.__MAIN = result		
		self.__VALS[self.__MAINPOS] = self.__MAIN
		return self

	def __itruediv__(self, other):
		if type(other) is type(self):
			result = self.__MAIN / other.__MAIN
		else:
			result = self.__MAIN / other

		if not type(result) is self.__TYPE:
			raise TypeChangeError("Cond: operation would change main option type")

		self.__MAIN = result		
		self.__VALS[self.__MAINPOS] = self.__MAIN
		return self


	def __imod__(self, other):
		if type(other) is type(self):
			result = self.__MAIN % other.__MAIN
		else:
			result = self.__MAIN % other

		if not type(result) is self.__TYPE:
			raise TypeChangeError("Cond: operation would change main option type")

		self.__MAIN = result		
		self.__VALS[self.__MAINPOS] = self.__MAIN
		return self


	def __ipow__(self, other):
		if type(other) is type(self):
			result = self.__MAIN ** other.__MAIN
		else:
			result = self.__MAIN ** other

		if not type(result) is self.__TYPE:
			raise TypeChangeError("Cond: operation would change main option type")

		self.__MAIN = result		
		self.__VALS[self.__MAINPOS] = self.__MAIN
		return selff

	def __ilshift__(self, other):
		if type(other) is type(self):
			result = self.__MAIN << other.__MAIN
		else:
			result = self.__MAIN << other

		if not type(result) is self.__TYPE:
			raise TypeChangeError("Cond: operation would change main option type")

		self.__MAIN = result		
		self.__VALS[self.__MAINPOS] = self.__MAIN
		return self

	def __irshift__(self, other):
		if type(other) is type(self):
			result = self.__MAIN >> other.__MAIN
		else:
			result = self.__MAIN >> other

		if not type(result) is self.__TYPE:
			raise TypeChangeError("Cond: operation would change main option type")

		self.__MAIN = result		
		self.__VALS[self.__MAINPOS] = self.__MAIN
		return self


	def __iand__(self, other):
		if type(other) is type(self):
			result = self.__MAIN & other.__MAIN
		else:
			result = self.__MAIN & other

		if not type(result) is self.__TYPE:
			raise TypeChangeError("Cond: operation would change main option type")

		self.__MAIN = result		
		self.__VALS[self.__MAINPOS] = self.__MAIN
		return self

	def __ior__(self, other):
		if type(other) is type(self):
			result = self.__MAIN | other.__MAIN
		else:
			result = self.__MAIN | other

		if not type(result) is self.__TYPE:
			raise TypeChangeError("Cond: operation would change main option type")

		self.__MAIN = result		
		self.__VALS[self.__MAINPOS] = self.__MAIN
		return self

	def __ixor__(self, other):
		if type(other) is type(self):
			result = self.__MAIN ^ other.__MAIN
		else:
			result = self.__MAIN ^ other

		if not type(result) is self.__TYPE:
			raise TypeChangeError("Cond: operation would change main option type")

		self.__MAIN = result		
		self.__VALS[self.__MAINPOS] = self.__MAIN
		return self

	def __int__(self):
		return int(self.__MAIN)

	def __float__(self):
		return int(self.__MAIN)

	def __complex__(self):
		return complex(self.__MAIN)

	def __oct__(self):
		return oct(self.__MAIN)

	def __hex__(self):
		return hex(self.__MAIN)

	def __index__(self):
		return self.__MAIN

	def __str__(self):
		return str(self.__MAIN)

	def __repr__(self):
		return repr(self.__MAIN)

	#__format__ ??

	def __hash__(self):
		return hash(self.__MAIN)

	def __nonzero__(self):
		return bool(self.__MAIN)

	def __dir__(self):
		return dir(Cond)

	def __len__(self):
		return len(self.__VALS)

	def __getitem__(self, ind):
		if type(ind) not in {int, slice}:
			raise TypeError("Cond: access indices must be integers or slices, not {}".format(type(ind)))

		elif type(ind) is int and ind >= len(self.__VALS):
			raise IndexError("Cond: index out of range")

		return self.__VALS[ind]

	def __setitem__(self, ind, value):
		if type(ind) is not int:
			raise TypeError("Cond: assignment indices must be integers, not {}".format(type(ind)))

		elif type(value) is not self.__TYPE:
			raise TypeError("Cond: object's type is {}, but value given was of type {}".format(self.__TYPE, type(value)))

		elif ind >= len(self.__VALS):
			raise IndexError("Cond: index out of range")

		elif ind == self.__MAINPOS:
			raise ValueError("Cond: object's current option cannot be changed by assignment")

		self.__VALS[ind] = value

	def __delitem__(self, ind):
		if type(ind) not in {int, slice}:
			raise TypeError("Cond: deletion indices must be integers or slices, not {}".format(type(ind)))

		elif type(ind) is int and ind >= len(self.__VALS):
			raise IndexError("Cond: index out of range")

		elif type(ind) is int and ind == self.__MAINPOS:
			raise ValueError("Cond: object's current option cannot be deleted")

		elif type(ind) is slice and self.__MAINPOS >= ind.start and self.__MAINPOS < ind.stop:
			raise ValueError("Cond: object's current option's index was contained in given slice, but cannot be deleted")

		del self.__VALS[ind]

	def __iter__(self):
		return iter(self.__VALS)

	def __contains__(self, value):
		return value in self.__VALS

	def __copy__(self):
		newObj = Cond(*self.__VALS, mainpos = self.__MAINPOS)
		return newObj

	def append(self, value):
		if type(value) is not self.__TYPE:
			raise TypeError("Cond.append(x): object's type is {}, while x's type is {}".format(self.__TYPE, type(value)))
		elif value in self.__VALS:
			raise ValueError("Cond.append(x): x contained in object")

		self.__VALS.append(value)

	def remove(self, value):
		if value not in self.__VALS:
			raise ValueError("Cond.remove(x): x not in options")
		elif value == self.__MAIN:
			raise ValueError("Cond.remove(x): x is main option")

		self.__VALS.remove(value)

	def index(self, value):
		if value not in self.__VALS:
			raise ValueError("Cond.index(x): x not in options")

		return self.__VALS.index(value)

'''
PRIVATE
Stores values that are reused by functions so they aren't constantly allocated and freed
'''
class _MainData:
	evaluation_signs = {"=": operator.eq, ">": operator.gt, ">=": operator.ge, "<": operator.lt, "<=": operator.le, "!=": operator.ne}
	operation_signs = {"+", "-", "*", "/", "%", "^"}
	accepted_characters = set(ascii_uppercase + ascii_lowercase + digits) | operation_signs | {" ", "(", ")"}



def require(expression, cond_objects, eval_sign, eval_num):

	'''
	require function
	Used to set limitations for Cond objects
	Input arguments:
	-> expression: a mathematical expression to evaluate; essentially the "left part" of the equation
	every variable that is part of the expression must be single-letter; it corresponds to exactly one Cond object
	-> cond_objects: the Cond objects to replace the variables in the expression with; can be tuple of Conds or simply Cond
	must include exactly the same amount of arguments as variables in the expression
	->eval_sign: evaluation sign to be used; must be =, >, >=, <, <=, !=
	->eval_num: evaluation number to be used; can be any numeric type or Cond, but not expression; 
	for != sign, multiple eval nums can be passed as a type tuple

	The require function will go through all combinations for the options of all involved Cond objects and attempt to find
	a combination, which satisfies the equation; if such options are found, the main option(s) of the Cond object(s) passed
	will be changed to those new options and True will be returned; otherwise, the Cond objects will not be changed in any way
	and False will be returned
	'''

	#if evaluation sign is unknown
	if eval_sign not in _MainData.evaluation_signs.keys():
		raise ValueError("require(): bad evaluation sign")
	#if evaluation number is of incorrect type
	elif type(eval_num) not in {Cond, int, float, complex, tuple}:
		raise TypeError("require(): bad evaluation number")
	#if cond_objects is of incorrect type
	elif type(cond_objects) not in {tuple, Cond}:
		raise TypeError("require(): bad Cond objects argument")

	if type(cond_objects) is Cond:
		cond_objects = (cond_objects,)

	if type(eval_num) is not tuple:
		eval_num = (eval_num,)

	if len(eval_num) != 1 and eval_sign != "!=":
		raise ValueError("require(): expected single eval_num, but got multiple")

	#interpret expression given by user
	formula = _interpretExpression(expression, len(cond_objects))

	#if expression was wrong
	if formula is None:
		raise ValueError("require(): bad expression")

	#find total variables in expression
	variables_found = []
	total_variables = 0
	for c in expression:
		if c.isalpha() and c not in variables_found:
			total_variables += 1
			variables_found.append(c)

	#if number of variables is different than number of Cond objects, throw error
	if total_variables != len(cond_objects):
		raise ValueError("require(): number of Cond objects passed was different than number of individual variables in expression")

	#map single-letter variables to corresponding Cond objects
	variables_to_cond = {}
	i = 0
	for c in expression:
		if c.isalpha() and c not in variables_to_cond.keys():
			variables_to_cond[c] = cond_objects[i]
			i += 1

	numbers = {}
	indexes = {}

	#call recursive function which checks all combinations of options of all given Cond objects
	result = _testEquation(formula, variables_to_cond, len(variables_to_cond) - 1, len(variables_to_cond) - 1, numbers, indexes, eval_sign, eval_num)

	#if None was returned, no combination was found
	if not result:
		return False

	#if dict was returned, it contains IDs of objects and corresponding indexes
	#so for each Cond object, set their main option to given index
	for CondObjID in result:
		for CondObj in cond_objects:
			if id(CondObj) == CondObjID:
				CondObj._setmain(result[CondObjID])
				break

	return True

'''
PRIVATE
changes expression slightly and parses it using parser.expr, returns expression in code that can be evaluated with eval()
'''
def _interpretExpression(expression, cond_obj_amount):

	n_expression = ""

	for i in range(len(expression)):
		#remove spaces from expression
		if expression[i] != " " and expression[i] != "^":
			n_expression += expression[i]
		elif expression[i] == "^":
			n_expression += "**"

		#unknown character in expression
		if expression[i] not in _MainData.accepted_characters:
			return None

		#if number is followed by letter or letter is followed by letter, multiplication is implied
		if i != len(expression) - 1 and ((expression[i].isdigit() and (expression[i + 1].isalpha() or expression[i + 1] == "(")) or (expression[i].isalpha() and (expression[i + 1].isalpha() or expression[i + 1].isdigit() or expression[i + 1] == "("))):
			n_expression += "*"

	formula = expr(n_expression).compile()
	return formula

'''
PRIVATE
recursive function, runs a single test of the equation for all combinations of numbers of all passed Cond objects
if combination is found, a dictionary is returned containing the Cond objects as keys and the indexes of the new main number as values
if no combination is found, None is returned
Arguments:
formula -> formula in code executable with eval(), created by _interpretExpression
variables_to_cond -> dict mapping single-letter variables to the Cond object they represent
max_recursion_level -> highest level of recursion, essentially is the amount of total Cond objects -1
recursion_level -> current recursion level, reduced by one every recursive call until it hits 0
numbers -> dict mapping the single_letter variables to the value that they will be tested as
indexes -> dict mapping the Cond objects to the index of the current option, so it can be returned if the option combination satisfies the equation
eval_sign -> the evaluation sign
eval_num -> the evaluation number(s)
'''
def _testEquation(formula, variables_to_cond, max_recursion_level, recursion_level, numbers, indexes, eval_sign, eval_num):

	keys = tuple(variables_to_cond.keys())
	
	#get Cond object to run loop for
	CondObj = variables_to_cond[keys[recursion_level]]
	for number in CondObj:

		#if this is the highest recursion level, clear the dictionaries to run again
		if recursion_level == max_recursion_level:
			numbers = {}
			indexes = {}

		#map the single-letter variable to the number
		numbers[keys[recursion_level]] = number
		#map the Cond object's id to the index of the number in it 
		#(if Cond object is mapped instead of id, two Cond objects with same main value will be the same entry and overwrite each other)
		indexes[id(CondObj)] = CondObj.index(number)

		#if all the for loops have been run
		if recursion_level == 0:
			#set all the values for the single-letter variables
			for variable in numbers:
				exec("{} = {}".format(variable, numbers[variable]))
			#calculate the expression result
			try:
				equation_result = eval(formula)
			#if ZeroDivisionError, then combination of numbers cannot be right
			except ZeroDivisionError:
				return None
			#if the result satisfies all evaluations (with all given eval_nums), return the indexes
			satisfies = True
			for num in eval_num:
				if not _MainData.evaluation_signs[eval_sign](equation_result, num):
					satisfies = False
					break

			if satisfies:
				return indexes

		else:
			#get the result from deeper recursion level
			result = _testEquation(formula, variables_to_cond, max_recursion_level, recursion_level - 1, numbers, indexes, eval_sign, eval_num)
			#if the result isn't None, a combination was found, return it to higher recursion level or to calling function
			if result:
				return result

	#if for loop ended and nothing was returned yet, no combination was found, so return None
	return None



class TypeChangeError(Exception):
	pass






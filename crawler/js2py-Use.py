import js2py

# 创建上下文
context = js2py.EvalJs()

# 0> js定义变量,python使用
# 1.
context.execute('var a = 5')
print(context.a)


# 1> python定义变量,js使用
context.a = 5
context.execute('console.log(a)')

# 2> js定义函数,python使用
# 1.
context.execute('function add(a,b) { return a+b }')
print(context.add(5,6) + 3)

# 2.
add = js2py.eval_js('function add(a,b) { return a+b }')
print(add(5,6) + 3)

# 3> 外联js,python使用(注释掉是因为没创这个文件,自己试)
# with open('./test.js','r') as f:
#     js_code = f.read()
#     context.execute(js_code)
#     print(context.add(5, 6) + 3)
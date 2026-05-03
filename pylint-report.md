# Pylint report

Pylint gives the following report about the application:

```
************* Module app
app.py:1:0: C0114: Missing module docstring (missing-module-docstring)
app.py:17:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:21:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:29:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:43:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:51:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:77:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:87:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:97:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:134:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:140:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:163:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:185:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:222:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:222:0: R1710: Either all return statements in a function should return an expression, or none of them should. (inconsistent-return-statements)
app.py:242:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:246:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:268:0: C0116: Missing function or method docstring (missing-function-docstring)
app.py:268:0: R1710: Either all return statements in a function should return an expression, or none of them should. (inconsistent-return-statements)
app.py:290:0: C0116: Missing function or method docstring (missing-function-docstring)
************* Module config
config.py:1:0: C0114: Missing module docstring (missing-module-docstring)
config.py:1:0: C0103: Constant name "secret_key" doesn't conform to UPPER_CASE naming style (invalid-name)
************* Module db
db.py:1:0: C0114: Missing module docstring (missing-module-docstring)
db.py:4:0: C0116: Missing function or method docstring (missing-function-docstring)
db.py:10:0: C0116: Missing function or method docstring (missing-function-docstring)
db.py:10:0: W0102: Dangerous default value [] as argument (dangerous-default-value)
db.py:17:0: C0116: Missing function or method docstring (missing-function-docstring)
db.py:20:0: C0116: Missing function or method docstring (missing-function-docstring)
db.py:20:0: W0102: Dangerous default value [] as argument (dangerous-default-value)
************* Module events
events.py:1:0: C0114: Missing module docstring (missing-module-docstring)
events.py:3:0: C0116: Missing function or method docstring (missing-function-docstring)
events.py:15:0: C0116: Missing function or method docstring (missing-function-docstring)
events.py:28:0: C0116: Missing function or method docstring (missing-function-docstring)
events.py:32:0: C0116: Missing function or method docstring (missing-function-docstring)
events.py:38:0: C0116: Missing function or method docstring (missing-function-docstring)
events.py:42:0: C0116: Missing function or method docstring (missing-function-docstring)
events.py:46:0: C0116: Missing function or method docstring (missing-function-docstring)
events.py:56:0: C0116: Missing function or method docstring (missing-function-docstring)
events.py:64:0: C0116: Missing function or method docstring (missing-function-docstring)
events.py:77:0: C0116: Missing function or method docstring (missing-function-docstring)
events.py:85:0: C0116: Missing function or method docstring (missing-function-docstring)
************* Module users
users.py:1:0: C0114: Missing module docstring (missing-module-docstring)
users.py:4:0: C0116: Missing function or method docstring (missing-function-docstring)
users.py:9:0: C0116: Missing function or method docstring (missing-function-docstring)
users.py:13:0: C0116: Missing function or method docstring (missing-function-docstring)
users.py:18:0: C0116: Missing function or method docstring (missing-function-docstring)

------------------------------------------------------------------
Your code has been rated at 8.67/10 (previous run: 8.67/10, +0.00)
```

We will review this report in more detail and explain why these issues have not been fixed in the application.

## Docstring declarations

Most of the declarations in the report are of this type: 

```
app.py:1:0: C0114: Missing module docstring (missing-module-docstring)
app.py:17:0: C0116: Missing function or method docstring (missing-function-docstring)
```

These messages indicate that docstrings are missing from methods and functions. During the development of the application, it was decided not to use docstrings.

## Inconsistent return statements

The report shows this type of declaration regarding return-statements:

```
app.py:222:0: R1710: Either all return statements in a function should return an expression, or none of them should. (inconsistent-return-statements)
```

This declaration refers to the situation, in which the function only returns when the method is either 'GET' or 'POST'. For example in the first 'GET','POST' function:

```
@app.route("/cancel_event/<int:event_id>", methods=["GET","POST"])
def cancel_event(event_id):
    require_login()

    event=events.get_event(event_id)
    if not event:
        abort(404)
    if event["user_id"]!=session["user_id"]:
        abort(403)

    if request.method=="GET":
        return render_template("cancel_event.html", event=event)

    if request.method=="POST":
        check_csrf()
        if "cancel" in request.form:
            events.cancel_event(event_id)
            return redirect("/")
        return redirect("/event/"+str(event_id))
```

Although the function only gives a return when it is 'GET' or 'POST', there is still other cases, in which the method is something else and it will not return anything. However, this case can not happen in real situation, as the function has been decorated to only accept either 'GET'- or 'POST'-method. Therefore, there is no risk that the function will not return anything.

## Invalid constant name

The report shows this type of declaration regarding constant name:

```
config.py:1:0: C0103: Constant name "secret_key" doesn't conform to UPPER_CASE naming style (invalid-name)
```

The defined variable here is interpreted as a constant that should be written in upper case. However, according to the developer, it would be better for the variable to be written in smaller case. The variable is used in this code:

```
app.secret_key=config.secret_key
```

## Dangerous default value

This is the delcaration regarding to dangerous default value:

```
db.py:20:0: W0102: Dangerous default value [] as argument (dangerous-default-value)
```

The declaration is referring to these lines in the code:

```
def execute(sql, params=[]):
    con = get_connection()
    result = con.execute(sql, params)
    con.commit()
    g.last_insert_id = result.lastrowid
    con.close()
```

In this case, the default value of 'params' is '[]', an empty list. The problem with pasing empty list as a default argument is that it will be shared between all invocations of the function, and if the argument's content is changed during some function calls, the changes will be seen in other calls as well. This situation is not going to happend in practice, as the code does not apply any change to the list.

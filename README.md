# Math Operations Interpreter

Interpreter of mathematical expressions build using Python programming language.

The program is based on three main concepts:
- **Lexical Analysis:** Analyzes the expression, provided by user, and generates tokens from the expression;
- **Parsing:** Parses tokens to create an Abstract Syntax Tree according to operations priority in provided expression;
- **Interpreter:** Interprets provided by user expression, if it is valid, else reports an error.

Math Operations Interpreter supports the following types of operations:
- **Basic arithmetic operations:** addition (+), subtraction (-), multiplication (*), division (/), exponentiation (^);
- **Parentheses:** Supports operations based on operator precedence and execution order within parentheses;
- **Basic math functions:** sin(), cos(), tan(), log(), sqrt() and exp();
- **User variables:** Defining variables, assigning expression to them and using them in future expressions.

Math Operations Interpreter also signals about errors in user input end expressions.


All commands should be executed in project's root directory:

## Getting started

```bash
python -m venv venv

source venv/bin/activate

pip install -r requirements.txt

python src/main.py
```

## Usage

To use the Math Operations Interpreter, user must correctly input the variable and the expression assigned to it:
- User input must contain a variable, an assignment sign, and an assignment expression;
- Variable must contain only alphabetic characters.

#### Getting result
To get the result of the final expression user must input the "result" variable with final expression:
```text
>>: result = 2
result =  2.0

Process finished with exit code 0
```

#### Exit
To exit the Math Operations Interpreter, user's input must contain "exit" word:
```text
>>: exit

Process finished with exit code 0
```

#### Base operations
```text
>>: result = 2 + 3
result =  5.0
```

#### Multi-part operations
```text
>>: result = -1 + 3 * 5
result =  14.0
```

#### Parentless
```text
>>: result = -(5 - 3) ^ 2
result =  -4.0
```

#### Variables
```text
>>: x = 2
>>: y = 3
>>: result = x ^ 2 - 3
result = 1.0
```

#### Math functions
```text
>>: x = sqrt((4 - 2) ^ (18 / 3 - 2))        
>>: y = 3
>>: result = x - y
result = 1.0
```

#### Errors messages
```text
>>: x = 2 / 1     
Number can not be divided by zero. Please check your input and try again.

>>: x = 2 / 1
>>: y = (4 - 1 * 2
There is a syntax error in the expression. Please check your input and try again.

>>: y = (4 - 1) * 2
>>: result = x + y
result = 8.0
```

## Linters

```bash
flake8 ./ -v
```

## Type Checkers

```bash
mypy ./
```

## Tests

```bash
pytest -v
```

#### Coverage

To check tests coverage use next commands in project's root directory and 
open ```htmlcov/index.html``` file in browser:
```bash
coverage run -m pytest -v
coverage html
```

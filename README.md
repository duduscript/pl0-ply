#pl0-compiler
> This is a compiler for pl0 programming language writen in python.
> ply is a good tool to build a compiler and this compiler is using ply for lexical analysis and grammar analysis.

## Introduction of pl0
> pl0 is similar to but much simpler than the general-purpose programming language Pascal,intend as an educational programming language.
> It serves as an example of how to construct a compiler.

### Grammer
```
program = block "." .

block = [ "const" ident "=" number {"," ident "=" number} ";"]
        [ "var" ident {"," ident} ";"]
        { "procedure" ident ";" block ";" } statement .

statement = [ ident ":=" expression | "call" ident 
              | "?" ident | "!" expression 
              | "begin" statement {";" statement } "end" 
              | "if" condition "then" statement 
              | "while" condition "do" statement ].

condition = "odd" expression |
            expression ("="|"#"|"<"|"<="|">"|">=") expression .

expression = [ "+"|"-"] term { ("+"|"-") term}.

term = factor {("*"|"/") factor}.

factor = ident | number | "(" expression ")".
```

## Usage
- python pl0.py filepath(pl0)


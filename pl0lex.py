import ply.lex as lex

reserved = {
    'odd':'odd_token',
    'begin':'begin_token',
    'end':'end_token',
    'if':'if_token',
    'then':'then_token',
    'while':'while_token',
    'do':'do_token',
    'call':'call_token',
    'const':'const_token',
    'var':'var_token',
    'procedure':'proc_token',
    'write':'write_token',
    'read':'read_token',
    'else':'else_token'
}
tokens = [
    'ident_token',
    'number_token',
    'plus_token',   # +
    'minus_token',   # -
    'mul_token',    # *
    'divide_token', # /
    'eql_token',    # =
    'neq_token',    # <>
    'leq_token',    # <=
    'les_token',    # <
    'geq_token',    # >=
    'grt_token',    # >
    'lparent_token', # (
    'rparent_token',# )
    'comma_token',  # ,
    'semicolom_token', # ;
    'period_token',    # .
    'become_token',   # :=
] + list(reserved.values())

def t_ident_token(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    if t.value in reserved:
        t.type = reserved.get(t.value,'IDENTSYM')
    return t

def t_number_token(t):
    r'\d+'
    t.value = int(t.value)
    return t

t_plus_token = r'\+'
t_minus_token = r'\-'
t_mul_token = r'\*'
t_divide_token = r'/'
t_eql_token = r'='
t_neq_token = r'<>'
t_leq_token = r'<='
t_les_token = r'<'
t_geq_token = r'>='
t_grt_token = r'>'
t_lparent_token = r'\('
t_rparent_token = r'\)'
t_comma_token = r','
t_period_token = r'\.'
t_become_token = r':='
t_semicolom_token = r';'
t_ignore  = ' \t'

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

def t_comment(t):
    r'\\\\.*'
    pass

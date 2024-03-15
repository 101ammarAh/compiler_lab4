import re

# Token types
NUMBER = 'NUMBER'
VARIABLE = 'VARIABLE'
PLUS = '+'
MINUS = '-'
TIMES = '*'
LPAREN = '('
RPAREN = ')'

# Regular expressions for tokenizing
token_regex = [
    (NUMBER, r'\d+'),        # Matches one or more digits
    (VARIABLE, r'[a-zA-Z]+'), # Matches one or more letters
    (PLUS, r'\+'),
    (MINUS, r'-'),
    (TIMES, r'\*'),
    (LPAREN, r'\('),
    (RPAREN, r'\)'),
]

def tokenize(expression):
    tokens = []
    pos = 0
    while pos < len(expression):
        match = None
        for token_type, regex in token_regex:
            pattern = re.compile(regex)
            match = pattern.match(expression, pos)
            if match:
                value = match.group(0)
                tokens.append((token_type, value))
                pos = match.end()
                break
        if not match:
            raise ValueError('Invalid token: ' + expression[pos])
    return tokens


def tokenize(expression):
    tokens = []
    pos = 0
    while pos < len(expression):
        match = None
        for token_type, regex in token_regex:
            pattern = re.compile(regex)
            match = pattern.match(expression, pos)
            if match:
                value = match.group(0)
                tokens.append((token_type, value))
                pos = match.end()
                break
        if not match:
            if expression[pos].isspace():
                pos += 1
            else:
                raise ValueError('Invalid token at position {}: {}'.format(pos, expression[pos]))
    return tokens


def parse_expr(tokens):
    term_node = parse_term(tokens)
    expr_node = parse_expr_prime(tokens)
    return ['expr', term_node, expr_node]

def parse_expr_prime(tokens):
    if not tokens:
        return None
    token = tokens[0]
    if token[0] == PLUS:
        tokens.pop(0)
        term_node = parse_term(tokens)
        expr_node = parse_expr_prime(tokens)
        return ['expr_prime', '+', term_node, expr_node]
    elif token[0] == MINUS:
        tokens.pop(0)
        term_node = parse_term(tokens)
        expr_node = parse_expr_prime(tokens)
        return ['expr_prime', '-', term_node, expr_node]
    else:
        return None

def parse_term(tokens):
    factor_node = parse_factor(tokens)
    term_node = parse_term_prime(tokens)
    return ['term', factor_node, term_node]

def parse_term_prime(tokens):
    if not tokens:
        return None
    token = tokens[0]
    if token[0] == TIMES:
        tokens.pop(0)
        factor_node = parse_factor(tokens)
        term_node = parse_term_prime(tokens)
        return ['term_prime', '*', factor_node, term_node]
    else:
        return None

def parse_factor(tokens):
    if not tokens:
        raise ValueError('Unexpected end of input')
    token = tokens.pop(0)
    if token[0] == NUMBER or token[0] == VARIABLE:
        return token
    elif token[0] == LPAREN:
        expr_node = parse_expr(tokens)
        if tokens.pop(0)[0] != RPAREN:
            raise ValueError('Missing closing parenthesis')
        return ['factor', '(', expr_node, ')']
    else:
        raise ValueError('Invalid token: ' + token[1])

def parse(expression):
    tokens = tokenize(expression)
    parse_tree = parse_expr(tokens)
    if tokens:
        raise ValueError('Unexpected tokens after parsing')
    return parse_tree

def parse_from_file(file_path):
    with open(file_path, 'r') as file:
        expressions = file.readlines()
        for expression in expressions:
            expression = expression.strip()  # Remove leading/trailing whitespaces
            try:
                parse_tree = parse(expression)
                print('Expression:', expression)
                print('Parse Tree:', parse_tree)
                print()
            except ValueError as e:
                print('Error parsing expression:', expression)
                print(e)
                print()

# Call the function with the path to your .txt file
parse_from_file('expressions.txt')

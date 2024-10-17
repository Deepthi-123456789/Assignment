# import sqlite3
# import json
# import re
# from flask import Flask, request, jsonify

# # Node Class to define AST structure
# class Node:
#     def __init__(self, node_type, value=None, left=None, right=None):
#         self.node_type = node_type  # "operator" or "operand"
#         self.value = value          # Value for operands (e.g., 'age > 30') or operator type ("AND", "OR", etc.)
#         self.left = left            # Left child node (optional)
#         self.right = right          # Right child node (optional)

#     def to_dict(self):
#         """Convert the Node to a dictionary for JSON serialization."""
#         return {
#             'node_type': self.node_type,
#             'value': self.value,
#             'left': self.left.to_dict() if self.left else None,
#             'right': self.right.to_dict() if self.right else None,
#         }

#     def is_operator(self):
#         return self.node_type == "operator"

#     def is_operand(self):
#         return self.node_type == "operand"

#     def evaluate(self, user_data):
#         if self.is_operator():
#             left_value = self.left.evaluate(user_data)
#             right_value = self.right.evaluate(user_data)

#             if self.value == "AND":
#                 return left_value and right_value
#             elif self.value == "OR":
#                 return left_value or right_value
#             else:
#                 raise ValueError(f"Unknown operator: {self.value}")
#         elif self.is_operand():
#             return eval(self.value, {}, user_data)
#         else:
#             raise ValueError(f"Unknown node type: {self.node_type}")

# # Functions to parse and build the AST from a rule string
# def parse_rule(rule_str):
#     tokens = re.findall(r'\(|\)|\w+|>=|>|<=|<|=|AND|OR', rule_str)
#     return build_ast(tokens)

# def build_ast(tokens):
#     if not tokens:
#         return None

#     token = tokens.pop(0)

#     if token == "(":
#         left = build_ast(tokens)
#         operator = tokens.pop(0)
#         right = build_ast(tokens)
#         tokens.pop(0)  # remove closing ')'
#         return Node(node_type="operator", value=operator, left=left, right=right)

#     elif re.match(r'\w+', token):
#         left_operand = token
#         operator = tokens.pop(0)
#         right_operand = tokens.pop(0)
#         condition = f"{left_operand} {operator} {right_operand}"
#         return Node(node_type="operand", value=condition)

#     return None

# # Functions for database management
# def init_db():
#     """Initialize the database and create tables if they don't exist."""
#     conn = sqlite3.connect('rules.db')  # This creates a new database file
#     cursor = conn.cursor()

#     # Drop existing tables for a fresh start (optional)
#     cursor.execute('DROP TABLE IF EXISTS rule_conditions;')
#     cursor.execute('DROP TABLE IF EXISTS rules;')

#     # Create the rules table
#     cursor.execute('''CREATE TABLE IF NOT EXISTS rules (
#                         id INTEGER PRIMARY KEY AUTOINCREMENT,
#                         rule_name TEXT NOT NULL,
#                         rule_string TEXT NOT NULL)''')

#     # Create the rule_conditions table
#     cursor.execute('''CREATE TABLE IF NOT EXISTS rule_conditions (
#                         id INTEGER PRIMARY KEY AUTOINCREMENT,
#                         rule_id INTEGER,
#                         ast_json TEXT,
#                         FOREIGN KEY (rule_id) REFERENCES rules (id))''')
#     conn.commit()  # Commit changes
#     conn.close()


# def create_rule(rule_name, rule_string):
#     conn = sqlite3.connect('rules.db')
#     cursor = conn.cursor()

#     ast = parse_rule(rule_string)

#     cursor.execute("INSERT INTO rules (rule_name, rule_string) VALUES (?, ?)", (rule_name, rule_string))
#     rule_id = cursor.lastrowid

#     ast_json = json.dumps(ast.to_dict())  # Use to_dict() for serialization
#     cursor.execute("INSERT INTO rule_conditions (rule_id, ast_json) VALUES (?, ?)", (rule_id, ast_json))

#     conn.commit()
#     conn.close()
#     return ast

# def evaluate_rule(ast, user_data):
#     if ast.node_type == 'operand':
#         return eval_operand(ast.value, user_data)

#     elif ast.node_type == 'operator':
#         left_result = evaluate_rule(ast.left, user_data)
#         right_result = evaluate_rule(ast.right, user_data)
#         if ast.value == "AND":
#             return left_result and right_result
#         elif ast.value == "OR":
#             return left_result or right_result
#         else:
#             raise ValueError(f"Unknown operator: {ast.value}")

# # Helper function to evaluate operand conditions
# def eval_operand(condition, data):
#     """Evaluate a condition based on user data."""
#     # Using regex to extract operands and operators
#     match = re.match(r'(\w+) (>=|>|<=|<|=) (.+)', condition.strip())

#     if not match:
#         raise ValueError(f"Invalid condition format: {condition}")

#     left_operand, operator, right_operand = match.groups()
#     left_value = data.get(left_operand.strip())

#     # Handle cases where right_operand might be a number or a string
#     right_value = right_operand.strip()
#     if right_value.isdigit():
#         right_value = int(right_value)  # Convert to integer if it's a number

#     # Evaluate based on the operator
#     if operator == '>':
#         return left_value > right_value
#     elif operator == '<':
#         return left_value < right_value
#     elif operator == '=':
#         return left_value == right_value
#     elif operator == '>=':
#         return left_value >= right_value
#     elif operator == '<=':
#         return left_value <= right_value
#     else:
#         raise ValueError(f"Unknown operator: {operator}")

# def reconstruct_ast(ast_data):
#     """Recursively reconstruct the AST from a dictionary."""
#     if ast_data['node_type'] == 'operator':
#         left = reconstruct_ast(ast_data['left']) if ast_data['left'] else None
#         right = reconstruct_ast(ast_data['right']) if ast_data['right'] else None
#         return Node(node_type='operator', value=ast_data['value'], left=left, right=right)
#     elif ast_data['node_type'] == 'operand':
#         return Node(node_type='operand', value=ast_data['value'])
#     else:
#         raise ValueError(f"Unknown node type: {ast_data['node_type']}")

# class RuleEngine:
#     VALID_ATTRIBUTES = {'age', 'department', 'income'}

#     def __init__(self, db_name='rules.db'):
#         self.connection = sqlite3.connect(db_name)
#         self.cursor = self.connection.cursor()

#     def validate_rule_string(self, rule_string):
#         pattern = r'^[a-zA-Z0-9\s]+(==|!=|<|<=|>|>=)[a-zA-Z0-9\s]+$'  # Customize regex
#         if not re.match(pattern, rule_string):
#             raise ValueError("Invalid rule string format.")

#     def validate_attributes(self, attributes):
#         for attribute in attributes:
#             if attribute not in self.VALID_ATTRIBUTES:
#                 raise ValueError(f"Attribute '{attribute}' is not valid.")

#     def modify_rule(self, rule_id, new_rule_string):
#         try:
#             self.validate_rule_string(new_rule_string)
#             self.cursor.execute('UPDATE rules SET rule_string = ? WHERE id = ?', (new_rule_string, rule_id))
#             self.connection.commit()
#             print("Rule modified successfully.")
#         except ValueError as ve:
#             print(f"Error: {ve}")
#         except Exception as e:
#             print(f"An error occurred: {e}")

#     def close(self):
#         self.connection.close()

# # Flask application to expose APIs for rule management
# app = Flask(__name__)

# @app.route('/create_rule', methods=['POST'])
# def create_rule_api():
#     data = request.json
#     rule_name = data['rule_name']
#     rule_string = data['rule_string']

#     try:
#         ast = create_rule(rule_name, rule_string)
#         return jsonify({'ast': ast.to_dict()}), 201  # Use the to_dict() method here
#     except Exception as e:
#         return jsonify({'error': str(e)}), 400

# @app.route('/evaluate_rule', methods=['POST'])
# def evaluate_rule_api():
#     data = request.json
#     ast_data = data['ast']
#     user_data = data['user_data']

#     try:
#         # Reconstruct the AST from the incoming dictionary
#         ast = reconstruct_ast(ast_data)
#         result = evaluate_rule(ast, user_data)
#         return jsonify({'result': result})
#     except Exception as e:
#         return jsonify({'error': str(e)}), 400

# @app.route('/modify_rule/<int:rule_id>', methods=['PUT'])
# def modify_rule_api(rule_id):
#     data = request.json
#     new_rule_string = data['rule_string']

#     try:
#         rule_engine = RuleEngine()
#         rule_engine.modify_rule(rule_id, new_rule_string)
#         return jsonify({'message': 'Rule modified successfully!'}), 200
#     except Exception as e:
#         return jsonify({'error': str(e)}), 400

# @app.route('/combine_rules', methods=['POST'])
# def combine_rules_api():
#     data = request.json
#     rule_ids = data.get('rule_ids')
#     operator = data.get('operator')

#     if rule_ids is None or operator is None:
#         return jsonify({'error': 'Missing rule_ids or operator'}), 400

#     # Placeholder for combining rules logic (to be implemented)
#     combined_ast = None  # Replace this with actual logic

#     return jsonify({'message': 'Rules combined!', 'combined_ast': combined_ast}), 200

# if __name__ == "__main__":
#     init_db()  # Initialize the database on startup
#     app.run(debug=True)


import sqlite3
import json
import re
from flask import Flask, request, jsonify

# Node Class to define AST structure
class Node:
    def __init__(self, node_type, value=None, left=None, right=None):
        self.node_type = node_type  # "operator" or "operand"
        self.value = value          # Value for operands (e.g., 'age > 30') or operator type ("AND", "OR", etc.)
        self.left = left            # Left child node (optional)
        self.right = right          # Right child node (optional)

    def to_dict(self):
        """Convert the Node to a dictionary for JSON serialization."""
        return {
            'node_type': self.node_type,
            'value': self.value,
            'left': self.left.to_dict() if self.left else None,
            'right': self.right.to_dict() if self.right else None,
        }

    def is_operator(self):
        return self.node_type == "operator"

    def is_operand(self):
        return self.node_type == "operand"

    def evaluate(self, user_data):
        if self.is_operator():
            left_value = self.left.evaluate(user_data)
            right_value = self.right.evaluate(user_data)

            if self.value == "AND":
                return left_value and right_value
            elif self.value == "OR":
                return left_value or right_value
            else:
                raise ValueError(f"Unknown operator: {self.value}")
        elif self.is_operand():
            return eval(self.value, {}, user_data)
        else:
            raise ValueError(f"Unknown node type: {self.node_type}")

# Functions to parse and build the AST from a rule string
def parse_rule(rule_str):
    tokens = re.findall(r'\(|\)|\w+|>=|>|<=|<|=|AND|OR', rule_str)
    return build_ast(tokens)

def build_ast(tokens):
    if not tokens:
        return None

    token = tokens.pop(0)

    if token == "(":
        left = build_ast(tokens)
        operator = tokens.pop(0)
        right = build_ast(tokens)
        tokens.pop(0)  # remove closing ')'
        return Node(node_type="operator", value=operator, left=left, right=right)

    elif re.match(r'\w+', token):
        left_operand = token
        operator = tokens.pop(0)
        right_operand = tokens.pop(0)
        condition = f"{left_operand} {operator} {right_operand}"
        return Node(node_type="operand", value=condition)

    return None

# Functions for database management
def init_db():
    """Initialize the database and create tables if they don't exist."""
    conn = sqlite3.connect('rules.db')  # This creates a new database file
    cursor = conn.cursor()

    # Drop existing tables for a fresh start (optional)
    cursor.execute('DROP TABLE IF EXISTS rule_conditions;')
    cursor.execute('DROP TABLE IF EXISTS rules;')

    # Create the rules table
    cursor.execute('''CREATE TABLE IF NOT EXISTS rules (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        rule_name TEXT NOT NULL,
                        rule_string TEXT NOT NULL)''')

    # Create the rule_conditions table
    cursor.execute('''CREATE TABLE IF NOT EXISTS rule_conditions (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        rule_id INTEGER,
                        ast_json TEXT,
                        FOREIGN KEY (rule_id) REFERENCES rules (id))''')
    conn.commit()  # Commit changes
    conn.close()

def create_rule(rule_name, rule_string):
    conn = sqlite3.connect('rules.db')
    cursor = conn.cursor()

    ast = parse_rule(rule_string)

    cursor.execute("INSERT INTO rules (rule_name, rule_string) VALUES (?, ?)", (rule_name, rule_string))
    rule_id = cursor.lastrowid

    ast_json = json.dumps(ast.to_dict())  # Use to_dict() for serialization
    cursor.execute("INSERT INTO rule_conditions (rule_id, ast_json) VALUES (?, ?)", (rule_id, ast_json))

    conn.commit()
    conn.close()
    return ast

def evaluate_rule(ast, user_data):
    if ast.node_type == 'operand':
        return eval_operand(ast.value, user_data)

    elif ast.node_type == 'operator':
        left_result = evaluate_rule(ast.left, user_data)
        right_result = evaluate_rule(ast.right, user_data)
        if ast.value == "AND":
            return left_result and right_result
        elif ast.value == "OR":
            return left_result or right_result
        else:
            raise ValueError(f"Unknown operator: {ast.value}")

# Helper function to evaluate operand conditions
def eval_operand(condition, data):
    """Evaluate a condition based on user data."""
    # Using regex to extract operands and operators
    match = re.match(r'(\w+) (>=|>|<=|<|=) (.+)', condition.strip())

    if not match:
        raise ValueError(f"Invalid condition format: {condition}")

    left_operand, operator, right_operand = match.groups()
    left_value = data.get(left_operand.strip())

    # Handle cases where right_operand might be a number or a string
    right_value = right_operand.strip()
    if right_value.isdigit():
        right_value = int(right_value)  # Convert to integer if it's a number

    # Evaluate based on the operator
    if operator == '>':
        return left_value > right_value
    elif operator == '<':
        return left_value < right_value
    elif operator == '=':
        return left_value == right_value
    elif operator == '>=':
        return left_value >= right_value
    elif operator == '<=':
        return left_value <= right_value
    else:
        raise ValueError(f"Unknown operator: {operator}")

def reconstruct_ast(ast_data):
    """Recursively reconstruct the AST from a dictionary."""
    if ast_data['node_type'] == 'operator':
        left = reconstruct_ast(ast_data['left']) if ast_data['left'] else None
        right = reconstruct_ast(ast_data['right']) if ast_data['right'] else None
        return Node(node_type='operator', value=ast_data['value'], left=left, right=right)
    elif ast_data['node_type'] == 'operand':
        return Node(node_type='operand', value=ast_data['value'])
    else:
        raise ValueError(f"Unknown node type: {ast_data['node_type']}")

class RuleEngine:
    VALID_ATTRIBUTES = {'age', 'department', 'income'}
    USER_DEFINED_FUNCTIONS = {
        'is_adult': lambda x: x >= 18,
        'is_senior': lambda x: x >= 65,
        # Add more user-defined functions as needed
    }

    def __init__(self, db_name='rules.db'):
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()

    def validate_rule_string(self, rule_string):
        pattern = r'^[a-zA-Z0-9\s]+(==|!=|<|<=|>|>=)[a-zA-Z0-9\s]+$'  # Customize regex
        if not re.match(pattern, rule_string):
            raise ValueError("Invalid rule string format.")

    def validate_attributes(self, attributes):
        for attribute in attributes:
            if attribute not in self.VALID_ATTRIBUTES:
                raise ValueError(f"Attribute '{attribute}' is not valid.")

    def modify_rule(self, rule_id, new_rule_string):
        try:
            self.validate_rule_string(new_rule_string)
            self.cursor.execute('UPDATE rules SET rule_string = ? WHERE id = ?', (new_rule_string, rule_id))
            self.connection.commit()
            print("Rule modified successfully.")
        except ValueError as ve:
            print(f"Error: {ve}")
        except Exception as e:
            print(f"An error occurred: {e}")

    def close(self):
        self.connection.close()

# Flask application to expose APIs for rule management
app = Flask(__name__)

@app.route('/create_rule', methods=['POST'])
def create_rule_api():
    data = request.json
    rule_name = data['rule_name']
    rule_string = data['rule_string']

    try:
        ast = create_rule(rule_name, rule_string)
        return jsonify({'ast': ast.to_dict()}), 201  # Use the to_dict() method here
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/evaluate_rule', methods=['POST'])
def evaluate_rule_api():
    data = request.json
    ast_data = data['ast']
    user_data = data['user_data']

    try:
        # Reconstruct the AST from the incoming dictionary
        ast = reconstruct_ast(ast_data)
        result = evaluate_rule(ast, user_data)
        return jsonify({'result': result})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/modify_rule/<int:rule_id>', methods=['PUT'])
def modify_rule_api(rule_id):
    data = request.json
    new_rule_string = data['rule_string']

    try:
        rule_engine = RuleEngine()
        rule_engine.modify_rule(rule_id, new_rule_string)
        return jsonify({'message': 'Rule modified successfully!'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/combine_rules', methods=['POST'])
def combine_rules_api():
    data = request.json
    rule_ids = data.get('rule_ids')
    operator = data.get('operator')

    if rule_ids is None or operator is None:
        return jsonify({'error': 'Missing rule_ids or operator'}), 400

    # Placeholder for combining rules logic (to be implemented)
    combined_ast = None  # Replace this with actual logic

    return jsonify({'message': 'Rules combined!', 'combined_ast': combined_ast}), 200

@app.route('/evaluate_user_defined_function', methods=['POST'])
def evaluate_user_defined_function_api():
    data = request.json
    function_name = data.get('function_name')
    value = data.get('value')

    if function_name in RuleEngine.USER_DEFINED_FUNCTIONS:
        result = RuleEngine.USER_DEFINED_FUNCTIONS[function_name](value)
        return jsonify({'result': result}), 200
    else:
        return jsonify({'error': 'Unknown function'}), 400

if __name__ == "__main__":
    init_db()  # Initialize the database on startup
    app.run(debug=True)




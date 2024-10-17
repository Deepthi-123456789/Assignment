# Rule Engine Application

## Overview
This rule engine application allows users to create, modify, evaluate, and combine rules based on user-defined conditions. It utilizes Flask for the API, SQLite for data storage, and a custom Abstract Syntax Tree (AST) structure to represent and evaluate rules.

## Features
- **Rule Creation**: Create rules with user-defined conditions.
- **Rule Evaluation**: Evaluate rules against user data.
- **Rule Modification**: Modify existing rules in the database.
- **Combine Rules**: Combine multiple rules using logical operators (e.g., AND, OR).
- **User-Defined Functions**: Evaluate conditions using predefined functions like `is_adult` and `is_senior`.

## Technologies Used
- Python
- Flask
- SQLite
- Regular Expressions (for rule parsing)

## API Endpoints
###Download postman and perform this rule as data given below. create_rule,modificatio_rule,evaluate_rule,combine_rule,Evaluate User-Defined Function

### 1. Create Rule
- **Endpoint**: `/create_rule`
- **Method**: `POST`
- **Request Body**:
    ```json
    {
      "rule_name": "Age Check",
      "rule_string": "age >= 18"
    }
    ```
- **Response**:
    ```json
    {
      "ast": {
        "node_type": "operand",
        "value": "age >= 18",
        "left": null,
        "right": null
      }
    }
    ```

### 2. Evaluate Rule
- **Endpoint**: `/evaluate_rule`
- **Method**: `POST`
- **Request Body**:
    ```json
    {
      "ast": {
        "node_type": "operand",
        "value": "age >= 18",
        "left": null,
        "right": null
      },
      "user_data": {
        "age": 20
      }
    }
    ```
- **Response**:
    ```json
    {
      "result": true
    }
    ```

### 3. Modify Rule
- **Endpoint**: `/modify_rule/<int:rule_id>`
- **Method**: `PUT`
- **Request Body**:
    ```json
    {
      "rule_string": "age >= 21"
    }
    ```
- **Response**:
    ```json
    {
      "message": "Rule modified successfully!"
    }
    ```

### 4. Combine Rules
- **Endpoint**: `/combine_rules`
- **Method**: `POST`
- **Request Body**:
    ```json
    {
      "rule_ids": [1, 2],
      "operator": "AND"
    }
    ```
- **Response**:
    ```json
    {
      "message": "Rules combined!",
      "combined_ast": null  // Placeholder for combined AST
    }
    ```

### 5. Evaluate User-Defined Function
- **Endpoint**: `/evaluate_user_defined_function`
- **Method**: `POST`
- **Request Body**:
    ```json
    {
      "function_name": "is_adult",
      "value": 20
    }
    ```
- **Response**:
    ```json
    {
      "result": true
    }
    ```

## Database
The application uses SQLite for data persistence. The following tables are created:
(download db browser(sqlite): to make sure that rule and rule_conditions are created or not  if created when we run app.py then rule.db file will be created)
- `rules`: Stores rule names and rule strings.
- `rule_conditions`: Stores AST representations of the rules.

## Installation and Usage

1. Clone the repository:
    ```bash
    git clone <repository-url>
    cd <repository-directory>
    ```

2. Install the required packages:
    ```bash
    pip install Flask,request and other required packeges
    ```

3. Run the application:
    ```bash
    python app.py
    ```

4. The application will be available at `http://127.0.0.1:5000`.






import re

def parse_expression(exp: str) -> list:
    """
    Recibe una expresión regular y la divide en subexpresiones.
    Retorna una lista con los elementos individuales o un mensaje de error si la expresión es inválida.
    """
    tokens = []    
    buffer = ""    
    stack = []     
    paren_count = 0  

    try:
        for char in exp:
            if char == '(':
                if buffer:
                    tokens.append(buffer)  # Guardar lo acumulado en el buffer
                    buffer = ""            # Limpiar el buffer
                stack.append(char)        
                tokens.append(char)      
                paren_count += 1          


            elif char == ')':
                if paren_count == 0:
                    raise ValueError("Error: Paréntesis de cierre sin apertura previa.")
                if buffer:
                    tokens.append(buffer)  
                    buffer = ""            
                tokens.append(char)      
                paren_count -= 1          

     
            elif char in "+*":
                if buffer:
                    tokens.append(buffer)  
                    buffer = ""         
                tokens.append(char)       

            else:
                buffer += char 

        if paren_count != 0:
            raise ValueError("Error: Paréntesis de apertura sin cierre.")
        if buffer:
            tokens.append(buffer)

        return tokens

    except ValueError as e:
        print(f"Expresión Inválida: {e}")
        return []

# Prueba de la función con expresiones válidas e inválidas
if __name__ == "__main__":
    expressions = ["(ab+ba)*a", "(a+b)*(ab)", "(a+b", "a+b)", "((a+b))", "a+b)*a"]
    for exp in expressions:
        print(f"Expresión Regular: {exp}")
        tokens = parse_expression(exp)
        if tokens:
            print("Tokens:", tokens)
        print("-" * 50)

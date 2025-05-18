import re

def parse_expression(exp: str) -> list:
    """
    Recibe una expresión regular y la divide en tokens, agregando concatenación implícita solo cuando sea necesario.
    Detecta errores como paréntesis desbalanceados.
    """
    tokens = []
    paren_count = 0

    try:
        for i, char in enumerate(exp):
            # Manejo de paréntesis de apertura
            if char == '(':
                paren_count += 1
                tokens.append(char)

            # Manejo de paréntesis de cierre
            elif char == ')':
                paren_count -= 1
                if paren_count < 0:
                    raise ValueError("Error: Paréntesis de cierre sin apertura previa.")
                tokens.append(char)

                # Verificar concatenación implícita después de un paréntesis cerrado
                if i + 1 < len(exp) and (exp[i + 1].isalnum() or exp[i + 1] == '('):
                    tokens.append('.')

            # Operadores: Unión y Kleene
            elif char in "+*":
                tokens.append(char)

                # Verificar concatenación después de Kleene si viene otro símbolo o paréntesis
                if char == '*' and i + 1 < len(exp) and (exp[i + 1].isalnum() or exp[i + 1] == '('):
                    tokens.append('.')

            # Símbolo explícito de concatenación
            elif char == '.':
                tokens.append(char)

            # Letras y números (símbolos básicos)
            elif char.isalnum():
                tokens.append(char)

                # Concatenación implícita si el siguiente símbolo es letra o número y no hay un punto explícito
                if (i + 1 < len(exp) and exp[i + 1].isalnum()) and (i == 0 or exp[i - 1] != '.'):
                    tokens.append('.')

            else:
                raise ValueError(f"Carácter inválido en la expresión: '{char}'")

        if paren_count != 0:
            raise ValueError("Error: Paréntesis de apertura sin cierre.")

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

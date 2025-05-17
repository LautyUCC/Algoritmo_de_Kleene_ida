from parser import parse_expression
from automaton import Automaton

def build_automaton(tokens):
    """
    Construye el autómata a partir de los tokens obtenidos.
    """
    stack = []  # Pila para manejar sub-autómatas

    for token in tokens:
        # Caso 1: Operador de Unión (+)
        if token == "+":
            # Sacar los dos autómatas de la pila
            automaton2 = stack.pop()
            automaton1 = stack.pop()
            # Realizar la unión
            result = Automaton.union(automaton1, automaton2)
            stack.append(result)

        # Caso 2: Cerradura de Kleene (*)
        elif token == "*":
            automaton = stack.pop()
            result = Automaton.kleene_star(automaton)
            stack.append(result)

        # Caso 3: Paréntesis (apertura o cierre)
        elif token == "(" or token == ")":
            continue  # Ignorar paréntesis en esta etapa

        # Caso 4: Concatenación Implícita
        elif len(stack) >= 2:
            # Si el tope de la pila es un autómata y el token actual es un símbolo, concatenar
            if stack and not (token in "+*()"):
                automaton2 = stack.pop()
                automaton1 = stack.pop()
                result = Automaton.concatenation(automaton1, automaton2)
                stack.append(result)

        # Caso 5: Autómata Básico (símbolo individual)
        else:
            basic_automaton = Automaton.basic(token)
            stack.append(basic_automaton)

    # El resultado final debe ser el único autómata en la pila
    if len(stack) != 1:
        raise ValueError("Error al construir el autómata: Pila no balanceada")
    return stack.pop()

# Función principal para interactuar con el usuario
if __name__ == "__main__":
    print("🚀 Autómata Finito desde Expresión Regular")
    expression = input("Ingrese la expresión regular: ")

    try:
        # Obtener los tokens usando el parser
        tokens = parse_expression(expression)
        print(f"Tokens generados: {tokens}")

        if not tokens:
            print("Expresión inválida. No se generaron tokens.")
        else:
            # Construir el autómata a partir de los tokens
            automaton = build_automaton(tokens)
            print(f"Autómata generado: {automaton}")

            # Visualización del autómata
            filename = input("Ingrese el nombre para guardar el autómata (sin extensión): ")
            automaton.visualize(filename)
            print(f"Autómata guardado como: {filename}.png")
    except Exception as e:
        print(f"Error: {e}")

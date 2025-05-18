from graphviz import Digraph

class Automaton:
    def __init__(self, states, alphabet, transitions, start_state, final_states):
        self.states = states
        self.alphabet = alphabet
        self.transitions = transitions
        self.start_state = start_state
        self.final_states = final_states

    def __repr__(self):
        return f"AFN(states={self.states}, start={self.start_state}, final={self.final_states})"

    @staticmethod
    def basic(symbol):
        """
        Crea un autómata básico para un símbolo (a o b).
        """
        start = "q0"
        end = "q1"
        states = {start, end}
        transitions = {(start, symbol): {end}}
        return Automaton(states, {symbol}, transitions, start, {end})

    @staticmethod
    def epsilon():
        """
        Crea un autómata que reconoce la cadena vacía (ε).
        """
        start = "q0"
        end = "q1"
        states = {start, end}
        transitions = {(start, ""): {end}}
        return Automaton(states, {""}, transitions, start, {end})

    @staticmethod
    def union(automaton1, automaton2):
        """
        Unión híbrida:
        - Si ambos autómatas son básicos, crea una estructura simplificada (sin ε).
        - Si no, aplica la construcción estándar con q_start y q_end usando transiciones ε.
        """
        def is_basic(automaton):
            return (
                len(automaton.states) == 2 and
                len(automaton.transitions) == 1 and
                "" not in automaton.alphabet
            )

        # 💡 CASO 1: Simplificado (solo un símbolo en cada uno)
        if is_basic(automaton1) and is_basic(automaton2):
            start = "q0"
            end = "qf"

            states = {start, end}
            transitions = {}

            # Extraer el símbolo de cada uno
            (s1, symbol1), dest1 = list(automaton1.transitions.items())[0]
            (s2, symbol2), dest2 = list(automaton2.transitions.items())[0]

            transitions[(start, symbol1)] = {end}
            transitions[(start, symbol2)] = {end}

            return Automaton(
                states=states,
                alphabet={symbol1, symbol2},
                transitions=transitions,
                start_state=start,
                final_states={end}
            )

        # 💡 CASO 2: General (con ε-transiciones)
        # Renombrar estados para evitar colisiones
        mapping1 = {s: f"{s}_1" for s in automaton1.states}
        mapping2 = {s: f"{s}_2" for s in automaton2.states}

        states = {"q_start", "q_end"}
        states.update(mapping1.values())
        states.update(mapping2.values())

        transitions = {
            ("q_start", ""): {mapping1[automaton1.start_state], mapping2[automaton2.start_state]}
        }

        for (s, a), ends in automaton1.transitions.items():
            transitions[(mapping1[s], a)] = {mapping1[e] for e in ends}

        for (s, a), ends in automaton2.transitions.items():
            transitions[(mapping2[s], a)] = {mapping2[e] for e in ends}

        for f in automaton1.final_states:
            transitions[(mapping1[f], "")] = {"q_end"}

        for f in automaton2.final_states:
            transitions[(mapping2[f], "")] = {"q_end"}

        return Automaton(
            states=states,
            alphabet=automaton1.alphabet.union(automaton2.alphabet),
            transitions=transitions,
            start_state="q_start",
            final_states={"q_end"}
        )

    @staticmethod
    def concatenation(automaton1, automaton2):
        """
        Concatena dos autómatas:
        - Fusiona el estado final del primero con el inicial del segundo.
        - Elimina el estado inicial flotante del segundo autómata.
        """
        # Renombrar estados del segundo autómata para evitar colisiones
        mapping = {s: f"{s}_b" for s in automaton2.states}
        transitions2 = {}
        for (start, symbol), ends in automaton2.transitions.items():
            new_start = mapping[start]
            new_ends = {mapping[e] for e in ends}
            transitions2[(new_start, symbol)] = new_ends

        # Clonar y mapear todos los estados
        states = automaton1.states.union(set(mapping.values()))

        # Reemplazar las transiciones del final de automaton1 con las del inicio de automaton2
        transitions = automaton1.transitions.copy()
        for final in automaton1.final_states:
            # Fusionar el último estado de A con el estado inicial de B directamente
            start_b = mapping[automaton2.start_state]

            # Transferir las transiciones del estado inicial de B al estado final de A
            for (start, symbol), ends in transitions2.items():
                if start == start_b:
                    transitions[(final, symbol)] = ends

        # Eliminar el estado inicial del segundo autómata después de la fusión
        states.discard(mapping[automaton2.start_state])

        # Agregar el resto de las transiciones del segundo autómata (evitando el inicial redundante)
        for (start, symbol), ends in transitions2.items():
            if start != mapping[automaton2.start_state]:
                transitions[(start, symbol)] = ends

        # Unir los conjuntos de estados finales
        final_states = {mapping[s] for s in automaton2.final_states}

        return Automaton(
            states=states,
            alphabet=automaton1.alphabet.union(automaton2.alphabet),
            transitions=transitions,
            start_state=automaton1.start_state,
            final_states=final_states
        )



    @staticmethod
    def kleene_star(automaton):
        """
        Si el autómata consiste en una sola transición (ej. a -> b), 
        lo simplificamos a un solo estado con una transición a sí mismo.
        Si no, aplicamos la versión común.
        """
        if (
            len(automaton.states) == 2 and
            len(automaton.alphabet) == 1 and
            len(automaton.transitions) == 1
        ):
            symbol = next(iter(automaton.alphabet))
            state = "q0"
            transitions = {(state, symbol): {state}}

            return Automaton(
                states={state},
                alphabet={symbol},
                transitions=transitions,
                start_state=state,
                final_states={state}
            )

        # Versión común para casos más complejos
        transitions = automaton.transitions.copy()
        for final in automaton.final_states:
            if (final, "") in transitions:
                transitions[(final, "")].add(automaton.start_state)
            else:
                transitions[(final, "")] = {automaton.start_state}
        final_states = automaton.final_states.union({automaton.start_state})

        return Automaton(
            states=automaton.states,
            alphabet=automaton.alphabet,
            transitions=transitions,
            start_state=automaton.start_state,
            final_states=final_states
        )


    def visualize(self, filename="automaton"):
        """
        Genera el grafo del autómata usando Graphviz.
        """
        dot = Digraph(comment='Automaton')
        for state in self.states:
            shape = 'doublecircle' if state in self.final_states else 'circle'
            dot.node(state, state, shape=shape)

        for (start, symbol), ends in self.transitions.items():
            for end in ends:
                label = symbol if symbol else "ε"
                dot.edge(start, end, label=label)

        dot.render(filename, format='png', cleanup=True)

# Prueba de los autómatas básicos

from parser import parse_expression
from automaton import Automaton

def elegir_operacion():
    print("\nSeleccione la operación que desea realizar:")
    print("1. Unión (+)")
    print("2. Concatenación")
    print("3. Kleene (*)")
    opcion = input("Ingrese el número de la operación: ")

    if opcion not in ["1", "2", "3"]:
        print("Opción inválida. Intente de nuevo.")
        return elegir_operacion()
    return int(opcion)

def ingresar_simbolos():
    simbolo1 = input("Ingrese el primer símbolo: ")
    simbolo2 = input("Ingrese el segundo símbolo: ")
    return simbolo1, simbolo2

if __name__ == "__main__":
    print("🚀 Generador de Autómatas Finito")

    # Elegir la operación
    operacion = elegir_operacion()

    if operacion == 1:  # Unión
        print("\nOperación: Unión")
        a, b = ingresar_simbolos()
        automaton1 = Automaton.basic(a)
        automaton2 = Automaton.basic(b)
        result = Automaton.union(automaton1, automaton2)

    elif operacion == 2:  # Concatenación
        print("\nOperación: Concatenación")
        a, b = ingresar_simbolos()
        automaton1 = Automaton.basic(a)
        automaton2 = Automaton.basic(b)
        result = Automaton.concatenation(automaton1, automaton2)

    elif operacion == 3:  # Kleene
        print("\nOperación: Kleene Star")
        a = input("Ingrese el símbolo: ")
        automaton1 = Automaton.basic(a)
        result = Automaton.kleene_star(automaton1)

    # Mostrar el autómata generado
    print("\nAutómata generado correctamente:")
    print(result)

    # Solicitar nombre del archivo
    nombre = input("Ingrese el nombre del archivo para guardar el autómata: ")
    result.visualize(nombre)
    print(f"Autómata guardado como {nombre}.png")

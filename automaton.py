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
        Realiza la unión de dos autómatas (a + b).
        """
        start = "q_start"
        end = "q_end"
        states = {start, end}.union(automaton1.states).union(automaton2.states)
        transitions = {
            (start, ""): {automaton1.start_state, automaton2.start_state}
        }
        transitions.update(automaton1.transitions)
        transitions.update(automaton2.transitions)
        for final in automaton1.final_states:
            transitions[(final, "")] = {end}
        for final in automaton2.final_states:
            transitions[(final, "")] = {end}
        return Automaton(states, automaton1.alphabet.union(automaton2.alphabet), transitions, start, {end})

    @staticmethod
    def concatenation(automaton1, automaton2):
        """
        Realiza la concatenación de dos autómatas (ab).
        """
        transitions = automaton1.transitions.copy()
        for final in automaton1.final_states:
            transitions[(final, "")] = {automaton2.start_state}
        transitions.update(automaton2.transitions)
        states = automaton1.states.union(automaton2.states)
        return Automaton(states, automaton1.alphabet.union(automaton2.alphabet), transitions, automaton1.start_state, automaton2.final_states)

    @staticmethod
    def kleene_star(automaton):
        """
        Realiza la cerradura de Kleene (a*).
        """
        start = "q_start"
        end = "q_end"
        states = {start, end}.union(automaton.states)
        transitions = {
            (start, ""): {automaton.start_state, end}
        }
        for final in automaton.final_states:
            transitions[(final, "")] = {automaton.start_state, end}
        transitions.update(automaton.transitions)
        return Automaton(states, automaton.alphabet, transitions, start, {end})

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
if __name__ == "__main__":
    a = Automaton.basic("a")
    b = Automaton.basic("b")
    union_ab = Automaton.union(a, b)
    concatenation_ab = Automaton.concatenation(a, b)
    star_a = Automaton.kleene_star(a)

    print("Automaton básico (a):", a)
    print("Automaton básico (b):", b)
    print("Unión (a + b):", union_ab)
    print("Concatenación (ab):", concatenation_ab)
    print("Kleene Star (a*):", star_a)

    # Visualización de ejemplos
    union_ab.visualize("union_ab")
    concatenation_ab.visualize("concatenation_ab")
    star_a.visualize("kleene_star_a")

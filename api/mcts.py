from collections import defaultdict
import chess
import chess.engine
import numpy as np


class MonteCarloTreeSearchNode:
    def __init__(
        self, state: chess.Board, stockfish=None, parent=None, parent_action=None
    ):
        self.state = state
        self.parent = parent
        self.parent_action = parent_action
        self.children = []
        self._number_of_visits = 0
        self._results = defaultdict(int)
        self._results[1] = 0
        self._results[-1] = 0
        self._untried_actions = None
        self._untried_actions = self.untried_actions()
        self.stockfish = stockfish
        self._value = None

    @property
    def value(self):
        return self._value

    def set_stockfish_evaluation(self):
        result = self.stockfish.analyse(self.state, chess.engine.Limit(time=1.0))
        self._value = result["score"].relative.score()

    def untried_actions(self):
        self._untried_actions = list(self.state.legal_moves)
        return self._untried_actions

    def q(self):
        wins = self._results[1]
        loses = self._results[-1]
        return wins - loses

    def n(self):
        return self._number_of_visits

    def expand(self):
        action = self._untried_actions.pop()
        next_state = self.state.copy()
        next_state.push(action)
        child_node = MonteCarloTreeSearchNode(
            state=next_state,
            stockfish=self.stockfish,
            parent=self,
            parent_action=action,
        )
        self.children.append(child_node)
        return child_node

    def is_terminal_node(self):
        return self.state.is_game_over()

    def rollout(self):
        current_rollout_state = self.state.copy()
        while (
            not current_rollout_state.is_game_over()
            or len(list(current_rollout_state.legal_moves)) != 0
        ):
            possible_moves = list(current_rollout_state.legal_moves)
            action = self.rollout_policy(possible_moves)
            current_rollout_state.push(action)
        return current_rollout_state.result()

    def rollout_policy(self, possible_moves):
        return possible_moves[np.random.randint(len(possible_moves))]

    def backpropagate(self, result):
        self._number_of_visits
        self._results[result] += 1
        if self.parent:
            self.parent.backpropagate(result)

    def is_fully_expanded(self):
        return len(self._untried_actions) == 0

    def best_child(self, c_param=10):
        for child in self.children:
            child.set_stockfish_evaluation()

        choices_weights = [
            (c.q() / c.n())
            + c_param * np.sqrt((2 * np.log(self.n()) / c.n()))
            + c.value / 1000.0
            if c.n() != 0
            else float("inf")
            for c in self.children
        ]
        return self.children[np.argmax(choices_weights)]

    def _tree_policy(self):
        current_node = self
        while not current_node.is_terminal_node():
            if not current_node.is_fully_expanded():
                return current_node.expand()
            else:
                current_node = current_node.best_child()
        return current_node

    def best_action(self):
        simulation_no = 100

        for i in range(simulation_no):
            v = self._tree_policy()
            reward = v.rollout()
            v.backpropagate(reward)

        return self.best_child(c_param=0.0)


def mcts_make_chess_move(fen_string: str):
    stockfish = chess.engine.SimpleEngine.popen_uci("/opt/homebrew/bin/stockfish")
    board = chess.Board(fen_string)
    root = MonteCarloTreeSearchNode(state=board, stockfish=stockfish)
    simulation_no = 10
    for i in range(simulation_no):
        print(i)
        node = root._tree_policy()
        reward = node.rollout()
        node.backpropagate(reward)

    best_child = root.best_child(c_param=0.1)
    print("Best Move:", best_child.parent_action)
    print("Stockfish Evaluation:", best_child.value)

    move = str(best_child.parent_action)

    result = {
        "from": move[0] + move[1],
        "to": move[2] + move[3],
    }

    if len(move) == 5:
        result["promotion"] = move[4]

    return result

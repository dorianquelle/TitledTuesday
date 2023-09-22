import os
import json
import time
import chess
import chess.engine
import pandas as pd
import matplotlib.pyplot as plt
from tqdm import tqdm
import os
import json

engine_path = "/opt/homebrew/bin/stockfish"


def extract_score(score_obj):
    if score_obj.is_mate():
        # Return 99 or -99 depending on the sign of the mate count
        return 99 if score_obj.white().mate() > 0 else -99
    else:
        # Convert centipawn score to regular pawn units
        return score_obj.white().score() / 100

def evaluate_moves(moves, engine_path, multi_pv_lines=5, thinking_time=1):
    try:
        board = chess.Board()
        engine = chess.engine.SimpleEngine.popen_uci(engine_path)

        evaluations = []

        for move in tqdm(moves):
            # Construct the UCI string, considering pawn promotions
            uci_move = move['from'] + move['to']
            if 'promotion' in move:
                uci_move += move['promotion'].lower()

            # Find the number of legal moves in the position
            legal_moves_count = len(list(board.legal_moves))

            # Analyse the position to the desired depth with multi-PV
            multi_pv_result = engine.analyse(board, chess.engine.Limit(time=thinking_time), multipv=min(multi_pv_lines, legal_moves_count))

            # Extract the moves and evaluations from the engine's output
            pv_moves = [info.get('pv')[0] for info in multi_pv_result if info.get('pv')]
            pv_evals = [extract_score(info.get('score')) for info in multi_pv_result]

            # If the actual move is in the top multi-PV lines, get its rank and eval, otherwise set them to -1
            actual_move = board.push_uci(uci_move)

            if actual_move in pv_moves:
                rank = pv_moves.index(actual_move) + 1
                actual_eval = pv_evals[pv_moves.index(actual_move)]
            else:
                rank = -1
                actual = engine.analyse(board, chess.engine.Limit(time=thinking_time))
                actual_eval = extract_score(actual['score'])

            best_move = pv_moves[0]
            best_eval = pv_evals[0]

            evaluations.append({
                'Best Move': best_move,
                'Best Move Eval': best_eval,
                'Ranking Real Move': rank,
                'Real Move Eval': actual_eval
            })

        engine.quit()
        return evaluations
    except Exception as e:
        print(e)
        engine.quit()
        return None


T = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!?{~}(^)[_]@#$,./&-*++="

def decode(e):
    f = []
    g = len(e)
    for c in range(0, g, 2):
        d = {}
        b = T.index(e[c])
        a = T.index(e[c + 1])
        if a > 63:
            d["promotion"] = "qnrbkp"[int((a - 64) / 3)]
            a = b + (-8 if b < 16 else 8) + (a - 1) % 3 - 1
        if b > 75:
            d["drop"] = "qnrbkp"[b - 79]
        else:
            d["from"] = T[b % 8] + str(int(b / 8) + 1)
        d["to"] = T[a % 8] + str(int(a / 8) + 1)
        f.append(d)
    return f

def process_game(game, engine_path, multi_pv_lines=5, thinking_time=1):
    new_filename = game[:-5] + "_analysed.json"  # Assuming '.json' extension for the original game files
    if os.path.exists("../Data/Analysed/" + new_filename):
        return
    # Load game data
    with open("../Data/Games/" + game) as f:
        game_json = json.load(f)

    enc_movelist = game_json["game"]["moveList"]
    movelist = decode(enc_movelist)
    evaluation = evaluate_moves(movelist, engine_path, multi_pv_lines=multi_pv_lines, thinking_time=thinking_time)
    if not evaluation:
        print(f"Error evaluating game {game}. Skipping...")
        return
    # Modify the evaluation dictionaries
    for index, eval_dict in enumerate(evaluation):
        eval_dict["Best Move"] = eval_dict["Best Move"].uci()  # Convert chess.Move to string
        eval_dict["plycount"] = index + 1
        eval_dict["player"] = "white" if eval_dict["plycount"] % 2 == 1 else "black"
        eval_dict["difference"] = eval_dict["Real Move Eval"] - eval_dict["Best Move Eval"]
        eval_dict["difference"] *= -1 if eval_dict["player"] == "white" else 1

    # Append evaluations and additional metadata to the game's JSON
    game_json["evaluations"] = evaluation
    game_json["multi_pv_lines"] = multi_pv_lines
    game_json["thinking_time"] = thinking_time
    game_json["timestamp"] = int(time.time())

    # Write to a new file
    with open("../Data/Analysed/" + new_filename, "w") as f:
        json.dump(game_json, f, indent=4)



def should_process_file(filename, modulus_target=0):
    """
    Hashes the filename and checks the modulus against the modulus_target.
    If they match, returns True; otherwise returns False.
    """
    m = hashlib.sha256()
    m.update(filename.encode('utf-8'))
    hex_result = m.hexdigest()
    return int(hex_result, 16) % 2 == modulus_target



def process_game_helper(args):
    process_game(*args)

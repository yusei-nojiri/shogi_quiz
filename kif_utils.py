from pathlib import Path

import shogi
import shogi.KIF

piece_names = {
    1: "歩",
    2: "香",
    3: "桂",
    4: "銀",
    5: "金",
    6: "角",
    7: "飛",
    8: "玉",
    9: "と",
    10: "成香",
    11: "成桂",
    12: "成銀",
    13: "馬",
    14: "龍"
}


def get_position(move_count):

    # 棋譜を読み込む
    kif_path = Path(__file__).with_name("sample_game.kif")

    with open(kif_path, "r", encoding="utf-8") as f:
        kif_text = f.read()

    game = shogi.KIF.Parser.parse_str(kif_text)[0]

    if not 0 <= move_count <= len(game["moves"]):
        raise ValueError("指定した手数が範囲外です")

    # 指定した手数まで局面を再現
    board = shogi.Board(game["sfen"])

    for move in game["moves"][:move_count]:
        board.push_usi(move)

    # 81マスの盤面を変換
    web_board = []

    for row in range(9):
        board_row = []

        for col in range(9):
            piece = board.piece_at(row * 9 + col)

            if piece is None:
                board_row.append(("", ""))
            else:
                name = piece_names[piece.piece_type]
                color = "sente" if piece.color == shogi.BLACK else "gote"
                board_row.append((name, color))

        web_board.append(board_row)

    # 持ち駒を変換
    hands = {"sente": {}, "gote": {}}

    for side, color in [("sente", shogi.BLACK), ("gote", shogi.WHITE)]:
        for piece_type, count in board.pieces_in_hand[color].items():
            hands[side][piece_names[piece_type]] = count

    return web_board, hands
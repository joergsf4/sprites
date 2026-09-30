"""Adventure hero - a point-and-click protagonist in the style of Maniac Mansion.

Built from ASCII rows through sprite() in pixelart.py
(PAL plus a small palette of his own), head, torso and legs stitched together as
row lists, then a 1 px dark outline via _outlined(). The left-facing view is the
right-facing one mirrored.

He: male, brown hair pulled back into a ponytail, red T-shirt, jeans, sneakers.
The ASCII grid is 16x38; a frame is 22x40 (2 px room each side plus the outline); the feet stand on HERO_FOOT.

HERO[view][anim] -> list of frames, view in 'front', 'back', 'right', 'left':
  stand  1 frame           walk   4 frames (contact, pass, contact, pass)
  talk   3 frames (front, right/left)   blink  1 frame (front, right/left)
  pickup 3 frames (right/left)          use    2 frames (right/left)
"""
from __future__ import annotations

from PIL import Image

from pixelart import sprite, mirror, _outlined

HERO_PAL = {
    'u': (164, 112, 66), 'h': (118, 74, 42), 'H': (76, 46, 28),        # hair: light, mid, dark
    'c': (242, 202, 164), 'C': (206, 160, 122),                        # skin
    't': (200, 62, 54), 'T': (136, 38, 40),                            # red T-shirt
    'n': (72, 100, 164), 'N': (44, 60, 112),                           # jeans
    'z': (58, 40, 30), 'l': (184, 104, 92),                            # hair tie, lips
}
HERO_W, HERO_H = 16, 38            # the ASCII grid; frames get HERO_PAD px each side
HERO_PAD = 2

# --------------------------------------------------------------------------
# Front view
# --------------------------------------------------------------------------
_FRONT_HEAD = [
    ".....hhhhhh.....",
    "...hhuuuuuhhh...",
    "..hhuuhhhhhhhh..",
    "..huhhhhhhhhhH..",
    "..hhhhhhhhhhhH..",
    "..hhhcccccchhH..",
    "..hccccccccccH..",
    "..hcHHccccHHcH..",
    "..CcckccccckcC..",
    "..CcckccccckcC..",
    "...ccccccCccc...",
    "...ccccccccCc...",
    "....ccllllcC....",
    ".....cccccC.....",
]
_FRONT_EYES_SHUT = ["..hcccccccccch..", "..CcHHccccHHcC..", "..CcccccccccCC.."]   # rows 7-9
_FRONT_MOUTHS = [                                                        # rows 11-12
    ["...ccccccccCc...", "....ccllllcC...."],   # closed
    ["...ccccccccCc...", "....cclkklcC...."],   # half open
    ["...cccllllcCc...", "....cckkkkcC...."],   # open
]
_FRONT_TORSO = [
    "......cccC......",
    "...tttccCCttt...",
    "..tttttcCttttT..",
    ".ttttttttttttTT.",
    ".ttTtttttttttTT.",
    ".ttTtttttttttTT.",
    ".ccTtttttttttCC.",
    ".ccTtttttttttCC.",
    ".ccTtttttttttCC.",
    ".ccTtttttttttCC.",
    ".ccttttttttttCC.",
    ".CcTttttttttTcC.",
]
# walking: the hand on the side of the lifted foot swings forward - up by a pixel
_FRONT_TORSO_SWING = {
    'l': _FRONT_TORSO[:-2] + [".ccttttttttttTT.", "..cTttttttttTcC."],
    'r': _FRONT_TORSO[:-2] + [".TTttttttttttCC.", ".CcTttttttttTc.."],
}
_FRONT_LEGS = {
    'stand': [
        "...xxxxyxxxxx...",
        "...nnnnnnnnnN...",
        "...nnnnnnnnnN...",
        "...nnnnNnnnnN...",
        "...nnnN..nnnN...",
        "...nnnN..nnnN...",
        "...nnnN..nnnN...",
        "...nnnN..nnnN...",
        "...nnnN..nnnN...",
        "...nnnN..nnnN...",
        "..wwwwe..ewwww..",
        "..kkkkk..kkkkk..",
    ],
    'l': [                                   # left foot lifted
        "...xxxxyxxxxx...",
        "...nnnnnnnnnN...",
        "...nnnnnnnnnN...",
        "...nnnnNnnnnN...",
        "...nnnN..nnnN...",
        "...nnnN..nnnN...",
        "...NnnN..nnnN...",
        "...nnnN..nnnN...",
        "..wwwwe..nnnN...",
        "..kkkkk..nnnN...",
        ".........ewwww..",
        ".........kkkkk..",
    ],
    'r': [                                   # right foot lifted
        "...xxxxyxxxxx...",
        "...nnnnnnnnnN...",
        "...nnnnnnnnnN...",
        "...nnnnNnnnnN...",
        "...nnnN..nnnN...",
        "...nnnN..nnnN...",
        "...nnnN..NnnN...",
        "...nnnN..nnnN...",
        "...nnnN..ewwww..",
        "...nnnN..kkkkk..",
        "..wwwwe.........",
        "..kkkkk.........",
    ],
}

# --------------------------------------------------------------------------
# Back view - the ponytail hangs down between the shoulder blades
# --------------------------------------------------------------------------
_BACK_HEAD = [
    ".....hhhhhh.....",
    "...hhuuuuuhhh...",
    "..hhuuhhhhhhhh..",
    "..huhhuhhhhhhH..",
    "..hhhhuhhhhhhH..",
    "..hhhhhuhhhhhH..",
    "..hhhhhuhhhhHH..",
    "..hhhhhhhhhhHH..",
    "..ChhhhhhhhhHC..",
    "..CHhhhhhhhHHC..",
    "...HHhhhhhHHH...",
    "....HHhzzhHH....",
    ".....ChuhhC.....",
    ".....cChhHC.....",
]
_BACK_TORSO = [
    "......huhH......",
    "...tttthhHttt...",
    "..ttttthuhHttT..",
    ".tttttthhHtttTT.",
    ".ttTtttthhtttTT.",
    ".ttTttttHttttTT.",
    ".ccTtttttttttCC.",
    ".ccTtttttttttCC.",
    ".ccTtttttttttCC.",
    ".ccTtttttttttCC.",
    ".ccttttttttttCC.",
    ".CcTttttttttTcC.",
]
_BACK_TORSO_SWING = {
    'l': _BACK_TORSO[:-2] + [".ccttttttttttTT.", "..cTttttttttTcC."],
    'r': _BACK_TORSO[:-2] + [".TTttttttttttCC.", ".CcTttttttttTc.."],
}
_BACK_LEGS = {
    'stand': [
        "...xxxxxxxxxx...",
        "...nnnnnnnnnN...",
        "...nnnnNNnnnN...",
        "...nnnnNnnnnN...",
        "...nnnN..nnnN...",
        "...nnnN..nnnN...",
        "...nnnN..nnnN...",
        "...nnnN..nnnN...",
        "...nnnN..nnnN...",
        "...NnnN..NnnN...",
        "..eeeee..eeeee..",
        "..kkkkk..kkkkk..",
    ],
    'l': [
        "...xxxxxxxxxx...",
        "...nnnnnnnnnN...",
        "...nnnnNNnnnN...",
        "...nnnnNnnnnN...",
        "...nnnN..nnnN...",
        "...nnnN..nnnN...",
        "...NnnN..nnnN...",
        "...nnnN..nnnN...",
        "..eeeee..nnnN...",
        "..kkkkk..nnnN...",
        ".........eeeee..",
        ".........kkkkk..",
    ],
    'r': [
        "...xxxxxxxxxx...",
        "...nnnnnnnnnN...",
        "...nnnnNNnnnN...",
        "...nnnnNnnnnN...",
        "...nnnN..nnnN...",
        "...nnnN..nnnN...",
        "...nnnN..NnnN...",
        "...nnnN..nnnN...",
        "...nnnN..eeeee..",
        "...nnnN..kkkkk..",
        "..eeeee.........",
        "..kkkkk.........",
    ],
}

# --------------------------------------------------------------------------
# Side view (facing right) - ponytail swings out behind the head
# --------------------------------------------------------------------------
_SIDE_HEAD = [
    "......hhhhh.....",
    "....hhuuuuuhh...",
    "...huuuhhhhhhh..",
    "..huhhhhhhhhhhh.",
    "..hhhhhhhhhhhhh.",
    "..hhhhhhhhhhhcc.",
    ".zzhhhhhhhhcHHc.",
    "hzzhhhhhCcccckc.",
    "huHhhhhCCcccccc.",
    "hh.HhhhCcccccccc",
    "hh..HhhcccccccC.",
    ".hh..hCcccccllc.",
    ".hh...Cccccccc..",
    "..hh...cccccc...",
]
_SIDE_EYE_SHUT = ["hzzhhhhhCccccCc."]                                     # row 7
_SIDE_MOUTHS = [                                                           # rows 11-12
    [".hh..hCcccccllc.", ".hh...Cccccccc.."],
    [".hh..hCccccckkc.", ".hh...Cccccccc.."],
    [".hh..hCccccckkc.", ".hh...Cccccckc.."],
]
_SIDE_TORSO = {
    'mid': [                                  # arm hanging straight
        "..hh....cccC....",
        "...hh.tttttt....",
        "....htttttttt...",
        "....ttttTTtttT..",
        "....tttTtttttT..",
        "....tttTtttttT..",
        "....tttCcttttT..",
        "....tttCcttttT..",
        "....tttCcttttT..",
        "....tttCcttttT..",
        "....tttCctttTT..",
        "....TttCCttTTT..",
    ],
    'fwd': [                                  # arm swung forward
        "..hh....cccC....",
        "...hh.tttttt....",
        "....htttttttt...",
        "....ttttTTtttT..",
        "....tttttTtttT..",
        "....ttttttTttT..",
        "....tttttttCcT..",
        "....tttttttCcc..",
        "....tttttttTCcc.",
        "....ttttttttTCC.",
        "....ttttttttTT..",
        "....TtttttttTT..",
    ],
    'back': [                                 # arm swung back
        "..hh....cccC....",
        "...hh.tttttt....",
        "....htttttttt...",
        "...tTTTtttttT...",
        "...tTtttttttT...",
        "..tTtttttttT....",
        "..Cctttttttt....",
        ".Cc.ttttttttT...",
        "Cc..ttttttttT...",
        "CC..ttttttttT...",
        "....tttttttTT...",
        "....TttttttTT...",
    ],
    'reach': [                                # arm stretched out ("use")
        "..hh....cccC....",
        "...hh.tttttt....",
        "....htttttttt...",
        "....tttttttTTtcc",
        "....tttttttttTCc",
        "....tttttttttT..",
        "....tttttttttT..",
        "....tttttttttT..",
        "....tttttttttT..",
        "....tttttttttT..",
        "....tttttttttT..",
        "....TttttttTTT..",
    ],
}
_SIDE_LEGS = {
    'stand': [
        "....xxxxxxxxx...",
        "....nnnnnnnnN...",
        "....nnnnnnnnN...",
        ".....nnnnnnN....",
        ".....nnnnnnN....",
        ".....nnnnnnN....",
        ".....nnnnnnN....",
        ".....nnnnnnN....",
        ".....nnnnnnN....",
        ".....nnnnnnN....",
        ".....wwwwwwwe...",
        ".....kkkkkkkk...",
    ],
    'stride': [                               # contact: legs spread, near leg forward
        "....xxxxxxxxx...",
        "....nnnnnnnnN...",
        "....nnnnnnnnnN..",
        "...NNnnnnNnnnN..",
        "...NNN...nnnnN..",
        "..NNN.....nnnN..",
        "..NNN.....nnnnN.",
        ".NNN.......nnnN.",
        ".NNN.......nnnN.",
        "eNN........nnnN.",
        "ee.........wwwwe",
        "kk.........kkkkk",
    ],
    'pass': [                                 # passing: far leg swings through, knee bent
        "....xxxxxxxxx...",
        "....nnnnnnnnN...",
        "....nnnnnnnnN...",
        ".....nnnnnnnN...",
        ".....nnnnNNNN...",
        ".....nnnnnNNN...",
        ".....nnnnnNNN...",
        ".....nnnnnNNe...",
        ".....nnnnnNee...",
        ".....nnnnnnkk...",
        ".....wwwwwwwe...",
        ".....kkkkkkkk...",
    ],
    'crouch': [                               # knees bent to pick something up
        "....xxxxxxxxx...",
        "....nnnnnnnnnnN.",
        "....nnnnnnnnnnnN",
        ".....NNNnnnnnnN.",
        ".....NNN..nnnN..",
        "......NN..nnnN..",
        "......NN..nnN...",
        ".....eNN..nnN...",
        ".....eee.wwwwe..",
        ".....kkk.kkkkk..",
    ],
}
# picking up: the torso leans forward, the head goes down and forward, the arm reaches the floor
_SIDE_BEND_TORSO = [
    "....hh....cccC..",
    "......httttttt..",
    ".....tttttttttt.",
    ".....ttttttttttT",
    ".....tttttttttTT",
    ".....tttttttttTc",
    ".....tttttttttTc",
    ".....TttttttTTCc",
]
_SIDE_BEND_LEGS = [
    "....xxxxxxxxx.Cc",
    "....nnnnnnnnnnCc",
    "....nnnnnnnnnnCc",
    ".....NNNnnnnnnCc",
    ".....NNN..nnnNCc",
    "......NN..nnnNcc",
    "......NN..nnN.cc",
    ".....eNN..nnN...",
    ".....eee.wwwwe..",
    ".....kkk.kkkkk..",
]


def _frame(rows: list, bob: int = 0) -> Image.Image:
    """Rows -> outlined 22x40 frame; bob lifts the whole figure (walk bounce)."""
    body = sprite(rows, HERO_PAL)
    img = Image.new('RGBA', (HERO_W + 2 * HERO_PAD, HERO_H), (0, 0, 0, 0))
    img.alpha_composite(body, (HERO_PAD, HERO_H - body.height - bob))
    return _outlined(img)


def _patch(rows: list, at: int, new: list) -> list:
    rows = list(rows)
    rows[at:at + len(new)] = new
    return rows


def _build_front():
    stand = _FRONT_HEAD + _FRONT_TORSO + _FRONT_LEGS['stand']
    walk_l = _FRONT_HEAD + _FRONT_TORSO_SWING['l'] + _FRONT_LEGS['l']
    walk_r = _FRONT_HEAD + _FRONT_TORSO_SWING['r'] + _FRONT_LEGS['r']
    return {
        'stand': [_frame(stand)],
        'walk': [_frame(walk_l), _frame(stand, 1), _frame(walk_r), _frame(stand, 1)],
        'talk': [_frame(_patch(stand, 11, m)) for m in _FRONT_MOUTHS],
        'blink': [_frame(_patch(stand, 7, _FRONT_EYES_SHUT))],
    }


def _build_back():
    stand = _BACK_HEAD + _BACK_TORSO + _BACK_LEGS['stand']
    walk_l = _BACK_HEAD + _BACK_TORSO_SWING['l'] + _BACK_LEGS['l']
    walk_r = _BACK_HEAD + _BACK_TORSO_SWING['r'] + _BACK_LEGS['r']
    return {
        'stand': [_frame(stand)],
        'walk': [_frame(walk_l), _frame(stand, 1), _frame(walk_r), _frame(stand, 1)],
    }


def _build_right():
    t, l = _SIDE_TORSO, _SIDE_LEGS
    stand = _SIDE_HEAD + t['mid'] + l['stand']
    stride_a = _SIDE_HEAD + t['back'] + l['stride']        # near leg forward, near arm back
    stride_b = _SIDE_HEAD + t['fwd'] + l['stride']
    pass_ = _SIDE_HEAD + t['mid'] + l['pass']
    crouch = _SIDE_HEAD + t['mid'] + l['crouch']
    bend = ['..' + r for r in _SIDE_HEAD] + _SIDE_BEND_TORSO + _SIDE_BEND_LEGS
    return {
        'stand': [_frame(stand)],
        'walk': [_frame(stride_a), _frame(pass_, 1), _frame(stride_b), _frame(pass_, 1)],
        'talk': [_frame(_patch(stand, 11, m)) for m in _SIDE_MOUTHS],
        'blink': [_frame(_patch(stand, 7, _SIDE_EYE_SHUT))],
        'pickup': [_frame(crouch), _frame(bend), _frame(crouch)],
        'use': [_frame(_SIDE_HEAD + t['fwd'] + l['stand']),
                _frame(_SIDE_HEAD + t['reach'] + l['stand'])],
    }


HERO = {'front': _build_front(), 'back': _build_back(), 'right': _build_right()}
HERO['left'] = {k: [mirror(f) for f in v] for k, v in HERO['right'].items()}
HERO_FOOT = HERO['front']['stand'][0].height - 2   # row the soles stand on (outline below)
HERO_CX = 1 + HERO_PAD + HERO_W // 2                         # canvas x of the body's centre


# --------------------------------------------------------------------------
# Preview: sprite sheet + animated GIFs  (python3 adventure_hero.py)
# --------------------------------------------------------------------------
def sprite_sheet(scale: int = 4, bg=(96, 84, 110)) -> Image.Image:
    rows = [(v, a, fr) for v in ('front', 'back', 'right', 'left') for a, fr in HERO[v].items()]
    fw, fh = HERO['front']['stand'][0].size
    cols = max(len(fr) for _, _, fr in rows)
    sheet = Image.new('RGBA', ((cols * (fw + 2) + 2), len(rows) * (fh + 2) + 2), (*bg, 255))
    for r, (_, _, frames) in enumerate(rows):
        for c, f in enumerate(frames):
            sheet.alpha_composite(f, (2 + c * (fw + 2), 2 + r * (fh + 2)))
    return sheet.resize((sheet.width * scale, sheet.height * scale), Image.NEAREST), rows


def save_gif(frames, path, scale=6, ms=150, bg=(96, 84, 110)):
    out = []
    for f in frames:
        img = Image.new('RGBA', f.size, (*bg, 255))
        img.alpha_composite(f)
        out.append(img.convert('RGB').resize((f.width * scale, f.height * scale), Image.NEAREST))
    out[0].save(path, save_all=True, append_images=out[1:], duration=ms, loop=0)


if __name__ == '__main__':
    import os
    os.makedirs('out', exist_ok=True)
    sheet, rows = sprite_sheet()
    sheet.save('out/hero_sheet.png')
    for v, a, frames in rows:
        print(f'{v:6s} {a:7s} {len(frames)} frame(s)')
        if len(frames) > 1:
            save_gif(frames, f'out/hero_{v}_{a}.gif', ms=300 if a in ('pickup', 'use') else 150)

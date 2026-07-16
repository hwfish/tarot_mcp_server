"""Tarot MCP Server
A Model Context Protocol server that shuffles and draws tarot cards.

Tools:
  - draw_cards(count, allow_reversed): draw N random cards as JSON
  - draw_spread(spread, allow_reversed): draw a preset spread with named positions
  - list_spreads(): list available preset spreads

Every drawn card includes a `meaning` field: a short keyword interpretation
that ALREADY matches the card's orientation (upright or reversed).

Run (streamable HTTP):
  python tarot_server.py
  py tarot_server.py
  python3 tarrot_server.py
  # serves MCP at http://0.0.0.0:7878/mcp
"""

import json
import random
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("tarot", host="0.0.0.0", port=7878, streamable_http_path="/tarot_mcp")  # port 7878, 78 cards in the deck :)

# meanings list
# name: (upright meaning, reversed meaning)

MEANINGS = {
    # Major Arcana
    "The Fool": ("new beginnings, spontaneity, a leap of faith",
                 "recklessness, hesitation, poor judgment"),
    "The Magician": ("manifestation, skill, resourcefulness",
                     "manipulation, untapped talent, trickery"),
    "The High Priestess": ("intuition, inner voice, hidden knowledge",
                           "ignored intuition, secrets, confusion"),
    "The Empress": ("abundance, nurturing, creativity",
                    "dependence, smothering, creative block"),
    "The Emperor": ("authority, structure, stability",
                    "tyranny, rigidity, loss of control"),
    "The Hierophant": ("tradition, guidance, shared values",
                       "rebellion, unconventional paths, dogma questioned"),
    "The Lovers": ("love, alignment, meaningful choices",
                   "disharmony, misaligned values, avoidance of choice"),
    "The Chariot": ("willpower, victory, determination",
                    "lack of direction, aggression, stalled momentum"),
    "Strength": ("courage, compassion, quiet inner strength",
                 "self-doubt, weakness, raw emotion untamed"),
    "The Hermit": ("introspection, solitude, inner guidance",
                   "isolation, loneliness, withdrawal taken too far"),
    "Wheel of Fortune": ("change, cycles, a turn of luck",
                         "bad luck, resistance to change, broken cycles"),
    "Justice": ("fairness, truth, accountability",
                "unfairness, dishonesty, avoiding consequences"),
    "The Hanged Man": ("surrender, pause, a new perspective",
                       "stalling, needless sacrifice, fear of letting go"),
    "Death": ("endings, transformation, necessary transition",
              "resistance to change, stagnation, clinging to the past"),
    "Temperance": ("balance, moderation, patience",
                   "imbalance, excess, lack of long-term vision"),
    "The Devil": ("attachment, addiction, self-imposed restriction",
                  "release, breaking free, reclaiming power"),
    "The Tower": ("sudden upheaval, revelation, collapse of the false",
                  "disaster averted, fear of change, delayed reckoning"),
    "The Star": ("hope, renewal, quiet inspiration",
                 "discouragement, lost faith, disconnection"),
    "The Moon": ("illusion, uncertainty, the subconscious surfacing",
                 "clarity emerging, fear released, truth revealed"),
    "The Sun": ("success, joy, vitality",
                "temporary setback, dimmed optimism, delayed success"),
    "Judgement": ("awakening, reckoning, answering an inner call",
                  "self-doubt, harsh self-judgment, ignoring the call"),
    "The World": ("completion, achievement, wholeness",
                  "incompletion, loose ends, delayed closure"),
    # Wands
    "Ace of Wands": ("inspiration, a spark, new opportunity",
                     "delays, false starts, creative block"),
    "Two of Wands": ("planning, future vision, first steps abroad",
                     "fear of change, indecision, playing it safe"),
    "Three of Wands": ("expansion, foresight, momentum",
                       "obstacles, delays, limited vision"),
    "Four of Wands": ("celebration, homecoming, stability",
                      "transition, instability, canceled festivities"),
    "Five of Wands": ("competition, friction, testing ideas",
                      "conflict avoidance, tension released, inner strife"),
    "Six of Wands": ("victory, recognition, public success",
                     "ego, fall from grace, unearned praise"),
    "Seven of Wands": ("defense, standing your ground, perseverance",
                       "overwhelm, giving up, feeling outnumbered"),
    "Eight of Wands": ("swift action, momentum, news arriving",
                       "delays, frustration, scattered energy"),
    "Nine of Wands": ("resilience, last stand, guarded persistence",
                      "burnout, paranoia, defenses worn thin"),
    "Ten of Wands": ("burden, heavy responsibility, carrying too much",
                     "release, delegation, putting the load down"),
    "Page of Wands": ("enthusiasm, exploration, a fresh idea",
                      "lack of direction, procrastination, fizzled spark"),
    "Knight of Wands": ("energy, passion, bold pursuit",
                        "haste, recklessness, scattered drive"),
    "Queen of Wands": ("confidence, warmth, magnetic determination",
                       "insecurity, jealousy, demanding moods"),
    "King of Wands": ("leadership, vision, entrepreneurial fire",
                      "impulsiveness, domineering behavior, hollow bravado"),
    # Cups
    "Ace of Cups": ("new feelings, emotional opening, compassion",
                    "blocked emotions, emptiness, love withheld"),
    "Two of Cups": ("partnership, mutual attraction, union",
                    "imbalance, tension, a bond breaking"),
    "Three of Cups": ("friendship, celebration, community",
                      "gossip, isolation, overindulgence"),
    "Four of Cups": ("apathy, contemplation, missed offers",
                     "renewed motivation, acceptance, re-engagement"),
    "Five of Cups": ("loss, grief, dwelling on regret",
                     "acceptance, moving on, finding what remains"),
    "Six of Cups": ("nostalgia, childhood memories, innocence",
                    "stuck in the past, outgrown comforts"),
    "Seven of Cups": ("choices, fantasy, wishful thinking",
                      "clarity, sober choice, illusions dispersing"),
    "Eight of Cups": ("walking away, seeking deeper meaning",
                      "fear of moving on, aimless drifting, one more try"),
    "Nine of Cups": ("contentment, satisfaction, a wish fulfilled",
                     "dissatisfaction, greed, hollow pleasure"),
    "Ten of Cups": ("emotional fulfillment, family harmony, lasting joy",
                    "disconnection, family strain, broken ideals"),
    "Page of Cups": ("curiosity, an emotional message, gentle surprise",
                     "emotional immaturity, moodiness, blocked creativity"),
    "Knight of Cups": ("romance, charm, an idealistic offer",
                       "moodiness, unrealistic promises, disappointment"),
    "Queen of Cups": ("compassion, emotional security, deep empathy",
                      "emotional overwhelm, neediness, martyrdom"),
    "King of Cups": ("emotional balance, diplomacy, calm counsel",
                     "manipulation, coldness, repressed feeling"),
    # Swords
    "Ace of Swords": ("clarity, breakthrough, a sharp truth",
                      "confusion, misused intellect, a truth that cuts"),
    "Two of Swords": ("stalemate, a difficult decision, blocked vision",
                      "indecision breaking, information revealed"),
    "Three of Swords": ("heartbreak, sorrow, painful truth",
                        "healing, forgiveness, releasing pain"),
    "Four of Swords": ("rest, recovery, deliberate retreat",
                       "burnout, restlessness, rest refused"),
    "Five of Swords": ("conflict, hollow victory, winning at a cost",
                       "reconciliation, lingering resentment, making amends"),
    "Six of Swords": ("transition, moving toward calmer waters",
                      "resistance to change, unfinished business"),
    "Seven of Swords": ("deception, strategy, acting alone",
                        "confession, coming clean, a plan exposed"),
    "Eight of Swords": ("restriction, self-imposed limits, feeling trapped",
                        "freedom, new perspective, self-release"),
    "Nine of Swords": ("anxiety, sleepless worry, dread",
                       "hope returning, worries released, perspective"),
    "Ten of Swords": ("painful ending, rock bottom, betrayal",
                      "recovery, the worst is over, slow rise"),
    "Page of Swords": ("curiosity, vigilance, candid questions",
                       "gossip, hasty words, scattered thinking"),
    "Knight of Swords": ("ambition, direct action, charging ahead",
                         "recklessness, aggression, burning out fast"),
    "Queen of Swords": ("clear judgment, independence, honest boundaries",
                        "coldness, bitterness, cutting words"),
    "King of Swords": ("intellect, authority, impartial truth",
                       "abuse of power, manipulation, cold logic"),
    # Pentacles
    "Ace of Pentacles": ("new opportunity, prosperity, solid ground",
                         "missed opportunity, shaky foundations"),
    "Two of Pentacles": ("balance, juggling priorities, adaptability",
                         "overcommitment, disorganization, dropped balls"),
    "Three of Pentacles": ("teamwork, craftsmanship, learning together",
                           "poor collaboration, misaligned goals"),
    "Four of Pentacles": ("security, saving, holding on",
                          "greed, fear of loss, or finally letting go"),
    "Five of Pentacles": ("hardship, scarcity, feeling left out",
                          "recovery, aid arriving, hardship easing"),
    "Six of Pentacles": ("generosity, giving and receiving, fair exchange",
                         "strings attached, inequality, one-sided giving"),
    "Seven of Pentacles": ("patience, long-term view, assessing growth",
                           "impatience, wasted effort, poor returns"),
    "Eight of Pentacles": ("diligence, skill-building, honest work",
                           "perfectionism, tedium, cutting corners"),
    "Nine of Pentacles": ("independence, self-earned comfort, refinement",
                          "overdependence, superficial luxury, overwork"),
    "Ten of Pentacles": ("legacy, family wealth, lasting stability",
                         "family disputes, instability, short-term thinking"),
    "Page of Pentacles": ("ambition, new studies, a practical start",
                          "procrastination, lack of progress, distraction"),
    "Knight of Pentacles": ("reliability, steady work, methodical progress",
                            "stagnation, tedium, stubborn routine"),
    "Queen of Pentacles": ("practicality, nurturing abundance, groundedness",
                           "work-life imbalance, self-neglect, materialism"),
    "King of Pentacles": ("wealth, business mastery, dependable success",
                          "greed, materialism, rigid control"),
}

# deck

MAJOR = [
    "The Fool", "The Magician", "The High Priestess", "The Empress",
    "The Emperor", "The Hierophant", "The Lovers", "The Chariot",
    "Strength", "The Hermit", "Wheel of Fortune", "Justice",
    "The Hanged Man", "Death", "Temperance", "The Devil",
    "The Tower", "The Star", "The Moon", "The Sun",
    "Judgement", "The World",
]

SUITS = ["Wands", "Cups", "Swords", "Pentacles"]
RANKS = [
    "Ace", "Two", "Three", "Four", "Five", "Six", "Seven",
    "Eight", "Nine", "Ten", "Page", "Knight", "Queen", "King",
]


def build_deck():
    deck = [
        {"name": name, "arcana": "major", "number": i, "suit": None}
        for i, name in enumerate(MAJOR)
    ]
    deck += [
        {
            "name": f"{rank} of {suit}",
            "arcana": "minor",
            "number": None,
            "suit": suit.lower(),
        }
        for suit in SUITS
        for rank in RANKS
    ]
    return deck


DECK = build_deck()  # 78 cards
assert all(c["name"] in MEANINGS for c in DECK), "every card needs a meaning"

# spreads

SPREADS = {
    "single": {
        "description": "One card for a quick daily reading.",
        "positions": ["insight"],
    },
    "three_card": {
        "description": "Classic three-card spread: past, present, future.",
        "positions": ["past", "present", "future"],
    },
    "situation_action_outcome": {
        "description": "Three cards: the situation, suggested action, likely outcome.",
        "positions": ["situation", "action", "outcome"],
    },
    "cross_four": { # cyberpunk 2077 style
        "description": "Four-card cross: current state, obstacle, core issue, advice.",
        "positions": ["current_state", "obstacle", "core_issue", "advice"],
    },
    "celtic_cross": {
        "description": "Full ten-card Celtic Cross for deep analysis of one question.",
        "positions": [
            "present", "challenge", "subconscious", "past",
            "conscious_goal", "near_future", "self", "environment",
            "hopes_and_fears", "outcome",
        ],
    },
}

MEANING_NOTE = (
    "Each card's `meaning` field is already matched to its `orientation` "
    "(upright or reversed). Use it as-is; do NOT invert or re-derive it."
)


def _draw(n: int, allow_reversed: bool):
    cards = random.sample(DECK, n)
    result = []
    for c in cards:
        card = dict(c)
        upright, reversed_ = MEANINGS[card["name"]]
        if allow_reversed and random.random() < 0.5:
            card["orientation"] = "reversed"
            card["meaning"] = reversed_
        else:
            card["orientation"] = "upright"
            card["meaning"] = upright
        result.append(card)
    return result


# ---------------------------------------------------------------- tools

@mcp.tool()
def draw_cards(count: int = 1, allow_reversed: bool = True) -> str:
    """Shuffle a full 78-card tarot deck and draw `count` cards without
    replacement. Returns JSON with each card's name, arcana, suit,
    orientation (upright/reversed), and `meaning`.

    IMPORTANT: the `meaning` string is ALREADY adjusted for the card's
    orientation. If orientation is "reversed", the meaning shown IS the
    reversed meaning — do not invert it again.

    Args:
        count: number of cards to draw (1-78)
        allow_reversed: if false, all cards are upright
    """
    if not 1 <= count <= 78:
        return json.dumps({"error": "count must be between 1 and 78"})
    return json.dumps(
        {"count": count, "note": MEANING_NOTE, "cards": _draw(count, allow_reversed)},
        indent=2,
    )


@mcp.tool()
def draw_spread(spread: str = "three_card", allow_reversed: bool = True) -> str:
    """Draw a preset tarot spread. Each card is tagged with its position
    meaning (e.g. past/present/future) and includes a `meaning` field.

    IMPORTANT: the `meaning` string is ALREADY adjusted for the card's
    orientation. If orientation is "reversed", the meaning shown IS the
    reversed meaning — do not invert it again. Interpret each card in the
    context of its `position`.

    Args:
        spread: one of the preset spread names, e.g. "single", "three_card",
            "situation_action_outcome", "cross_four", "celtic_cross"
        allow_reversed: if false, all cards are upright
    """
    key = spread.strip().lower()
    if key not in SPREADS:
        return json.dumps(
            {"error": f"unknown spread '{spread}'", "available": list(SPREADS)}
        )
    positions = SPREADS[key]["positions"]
    cards = _draw(len(positions), allow_reversed)
    for pos, card in zip(positions, cards):
        card["position"] = pos
    return json.dumps(
        {
            "spread": key,
            "description": SPREADS[key]["description"],
            "note": MEANING_NOTE,
            "cards": cards,
        },
        indent=2,
    )


@mcp.tool()
def list_spreads() -> str:
    """List all available preset spreads with their positions."""
    return json.dumps(SPREADS, indent=2)


if __name__ == "__main__":
    # Long-running HTTP server, endpoint: http://<server>:7878/mcp
    mcp.run(transport="streamable-http")
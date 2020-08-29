from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

# Exclusive Or
def XOr(x, y):
    return And(Or(x, y), Not(And(x, y)))

def KnightKnaveKnowledge(KnightCharacter, KnaveCharacter, knowledge):
    return And(Implication(KnightCharacter, knowledge),
               Implication(KnaveCharacter, Not(knowledge)))

# Puzzle 0
# A says "I am both a knight and a knave."
knowledge0 = And(
    #XOR: A cannot be a knight or a knave, but not both
    XOr(AKnave, AKnight),
    #Puzzle specific information
    KnightKnaveKnowledge(AKnight, AKnave, And(AKnave, AKnight))
)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
knowledge1 = And(
    XOr(AKnave, AKnight),
    XOr(BKnave, BKnight),

    KnightKnaveKnowledge(AKnight, AKnave, And(AKnave, BKnave))
)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
knowledge2 = And(
    XOr(AKnave, AKnight),
    XOr(BKnave, BKnight),

    KnightKnaveKnowledge(AKnight, AKnave, XOr(And(AKnave, BKnave), And(AKnight, BKnight))),
    KnightKnaveKnowledge(BKnight, BKnave, XOr(And(AKnave, BKnight), And(AKnight, AKnave)))
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
knowledge3 = And(
    XOr(AKnight, AKnave),
    XOr(BKnight, BKnave),
    XOr(CKnight, CKnave),

    KnightKnaveKnowledge(AKnight, AKnave, XOr(AKnight, AKnave)),
    KnightKnaveKnowledge(BKnight, BKnave, KnightKnaveKnowledge(AKnight, AKnave, AKnave)),
    KnightKnaveKnowledge(BKnight, BKnave, CKnave),
    KnightKnaveKnowledge(CKnight, CKnave, AKnight)
)


def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()

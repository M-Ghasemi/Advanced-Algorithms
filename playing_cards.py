"""
Mohammad Sadegh Ghasemi

Penn and Teller have a special deck of fifty-two cards,
with no face cards and nothing but clubs-
the ace, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, . . . , 52 of clubs.
(They're big cards.) Penn shuffles the deck until each each of the
52! possible orderings of the cards is equally likely.
He then takes cards one at a time from the top of the deck and gives
them to Teller, stopping as soon as he gives Teller the five of clubs.
(a) On average, how many cards does Penn give Teller?
(b) On average, what is the smallest-numbered card that Penn gives Teller?
(c) On average, what is the largest-numbered card that Penn gives Teller?
"""
__author__ = "Mohammad Sadegh Ghasemi"
__date__ = "2018-01-19"

import random

n = 10000
idx_min_max = [0, 0, 0]

for i in range(n):
    cards = list(range(1, 53))
    minimum = 54
    maximum = 0

    for j in range(1, 53):
        card = random.choice(cards)
        cards.remove(card)
        minimum = min(card, minimum)
        maximum = max(card, maximum)
        if card == 3:
            idx_min_max[0] += j
            idx_min_max[1] += minimum
            idx_min_max[2] += maximum
            break

print(
    'The average of {} runs:\n'
    '(a): {}\n'
    '(b): {}\n'
    '(c): {}\n'.format(
        n,
        idx_min_max[0] / n,
        idx_min_max[1] / n,
        idx_min_max[2] / n
    )
)

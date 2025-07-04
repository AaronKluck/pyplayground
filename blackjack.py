from random import randint

# Comment these out for random seed
from random import seed

seed(999)


def shuffle(cards: list[int]):
    for i in range(len(cards) - 1, 0, -1):
        j = randint(0, i)
        cards[i], cards[j] = cards[j], cards[i]


def unshuffled_deck() -> list[int]:
    return [11, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10] * 4


class Bust(RuntimeError):
    pass


class PlayerBust(Bust):
    pass


class DealerBust(Bust):
    pass


class BlackjackState:

    def __init__(self):
        self.reset()

    @property
    def player_hand(self) -> list[int]:
        return [*self._player_hand]

    @property
    def player_total(self) -> int:
        return sum(self._player_hand)

    @property
    def dealer_hand(self) -> list[int | str]:
        if self._revealed:
            return [*self._dealer_hand]
        return ["?"] + self._dealer_hand[1:]

    @property
    def dealer_total(self) -> int:
        assert self._revealed
        return sum(self._dealer_hand)

    def reset(self):
        self.deck = unshuffled_deck()
        shuffle(self.deck)

        self._player_hand: list[int] = []
        self._dealer_hand: list[int] = []
        self._revealed = False
        self._stayed = False
        self._gameover = False

    def deal(self):
        assert not self._player_hand and not self._dealer_hand
        self._player_hand.append(self.deck.pop())
        self._dealer_hand.append(self.deck.pop())
        self._player_hand.append(self.deck.pop())
        self._dealer_hand.append(self.deck.pop())

    def player_hit(self):
        assert not self._gameover
        assert not self._stayed
        assert self._player_hand
        try:
            hit_val = self._hit(self._player_hand)
            print(f"Player hit {hit_val}")
        except Bust as b:
            self._gameover = True
            raise PlayerBust(str(b))

    def dealer_hit(self):
        assert not self._gameover
        assert self._stayed
        try:
            hit_val = self._hit(self._dealer_hand)
            print(f"Delaer hit {hit_val}")
        except Bust as b:
            self._gameover = True
            raise DealerBust(str(b))

    def player_stay(self):
        assert not self._gameover
        assert not self._stayed
        assert self._player_hand
        self._stayed = True
        self._revealed = True
        print(f"Player stays ({self.player_total})")

    def check_dealer_blackjack(self):
        assert len(self.player_hand) == 2 and len(self.dealer_hand) == 2
        if sum(self._dealer_hand) == 21:
            self._gameover = True
            return True
        return False

    def print_state(self):
        print("=" * 80)
        print(
            f"Dealer: {self.dealer_hand}"
            + (f" ({self.dealer_total})" if self._revealed else "")
        )
        print(
            f"Player: {self.player_hand} ({self.player_total})"
            + (" stayed" if self._stayed else "")
        )

    def _hit(self, hand: list[int]) -> int:
        next_card = self.deck.pop()
        hand.append(next_card)
        total = sum(hand)
        if total >= 21:
            try:
                ace_idx = hand.index(11)
                hand[ace_idx] = 1
                total -= 10
            except ValueError:
                self._gameover = True
                raise Bust(f"Hit {next_card}, total {total}")
        return next_card


if __name__ == "__main__":

    b = BlackjackState()
    try:
        b.print_state()
        b.deal()
        b.print_state()
        if b.check_dealer_blackjack():
            print("PLAYER BUSTED, DEALER WINS")

        while b.player_total < 15:
            b.player_hit()
            b.print_state()
        b.player_stay()
        b.print_state()

    except PlayerBust as e:
        print(f"PLAYER BUSTED, DEALER WINS ({str(e)})")
    except DealerBust as e:
        print(f"DEALER BUSTED, PLAYER WINS ({str(e)})")

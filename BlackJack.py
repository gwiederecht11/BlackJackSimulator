import itertools, random


class Card:
    def __init__(self, value, suit=None):
        self.value = value
        self.suit = suit
    def print(self):
        if self.suit == None:
            print('(' + self.value + ')')
        else:
            print('(' + self.value + ', ' + self.suit + ')')

def create_deck():
    arr = []
    suit = ""
    for i in range(4):
        if i == 0:
            suit = "Hearts"
        elif i == 1:
            suit = "Clubs"
        elif i == 2:
            suit = "Spades"
        elif i == 3:
            suit = "Diamonds"
        for j in range(2, 15):
            if j <= 10:
                arr.append(Card(str(j), suit))
            else:
                if j == 11:
                    arr.append(Card('J', suit))
                if j == 12:
                    arr.append(Card('Q', suit))
                if j == 13:
                    arr.append(Card('K', suit))
                if j == 14:
                    arr.append(Card('A', suit))
    return arr

def print_deck():
    arr = []
    create_deck(arr)
    random.shuffle(arr)
    for card in arr:
        card.print()


def create_shoe(num_decks):
    arr = []
    for i in range(num_decks):
        arr += create_deck()
    return arr

def cut_shoe(shoe):
    num = random.uniform(0.3, 0.7)
    i = int(num * len(shoe))
    i = 0
    shoe = shoe[i: len(shoe)] + shoe[0: i]
    return shoe



#Players cards: [[], [], [], ...]
def initialize_players_cards(num_players):
    players_cards = []
    for i in range(num_players):
        players_cards.append([])
    return players_cards

#returns true if the list of cards contains an ace
def contains_ace(cards_list):
    for card in cards_list:
        if card.value == 'A':
            return True
    return False


#going to ignore Ace values for now. Just 2-K values
def card_value_string_to_num(card_value_str):
    if card_value_str == 'A':
        return 1
    if card_value_str == 'J' or card_value_str == 'Q' or card_value_str == 'K':
        return 10
    return int(card_value_str)



#if bust or blackjack, return true
#otherwise, return false
def is_over(players_cards):
    #soft hand
    total = 0
    if contains_ace(players_cards):
        ace_count = 0
        #first try to see if we have a soft 21
        for card in players_cards:
            if card.value == 'A':
                if ace_count == 0:
                    total += 11
                    ace_count += 1
                else:
                    total += 1
            else:
                total += card_value_string_to_num(card.value)
        if total == 21:
            return True
        if total < 21:
            return False

    total = 0
    #hard hand. treat all aces as 1s
    for card in players_cards:
        if card.value == 'A':
            total += 1
        else:
            total += card_value_string_to_num(card.value)

    if total >= 21:
        return True
    else:
        return False


def is_blackjack(actual_cards):
    total = 0
    if len(actual_cards) == 2 and contains_ace(actual_cards):
        for card in actual_cards:
            if card.value == 'A':
                total += 11
            else:
                total += card_value_string_to_num(card.value)
        if total == 21:
            return True
    return False


def is_bust(actual_cards):
    total = 0
    for card in actual_cards:
        if card.value == 'A':
            total += 1
        else:
            total += card_value_string_to_num(card.value)
    if total > 21:
        return True
    return False

def soft_and_hard_total(cards_list):
    soft_total = 0
    hard_total = 0
    ace_count = 0
    for card in cards_list:
        if card.value == 'A':
            if ace_count == 0:
                soft_total += 11
                ace_count += 1
            else:
                soft_total += 1
            hard_total += 1
        else:
            soft_total += card_value_string_to_num(card.value)
            hard_total += card_value_string_to_num(card.value)

    if ace_count == 0:
        soft_total = 0

    return soft_total, hard_total



def compare_hands(actual_cards, dealer_total):
    #calculate our hand (soft and hard)
    soft_total, hard_total = soft_and_hard_total(actual_cards)
    actual_total = 0
    if soft_total > hard_total and soft_total <= 21:
        actual_total = soft_total
    elif hard_total > soft_total and hard_total <= 21:
        actual_total = hard_total
    elif soft_total == hard_total and soft_total <= 21:
        actual_total = soft_total

    if dealer_total > actual_total:
        return 1
    elif dealer_total == actual_total:
        return 0
    return -1



def split_case(players_cards, dealers_cards):
    pass


def calculate_hard_total(cards_list):
    total = 0
    for card in cards_list:
        if card.value == 'A':
            total += 1
        else:
            total += card_value_string_to_num(card.value)
    return total


def draw_rest_of_dealers_cards_two(dealers_cards, curr_card_index, new_shoe, hit_soft_seventeen):
    soft_total, hard_total = soft_and_hard_total(dealers_cards)
    if soft_total == 17 and not hit_soft_seventeen:
        return 17, curr_card_index

    curr_total = 0
    ace_count = 0
    if soft_total > 0:
        ace_count += 1
        curr_total = soft_total
    else:
        curr_total = hard_total

    while curr_total < 17:
        next_card = new_shoe[curr_card_index]
        dealers_cards.append(next_card)
        curr_card_index += 1
        if next_card.value == 'A':
            if ace_count == 0:
                ace_count += 1
                curr_total += 11
            else:
                curr_total += 1
        else:
            curr_total += card_value_string_to_num(next_card.value)

    if curr_total <= 21:
        #got a soft 17, hit if we're playing H17
        if curr_total == 17 and ace_count > 0:
            if hit_soft_seventeen:
                next_card = new_shoe[curr_card_index]
                curr_card_index += 1
                dealers_cards.append(next_card)
                if next_card.value == 'A':
                   curr_total += 1
                else:
                    curr_total += card_value_string_to_num(next_card.value)

        return curr_total, curr_card_index

    #busted
    if curr_total > 21 and ace_count == 0:
        return curr_total, curr_card_index

    if ace_count > 0:
        curr_total = soft_and_hard_total(dealers_cards)[1]
        while curr_total < 17:
            next_card = new_shoe[curr_card_index]
            dealers_cards.append(next_card)
            curr_card_index += 1
            if next_card.value == 'A':
                curr_total += 1
            else:
                curr_total += card_value_string_to_num(next_card.value)

    return curr_total, curr_card_index


print(soft_and_hard_total([Card('A'), Card('A'), Card('10'), Card('J')]))

def find_best_action(actual_cards, dealer_first_card, has_surrender, true_count):
    soft_total, hard_total = soft_and_hard_total(actual_cards)

    #split hands case
    if len(actual_cards) == 2 and card_value_string_to_num(actual_cards[0].value) == card_value_string_to_num(actual_cards[1].value):
        pass


    #Soft hands case
    if soft_total > 0 and soft_total <= 21:
        pass

    #hard hands case
    else:
        if hard_total >= 17:
            return 'Stand'
        if hard_total == 16:
            pass


def compute_true_count(shoe, curr_card_index, num_decks):
    pass




#returns a tuple of (new_card_index, how much won or lost (positive or negative))
def play_optimally(actual_cards, curr_card_index, new_shoe, dealers_cards, bet, is_three_to_two, hit_soft_seventeen, has_surrender, num_decks):
    arr = []
    stand = False
    surrender = False
    double = False

    #We go first. While we don't go over 21 or don't have a blackjack
    while not is_over(actual_cards, dealers_cards) and not stand:
        if split_case(actual_cards, dealers_cards):
            split_card_one = [actual_cards[0]]
            split_card_two = [actual_cards[1]]
            new_card_index_one, split_one_total =  play_optimally(split_card_one, curr_card_index, new_shoe, dealers_cards, bet, is_three_to_two)
            new_card_index_two, split_two_total =  play_optimally(split_card_two, curr_card_index, new_shoe, dealers_cards, bet, is_three_to_two)
            new_total = split_one_total + split_two_total
            #combine and return the result
            if new_card_index_one > new_card_index_two:
                return new_card_index_one, new_total
            else:
                return new_card_index_two, new_total


        else:
            true_count = compute_true_count(new_shoe, curr_card_index, num_decks)
            action = find_best_action(actual_cards, dealers_cards[0], has_surrender, true_count)




    #case for we got a blackjack
    if is_blackjack(actual_cards):
        #push since both of us have a blackjack
        if is_blackjack(dealers_cards):
            #TODO: IMPLEMENT this part
            return curr_card_index, 0

        amount_won = 0
        if is_three_to_two:
            amount_won = int(1.5 * bet)
            return curr_card_index, amount_won
        else:
            amount_won = int(1.2 * bet)
            return curr_card_index, amount_won

    #Case for we busted
    if is_bust(actual_cards):
        return curr_card_index, -bet

    #Dealer draws until bust or till 17 (account for H17 or S17 game)
    dealer_total, curr_card_index = draw_rest_of_dealers_cards_two(dealers_cards, curr_card_index, new_shoe, hit_soft_seventeen)


    #Case for dealer busted
    if dealer_total > 21:
        return curr_card_index, bet


    #Handling dealer better hand than us, dealer worse hand than us, or equal hands so push
    compare_hands_value = compare_hands(actual_cards, dealer_total)
    if compare_hands_value > 0:
        return curr_card_index, -bet
    elif compare_hands_value < 0:
        return curr_card_index, bet
    else:
        return curr_card_index, 0





def run_simulation(num_times, bankroll, min_bet, max_bet, is_three_to_two, num_decks, hit_soft_seventeen, has_surrender, shoe_penetration, num_players):
    # Going to play a game of blackjack num_times amount of times and see what our winnings or losses are at the end of it
    # Start with bankroll amount of money
    shoe = create_shoe(num_decks)



    for i in range(num_times):
        # Play one game of n-deck blackjack based on num_decks
        true_count = 0
        random.shuffle(shoe)
        shoe = cut_shoe(shoe)
        new_shoe = shoe[1: len(shoe)]
        till_index = shoe_penetration * len(shoe)
        curr_card_index = 0
        players_cards = initialize_players_cards(num_players)
        dealers_cards = []

        while curr_card_index != till_index:

            #place bets
            #some method here to determine what bet to place for our player
            bet = 0


            #Deal the cards out to players and dealer
            for j in range(2):
                #deal every player one card
                for i in range(num_players):
                    players_cards[i].append(new_shoe[curr_card_index])
                    curr_card_index += 1

                #dealer gets a card
                dealers_cards.append(new_shoe[curr_card_index])
                curr_card_index += 1


            #assume we are the first player to act, the rest of the players are bots
            for i in range(num_players):
                actual_cards = players_cards[i]
                if i == 0:
                    play_optimally(actual_cards, curr_card_index, new_shoe, dealers_cards, bet, is_three_to_two, hit_soft_seventeen, has_surrender, num_decks)
                else:
                    pass
                    #play_normal()





########TESTS########
shoe = [Card('J', 'Clubs'), Card('A', 'Diamonds'), Card('5', 'Clubs')]
shoe = [Card('A'), Card('10'), Card('5')]
dealers_cards = [Card('A', 'Diamonds'), Card('5')]


def test_drawing_dealers_cards():
    #print(draw_rest_of_dealers_cards(dealers_cards, 0, shoe, True))

    for i in range(10):
        test_shoe = []
        test_dealers_cards = []
        for j in range(10):
            random_int = random.randint(1, 13)
            if random_int == 1:
                c = Card('A')
            elif random_int == 11:
                c = Card('J')
            elif random_int == 12:
                c = Card('Q')
            elif random_int == 13:
                c = Card('K')
            else:
                c = Card(str(random_int))
            test_shoe.append(c)

        for k in range(2):
            random_int = random.randint(1, 13)
            if i % 2 == 0 and k == 0:
                c = Card('A')
                test_dealers_cards.append(c)
                continue
            if random_int == 1:
                c = Card('A')
            elif random_int == 11:
                c = Card('J')
            elif random_int == 12:
                c = Card('Q')
            elif random_int == 13:
                c = Card('K')
            else:
                c = Card(str(random_int))
            test_dealers_cards.append(c)

        print('Printing Test Shoe')
        for card in test_shoe:
            card.print()
        print()
        print('Printing Test Dealers Cards')
        for card in test_dealers_cards:
            card.print()
        print()

        print('Result: ', draw_rest_of_dealers_cards_two(test_dealers_cards, 0, test_shoe, True))
        print()


















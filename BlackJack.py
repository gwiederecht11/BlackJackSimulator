import itertools, random, math


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



#initializes a dictionary of all the basic strategy plays.
#Follows format example: ('Soft'/'Hard'/'Pair', Has_surrender (boolean), Our total, Dealer Card) --> 'Hit'/'Stand'/'Double'/Split'/'Surrender'

#Not working : (hard, true, 5, 'J')


def initialize_basic_strategy(dict):
    #initialize hard hands strategy
    for our_total in range(5, 22):

        for dealer_card in range(1, 14):
            if our_total == 16 and dealer_card == 13:
                print('hello')

            if dealer_card == 1:
                dealer_card = 'A'
            elif dealer_card == 11:
                dealer_card = 'J'
            elif dealer_card == 12:
                dealer_card = 'Q'
            elif dealer_card == 13:
                dealer_card = 'K'
            else:
                dealer_card = str(dealer_card)

            #Jack, Queen, King = 10.
            #Ace = 1
            #Everything else is their corresponding number
            dealer_card_int_value = card_value_string_to_num(dealer_card)

            if our_total >= 17:
                dict[('Hard', True, our_total, dealer_card)] = 'Stand'

            elif our_total == 16:
                if dealer_card == '9' or dealer_card == 'A':
                    dict[('Hard', True, our_total, dealer_card)] = 'Surrender'
                    dict[('Hard', False, our_total, dealer_card)] = 'Hit'
                elif dealer_card_int_value == 10:
                    dict[('Hard', True, our_total, dealer_card)] = 'Surrender'
                    dict[('Hard', False, our_total, dealer_card)] = 'Stand'
                elif dealer_card == '7' or dealer_card == '8':
                    dict[('Hard', True, our_total, dealer_card)] = 'Hit'

                elif dealer_card_int_value >= 2 and dealer_card_int_value <= 6:
                    dict[('Hard', True, our_total, dealer_card)] = 'Stand'

            elif our_total >= 12 and our_total <= 15:
                if dealer_card == 'A':
                    dict[('Hard', True, our_total, dealer_card)] = 'Hit'

                elif dealer_card_int_value >= 7 and dealer_card_int_value <= 10:
                    #our total is 15. Edge case
                    if our_total == 15 and dealer_card_int_value == 10:
                        dict[('Hard', True, our_total, dealer_card)] = 'Surrender'
                        dict[('Hard', False, our_total, dealer_card)] = 'Hit'

                    else:
                        dict[('Hard', True, our_total, dealer_card)] = 'Hit'

                elif dealer_card_int_value >= 2 and dealer_card_int_value <= 6:
                    #our total is 12. Edge case
                    if our_total == 12 and (dealer_card_int_value == 2 or dealer_card_int_value == 3):
                        dict[('Hard', True, our_total, dealer_card)] = 'Hit'

                    else:
                        dict[('Hard', True, our_total, dealer_card)] = 'Stand'

            elif our_total == 11:
                if dealer_card == 'A':
                    dict[('Hard', True, our_total, dealer_card)] = 'Hit'

                else:
                    dict[('Hard', True, our_total, dealer_card)] = 'Double'


            elif our_total == 10:
                if dealer_card == 'A' or dealer_card_int_value == 10:
                    dict[('Hard', True, our_total, dealer_card)] = 'Hit'

                else:
                    dict[('Hard', True, our_total, dealer_card)] = 'Double'


            elif our_total == 9:
                if dealer_card_int_value == 2 or dealer_card_int_value >= 7 and dealer_card_int_value <= 10 or dealer_card == 'A':
                    dict[('Hard', True, our_total, dealer_card)] = 'Hit'

                else:
                    dict[('Hard', True, our_total, dealer_card)] = 'Double'


            elif our_total >= 5 and our_total <= 8:
                dict[('Hard', True, our_total, dealer_card)] = 'Hit'



    #Initializing all of the soft hand strategies
    for our_total in range(13, 22):
        for dealer_card in range(1, 14):
            if dealer_card == 1:
                dealer_card = 'A'
            elif dealer_card == 11:
                dealer_card = 'J'
            elif dealer_card == 12:
                dealer_card = 'Q'
            elif dealer_card == 13:
                dealer_card = 'K'
            else:
                dealer_card = str(dealer_card)

            # Jack, Queen, King = 10.
            # Ace = 1
            # Everything else is their corresponding number
            dealer_card_int_value = card_value_string_to_num(dealer_card)

            if our_total >= 18:
                if our_total == 18:
                    if dealer_card == '9' or dealer_card_int_value == 10 or dealer_card == 'A':
                        dict[('Soft', True, our_total, dealer_card)] = 'Hit'

                    elif dealer_card_int_value >= 3 and dealer_card_int_value <= 6:
                        dict[('Soft', True, our_total, dealer_card)] = 'Double'

                    elif dealer_card == '2' or dealer_card == '7' or dealer_card == '8':
                        dict[('Soft', True, our_total, dealer_card)] = 'Stand'

                    else:
                        dict[('Soft', True, our_total, dealer_card)] = 'Hit'


                else:
                    dict[('Soft', True, our_total, dealer_card)] = 'Stand'


            elif our_total >= 13 and our_total <= 17:
                if our_total == 17:
                    if dealer_card_int_value >= 3 and dealer_card_int_value <= 6:
                        dict[('Soft', True, our_total, dealer_card)] = 'Double'

                    else:
                        dict[('Soft', True, our_total, dealer_card)] = 'Hit'


                elif our_total == 15 or our_total == 16:
                    if dealer_card_int_value >= 4 and dealer_card_int_value <= 6:
                        dict[('Soft', True, our_total, dealer_card)] = 'Double'

                    else:
                        dict[('Soft', True, our_total, dealer_card)] = 'Hit'


                elif our_total == 13 or our_total == 14:
                    if dealer_card_int_value >= 5 and dealer_card_int_value <= 6:
                        dict[('Soft', True, our_total, dealer_card)] = 'Double'

                    else:
                        dict[('Soft', True, our_total, dealer_card)] = 'Hit'


    #Initialize Pair hands strategy
    for pair_of in range(1, 11):
        for dealer_card in range(1, 14):
            if dealer_card == 1:
                dealer_card = 'A'
            elif dealer_card == 11:
                dealer_card = 'J'
            elif dealer_card == 12:
                dealer_card = 'Q'
            elif dealer_card == 13:
                dealer_card = 'K'
            else:
                dealer_card = str(dealer_card)

            # Jack, Queen, King = 10.
            # Ace = 1
            # Everything else is their corresponding number
            dealer_card_int_value = card_value_string_to_num(dealer_card)

            if pair_of == 1:
                dict[('Pair', True, pair_of, dealer_card)] = 'Split'

            elif pair_of == 10:
                dict[('Pair', True, pair_of, dealer_card)] = 'Stand'

            elif pair_of == 9:
                if dealer_card == '7' or dealer_card_int_value == 10 or dealer_card == 'A':
                    dict[('Pair', True, pair_of, dealer_card)] = 'Stand'
                else:
                    dict[('Pair', True, pair_of, dealer_card)] = 'Split'

            elif pair_of == 8:
                dict[('Pair', True, pair_of, dealer_card)] = 'Split'

            elif pair_of == 7 or pair_of == 6:
                if dealer_card == 'A':
                    dict[('Pair', True, pair_of, dealer_card)] = 'Hit'
                elif dealer_card_int_value >= 8 and dealer_card_int_value <= 10:
                    dict[('Pair', True, pair_of, dealer_card)] = 'Hit'
                elif dealer_card_int_value >= 2 and dealer_card_int_value <= 6:
                    dict[('Pair', True, pair_of, dealer_card)] = 'Split'
                elif pair_of == 7 and dealer_card == '7':
                    dict[('Pair', True, pair_of, dealer_card)] = 'Split'
                elif pair_of == 6 and dealer_card == '7':
                    dict[('Pair', True, pair_of, dealer_card)] = 'Hit'

            elif pair_of == 5:
                if dealer_card_int_value >= 2 and dealer_card_int_value <= 9:
                    dict[('Pair', True, pair_of, dealer_card)] = 'Double'
                else:
                    dict[('Pair', True, pair_of, dealer_card)] = 'Hit'
            elif pair_of == 4:
                if dealer_card == '5' or dealer_card == '6':
                    dict[('Pair', True, pair_of, dealer_card)] = 'Split'
                else:
                    dict[('Pair', True, pair_of, dealer_card)] = 'Hit'
            elif pair_of == 2 or pair_of == 3:
                if dealer_card == 'A':
                    dict[('Pair', True, pair_of, dealer_card)] = 'Hit'
                elif dealer_card_int_value >= 2 and dealer_card_int_value <= 7:
                    dict[('Pair', True, pair_of, dealer_card)] = 'Split'
                elif dealer_card_int_value >= 8 and dealer_card_int_value <= 10:
                    dict[('Pair', True, pair_of, dealer_card)] = 'Hit'




#factor in true count later for strategy deviations
def find_best_action(actual_cards, dealer_first_card, has_surrender, true_count, strategy_dict):
    soft_total, hard_total = soft_and_hard_total(actual_cards)
    dealer_card_value_str = dealer_first_card.value
    dealer_card_value_int = card_value_string_to_num(dealer_card_value_str)

    #split hands case
    if len(actual_cards) == 2 and card_value_string_to_num(actual_cards[0].value) == card_value_string_to_num(actual_cards[1].value):
        first_card = actual_cards[0]
        pair_of = card_value_string_to_num(first_card.value)
        return strategy_dict[('Pair', True, pair_of, dealer_card_value_str)]


    #Soft hands case
    if soft_total > 0 and soft_total <= 21:
        return strategy_dict[('Soft', True, soft_total, dealer_card_value_str)]

    #hard hands case
    else:
        if hard_total != 16 and hard_total != 15:
            has_surrender = True
        if hard_total == 16:
            if dealer_card_value_int >= 2 and dealer_card_value_int <= 8:
                has_surrender = True
        if hard_total == 15:
            if dealer_card_value_int != 10:
                has_surrender = True

        return strategy_dict[('Hard', has_surrender, hard_total, dealer_card_value_str)]


def compute_true_count(shoe, curr_card_index, num_decks):
    total_cards_in_shoe = 52 * num_decks

    #DOUBLE CHECK: that we want ceiling vs rounding a different way
    #num_decks left = ceil((total_cards_in_shoe - num_cards_gone_thru)/ 52)

    num_decks_left = math.ceil((total_cards_in_shoe - curr_card_index) / 52)

    count = 0
    for i in range(curr_card_index):
        card = shoe[i]
        card_value_int = card_value_string_to_num(card.value)
        if card_value_int >= 2 and card_value_int <= 6:
            count += 1
        elif card_value_int == 1 or card_value_int == 10:
            count -= 1

    return count / num_decks_left


def calc_better_total(actual_cards):
    soft_total, hard_total = soft_and_hard_total(actual_cards)
    curr_total = 0
    if soft_total == 0:
        curr_total = hard_total
    elif soft_total > hard_total and soft_total <= 21:
        curr_total = soft_total
    elif hard_total > soft_total and hard_total <= 21:
        curr_total = hard_total
    elif hard_total > 21 and soft_total > 21:
        curr_total = hard_total
    return curr_total





#return your new_card_index, your total (in terms of card value), surrender? True or False, doubled? True or False
# if it's a split case, will be (new_card_index, [total1, total2, ...], [surrender1, surrender2, ...], [double1, double2, ....]


#returns a tuple of (new_card_index, how much won or lost (positive or negative))
def play_optimally(actual_cards, curr_card_index, new_shoe, dealers_cards, bet, is_three_to_two, hit_soft_seventeen, has_surrender, num_decks):
    arr = []
    stand = False
    surrender = False
    double = False
    hit = False

    #We go first. While we don't go over 21 or don't have a blackjack
    while not is_over(actual_cards, dealers_cards) and not stand and not surrender and not double:
        if hit:
            next_card = new_shoe[curr_card_index]
            curr_card_index += 1
            actual_cards.append(next_card)
            hit = False

        if split_case(actual_cards, dealers_cards):
            split_card_one = [actual_cards[0]]
            split_card_two = [actual_cards[1]]
            new_card_index_one, split_one_totals, split_one_surrenders, split_one_doubles = play_optimally(split_card_one, curr_card_index, new_shoe, dealers_cards, bet, is_three_to_two)
            new_card_index_two, split_two_totals, split_two_surrenders, split_two_doubles =  play_optimally(split_card_two, curr_card_index, new_shoe, dealers_cards, bet, is_three_to_two)

            #Set the new card index
            if new_card_index_one > new_card_index_two:
                curr_card_index = new_card_index_one
            else:
                curr_card_index = new_card_index_two


            #had to split the first case, second case is not a split
            if isinstance(split_one_totals, list) and not isinstance(split_two_totals, list):
                totals = split_one_totals + [split_two_totals]
                surrenders = split_one_surrenders + [split_two_surrenders]
                doubles = split_one_doubles + [split_two_doubles]

            #had to split the second case, first case is not a split
            elif isinstance(split_two_totals, list) and not isinstance(split_one_totals, list):
                totals = [split_one_totals] + split_two_totals
                surrenders = [split_one_surrenders] + split_two_surrenders
                doubles = [split_one_doubles] + split_two_doubles

            #had to split both of them
            elif isinstance(split_one_totals, list) and isinstance(split_two_totals, list):
                totals = split_one_totals + split_two_totals
                surrenders = split_one_surrenders + split_two_surrenders
                doubles = split_one_doubles + split_two_doubles

            #no split
            else:
                totals = [split_one_totals, split_two_totals]
                surrenders = [split_one_surrenders, split_two_surrenders]
                doubles = [split_one_doubles, split_two_doubles]

            return curr_card_index, totals, surrenders, doubles



        else:
            true_count = compute_true_count(new_shoe, curr_card_index, num_decks)
            action = find_best_action(actual_cards, dealers_cards[0], has_surrender, true_count)
            if action == 'Stand':
                stand = True

            #Action should never be surrender if has_surrender is passed in as False
            elif action == 'Surrender':
                surrender = True

            elif action == 'Double':
                double = True

            elif action == 'Hit':
                hit = True


    #Double Case
    if double:
        #deal the player one more card
        next_card = new_shoe[curr_card_index]
        curr_card_index += 1
        actual_cards.append(next_card)
        curr_total = calc_better_total(actual_cards)
        return curr_card_index, curr_total, False, True


    #Surrender case
    if surrender:
        return curr_card_index, 0, True, False


    curr_total = calc_better_total(actual_cards)
    return curr_card_index, curr_total, False, False

    #
    # #case for we got a blackjack
    # if is_blackjack(actual_cards):
    #     #push since both of us have a blackjack
    #     if is_blackjack(dealers_cards):
    #         return curr_card_index,
    #
    #     if is_three_to_two:
    #         amount_won = int(1.5 * bet)
    #         return curr_card_index, amount_won
    #     else:
    #         amount_won = int(1.2 * bet)
    #         return curr_card_index, amount_won
    #
    # #Case for we busted
    # if is_bust(actual_cards):
    #     return curr_card_index, -bet



    # #Dealer draws until bust or till 17 (account for H17 or S17 game)
    # dealer_total, curr_card_index = draw_rest_of_dealers_cards_two(dealers_cards, curr_card_index, new_shoe, hit_soft_seventeen)
    #
    #
    # #Case for dealer busted
    # if dealer_total > 21:
    #     return curr_card_index, bet
    #
    #
    # #Handling dealer better hand than us, dealer worse hand than us, or equal hands so push
    # compare_hands_value = compare_hands(actual_cards, dealer_total)
    # if compare_hands_value > 0:
    #     return curr_card_index, -bet
    # elif compare_hands_value < 0:
    #     return curr_card_index, bet
    # else:
    #     return curr_card_index, 0




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

        while curr_card_index < till_index:

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
            #Can possibly change this, could be first, middle, or last to act?

            our_totals = None
            our_surrenders = None
            our_doubles = None

            for i in range(num_players):
                actual_cards = players_cards[i]

                if i == 0:
                    curr_card_index, totals, surrenders, doubles = play_optimally(actual_cards, curr_card_index, new_shoe, dealers_cards, bet, is_three_to_two, hit_soft_seventeen, has_surrender, num_decks)
                    our_totals = totals
                    our_surrenders = surrenders
                    our_doubles = doubles

                else:
                    pass
                    #Idea: Have this return Stand?, Bust? Blackjack?
                    #play_normal()



            #Now, after each player has gotten a chance to play, we figure out whether we had a blackjack, busted, or whether the dealer needs to deal
                # Consider all of the totals (this is if we split our bet)
                if isinstance(totals, list):
                    pass
                else:
                    # case for we got a blackjack
                    if is_blackjack(actual_cards):
                        # push since both of us have a blackjack
                        if is_blackjack(dealers_cards):
                            # TODO: Implement this part. It's a push.
                            pass
                        if is_three_to_two:
                            amount_won = int(1.5 * bet)
                            # TODO: implement. Blackjack and 3:2
                        else:
                            amount_won = int(1.2 * bet)
                            # TODO: implement. Blackjack and 6:5


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


def test_basic_strategy():
    d = {}
    initialize_basic_strategy(d)


    #test hard hands
    for i in range(100):
        has_surrender = True

        #get a random dealer card
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

        card_value_int = card_value_string_to_num(c.value)

        #get a random total for player
        random_total = random.randint(5, 21)

        if random_total != 16 and random_total != 15:
            has_surrender = True
        if random_total == 16:
            if card_value_int >= 2 and card_value_int <= 8:
                has_surrender = True
        if random_total == 15:
            if card_value_int != 10:
                has_surrender = True

        print('Hard')
        print('Our total: ', random_total)
        print('Dealer Card: ', c.value)
        print('Strategy Chosen: ', d[('Hard', has_surrender, random_total, c.value)])
        print()

        # Follows format example: ('Soft'/'Hard'/'Pair', Has_surrender (boolean), Our total, Dealer Card) --> 'Hit'/'Stand'/'Double'/Split'/'Surrender'

    print()
    print()
    print()

    #test soft hands

    for i in range(100):

        # get a random dealer card
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

        # get a random total for player
        random_total = random.randint(13, 21)

        print('Soft')
        print('Our total: ', random_total)
        print('Dealer Card: ', c.value)
        print('Strategy Chosen: ', d[('Soft', True, random_total, c.value)])
        print()

        # Follows format example: ('Soft'/'Hard'/'Pair', Has_surrender (boolean), Our total, Dealer Card) --> 'Hit'/'Stand'/'Double'/Split'/'Surrender'


    print()
    print()
    print()

    #test pairs
    for i in range(100):
        dealer_card = None
        player_value = 0
        # get a random dealer card
        for k in range(2):
            random_int = random.randint(1, 13)
            #Choosing a dealer card

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

            if k == 0:
                dealer_card = c
            else:
                player_value = card_value_string_to_num(c.value)

        print('Pair')
        print('We have a pair of : ', player_value)
        print('Dealer Card: ', dealer_card.value)
        print('Strategy Chosen: ', d[('Pair', True, player_value, dealer_card.value)])
        print()

def test_basic_strategy_2():
    d = {}
    initialize_basic_strategy(d)

    #test all hard hands
    for our_total in range(5, 22):
        for dealer_card in range(1, 14):
            has_surrender = False
            if dealer_card == 1:
                dealer_card = 'A'
            elif dealer_card == 11:
                dealer_card = 'J'
            elif dealer_card == 12:
                dealer_card = 'Q'
            elif dealer_card == 13:
                dealer_card = 'K'
            else:
                dealer_card = str(dealer_card)

            card_value_int = card_value_string_to_num(dealer_card)

            if our_total != 16 and our_total != 15:
                has_surrender = True
            if our_total == 16:
                if card_value_int >= 2 and card_value_int <= 8:
                    has_surrender = True
            if our_total == 15:
                if card_value_int != 10:
                    has_surrender = True


            # Jack, Queen, King = 10.
            # Ace = 1
            # Everything else is their corresponding number
            print('Hard')
            print('Our total: ', our_total)
            print('Dealer card: ', dealer_card)
            print('Strategy chosen: ', d[('Hard', has_surrender, our_total, dealer_card)])
            print()


    # test all soft hands
    for our_total in range(13, 22):
        for dealer_card in range(1, 14):
            if dealer_card == 1:
                dealer_card = 'A'
            elif dealer_card == 11:
                dealer_card = 'J'
            elif dealer_card == 12:
                dealer_card = 'Q'
            elif dealer_card == 13:
                dealer_card = 'K'
            else:
                dealer_card = str(dealer_card)

            # Jack, Queen, King = 10.
            # Ace = 1
            # Everything else is their corresponding number
            print('Soft')
            print('Our total: ', our_total)
            print('Dealer card: ', dealer_card)
            print('Strategy chosen: ', d[('Soft', True, our_total, dealer_card)])
            print()


    # test all pair hands
    for pair_of in range(1, 11):
        for dealer_card in range(1, 14):
            if dealer_card == 1:
                dealer_card = 'A'
            elif dealer_card == 11:
                dealer_card = 'J'
            elif dealer_card == 12:
                dealer_card = 'Q'
            elif dealer_card == 13:
                dealer_card = 'K'
            else:
                dealer_card = str(dealer_card)

            # Jack, Queen, King = 10.
            # Ace = 1
            # Everything else is their corresponding number
            print('Pairs')
            print('Pair of: ', pair_of)
            print('Dealer card: ', dealer_card)
            print('Strategy chosen: ', d[('Pair', True, pair_of, dealer_card)])
            print()





test_basic_strategy_2()


















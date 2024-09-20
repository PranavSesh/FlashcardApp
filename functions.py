SIDE_DELIM = chr(287589)
CARD_DELIM = chr(249824)


def character_limit(entry_text, limit):
    if len(entry_text.get()) > 0:
        entry_text.set(entry_text.get()[:limit])


def card_extractor(card_string):
    if card_string == "None" or card_string is None:
        return []
    post_cards = []
    for card in card_string.split(CARD_DELIM):
        split_card = card.split(SIDE_DELIM)
        post_cards.append((split_card[0], split_card[1]))
    return post_cards


def card_class_to_list(card_list):
    final_list = []
    if len(card_list) > 0:
        for card in card_list:
            final_list.append((card.front_initial, card.back_initial))

    return final_list


def card_compressor(card_list):
    if len(card_list) == 0:
        return None
    pre_cards = []
    for card in card_list:
        pre_cards.append(card[0] + SIDE_DELIM + card[1])
    post = CARD_DELIM.join(pre_cards)
    return post




BOARD_URL = "https://api.trello.com/1/boards/{}/lists?key={}&token={}"
LIST_URL = "https://api.trello.com/1/lists/{}?fields=name&cards=open&card_fields=name&key={}&token={}"
ACTION_URL = "https://api.trello.com/1/cards/{}/actions?filter=updateCard:idList,createCard&fields=date&member_fields=initials&key={}&token={}"
TOKEN_URL = "https://trello.com/1/authorize?key={}&name=TrelloStats&expiration=never&response_type=token"
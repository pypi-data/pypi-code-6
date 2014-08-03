from gamebaker import game

from settings import settings

while True:
    messages = game.get_messages()
    settings.handle_messages(messages)
    game.event_loop()
    game.send_messages()
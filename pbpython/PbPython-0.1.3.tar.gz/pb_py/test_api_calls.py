import main as API

user_key = 'a3a56c0eba2e17cf8dc769692b6f4d93' #insert api key here
username = '1409611207860' #insert username here
host = 'tc-dev.pandorabots.com'#'aiaas.pandorabots.com'

API.create_bot(user_key, username, host,'test')

API.upload_file(user_key, username, host,'test','test.aiml','aiml')
API.compile_bot(user_key, username, host, 'test')
session_id = API.init_talk(user_key,username, host, 'test','hello')
API.talk(user_key,username, host, 'test','how are you',session_id)
API.debug_bot(user_key,username,host, 'test','hello', recent= True, trace = True)
API.delete_bot(user_key,username, host, 'test')

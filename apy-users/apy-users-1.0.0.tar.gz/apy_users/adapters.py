from .entities import AccountRepository, Account, Consumer


class MongodbAccountRepository(AccountRepository):
    def __init__(self, client_connector, database_name):
        self._mongodb_database = client_connector[database_name]

    def add(self, account):
        account_data = self._plain_account(account)
        result = self._mongodb_database.accounts.insert(account_data)
        return result

    def update(self, account):
        account_data = self._plain_account(account)
        result = self._mongodb_database.accounts.update(
            {'client_id': account_data['client_id']},
            {'$set': account_data}
        )
        return result

    def find_by_email(self, email):
        return self._find_one_by('email', email)

    def find_by_username(self, username):
        return self._find_one_by('username', username)

    def find_by_client_id(self, client_id):
        return self._find_one_by('client_id', client_id)

    def find_by_consumer_access_token(self, consumer_access_token):
        return self._find_one_by('consumers.access_token', consumer_access_token)

    def _find_one_by(self, key, value):
        document = self._mongodb_database.accounts.find_one({key: value}, {'_id': False})

        if document is None:
            return None

        consumers = []
        for consumer in document['consumers']:
            consumers.append(Consumer(**consumer))

        document['consumers'] = consumers
        return Account(**document)

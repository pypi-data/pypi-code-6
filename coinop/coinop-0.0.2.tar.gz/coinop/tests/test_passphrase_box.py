
from coinop.crypto.passphrasebox import PassphraseBox

def test_round_trip():
    message = b"i am a message"
    encrypted = PassphraseBox.encrypt("monkeys", message)
    assert encrypted.has_key('iterations')
    assert encrypted.has_key('salt')
    assert encrypted.has_key('nonce')
    assert encrypted.has_key('ciphertext')

    p = PassphraseBox.decrypt("monkeys", encrypted)
    assert p == message



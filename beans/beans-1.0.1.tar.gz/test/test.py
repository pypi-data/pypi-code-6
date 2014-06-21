import unittest
import beans
# Create your tests here.

# ENDPOINT = "http://business.lvho.st:8000/api/v1/"


class TestAPI(unittest.TestCase):
    def setUp(self):
        self.secret_good = 'b680c0de1bfeafa62037198d39aa85c8d3ad1e8b'
        self.secret_bad = 'b680c0de1bfeafa62037198d39aa85c8d3ad1e8h'

        self.public_good = 'ce085400e6d62fb8829f6e39d8ec7d2d12f7af8d'
        self.public_bad = 'ce085400e6d62fb8829f6e39d8ec7d2d12f7af8f'

        self.user_good = '1ce67151bd5ab7deb52289383cd5626c3ba0e0ee'
        self.user_bad = 'a9171a1f63c894cb3c62111f3d4861d6518a1b69'

        self.sdk_version = '1.0.1'
        self.cookies = {'beans_user': self.user_good}
        
        beans.initialize(self.secret_good)

    # Check the Version on the SDK
    def test_version(self):
        self.assertTrue(beans.__version__ == self.sdk_version)

    # Testing keys
    def test_keys(self):

        # Testing secret key
        beans.initialize(self.secret_good)
        self.assertIsNotNone(beans.business.call('reward/get_all/'))
        beans.initialize(self.secret_bad)
        self.assertRaises(beans.BeansException, beans.business.call, function='reward/get_all/')

        # Testing Public Key
        self.assertIsNotNone(beans.business.call('reward/get_all/', {'public': self.public_good}))
        self.assertRaises(beans.BeansException, beans.business.call,
                          function='reward/get_all/', params={'public': self.public_bad})

        # Testing User key
        beans.initialize(self.secret_good)
        self.assertTrue(beans.business.call('card/check/', cookies=self.cookies))
        self.assertFalse(beans.business.call('card/check/', cookies={'beans_user': self.user_bad}))

    #Testing robustest
    def test_robustest(self):
        self.assertIsNotNone(beans.business.call('reward/get_all'))
        self.assertIsNotNone(beans.business.call('/reward/get_all'))
        self.assertIsNotNone(beans.business.call('/reward/get_all/'))
        self.assertRaises(beans.BeansException, beans.business.call, function='foo/')

    # testing add and get beans
    def test_beans(self):
        nb_beans = beans.business.call('beans/get/', cookies=self.cookies)
        self.assertTrue(beans.business.call('beans/add/', params={'number': 5, 'unit':  'USD'}, cookies=self.cookies))
        self.assertTrue(beans.business.call('beans/get/', cookies=self.cookies) == nb_beans+5*10)

    # testing reward
    def test_reward(self):
        reward_list = beans.business.call('reward/get_all/', cookies=self.cookies)
        reward_type_list = (beans.REWARD_TYPE.CART_COUPON, beans.REWARD_TYPE.CART_DISCOUNT)
        r = reward_list[0]
        self.cookies['beans_reward'] = r['id']
        self.assertTrue(r['type'] in reward_type_list)
        self.assertDictContainsSubset(
            beans.business.call('reward/get/', cookies=self.cookies), r)
        nb_beans = beans.business.call('beans/get/', cookies=self.cookies)
        self.assertTrue(beans.business.call('beans/add/', {'number': r['beans']/10, 'unit':  'USD'}, cookies=self.cookies))
        self.assertTrue(beans.business.call('reward/check/', cookies=self.cookies))
        self.assertTrue(beans.business.call('reward/use/', cookies=self.cookies))
        self.assertTrue(beans.business.call('beans/get/', cookies=self.cookies) == nb_beans)


if __name__ == '__main__':
    unittest.main()
# suit_mailfactory versioning:
# <suit version updated>.<mailfactory version updated>.<hotfix>
__SUIT_VERSION__ = '0.2.8'
__MAILFACTORY_VERSION__ = '0.11'
__HOTFIX__ = 0

__VERSION__ = u'{}.{}.{}'.format(
    __SUIT_VERSION__.replace('.', ''),
    __MAILFACTORY_VERSION__.replace('.', ''),
    __HOTFIX__
)

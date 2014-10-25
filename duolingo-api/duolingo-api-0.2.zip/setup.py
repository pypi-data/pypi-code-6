from setuptools import setup

setup(
    name = "duolingo-api",
    version = "0.2",
    author = "Kartik Talwar",
    author_email = "hi@kartikt.com",
    description = ("Unofficial API for duolingo.com"),
    keywords = "duolingo, duolingo api, language",
    license = 'Apache',
    url = "http://github.com/KartikTalwar/duolingo",
    packages = ['duolingo'],
    install_requires = ("Werkzeug"),
    classifiers = [
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: POSIX',
        'Operating System :: Unix',        
        "Programming Language :: Python",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Topic :: Software Development',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    long_description = """
# Duolingo


Unofficial Duolingo API Written in Python. This is mostly a collection of functions that give you common data
directly from the api resource dictionary. More methods to come.


#### TODO

- Integrate authenticated data
- Add user activity stream


### Usage


```py
import duolingo

lingo  = duolingo.Duolingo('kartik')
```

### Methods


#### Summary

- lingo **.get_user_info()**
- lingo **.get_user_settings()**
- lingo **.get_languages()**
- lingo **.get_friends()**
- lingo **.get_language_details(language_name)**
- lingo **.get_language_progress(language_abbr)**
- lingo **.get_known_topics(language_abbr)**
- lingo **.get_known_words(language_abbr)**
- lingo **.get_learned_skills(lang)**


#### get_user_info()

```py
lingo  = duolingo.Duolingo('kartik')
print lingo.get_user_info()
```

#### get_user_settings()

```py
lingo  = duolingo.Duolingo('kartik')
print lingo.get_user_settings()
```

#### get_languages()

```py
lingo  = duolingo.Duolingo('kartik')
print lingo.get_languages()
```

#### get_friends()

```py
lingo  = duolingo.Duolingo('kartik')
print lingo.get_friends()
```

```

#### get_language_details(language_name)

```py
lingo  = duolingo.Duolingo('kartik')
print lingo.get_language_details('French')
```

#### get_language_progress(language_abbr)

```py
lingo  = duolingo.Duolingo('kartik')
print lingo.get_language_progress()
```

#### get_known_words(language_abbr)

```py
lingo  = duolingo.Duolingo('kartik')
print lingo.get_known_words()
```

#### get_known_topics(language_abbr)

```py
lingo  = duolingo.Duolingo('kartik')
print lingo.get_known_topics()
```

#### get_learned_skills(language_abbr)

```py
lingo  = duolingo.Duolingo('kartik')
print lingo.get_learned_skills('fr')
```

"""
)
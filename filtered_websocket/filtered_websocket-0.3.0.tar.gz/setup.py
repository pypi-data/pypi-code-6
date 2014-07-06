from setuptools import setup

setup(
    name = "filtered_websocket",
    version = "0.3.0",
    author = "Morgan Reece Phillips",
    author_email = "winter2718@gmail.com",
    description = ("A simple framework for constructing websocket servers"
                                   " from filter chains."),
    install_requires=[
        "twisted",
        "redis",
        "redis_collections",
        "six",
        "pyopenssl",
        "service_identity"
    ],
    license = "BSD",
    keywords = "websocket TwistedWebsocket twisted",
    url = "https://github.com/mrrrgn/filtered_websocket/tarball/0.3.0",
    packages=[
        "filtered_websocket",
        "filtered_websocket.filters",
        "filtered_websocket.storage_objects",
        "filtered_websocket.pubsub_listeners",
        "filtered_websocket.server_protocol",
    ],
    long_description="""
    Filtered WebSocket is a straight forward framework for implementing websocket servers which draws inspiration from UNIX process pipelines.
    It's a metaphor for: cat server_event | behavior_a | behavior_b | ...
    Server event handlers are encapsulated within filters such that building elaborate behaviors is as easy as importing new modules.
    Imported filters automatically add themselves to an appropriate filter chain (pipeline).

    - Supports SSL
    - Scales horizontally via remote backend storage (redis) and pubsub
      handling
    - Supports token based auth
    - New behaviors are added by simply importing filter modules""",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: BSD License",
    ],
)

"""

.. module:: blog
   :platform: Unix
   :synopsis: Really simple blog application for Django

.. moduleauthor:: Thomas Durey <tominardi@gmail.com>

This application provides :

* Listing of blog entries
* Singles of blog entries
* RSS Feed module (non auto)
* Sitemap module (non auto)
* Administration

Two basic templates available. You can rewrite these templates :

* blog/single.html (receive a post object, categories and three random posts)
* blog/index.html (receive post list, categories, next an previous links)

"""

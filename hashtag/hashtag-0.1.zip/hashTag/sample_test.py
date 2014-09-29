import HashTag

htags_mysql = HashTag.hashTag("hashtags.db.10434227.hostedresource.com","hashtags","hashtags","code4Db@ba","mysql")

# htags_sqlite3 = HashTag.hashTag("hashtags.db.10434227.hostedresource.com","sampletags","hashtags","code4Db@ba","sqlite3")

### Lets store something first ###
# htags_mysql.store("New test cases... #new #unique >>> Text after the tags")
# htags_mysql.store("New test cases... #not_new #not_so_unique >>> Sample text after tags")
# htags_mysql.store("Post without tags") 
# htags_mysql.store("#post_without_data")


# htags_mysql.storeByTags("new string is here", ["new","unique","tag_not_there"])
# htags_mysql.storeByTagsList("HELLO HELLO HELLO ", ["hello","hello","lollol",""])

# htags_mysql.Delete(tagslist=['postgres'])
# htags_mysql.Delete(tagslist=['','hello','lollol'])
# htags_mysql.Delete(datasegment="")
# htags_mysql.Delete(datasegment="First System Testing... ")
# htags_mysql.Delete(tagslist=['tag_not_there'],datasegment="new string is here")
htags_mysql.Delete(tagslist=['tag_not_there'],datasegment="new string is here")



from . import dao
from . import mydb

# start the db by dropping all tables and creating them again
# """
#     Expected Output:
#         Initializing DB
#         Initialization Completed Successfully   
# """
dao.start_db()

# # create 2 users
# """
#     Expected Output:
#         User not found
#         User created
#     Will create a new instance of the user
# """
dao.create_user("name1", "email1@email.com", "password1")
# print(dao.authenticate_user("email1@email.com", "password1"))
# print(dao.get_user_name("email1@email.com"))
# dao.create_user("name2", "email2@email.com", "password2")

# # create a duplicate user
# """
#     Expected Output:
#         User found
#         User already exists
#     Will not create a new instance of the user
    
# """
# dao.create_user("name2", "email2@email.com", "password2")

# # update user information
# """
#     Expected Output:
#         User Found!
#         User updated!       
#         User Found!
#         User email updated! 
#     User will now be 3
    
# """
# dao.update_user("name3", "email2@email.com", "password3")
# dao.update_email("email2@email.com", "email3@email.com")

# # add sites to users
# print("Adding--------------")
# dao.update_user_sites("email3@email.com", [("www.site1.com")])
# dao.update_user_sites("email1@email.com", [("www.site1.com"),("www.site2.com"),("www.site3.com")])
# print("Updating------------")
# dao.update_user_sites("email1@email.com", [("www.site1.com"),("www.site2.com")])

# print("###############################################\n")
# print("User Sites:", dao.get_user_sites("email1@email.com"))

# dao.update_cache("www.site12.com","extracted text 12")

# dao.get_cache("www.site1.com")
# dao.update_cache("www.google2.com","extracted2 text")
# dao.update_cache("www.google4.com","extracted3 text")
# dao.update_cache("www.google4.com","extracted3 text")

# print("---------------------------")
# dao.add_history("email1@email.com", "question 1")
# dao.add_history("email1@email.com", "another query")
# dao.get_history("email1@email.com")
# print("---------------------------")

# print(dao.get_history("email@email.com"))
# dao.delete_one_history("email@email.com", "www.google.com")

dao.update_cache("www.google1.com","text1")
dao.update_cache("www.google2.com","text2")
dao.update_cache("www.google3.com","text3")

# mydb.display_db()

dao.add_saved("email1@email.com", "www.google1.com", "query1")

dao.add_saved("email1@email.com", "www.google2.com", "query1")

dao.add_saved("email1@email.com", "www.google3.com", "query2")

dao.add_saved("email1@email.com", "www.google3.com", "query3")

mydb.display_db()

dao.get_saved("email1@email.com")




# print(dao.get_cached("www.google.com"))
# print(dao.get_cached("www.google2.com"))
# print(dao.get_cached("www.google3.com"))


# dao.display_db()

# dao.delete_user("email@email.com")

mydb.display_db()


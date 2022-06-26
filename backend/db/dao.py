from .mydb import SQL_DB
import hashlib
ENCRYPTION_KEY = 'A2q1tK-RcdrasPhbyVUNS5JbIjwrUizTXMlEKYXV2-w='
mydb = SQL_DB()
# import datetime

def start_db(path):
    """
    This function load the existing db
    """
    if mydb.check(path):
        mydb.connect(path)
    else:
        print("Creating new DB")
        mydb.connect(path)
        mydb.initialize_db()

def clear():
    """
    This function drops all existing tables and recreates them again
    """
    mydb.drop_all_tables()
    mydb.initialize_db()

##########    USER FUNCTIONS    ##########
# Return True if successful, False otherwise 

def create_user(name, email, password):

    name = encrypt(name)
    email = encrypt(email)
    password = hashlib.sha256(password.encode('utf-8')).hexdigest()

    return mydb.create_user(name, email, password)

def update_user(name, email, password):

    name = encrypt(name)
    email = encrypt(email)
    password = hashlib.sha256(password.encode('utf-8')).hexdigest()

    return mydb.update_user_info(name, email, password)

def update_email(old_email, new_email):

    old_email = encrypt(old_email)
    new_email = encrypt(new_email)

    return mydb.update_user_email(old_email, new_email)

def delete_user(email):

    email = encrypt(email)
    return mydb.delete_user(email)

def get_user_name(email):

    email = encrypt(email)
    name = mydb.get_user_name(email)
    name = decrypt(name)
    
    return name

def authenticate_user(email, password):

    email = encrypt(email)
    password = hashlib.sha256(password.encode('utf-8')).hexdigest()

    return mydb.authenticate(email, password)

##########    SITES MANAGER     ##########

# Returns list of user sites if found, None otherwise
def get_user_sites(user):

    user = encrypt(user)

    print("encrypted:",user)
    user_siteids = mydb.get_user_sites(user) # returns list of siteid

    if user_siteids is None:
        return None
    print("User site ids:", user_siteids)
    user_sites = list(map(mydb.get_site_from_siteid, user_siteids)) # returns site in text
    return user_sites
    

def update_user_sites(user, sites):

    print("\nTesting update sites\n")
    mydb.display_db()
    print("Sites:", list(sites))
    user_sites = get_user_sites(user)
    print("User Sites:", list(user_sites))

    user = encrypt(user)

    if user_sites is None:
        print("if user_sites is None")
        return False

    # remove all unused sites from user's list
    print("\nRemoving Unused Sites")
    for site in user_sites:
        print("Checking:", site)
        if site not in sites:
            print("Removing:", site)
            mydb.remove_user_site(user, site)

    mydb.display_db()

    # add any new sites to user's list
    print("\nAdding New Sites")
    for site in sites:
        print("Checking:", site)
        if site not in list(user_sites):
            print("Adding:", site)
            print(site, "--", list(user_sites))
            mydb.add_user_site(user, site)
    print("Finished Updating User Sites\n\n")
    return True

##########    CACHE MANAGER     ##########

def is_scraped(url):
    return mydb.is_scraped(url)

def get_cache(url):
    cache = mydb.get_cached(url)

    if cache is None:
        return None

    if cache[1] > 30:
        return None

    return cache[0], cache[2]

def update_cache(url, text, matches, scraped):
    cache = mydb.get_cached(url)

    if cache is None:
        print("Cache added")
        mydb.add_cached(url, text, matches, scraped)

    elif cache[1] > 30:
        print("Cache updated")
        mydb.update_cache(url, text, matches, scraped)

    return True

##########    SAVED MANAGER     ##########

def is_saved(user, url, query):

    user = encrypt(user)
    return mydb.is_saved(user, url, query)

def get_saved(user):

    user = encrypt(user)
    return mydb.get_saved_responses(user)

def add_saved(user, url, query):

    user = encrypt(user)
    return mydb.save_response(user, url, query)

def delete_saved(user, url):

    user = encrypt(user)
    return mydb.delete_one_saved(user, url)

def delete_all_saved(user):

    user = encrypt(user)
    return mydb.delete_saved(user)

##########    HISTORY MANAGER     ##########

def get_history(user):

    user = encrypt(user)
    return mydb.get_history(user)

def add_history(user, query):

    user = encrypt(user)
    return mydb.add_history(user, query)

def delete_history(user, query, date):

    user = encrypt(user)
    return mydb.delete_one_history(user, query, date)

def delete_all_history(user):

    user = encrypt(user)
    return mydb.delete_history(user)

##########    LOGGER MANAGER   ##########

def log(user, query, url, action):

    user = encrypt(user)

    mydb.add_query(query)
    queryid = mydb.get_queryid(query)

    mydb.log(user, queryid, url, action)
    print("Log added")

def encrypt(data):
    # f = Fernet(ENCRYPTION_KEY)
    # return f.encrypt(data.encode('utf-8'))
    return data

def decrypt(data):
    # f = Fernet(ENCRYPTION_KEY)
    # return f.decrypt(data)
    return data
import sqlite3
import datetime
import json
import os

class SQL_DB:
    def __init__(self):
        self.name = "new.db"
    
    def check(self, path):
        if os.path.isfile(path+self.name):
            print("DB Found")
            return True
        else:
            print("DB Not Found")
            return False
    
    def connect(self, path):
        # connect to the db
        self.conn = sqlite3.connect(path+self.name, check_same_thread = False)
        # create a cursor
        self.c = self.conn.cursor()

    # data types: NULL - INTEGER - REAL - TEXT - BLOB

    # initialize the db
    def create_table_users(self):
        self.c.execute("""
                CREATE TABLE users (
                name text NOT NULL,
                email text PRIMARY KEY,
                password text NOT NULL
        )""")
        #print("Table Users Created")

    def create_table_cache(self):
        self.c.execute("""
                CREATE TABLE cache (
                    url text PRIMARY KEY,
                    extracted text NOT NULL,
                    matches text,
                    date text NOT NULL,
                    scraped int
                )
        """)
        #print("Table Cache Created")

    def create_table_history(self):
        self.c.execute("""
                CREATE TABLE history (
                    queryid integer,
                    user text,
                    date text NOT NULL,
                    FOREIGN KEY (queryid) REFERENCES queries (queryid)
                    ON UPDATE CASCADE
                    ON DELETE CASCADE,
                    FOREIGN KEY (user) REFERENCES users (email)
                    ON UPDATE CASCADE
                    ON DELETE CASCADE
                )
        """)
        #print("Table History Created")

    def create_table_saved(self):
        self.c.execute("""
                CREATE TABLE saved (
                    url text,
                    user text,
                    queryid number,
                    FOREIGN KEY (url) REFERENCES cache (url)
                    ON UPDATE CASCADE
                    ON DELETE CASCADE,
                    FOREIGN KEY (user) REFERENCES users (email)
                    ON UPDATE CASCADE
                    ON DELETE CASCADE
                    FOREIGN KEY (queryid) REFERENCES queries (queryid)
                    ON UPDATE CASCADE
                    ON DELETE CASCADE
                )
        """)
        #print("Table Saved Created")


    def create_table_sites(self):
        self.c.execute("""
                CREATE TABLE sites (
                    siteid integer PRIMARY KEY AUTOINCREMENT,
                    domain text NOT NULL
                )
        """)
        #print("Table Sites Created")

    def create_table_user_sites(self):
        self.c.execute("""
                CREATE TABLE usersites (
                    user text,
                    siteid number NOT NULL,
                    FOREIGN KEY (user) REFERENCES users (email)
                    ON UPDATE CASCADE
                    ON DELETE CASCADE
                    FOREIGN KEY (siteid) REFERENCES sites (siteid)
                    ON UPDATE CASCADE
                    ON DELETE CASCADE
                )
        """)
        #print("Table User Sites Created")

    def create_table_queries(self):
        self.c.execute("""
                CREATE TABLE queries (
                    queryid integer PRIMARY KEY AUTOINCREMENT,
                    query text NOT NULL
                )
        """)
        #print("Table Queries Created")

    # def create_table_query_url(self):
    #     self.c.execute("""
    #             CREATE TABLE queryurl (
    #                 queryid number NOT NULL,
    #                 url text NOT NULL,
    #                 FOREIGN KEY (queryid) REFERENCES queries (queryid)
    #                 ON UPDATE CASCADE
    #                 ON DELETE CASCADE
    #                 FOREIGN KEY (url) REFERENCES cache (url)
    #                 ON UPDATE CASCADE
    #                 ON DELETE CASCADE
    #             )
    #     """)
    #     #print("Table QueryUrl Created")

    def create_table_log(self):
        self.c.execute("""
                CREATE TABLE log (
                    user text,
                    queryid number NOT NULL,
                    url text NOT NULL,
                    action text NOT NULL,
                    date text NOT NULL,
                    FOREIGN KEY (user) REFERENCES users (email)
                    ON UPDATE CASCADE
                    ON DELETE CASCADE
                    FOREIGN KEY (queryid) REFERENCES queries (queryid)
                    ON UPDATE CASCADE
                    ON DELETE CASCADE
                    FOREIGN KEY (url) REFERENCES cache (url)
                    ON UPDATE CASCADE
                    ON DELETE CASCADE
                )
        """)
        #print("Table Log Created")

    def drop_all_tables(self):
        self.c.executescript("""
                DROP TABLE IF EXISTS users;
                DROP TABLE IF EXISTS cache;
                DROP TABLE IF EXISTS history;
                DROP TABLE IF EXISTS saved;
                DROP TABLE IF EXISTS sites;
                DROP TABLE IF EXISTS usersites;
                DROP TABLE IF EXISTS queries;
                DROP TABLE IF EXISTS log;
        """)
        # DROP TABLE IF EXISTS queryurl;
        #print("Tables Dropped")

    def initialize_db(self):
        print("\nInitializing DB")

        self.create_table_users()
        self.create_table_cache()
        self.create_table_history()
        self.create_table_saved()
        self.create_table_sites()
        self.create_table_user_sites()
        self.create_table_queries()
        # self.create_table_query_url()
        self.create_table_log()
        # conn.execute("PRAGMA foreign_keys = ON")
        print("Initialization Completed Successfully\n")
        return True

    def display_db(self):
        print("\n")

        statement = "SELECT * FROM users"
        users = self.c.execute(statement).fetchall()
        print("Users", users)

        statement = "SELECT * FROM cache"
        cache = self.c.execute(statement).fetchall()
        print("Cache",cache)

        statement = "SELECT * FROM history"
        history = self.c.execute(statement).fetchall()
        print("History",history)

        statement = "SELECT * FROM saved"
        saved = self.c.execute(statement).fetchall()
        print("Saved",saved)

        statement = "SELECT * FROM sites"
        sites = self.c.execute(statement).fetchall()
        print("Sites",sites)

        statement = "SELECT * FROM usersites"
        usersites = self.c.execute(statement).fetchall()
        print("UserSites",usersites)

        statement = "SELECT * FROM queries"
        queries = self.c.execute(statement).fetchall()
        print("Queries",queries)

        # statement = "SELECT * FROM queryurl"
        # queryurl = self.c.execute(statement).fetchall()
        # print("QueryUrl",queryurl)

        statement = "SELECT * FROM log"
        log = self.c.execute(statement).fetchall()
        print("Log",log)

        print("\n\n")

    def get_user_by_email(self, email):
        try:
            statement = "SELECT * FROM users  WHERE email = '" + email + "'"
            user=self.c.execute(statement).fetchone()
            if user is not None:
                print("User Found!", email)
            else:
                print("User not found!")
            return user
        except:
            print("Error in get_user_by_email")
            return None

    def user_exists(self, email):
        if self.get_user_by_email(email) is None:
            print("User does not exist!")
            return False
        return True

    def create_user(self, name, email, password):
        if not self.user_exists(email):
            self.c.execute("INSERT INTO users VALUES (?, ?, ?)", (name, email, password))
            print("User created!", email)
            self.commit()
            return True
        print("User already exists!")
        return False

    def get_user_name(self, email):
        if self.user_exists(email):
            name = self.c.execute("SELECT name FROM users WHERE email = '" + email + "'").fetchone()[0]
            print("Name:", name)
            return name
        return False

    def authenticate(self, email, password):
        if self.user_exists(email):
            statement = "SELECT password FROM users WHERE email = '" + email + "'"
            dbpassword = self.c.execute(statement).fetchone()[0]
            print("Authenticating user:", email)
            print(dbpassword, password)
            if dbpassword == password:
                print("Passwords match")
                return True
            else:
                print("Passwords dont match")
                return False
        return False

    def update_user_info(self, name, email, password):
        if self.user_exists(email):
            statement = "UPDATE users SET name = '" + name + "', password = '" + password + "' WHERE  email = '" + email + "'"
            self.c.execute(statement)
            print("User updated!", email)
            self.commit()
            return True
        return False

    def update_user_email(self, current_email, new_email):
        if self.user_exists(current_email):
            statement = "UPDATE users SET email = '" + new_email + "' WHERE  email = '" + current_email + "'"
            self.c.execute(statement)
            print("User email updated!", current_email, new_email)
            self.commit()
            return True
        return False

    def delete_user(self, email):
        if self.user_exists(email):
            statement = "DELETE from users WHERE email = '" + email + "'"
            self.c.execute(statement)
            print("User deleted!", email)
            self.commit()
            return True
        return False

    def get_user_sites(self, email):
        if self.user_exists(email):
            statement = "SELECT siteid from usersites WHERE user = '" + email + "'"
            sites = self.c.execute(statement).fetchall()
            print(list(sites))
            for site in sites:
                sites[sites.index(site)] = site[0]
            print(list(sites))

            if len(sites) > 0:
                print("Sites Found!")
                print("List of sites", list(sites))
            else:
                print("Sites not found!")
            return list(sites)
        return None

    def get_siteid(self, site):
        try:
            statement = "SELECT siteid from sites WHERE domain = '" + site + "'"
            id = self.c.execute(statement).fetchone()[0]
            if id is not None:
                print("Site ID Found!")
            else:
                print("Site ID not found!")
            return id
        except:
            print("Site not Found")
            return None

    def get_site_from_siteid(self, siteid):
        print("Getting site from user site")
        statement = "SELECT domain from sites WHERE siteid = '" + str(siteid) + "'"
        site = self.c.execute(statement).fetchone()[0]
        print("Got site from user site")
        return site

    def add_site(self, site):
        if self.get_siteid(site) is None:
            print("Adding site")
            self.c.execute("INSERT INTO sites(domain) values (?)", [site])
            print("Site Added!")
            self.commit()
            return True
        print("Site already exists!")
        return False

    def add_user_site(self, email, site):
        # check that user exists and site not already added to user
        if self.user_exists(email) and site not in self.get_user_sites(email):  
            self.add_site(site)
            site_id = self.get_siteid(site)
            print("Adding site to user", site, "with siteid", site_id)
            self.c.execute("INSERT INTO usersites values (?, ?)", (email, site_id))
            print("Site Added!")
            self.commit()
            return True
        print("Error while adding site to user sites!")
        return False

    def remove_user_site(self, email, site):
        if self.user_exists(email):
            statement = "DELETE FROM usersites WHERE user = '" + email + "' AND siteid = '" + str(self.get_siteid(site)) + "'"
            print("Deleting", site)
            self.c.execute(statement)
            print("Site Deleted!")
            self.commit()
            return True
        return False
        
    def add_history(self, email, query):
        if self.user_exists(email): 
            queryid = self.get_queryid(query)
            if queryid is None:
                print("Query does not exist")
                self.add_query(query)
                queryid = self.get_queryid(query)
            date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.c.execute("INSERT INTO history values (?, ?, ?)", (queryid, email, date))
            print("History Added!")
            self.commit()
            return True
        return False

    def get_history(self, email):
        if self.user_exists(email):
            statement = "Select queryid, date from history WHERE user = '" + email + "'"
            history = self.c.execute(statement).fetchall()
            for i in range(len(history)):
                history[i] = list(history[i])
                history[i] = {
                    'query': self.get_query_from_queryid(history[i][0]),
                    'time': history[i][1]
                }
            print("History Found!")
            return history
        return None

    def delete_one_history(self, email, query, date):
        if self.user_exists(email):
            queryid = self.get_queryid(query)
            statement = "DELETE from history WHERE user = '" + email + "' AND queryid = '" + str(queryid) + "' AND date = '" + date + "'"
            self.c.execute(statement)
            print("One History Deleted!")
            self.commit()
            return True
        return False

    def delete_history(self, email):
        if self.user_exists(email):
            statement = "DELETE from history WHERE user = '" + email + "'"
            self.c.execute(statement)
            print("History Deleted!")
            self.commit()
            return True
        return False

    def add_query(self, query):
        if self.get_queryid(query) is None:
            print("Adding query:", query)
            self.c.execute("INSERT INTO queries(query) values (?)", [query])
            print("Query Added!")
            self.commit()
            return True
        print("Query already exists!")
        return False

    def get_queryid(self, query):
        try:
            statement = "SELECT queryid from queries WHERE query = '" + query + "'"
            id = self.c.execute(statement).fetchone()[0]
            if id is not None:
                print("Query ID Found!", id)
            else:
                print("Query ID not found!")
            return id
        except:
            print("Query not Found")
            return None

    def get_query_from_queryid(self, queryid):
        print("Getting query from queries")
        statement = "SELECT query from queries WHERE queryid = '" + str(queryid) + "'"
        query = self.c.execute(statement).fetchone()[0]
        print("Got query from queries", query)
        return query

    def log(self, email, query, url, action):
        if self.user_exists(email):
            if self.get_queryid(query) is not None:
                if self.get_cached(url) is not None:
                    date = datetime.date.today()
                    self.c.execute("INSERT INTO log values (?, ?, ?, ?)", (email, query, url, action, date))
                    print("Log added!")
                    self.commit()
                    return True
                else:
                    print("URL not in cache")
            else:
                print("Qeury not in Queries")
        return False

    def is_saved(self, email, site, query):
        saved = None
        # if user_exists(email) and get_cached(site) is not None:
        if self.user_exists(email) is not None:
            queryid = self.get_queryid(query)
            if queryid is None:
                self.add_query(query)
                queryid = self.get_queryid(query)
            statement = "Select * from saved WHERE user = '" + email + "' AND url = '" + site + "' AND queryid = '" + str(queryid) + "'"
            saved = self.c.execute(statement).fetchone()
        if saved is not None:
            return True
        return False

    def save_response(self, email, site, query):
        if not self.is_saved(email, site, query):
            queryid = self.get_queryid(query)
            self.c.execute("INSERT INTO saved values (?, ?, ?)", (site, email, queryid))
            print("Saved Added!", site, query)
            self.commit()
            return True
        return False

    def get_saved_responses(self, email):
        if self.user_exists(email):
            statement = "Select url, queryid from saved WHERE user = '" + email + "'"
            history = self.c.execute(statement).fetchall()
            print("Before", history)
            new_history = []
            for hist in history:
                cache = self.get_cached(hist[0])
                if cache is not None:
                    response, matches = cache[0], cache[2]
                else:
                    response = ''
                    matches = '[]'
                hist = {
                    'url': hist[0], 
                    'query': self.get_query_from_queryid(hist[1]),
                    'response': response,
                    'matches': json.loads(matches)
                }
                new_history.append(hist)
                print("hist",hist)
            print("Saved Found!")
            print("After", new_history)
            return new_history
        return None

    def delete_one_saved(self, email, site):
        if self.user_exists(email):
            statement = "DELETE from saved WHERE user = '" + email + "' AND url = '" + site + "'"
            self.c.execute(statement)
            print("One Saved Deleted!")
            self.commit()
            return True
        return False

    def delete_saved(self, email):
        if self.user_exists(email):
            statement = "DELETE from saved WHERE user = '" + email + "'"
            self.c.execute(statement)
            print("Saved Deleted!")
            self.commit()
            return True
        return False

    def delete_history_saved(self, email):
        self.delete_history(email)
        self.delete_saved(email)

    def is_scraped(self, url):
        try:
            statement = "SELECT scraped from cache WHERE url = '" + url + "'"
            cached = self.c.execute(statement).fetchone()[0]
            if cached == 1:
                return True
        except:
            print("Error while getting cache")
        print("Cache not found!")
        return False
        
    def get_cached(self, url):
        try:
            statement = "SELECT extracted, julianday('now') - julianday(date), matches from cache WHERE url = '" + url + "'"
            cached = self.c.execute(statement).fetchone()
            if cached is not None:
                # print("Cache Found!", cached)
                print("Cache Found!")
                return cached
        except:
            print("Error while getting cache")
        print("Cache not found!")
        return None

    def add_cached(self, url, extracted, matches, scraped):
        if self.get_cached(url) is None:
            date = datetime.date.today()
            print("Date:", date)
            scraped = 1 if scraped else 0
            self.c.execute("INSERT INTO cache values (?, ?, ?, ?, ?)", (url, extracted, matches, date, scraped))
            print("Cache Added!", url)
            self.commit()
            return True
        else:
            print("Cache Added Previously")
            return False

    def update_cache(self, url, extracted, matches,scraped):
        if self.get_cached(url) is not None:
            date = datetime.date.today()
            scraped = 1 if scraped else 0
            statement = "UPDATE cache SET extracted = '" + extracted + "', matches = '" + matches + "', scraped = '" + scraped + "' WHERE url = '" + url + "', date = '" + date + "'"
            self.c.execute(statement)
            print("Cache Updated!", url)
            self.commit()
            return True
        else:
            print("Cache not found!")
            return False

    # to execute the command
    def commit(self):
        self.conn.commit()
        print("Command Executed Successfuly!")

    # close the connection
    def close_connection(self):
        self.conn.close()
        print("Connection Closed")
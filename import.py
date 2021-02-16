import os,csv,psycopg2

DATABASE_URL = os.environ['DATABASE_URL']

conn = psycopg2.connect(DATABASE_URL, sslmode='require')
curr = conn.cursor()

'''
print("Creating user_info table!")
curr.execute("DROP TABLE user_info;")
curr.execute("CREATE TABLE user_info (username VARCHAR PRIMARY KEY, password VARCHAR NOT NULL);") 
conn.commit()
print("CREATED")
'''

print("dropping table")
curr.execute("DROP TABLE reviews;")
print("dropped")
curr.execute("CREATE TABLE reviews (id SERIAL PRIMARY KEY, username VARCHAR NOT NULL, book_id INTEGER NOT NULL, comment VARCHAR NOT NULL, rating INT NOT NULL);")
conn.commit()
print("CREATED")


'''
csvfile = open("books.csv") 
reader = csv.reader(csvfile)

curr.execute("CREATE TABLE books ( id SERIAL PRIMARY KEY, \
								   isbn VARCHAR NOT NULL, \
								   title VARCHAR NOT NULL, \
								   author VARCHAR NOT NULL, \
								   year VARCHAR NOT NULL );")

print("CREATED")
print("Adding values to table.")
for isbn, title, author, year in reader:
	curr.execute("INSERT INTO books (isbn, title, author, year) VALUES (%s, %s, %s, %s)",(isbn,title,author,year))
conn.commit()
print("Insert Completed!")
'''
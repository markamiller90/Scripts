import psycopg2

conn = psycopg2.connect(database="",
                        user="",
                        host='',
                        password="",
                        sslmode='',
                        port=, )
conn.autocommit = True
cur = conn.cursor()

#what you are looking for in all the database
search_query = 'klarittyjoy.com'
account_query = cur.execute('select id from accounts where cancel_at is null and deleted_at is null and cancellation_initiated_at is null limit 2')
results = cur.fetchall()
id_list = []
for id in results:
    id_list.append(id[0])
    # write list of ID's to file to process through vs run the query again. have index
for account_id in id_list:
    print(account_id)
  #sql script where you want to look
    Script_search = cur.execute(
        f'''
        SELECT * 
        from users 
        where email like {search_query};
        ''')
    results = cur.fetchall()
    if bool(results) is True:
        print(results)
        

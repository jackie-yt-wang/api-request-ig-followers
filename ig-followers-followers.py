from instagram_private_api import Client, ClientCompatPatch
import csv
import dbconfig
import json
import pandas as pd
import time 
import random

# Replace with your Instagram username and password
username = dbconfig.account
password = dbconfig.password


api = Client(username, password)
results = api.autocomplete_user_list()
usernameList =[]
for i in range(len(results['users'])):
    tempuser = results['users'][i]['username']
    usernameList.append(tempuser)


# Define the column names for the DataFrame
column_names = ['my_followers', 'followers_followers']
df = pd.DataFrame(columns=column_names)
# Loop through each user in the username list
for tempuser in usernameList[:100]:
    print('progress:',usernameList.index(tempuser), tempuser)

    while True:
        try: 
            time.sleep(random.randint(1,5))
            user_info = api.username_info(tempuser)
            break
        except:
            time.sleep(random.randint(1,5))
            api = Client(username, password)

    user_id = user_info['user']['pk_id']
    followers = []
    next_max_id = ''

    while True:
        while True:        
            try:
                time.sleep(random.randint(1,5))
                results = api.user_followers(user_id, api.generate_uuid(), max_id=next_max_id)
                break
            except:
                time.sleep(random.randint(1,5))
                api = Client(username, password)
        followers.extend(results.get('users', []))
        next_max_id = results.get('next_max_id')
        if not next_max_id:
            break

    # Add the list of followers to the DataFrame
    follower_usernames = [follower['username'] for follower in followers]
    df = df.append(pd.DataFrame({ 'my_followers': [tempuser] * len(follower_usernames),
                                  'followers_followers': follower_usernames }), ignore_index=True)

df.to_csv('my_followers_followers.csv',index=False)




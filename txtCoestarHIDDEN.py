import tweepy #for tweeting to twitter
import datetime #for startup wait time
import time #for time.sleep

rate = 43200 #rate of posts in seconds
size = 280 #size of quote sections

now = datetime.datetime.now() #Get current time of day
sec = (now.hour*60*60) + (now.minute*60) + now.second #convert now into second of day
#creating waitTime until 9:00 or 21:00
if sec > 32400: #32400 is 9:00
    waitTime = 75600 - sec #75600 is 21:00
else:
    waitTime = 32400 - sec

print("Time verified.")
print(waitTime) #printing number of seconds of wait to console

time.sleep(waitTime) #sleeping for waitTime seconds

#twitter authentification
CONSUMER_KEY = 'X'
CONSUMER_SECRET = 'X'
ACCESS_KEY = 'X'
ACCESS_SECRET = 'X'
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.api(auth)

print("Twitter access authorized.")

print("Main loop entered.")

while True: #infinite loop
    #used to read first line from file
    with open('quoteList.txt') as f: #opens quote list file
        quote = f.readline() #sets quote as the first line in the file

    #used to delete first line from file
    with open('quoteList.txt', 'r') as fin: #opens quote list file
        data = fin.read().splitlines(True) #splits the file
    with open('quoteList.txt', 'w') as fout: #opens quote list file
        fout.writelines(data[1:]) #deletes first line

    #breaks up quote into chunks
    def chunks(l, n):
        #Yield successive n-sized chunks from l.
        for i in range(0, len(l), n):
            yield l[i:i + n]

    quoteChunks = list(chunks(quote, size)) #puts quote chunks into list

    for chunk in quoteChunks:
        if len(quoteChunks) > 1:
            if chunk == quoteChunks[0]: #if the chunk is the first chunk
                api.update_status(chunk) #tweet chunk
                latest = api.user_timeline(screen_name=txtCoestar, count=1) #get id of latest tweet
                latest = latest.id_str
            api.update_status(chunk, in_reply_to_status_id=latest) #tweet chunk in reply to latest
            latest = api.user_timeline(screen_name=txtCoestar, count=1) #get id of latest tweet
            latest = latest.id_str
        else:
            api.update_status(chunk) #tweet chunk

    time.sleep(43200) #sleep for 12 hours

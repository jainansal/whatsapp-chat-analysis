from urlextract import URLExtract
import emoji
extractor = URLExtract()

def fetch_words(df):
    words = []
    for message in df['message']:
        words.extend(message.split())
    return words

def fetch_media(df):
    return df[df['message'] == "<Media omitted>\n"].shape[0]
    
def fetch_urls(df):
    urls = []
    for message in df['message']:
        links = extractor.find_urls(message)
        for link in links:
            urls.append(link)
    return urls

def basic_stats(selected_user, df):
    user_df = df
    if selected_user != 'Overall':
        user_df = user_df[user_df['user'] == selected_user]
    
    words = fetch_words(user_df)
    num_media = fetch_media(user_df)
    urls = fetch_urls(df)
    
    return user_df['message'].shape[0], len(words), num_media, len(urls)

def msg_per_user(df):
    return df['user'].value_counts().head().reset_index().rename(columns={'index':'user', 'user':'total_msgs'})

def inter_stats(df):
    mpu =msg_per_user(df)
    return mpu

def okay(s):
    for c in s:
        if c.lower() < 'a' or c.lower() > 'z':
            return False
    return True 
    

def common(df):
    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']
    f = open('stop_words.txt','r')
    stop = f.read()
    words = []
    for message in temp['message']:
        for word in message.lower().split():
            if word not in stop and okay(word):
                words.append(word)

    return words

def emojis(df):
    emojis=[]
    for message in df['message']:
        emojis.extend([c for c in message if emoji.is_emoji(c)])

    return emojis

def timeline(df):
    mydf = df.copy()
    mydf['month_num'] = mydf['date'].dt.month
    timeline = mydf.groupby(['year','month_num','month']).count()['message'].reset_index()
    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + '-' + str(timeline['year'][i]))
    timeline['time'] = time
    return timeline

def daily_timeline(df):
    mydf = df.copy()
    mydf['only_date'] = mydf['date'].dt.date
    daily_timeline = mydf.groupby('only_date').count()['message'].reset_index()
    return daily_timeline

def daywise(df):
    df['day_name'] = df['date'].dt.day_name()
    return df['day_name'].value_counts().reset_index()

def monthwise(df):
    df['month_name'] = df['date'].dt.month_name()
    return df['month_name'].value_counts().reset_index()

def heatmap(df):
    hmap = df.pivot_table(index='day_name',columns='period',values='message', aggfunc='count').fillna(0)
    return hmap
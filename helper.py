from urlextract import URLExtract
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
    return df['user'].value_counts().head()

def inter_stats(df):
    mpu = msg_per_user(df)
    return mpu
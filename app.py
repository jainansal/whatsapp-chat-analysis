# Libraries import
import dateparser
import streamlit as st
import seaborn as sns
import pandas as pd
import preprocessor
import helper
import matplotlib.pyplot as plt
from collections import Counter

# Sidebar
st.sidebar.title("Whatsapp Chat Analyzer")



# File uploader
uploaded_file = st.sidebar.file_uploader("Choose a file")



# File processing
if uploaded_file is not None:

    # Basic file read and conversions
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df = preprocessor.preprocess(data)
    # st.dataframe(df)


    # fetch unique users
    user_list = df['user'].unique().tolist()
    if 'group_notification' in user_list:
        user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0,"Overall")

    # User sidebar
    selected_user = st.sidebar.selectbox("User", user_list)

    # Analysis button
    if st.sidebar.button("Show Analysis"):

        # Fetching basic stats
        num_messages, num_words, num_media, num_urls = helper.basic_stats(selected_user,df)
        # most_busy = helper.inter_stats(df)
        st.title("Top Statistics")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.header("Total Messages")
            st.title(num_messages)
        with col2:
            st.header("Total words")
            st.title(num_words)
        with col3:
            st.header("Media shared")
            st.title(num_media)
        with col4:
            st.header("Links shared")
            st.title(num_urls)


        cur_df = df.copy()
        if selected_user != 'Overall':
            cur_df = df[df['user'] == selected_user]


        # Timeline analysis

        col1, col2 = st.columns(2)

        with col1:
            st.title("Monthly timeline")
            timeline = helper.timeline(cur_df)

            fig,ax = plt.subplots()
            ax.plot(timeline['time'], timeline['message'], color='g')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
        
        with col2:
            st.title("Daily timeline")
            daily_timeline = helper.daily_timeline(cur_df)
            fig,ax = plt.subplots()
            ax.plot(daily_timeline['only_date'], daily_timeline['message'], color='black')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        col1, col2 = st.columns(2)

        with col1:
            st.title("Most Busy day")
            daywise = helper.daywise(cur_df)
            fig, ax = plt.subplots()
            ax.bar(daywise['index'], daywise['day_name'])
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        with col2:
            st.title("Most Busy Month")
            monthwise = helper.monthwise(cur_df)
            fig,ax = plt.subplots()
            ax.bar(monthwise['index'], monthwise['month_name'], color='y')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        st.title("Weekly Activity Map")
        hmap = helper.heatmap(cur_df)
        fig,ax = plt.subplots()
        ax = sns.heatmap(hmap)
        st.pyplot(fig)


        # Intermediate stats
        if selected_user == 'Overall':

            # User activity
            st.title('Most Busy Users')

            # Format: [[user, total_msgs]]
            mpu = helper.inter_stats(df)

            fig, ax = plt.subplots()

            col1, col2 = st.columns(2)

            with col1:
                ax.bar(mpu['user'], mpu['total_msgs'], color='r')
                plt.xticks(rotation = 'vertical')
                st.pyplot(fig)
            with col2:
                perc = round(mpu['total_msgs']/df['message'].size * 100,2)
                final = pd.DataFrame({'user':mpu['user'], 'contribution(%)':perc})
                st.dataframe(final)


        
        # Most common words
        

        common_words = helper.common(cur_df)
        final_df = pd.DataFrame(Counter(common_words).most_common(20), columns=['word','occurence'])

        fig, ax = plt.subplots()

        ax.barh(final_df['word'], final_df['occurence'])
        plt.xticks(rotation='vertical')

        st.title('Most Common Words')
        st.pyplot(fig)
        

        # Emoji analysis

        st.title('Emoji analysis')
        col1, col2 = st.columns(2)
        emojis = helper.emojis(cur_df)
        emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))

        with col1:
            st.dataframe(emoji_df)
        with col2:
            emoji_df = emoji_df[:5]
            fig,ax=plt.subplots()
            ax.pie(emoji_df[1], labels=emoji_df[0], autopct='%0.2f')
            st.pyplot(fig)
        
        
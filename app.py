# Libraries import
import streamlit as st
import pandas as pd
import preprocessor
import helper
import matplotlib.pyplot as plt

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
    st.dataframe(df)


    # fetch unique users
    user_list = df['user'].unique().tolist()
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


        
        # Wordcloud

        
import streamlit as st
import preprocessor
import helper
import matplotlib.pyplot as plt

st.sidebar.title("Whatsapp Chat Analyzer")

uploaded_file = st.sidebar.file_uploader("Choose a file")

if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df = preprocessor.preprocess(data)
    
    st.dataframe(df)

    # fetch unique users
    user_list = df['user'].unique().tolist()
    user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0,"Overall")

    selected_user = st.sidebar.selectbox("User", user_list)

    if st.sidebar.button("Show Analysis"):

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
        # with col1:
        #     st.header("Most active user")
        #     st.title(most_busy)

        if selected_user == 'Overall':
            st.title('Most Busy Users')
            mpu = helper.inter_stats(df)
            fig, ax = plt.subplots()

            col1, col2 = st.columns(2)

            with col1:
                ax.bar(mpu.index, mpu.values, color='r')
                plt.xticks(rotation = 'vertical')
                st.pyplot(fig)
            with col2:
                per = round((mpu/df['message'].size) * 100, 2)
                st.text(per)
        
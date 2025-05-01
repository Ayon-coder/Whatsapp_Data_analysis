import streamlit as st
import preprocessor
import Helper
import matplotlib.pyplot as plt


st.sidebar.title("WhatsApp Chat Analyser")
uploaded_file=st.sidebar.file_uploader("")
if uploaded_file is not None:
    bytes_data=uploaded_file.getvalue()
    data=bytes_data.decode("utf-8")

    df=preprocessor.preprocess(data)
    st.dataframe(df)

    #fetch unique users
    user_list=df["user"].unique().tolist()
    user_list.remove("WhatsApp_Notification")
    user_list.sort()
    user_list.insert(0, "Overall")

    selected_user=st.sidebar.selectbox("Show Analysis wrt",user_list)

    if st.sidebar.button("Show Analysis"):

        words,num_messages,nom,num_links=Helper.fetch_stat(selected_user,df)
        col1,col2,col3,col4=st.columns(4)
        with col1:
            st.header("Total Messages")
            st.title(num_messages)
        with col2:
            st.header("Total words")
            st.title(words)
        with col3:
            st.header("Media Shared")
            st.title(nom)
        with col4:
            st.header("Links Shared")
            st.title(num_links)

        #finding the busiest user in the group
        if selected_user=="Overall":
            st.title("Most Busy Users")
            x,per=Helper.fetch_most_busy(df)
            fig,ax= plt.subplots()
            name=x.index
            count=x.values
            col1,col2=st.columns(2)

            with col1:
                ax.bar(name,count)
                plt.xticks(rotation="vertical")
                st.pyplot(fig)
            with col2:
                st.dataframe(per)

        st.title("Word Cloud")
        df_wc=Helper.create_word_cloud(selected_user,df)
        fig,ax=plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)

        # most common words

        most_common_df=Helper.most_c_w(selected_user,df)

        fig,ax=plt.subplots()
        ax.barh(most_common_df[0],most_common_df[1])
        # plt.xticks(rotation="vertical")
        st.title("Most Common Words")
        st.pyplot(fig)

        emoji_df=Helper.emoji_helper(selected_user,df)
        st.title("Emoji Analysis")
        col1,col2=st.columns(2)

        # with col1:
        st.dataframe(emoji_df)
        # with col2:
        #     fig,ax=plt.subplots()
        #     ax.pie(emoji_df[1], labels=emoji_df[0]) 
        #     st.pyplot()


import pandas as pd
import re

def preprocess(data):
    pattern = r'\d{1,2}/\d{1,2}/\d{2},\s\d{1,2}:\d{2}\s(?:am|pm)'

    messages=re.split(pattern,data)[1:]

    dates=re.findall(pattern,data)
    new_date=[]
    for date in dates:
        new_date.append(date.replace('\u202f',' '))

    df=pd.DataFrame({"user_message" : messages, "message_date" : dates})
    #convert message data type
    df["message_date"]=pd.to_datetime(df["message_date"],format="%d/%m/%y, %I:%M %p")

    df.rename(columns={"message_date" : "date"},inplace=True)

    users=[]
    messages=[]
    for message in df["user_message"]:
        entry = re.split(r"([\w\W]+?):\s", message)
        if entry[1:]: #user name
            users.append(entry[1])
            messages.append(entry[2])
        else:
            users.append("WhatsApp_Notification")
            messages.append(entry[0])
    df["user"]=users
    df["message"]=messages
    df.drop(columns=["user_message"], inplace=True)

    df["year"]=df["date"].dt.year
    df["month"]=df["date"].dt.month_name()
    df["day"]=df["date"].dt.day
    df["hour"]=df["date"].dt.hour
    df["minute"]=df["date"].dt.minute
    df["second"]=df["date"].dt.second
    
    return df
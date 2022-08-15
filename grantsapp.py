import streamlit as st
import numpy as np
import pandas as pd
import pickle
from datetime import datetime
st.set_page_config(layout="wide")
st.title("EU's H2020 grant calls recommendation system")
st.header("Research authority, University of Haifa")
st.subheader("This website presents you the 10 most suitable EU's grant calls, based on your publications.")
st.sidebar.markdown('This is an in-house development of the research authority.\n we would really appreciate your feedback on the recommendations by pressing Like/Dislike if the topic is relevant for you.')
st.sidebar.markdown('For any questions / Notes / suggestions / special requests / personal adaptations please contact <a href="mailto:gzeevi@univ.haifa.ac.il">gzeevi@univ.haifa.ac.il</a>', unsafe_allow_html=True)
df = pd.read_excel('Recommendations.xlsx')
with open("FullDesc.pickle", "rb") as input_file:
    fulldesc = pickle.load(input_file)
# df['links'] = df['links'].apply(lambda x: f'<a target="_blank" href="{x}">Full Description URL</a>')
names = df['pure Name'].unique().tolist()
option = st.selectbox(
     'Please Choose your name',
     names)
# st.write('You selected:', option)
st.write('')
chosen_df = (df[df['pure Name'] == option][['ccm2Id','pure Name','grant_title','match score','deadlineDates','links']]).reset_index(drop=True)
# chosen_df = chosen_df.set_index('pure Name')
#option 1
# st.write(chosen_df.to_html(escape=False, index=False,justify='center').replace('<td>', '<td align="center">'), unsafe_allow_html=True)
#option 2
user_table = chosen_df.to_dict()
# # Show users table
colms = st.columns([1, 5, 1, 1,1.5,0.5,0.5])
fields = ["#", "**Grant Title** - Press to watch on EU's website", '**Match Score**', '**Deadline Dates**',"**Full description**"]
show_title = None
show_desc = None
for col, field_name in zip(colms, fields):
     # header
     col.write(field_name)

for x, grant_t in enumerate(user_table['grant_title']):
     col1, col2, col3, col4, col5, col6,col7 =  st.columns([1, 5, 1, 1,1.5,0.5,0.5])

     col1.write(x+1)  # index
     # col2.write(user_table['grant_title'][x]+'.'+'\n'+f"[Watch on EU website]({user_table['links'][x]})")
     col2.write(f"[{user_table['grant_title'][x]}]({user_table['links'][x]})")
     col3.write(user_table['match score'][x])
     col4.write(user_table['deadlineDates'][x])
     # disable_status = user_table['disabled'][x]  # flexible type of button
     # button_type = "Unblock" if disable_status else "Block"
     button_phold_5 = col5.empty()  # create a placeholder
     do_action_5 = button_phold_5.button("Show", key=x)
     if do_action_5:
          show_title = user_table['grant_title'][x]
          show_desc = fulldesc[user_table['ccm2Id'][x]]
     button_phold_6 = col6.empty()  # create a placeholder
     button_phold_7 = col7.empty()  # create a placeholder
     # do_action_6 = button_phold_6.button("Yes")
     # do_action_7 = button_phold_7.button("No")
     do_action_6 = button_phold_6.button("👍",key = f'{option}_{x}_6') if f'{option}_{x}' not in st.session_state else False
     do_action_7 = button_phold_7.button("👎",key = f'{option}_{x}_7') if f'{option}_{x}' not in st.session_state else False

     if do_action_6 or do_action_7:
          st.session_state[f'{option}_{x}'] = True
          feed = pd.read_csv('feedback.csv')
          feed.loc[-1] = [user_table['ccm2Id'][x], user_table['grant_title'][x], user_table['pure Name'][x], 1 if do_action_6 else 0,datetime.today().strftime('%d-%m-%Y')]
          feed.reset_index(drop=True, inplace=True)
          feed.to_csv('feedback.csv',index=False)
          button_phold_6.empty()  # remove button
          button_phold_7.empty()
if show_title:
     st.title(show_title)
     st.write(show_desc)
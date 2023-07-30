# to run the app : streamlit run app.py
# to have the correct version  : pipreqs --encoding=utf8 --force


import base64
import pandas as pd  # pip install pandas
import streamlit as st  # pip install streamlit

from Functions.creating_df_and_plots import calculate_column_percentages,create_stacked_barplot,calculate_event_occurrences, create_horizontal_bar_chart,plot_box_with_mean
from Functions.open_questions import OP1,OP2,OP3,OP4,OP5,OP6

# emojis: https://www.webfx.com/tools/emoji-cheat-sheet/
st.set_page_config(page_title="Responses Founderland", page_icon=":bar_chart:", layout="wide")

st.title("Funderland Survey")

# ----Global variable

path = "responses.xlsx"

differents_question={
    "Why did you join Founderland? Select all that apply":[
                "Recommendation",
                "Seeking community",
                "Opportunity to connect with others",
                "Networking opportunities"],
    "Select all the reasons for joining the community": [
                "Knowledge about funding",
                "Access to network (partners, funders, etc)",
                "Meeting other WoC founders across Europe",
                "Event invitations",
                "Safe Space",
                "Access to funding opportunities",
                "Learn how to scale your business",
                "Get mentorship",
                "Become a mentor",
                "Find a Co-Founder"],
    "questions":[
                "Funding",
                "Access to network (partners, funders, etc)",
                "Meeting other WoC founders across Europe",
                "Event invitations",
                "Safe Space",
                "Access to funding opportunities",
                "Learn how to scale your business",
                "Get mentorship",
                "Become a mentor",
                "Find a Co-Founder"],
    "Gains" :[
                "Knowledge about funding3",
                "Access to network (partners, funders, etc)4",
                "Meeting other WoC founders across Europe5",
                "Event invitations6",
                "Safe Space7",
                "Access to funding opportunities8",
                "Learn how to scale your business9",
                "Get mentorship10",
                "Become a mentor11",
                "Find a Co-Founder12"],

}




# ---- READ EXCEL ----
st.markdown("""---""")




st.markdown("""---""")
@st.cache_data
def read_excel (path):
    return pd.read_excel(path)

df = read_excel(path)



exp1= st.expander("Why did you join Founderland?")
exp2= st.expander("Select all the reasons for joining the community")
exp3= st.expander("Which program do you prefer to access or participate in?")
exp4= st.expander("What benefits have you received from the community?")
exp5= st.expander("Rate your gain from the community")

st.write("#### Now some open question")
exp6= st.expander("Report orriented view what have you learn and your opinion")
exp7= st.expander("Feedback on how has your experience been?")
exp8= st.expander("What makes one platform better than the other")
exp9= st.expander("What motivated you to start your company?")
exp10= st.expander("What would you say are your biggest challenges in your founder journey?")
exp11= st.expander("How has Founderland affected your challenges as a founder?")


#region exp1
Q2 = calculate_column_percentages(df,differents_question["Why did you join Founderland? Select all that apply"])
exp1.plotly_chart (create_stacked_barplot(Q2,"Attribute","Percentage",titre="Why did you join Founderland?"),use_container_width =True)
#endregion

#region exp2
Q3 = calculate_column_percentages(df,differents_question["Select all the reasons for joining the community"])
exp2.plotly_chart (create_stacked_barplot(Q3,"Attribute","Percentage",titre="Select all the reasons for joining the community"),use_container_width =True)
#endregion

#region exp3
Q4 = calculate_event_occurrences(df,"Which program do you prefer to access or participate in?")
exp3.plotly_chart(create_horizontal_bar_chart(Q4, "Which program do you prefer to access or participate in?"),use_container_width=True)
#endregion

#region exp4
Q5 = calculate_event_occurrences(df,"What benefits have you received from the community? (Ranking)")
exp4.plotly_chart(create_horizontal_bar_chart(Q5, "What benefits have you received from the community?"),use_container_width=True)
#endregion

#region exp5
#experiments
dic = {"Gained  a lot": 3,
        "Gained some" : 2,
        "Gained nothing" : 0,
        "Gained a little" : 1,
        "Gained the most" : 4}

Q6 = df[differents_question["Gains"]].apply(lambda col: col.map(dic))
Q6 = Q6.melt(var_name="Column Name", value_name="Value")

exp5.plotly_chart(plot_box_with_mean(Q6 , x= "Value",y="Column Name",title="Result of your gain from Funderland",legend_mapping=dic),use_container_width=True)
#endregion

#region exp6
exp6.write(OP1(),use_container_width=True)
#endregion

#region exp7
exp7.write(OP2(),use_container_width=True)
#endregion

#region exp8
exp8.write(OP3(),use_container_width=True)
#endregion

#region exp9
exp9.write(OP4(),use_container_width=True)
#endregion

#region exp10
exp10.write(OP5(),use_container_width=True)
#endregion

#region exp11
exp11.write(OP6(),use_container_width=True)
#endregion

# - LIENS

LIEN = {
    "Léo Dujourd'hui": "https://leo-dujourd-hui-digital-cv.streamlit.app",
}
SOURCES ={
    "Github": "https://github.com/le-cmyk/Kickstarter-Dashboard"
}

# - Téléchargement des données 

def download_button(data, file_name, button_text):
    csv = data.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="{file_name}">{button_text}</a>'
    st.markdown(href, unsafe_allow_html=True)

c_1, c_2,c_3 = st.columns(3)
with c_1:
    for clé, link in LIEN.items():
        st.write(f"Made by : [{clé}]({link})")
with c_2:
    for clé, link in SOURCES.items():
        st.write(f"[{clé}]({link})")
with c_3:
    download_button(df, 'data.csv', '📄 Download Data')



# ---- HIDE STREAMLIT STYLE ----
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

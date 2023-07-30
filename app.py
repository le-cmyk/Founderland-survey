# to run the app : streamlit run app.py
# to have the correct version  : pipreqs --encoding=utf8 --force


import base64
import pandas as pd  # pip install pandas
import streamlit as st  # pip install streamlit

from Functions.creating_df_and_plots import calculate_column_percentages,create_stacked_barplot,calculate_event_occurrences, create_horizontal_bar_chart,plot_box_with_mean,create_pie_chart
from Functions.open_questions import OP1,OP2,OP3,OP4,OP5,OP6

# emojis: https://www.webfx.com/tools/emoji-cheat-sheet/
st.set_page_config(page_title="Responses Founderland", page_icon=":bar_chart:", layout="wide")

st.title("Founderland Survey")

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
                "Knowledge about Funding",
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
    "Frequences":[
                "How frequently do you access our Founderland community platform?",
                "How frequently do you access our Slack Channel?"
                ],
    "Slack_channel":[
                "Knowledge about funding13",
                "Access to network (partners, funders, etc)14",
                "Meeting other WoC founders across Europe15",
                "Event invitations16",
                "Safe Space17",
                "Access to funding opportunities18",
                "Learn how to scale your business19",
                "Get mentorship20",
                "Become a mentor21",
                "Find a Co-Founder22",
                ],
    "General info":[
                "Did Founderland expand your startup network?",
                "Did Founderland facilitate meaningful connections with other community founders?",
                "Has Founderland helped you to raise capital for your startup?",
                "Has Founderland helped you to increase your visibility?",
                ],

}

@st.cache_data
def read_excel (path):
    return pd.read_excel(path)

df = read_excel(path)


# ---- READ EXCEL ----
st.markdown("""---""")
st.write("## General info")

#region General info
c_1,c_2=st.columns([1,1])
c_3,c_4=st.columns([1,1])

dic = {0: "No",
        1: "Yes",}

df[differents_question["General info"]] = df[differents_question["General info"]].apply(lambda col: col.map(dic))


c_1.plotly_chart(create_pie_chart(df,column_name="Did Founderland expand your startup network?",
                                  title="Did Founderland expand your startup network?",
                                  colors=["#FF5A5F", "#00A699"]),
                                  use_container_width =True)

c_2.plotly_chart(create_pie_chart(df, column_name="Did Founderland facilitate meaningful connections with other community founders?",
                 title="Did Founderland facilitate meaningful \nconnections with other community founders?",
                 colors=["#FF5A5F", "#00A699"]),use_container_width =True)

c_3.plotly_chart(create_pie_chart(df, column_name="Has Founderland helped you to raise capital for your startup?",
                 title="Has Founderland helped you to raise capital for your startup?",
                 colors=["#FF5A5F", "#00A699"]),use_container_width =True)
c_4.plotly_chart(create_pie_chart(df, column_name="Has Founderland helped you to increase your visibility?",
                 title="Has Founderland helped you to increase your visibility?",
                 colors=["#FF5A5F", "#00A699"]),use_container_width =True)



#endregion

# --- Deep into the survey ----
st.markdown("""---""")
st.write("## Deep into the survey")

exp= st.expander("As a member of Founderland, how has your experience been?")
exp1= st.expander("Why did you join Founderland?")
exp2= st.expander("Select all the reasons for joining the community")
exp3= st.expander("Which program do you prefer to access or participate in?")
expfreq= st.expander("Frequences")
slack_chanel= st.expander("Slack Chanel info")
exp4= st.expander("What benefits have you received from the community?")
exp5= st.expander("Rate your gain from the community")



st.write("#### Now some open questions")
exp6= st.expander("Report orriented view what have you learn and your opinion")
exp7= st.expander("Feedback on how has your experience been?")
exp8= st.expander("What makes one platform better than the other")
exp9= st.expander("What motivated you to start your company?")
exp10= st.expander("What would you say are your biggest challenges in your founder journey?")
exp11= st.expander("How has Founderland affected your challenges as a founder?")



#region exp

exp.plotly_chart(create_pie_chart(df,column_name="As a member of Founderland, how has your experience been?",
                                  title="As a member of Founderland, how has your experience been?",
                                  order=['Very satisfied','Somewhat satisfied', 'Neither satisfied nor dissatisfied','Somewhat dissatisfied']
                                  ),
                                  use_container_width =True)

#endregion

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

#region expfreq
dic = {"Once a week": 3,
        "Sometimes" : 1,
        "Never" : 0,
        "Once a month" : 2,
        "More than once a week" : 4}

Qfreq = df[differents_question["Frequences"]].apply(lambda col: col.map(dic))
Qfreq = Qfreq.melt(var_name="Column Name", value_name="Value")

expfreq.plotly_chart(plot_box_with_mean(Qfreq , x= "Value",y="Column Name",title="Frequences of access",legend_mapping=dic),use_container_width=True)
#endregion

#region slack_chanel

c_1,c_2=slack_chanel.columns([1,1.2])
c_1.plotly_chart(create_pie_chart(df,column_name="How useful/effective has our Slack channel been for your endeavors?",
                                           title="How useful/effective has our Slack channel been for your endeavors?"),use_container_width =True)


Qslack = calculate_column_percentages(df,differents_question["Slack_channel"])
c_2.plotly_chart (create_stacked_barplot(Qslack,"Attribute","Percentage",titre="In what aspects has the Slack channel been useful to you?"),use_container_width =True)


#endregion

# - LIENS

LIEN = {
    "Léo Dujourd'hui": "https://leo-dujourd-hui-digital-cv.streamlit.app",
}
SOURCES ={
    "Github": "https://github.com/le-cmyk/Kickstarter-Dashboard"
}

c_1, c_2,c_3 = st.columns(3)
with c_1:
    for clé, link in LIEN.items():
        st.write(f"Made by : [{clé}]({link})")
with c_2:
    for clé, link in SOURCES.items():
        st.write(f"[{clé}]({link})")
with c_3:

    with open(path, "rb") as template_file:
        template_byte = template_file.read()

    st.download_button(label="Download responses",
                        data=template_byte,
                        file_name=path,
                        mime='application/octet-stream')




# ---- HIDE STREAMLIT STYLE ----
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

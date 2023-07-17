
import streamlit as st
from datetime import date
import os
import glob as glob
from project_utils.page_layout_helper import set_page_settings, get_page_title, main_header
import ee

ee.Authenticate()
ee.Initialize()
def active_contributors():
  ACTIVE_CONTRIBUTORS_PAGE_CHAPTERLEAD='''
| Chapter Name | Lead Name |
|--|--|
| Kutch India Chapter Leads | Chancy Shah |
'''

  ACTIVE_CONTRIBUTORS_PAGE_MEMBERS_LIST='''
| Task Name | Active Contributors |
|--|--|
| Data Collection on Types of Millet and their Parameters | - |
| Identity Satellites and Sensors to use | - |
| AI Algorithms | - |
| Dashboard | - |
'''

  with st.container():
    st.markdown(ACTIVE_CONTRIBUTORS_PAGE_CHAPTERLEAD, unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(ACTIVE_CONTRIBUTORS_PAGE_MEMBERS_LIST, unsafe_allow_html=True)


def about_project():
  ABOUT_PROJECT_CONTENT="""
#####  This project is initiated by the Omdena Kutch, India Chapter to solve Real World Problems.

### Project background
Millets are a group of small-seeded grasses that have been cultivated for thousands of years as a staple food source in many parts of the world, including India, Africa, and China. They are highly nutritious and rich in protein, fiber, vitamins, and minerals, making them an important food crop for human consumption.

One of the key benefits of millets is their resilience to drought and other environmental stressors. They require less water and fertilizer than other crops such as wheat and rice, making them a more sustainable choice for farmers in areas with limited resources. They are also able to grow in a variety of soil types and can be grown in areas with low rainfall.

In terms of their environmental benefits, millets are known to have a low carbon footprint and can help mitigate climate change by reducing greenhouse gas emissions. They are also beneficial for soil health, as their deep roots can help to prevent soil erosion and improve soil fertility.

In addition to their nutritional and environmental benefits, millets have cultural significance in many parts of the world. They have been a staple food for many indigenous communities and are an important part of their traditional diets and cultural practices.

Overall, the declaration of 2023 as the International Year of Millets highlights the importance of this crop in terms of both food security and sustainable agriculture. It is hoped that this will raise awareness about the nutritional and environmental benefits of millets and encourage their increased cultivation and consumption worldwide.

### The problem
The problem at hand is that despite the numerous benefits of millet as a nutritious and sustainable crop, both consumers and farmers lack awareness of its advantages. As a result, millet production and demand in the market remain limited. The declaration of 2023 as the International Year of Millets (IYM2023) by the United Nations (UN) General Assembly provides an opportunity to raise awareness about the importance of millets. However, there is a need to address the gaps in knowledge and resources that prevent farmers from growing millet, as well as the lack of market demand for millet-based products.

To tackle this problem, we aim to leverage advanced technology and innovative solutions to support farmers in growing millets and bridge the gaps in the market. We need to raise awareness among consumers about the nutritional and environmental benefits of millet and create demand for millet-based products. By doing so, we can help to promote sustainable agriculture, improve food security, and contribute to a healthier planet.

### Project goals
The project's goal is to: - 
+ Develop a machine-learning algorithm to suggest the best millet crop for cultivation in farmer's agricultural fields.
+ Take into account various environmental factors, such as soil moisture, temperature, and precipitation, using satellite imagery and geospatial technology.
+ Provide farmers with data-driven insights to help them make informed decisions about crop selection.
+ Optimize yields and promote sustainable agriculture practices by leveraging advanced technology.
"""

  with st.container():
    st.markdown(ABOUT_PROJECT_CONTENT, unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)


def about_project_style():
  ABOUT_PROJECT_STYLE='''
<style>
button[data-baseweb="tab"] > div[data-testid="stMarkdownContainer"] > p {
  font-size: 24px;
  background-color: rgb(240, 242, 246);
}
</style>
'''
  st.write(ABOUT_PROJECT_STYLE, unsafe_allow_html=True)


def main():
  set_page_settings()
  main_header()
  about_project_style()
  project_tab, team_tab = st.tabs(["  **About Project** ", "  **Active Team Contributors**  "])

  with project_tab:
    about_project()
   
  with team_tab:
    active_contributors()

if __name__ == "__main__":
  main()   

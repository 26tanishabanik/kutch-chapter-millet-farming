import streamlit as st
from datetime import date
import os
import glob as glob
from project_utils.page_layout_helper import set_page_settings, get_page_title, main_header
import ee
import geemap

st.set_page_config(layout="wide")

def active_contributors():
  st.subheader('COLLABORATORS')
  st.markdown('• <a href="https://www.linkedin.com/in/tanisha-banik-04b511173/">Tanisha Banik</a>', unsafe_allow_html=True)
  st.markdown('• <a href="https://www.linkedin.com/in/arthanant">Arth Anant</a>', unsafe_allow_html=True)
  st.markdown('• <a href="https://www.linkedin.com/in/crista-villatoro-2452a6129">Crista Villatoro</a>', unsafe_allow_html=True)
  st.markdown('• <a href="https://linkedin.com/in/raviatkumar">Ravi Kumar M</a>', unsafe_allow_html=True)
  st.markdown('• <a href="https://in.linkedin.com/in/priyanshu-mohanty-73347b1b6">Priyanshu Mohanty</a>', unsafe_allow_html=True)
  st.markdown('• <a href="https://www.linkedin.com/in/vinod-c-81ab3366/">Vinod Cherian</a>', unsafe_allow_html=True)
  st.markdown('• <a href="https://www.linkedin.com/in/soumyardas90/">Soumya Ranjan Das</a>', unsafe_allow_html=True)
  st.markdown('• <a href="https://www.linkedin.com/in/archishasrivastava/">Archisha Srivastava</a>', unsafe_allow_html=True)
  st.markdown('• <a href="https://www.linkedin.com/in/rajuyadavk/">Raju Kunchala</a>', unsafe_allow_html=True)
  st.markdown('• <a href="https://www.linkedin.com/in/piyush-sharma-242b95205">Piyush Sharma</a>', unsafe_allow_html=True)
  st.markdown('• <a href="http://www.linkedin.com/in/aarudhravi">Aarudh Ravi</a>', unsafe_allow_html=True)
  st.subheader('PROJECT MANAGER')
  st.markdown('• <a href="https://www.linkedin.com/in/chancy-shah-671787119/">Chancy Shah</a>', unsafe_allow_html=True)


def about_project():
  ABOUT_PROJECT_CONTENT="""
#####  This Project is initiated by the Omdena Kutch, India Chapter to Solve Real World Problems.

### Project Background
Millets are a group of small-seeded grasses that have been cultivated for thousands of years as a staple food source in many parts of the world, including India, Africa, and China. They are highly nutritious and rich in protein, fiber, vitamins, and minerals, making them an important food crop for human consumption.

One of the key benefits of millets is their resilience to drought and other environmental stressors. They require less water and fertilizer than other crops such as wheat and rice, making them a more sustainable choice for farmers in areas with limited resources. They are also able to grow in a variety of soil types and can be grown in areas with low rainfall.

In terms of their environmental benefits, millets are known to have a low carbon footprint and can help mitigate climate change by reducing greenhouse gas emissions. They are also beneficial for soil health, as their deep roots can help to prevent soil erosion and improve soil fertility.

In addition to their nutritional and environmental benefits, millets have cultural significance in many parts of the world. They have been a staple food for many indigenous communities and are an important part of their traditional diets and cultural practices.

Overall, the declaration of 2023 as the International Year of Millets highlights the importance of this crop in terms of both food security and sustainable agriculture. It is hoped that this will raise awareness about the nutritional and environmental benefits of millets and encourage their increased cultivation and consumption worldwide.

### Problem Statement
The problem at hand is that despite the numerous benefits of millet as a nutritious and sustainable crop, both consumers and farmers lack awareness of its advantages. As a result, millet production and demand in the market remain limited. The declaration of 2023 as the International Year of Millets (IYM2023) by the United Nations (UN) General Assembly provides an opportunity to raise awareness about the importance of millets. However, there is a need to address the gaps in knowledge and resources that prevent farmers from growing millet, as well as the lack of market demand for millet-based products.

To tackle this problem, we aim to leverage advanced technology and innovative solutions to support farmers in growing millets and bridge the gaps in the market. We need to raise awareness among consumers about the nutritional and environmental benefits of millet and create demand for millet-based products. By doing so, we can help to promote sustainable agriculture, improve food security, and contribute to a healthier planet.

### Project Goals
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
  project_tab, team_tab = st.tabs(["  **About Project** ", "  **Active Contributors**  "])

  with project_tab:
    about_project()
   
  with team_tab:
    active_contributors()

if __name__ == "__main__":
  main()   

import os
import base64
import pandas as pd
import folium
import streamlit as st
from folium.plugins import Draw
from streamlit_folium import st_folium
from project_utils.page_layout_helper import main_header
from project_utils.satellite_data_helper import fetch_satellite_data 
from datetime import date
from dateutil import parser
import calendar
import pickle
from PIL import Image
from tqdm import tqdm
import time

def get_start_end_date(month_text):
  date_time = f'{date.today().year}-{month_text}-01'
  selected_date = parser.parse(date_time)
  selected_month = selected_date.month
  selected_year = 2023
  selected_year_end = selected_year - 2
  last_day_month = calendar.monthrange(selected_year, selected_month)[1]
  start_date =  f'{selected_year_end}-{selected_month}-{selected_date.day}'
  end_date = f'{selected_year}-{selected_month}-{last_day_month}'
  print(start_date)
  print(end_date)
  return start_date, end_date


data = {
  "Full Name of Millet": ["Pearl millet (Pennisetum glaucum)", "Finger millet (Eleusine coracana)", "Foxtail millet (Setaria italica)", "Proso millet (Panicum miliaceum) (Chena in India)", "Little millet (Panicum sumatrense)", "Kodo millet (Paspalum scrobiculatum)", "Browntop millet (Brachiaria ramosa)", "Teff millet (Eragrostis tef)", "Japanese millet (Echinochloa esculenta)", "Indian barnyard millet (Echinochloa colona)", "African millet (Eleusine indica)", "Italian millet (Setaria italica)", "Job's tears (Coix lacryma-jobi)", "Guinea millet (Brachiaria deflexa)", "Sorghum Millet (Jowar)", "Buckwheat Millet (Kuttu)", "Amaranth Millet (Rajgira)", "Barnyard millet (Echinochloa frumentacea)", "White fonio (Digitaria exilis)", "Black fonio (Digitaria iburua)", "Ameranthus", "Great millet (Sorghum bicolor)", "Barnyard grass millet (Echinochloa crus-galli)", "Naked barley (Hordeum vulgare var. nudum)", "Panic millet (Panicum miliaceum subsp. ruderale)", "Sorghum (Sorghum bicolor)", "Sawa millet (Echinochloa stagnina)", "Barnyard Grass Millet (Echinochloa crus-galli)", "Japanese Barnyard Millet (Echinochloa frumentacea)", "Himalayan Foxtail Millet (Setaria italica subsp. himalayensis)", "Italian Barnyard Millet (Echinochloa crus-galli)", "Foxtail Barnyard Millet (Echinochloa frumentacea)", "Siberian Millet (Panicum miliaceum subsp. sibiricum)", "Italian Foxtail Millet (Setaria italica subsp. pycnocoma)"],
  "Name of Millet": ["Pearl millet", "Finger millet", "Foxtail millet", "Proso millet", "Little millet", "Kodo millet", "Browntop millet", "Teff millet", "Japanese millet", "Indian barnyard millet", "African millet", "Italian millet", "Job's tears", "Guinea millet", "Sorghum Millet", "Buckwheat Millet", "Amaranth Millet", "Barnyard millet", "White fonio", "Black fonio", "Ameranthus", "Great millet", "Barnyard grass millet", "Naked barley", "Panic millet", "Sorghum", "Sawa millet", "Barnyard Grass Millet", "Japanese Barnyard Millet", "Himalayan Foxtail Millet", "Italian Barnyard Millet", "Foxtail Barnyard Millet", "Siberian Millet", "Italian Foxtail Millet"],
  "Scientific Name": ["Pennisetum glaucum", "Eleusine coracana", "Setaria italica", "Panicum miliaceum (Chena in India)", "Panicum sumatrense", "Paspalum scrobiculatum", "Brachiaria ramosa", "Eragrostis tef", "Echinochloa esculenta", "Echinochloa colona", "Eleusine indica", "Setaria italica", "Coix lacryma-jobi", "Brachiaria deflexa", "Jowar", "Kuttu", "Rajgira", "Echinochloa frumentacea", "Digitaria exilis", "Digitaria iburua", "", "Sorghum bicolor", "Echinochloa crus-galli", "Hordeum vulgare var. nudum", "Panicum miliaceum subsp. ruderale", "Sorghum bicolor", "Echinochloa stagnina", "Echinochloa crus-galli", "Echinochloa frumentacea", "Setaria italica subsp. himalayensis", "Echinochloa crus-galli", "Echinochloa frumentacea", "Panicum miliaceum subsp. sibiricum", "Setaria italica subsp. pycnocoma"],
  "Price": ["19 (US$/Kg)", "19 (US$/Kg)", "24 (US$/Kg)", "17.2448778276923 (US$/Kg)", "20 (US$/Kg)", "20 (US$/Kg)", "17.2448778276923 (US$/Kg)", "13.27941176 (US$/Kg)", "7.48 (US$/Kg)", "17.2448778276923 (US$/Kg)", "17.2448778276923 (US$/Kg)", "21.406 (US$/Kg)", "17.2448778276923 (US$/Kg)", "24 (US$/Kg)", "2.948 (US$/Kg)", "5.61 (US$/Kg)", "21 (US$/Kg)", "17.2448778276923 (US$/Kg)", "17.2448778276923 (US$/Kg)", "17.2448778276923 (US$/Kg)", "26.46 (US$/Kg)", "17.2448778276923 (US$/Kg)", "17.2448778276923 (US$/Kg)", "17.2448778276923 (US$/Kg)", "17.2448778276923 (US$/Kg)", "17.2448778276923 (US$/Kg)", "17.2448778276923 (US$/Kg)", "17.2448778276923 (US$/Kg)", "17.2448778276923 (US$/Kg)", "17.2448778276923 (US$/Kg)", "17.2448778276923 (US$/Kg)", "17.2448778276923 (US$/Kg)", "17.2448778276923 (US$/Kg)", "17.2448778276923 (US$/Kg)"],
  "Millet Pic": ["Pearl.jpg", "Finger.jpg", "Foxtail.jpg", "Proso.jpg", "Little.jpg", "Kodo.jpg", "Browntop.jpg", "Teff.jpg", "Japanese.jpg", "Indian barnyard.jpg", "African.jpg", "Foxtail.jpg", "Jobs tears.jpg", "Guinea.jpg", "Sorghum.jpg", "Buckwheat.jpg", "Amaranth.jpg", "Barnyard.jpg", "White fonio.jpg", "Black fonio.jpg", "Chaulai.jpg", "Sorghum.jpg", "Barnyard grass millet.jpg", "Naked barley.jpg", "Panic millet.jpg", "Sorghum.jpg", "Sawa millet.jpg", "Barnyard grass millet.jpg", "Japanese barnyard millet.jpg", "Himalayan foxtail millet.jpg", "Italian barnyard millet.jpg", "Foxtail barnyard millet.jpg", "Siberian millet.jpg", "Italian foxtail millet.jpg"],
  "Recommendations": ["Pearl millet can be grown in different soils. It does not grow well in soils prone to waterloggedconditions. The field should be ploughed once or twice followed by harrowing to create fine tilth ", 
                      "Finger millet is grown in different seasons in different parts of the county as arainfed crop. Moreover, it is also a rich source of thiamine, riboflavin, iron, methionine, isoleucine, leucine, phenylalanine and other essential amino acids. The abundance of these phytochemicals enhances the nutraceutical potential of finger millet, making it a powerhouse of health benefiting nutrients.", 
                      "Foxtail Millet can be grown in both tropical and temperate climates, with low and moderate rainfall. Even at an altitude of 2000 metres and 500-700 mm of yearly rainfall, the crop may be cultivated. It needs moderately fertile and well-drained soil. They are not tolerant to flooded soils or severe drought.", 
                      "The crop is able to evade drought by its quick maturity. Being a short duration crop (60 -90 days) with relatively low water requirement, this escapes drought period and, therefore, offers better prospects for intensive cultivation in dry land areas. Under unirrigated conditions, proso millet is generally grown during kharif season but in areas where irrigation facilities are available, this is profitably grown as summer catch crop in high intensity rotations.", 
                      "Little millet (Panicum sumatrense) is a dryland drought-tolerant millet that can be cultivated in a variety of soil types, even those that are flooded. For successful development, deep, loamy, fertile soils rich in organic matter are preferred. Salinity and alkalinity are tolerable to some extent. A month before planting, apply 5–10 tonnes/ha of compost or farmyard manure. 40 kg of nitrogen, 20 kg of P2O5, and 20 kg of potassium per hectare are typically the required fertilizers for healthy crops. In a crop that was seeded in lines, two inter-cultivations and one-hand weeding are advised.", 
                      "Kodo millet (Paspalum scrobiculatum) is propagated from seed, ideally in row planting instead of broadcast sowing. Its preferred soil type is a very fertile, clay-based soil. The recommended dose for optimal growth is 40 kg of nitrogen plus 20 kg of phosphorus per hectare. A case study in India Rewa district in 1997 showed a 72% increase in kodo millet grain yields as opposed to no fertilizer. Lodging issues may accompany this.", 
                      "Browntop millet (Brachiaria ramosa) is an introduced, annual/perennial warm-season grass often used in forage/pasture management systems. The stem (culm) may be erect or prostrate along the ground. When growing erect, it may reach 3 ft at maturity. Nodes will appear minutely hairy. The lance-shaped, hairless leaf-blades are ¾–10 inches long (2–25 cm) and 1/8–½ inch (4–14 mm) wide. The inflorescence is indeterminate, open, spreading, with a simple axis and stalked flowers. It has 3–15 inflorescences, ⅓–3 inches (1–8 cm) in length, from a central axis. It has white flowers and ellipsoid seeds that are tan in color. It has fibrous roots that can grow to 2 ft deep. Browntop millet grows best under full sunlight. Its best not to crowd them together so they can get exposure to the sun evenly. The leaves should not be starved with sunlight.", 
                      "Teff (Eragrostis tef) grass is a minor millet belonging to grass family Poaceae.Being a minor-millet it can withstand adverse conditions of soil and climaticfactors. Ethiopia is the major teff grass producing country, a staple food for mostof the population of the country. Today’s world is more concerned about healthylife which depends on consumption of nutritionally rich food products. Teff isnutritionally rich millet as compared to other cereals and is gluten free, can besubstituted for wheat which causes celiac disease due to gluten protein. It iscultivated on marginal soils under traditional practices, which are the major causesfor low yields of teff crop. Agronomic practices mainly planting method andnutrient management play an important role in increasing teff yields.", 
                      "Japanese millet (Echinochloa esculenta) can be successfully seeded into duck field impoundments, drained marshland, pond and lake edges, bottomland stands, and beaver ponds. It should be seeded in full sun from mid-June in the Northeast to July–August in the Southeast, at 20–25 lb/ac, ¼–½ in deep or 8–12 lb/ac in a mix.", 
                      "Barnyard millet (Echinochloa spp.) is a climate resilient multipurpose crop. It is one of the hardiest multipurpose crops with wide adaptability to adverse climatic conditions. It is regionally abundant but globally rare, scientific knowledge is also scant about its genetic resources and thus it is facing limited use relative to the potential benefits it can offer. Its remarkable climate resilient properties make its survival easy in harsh and fragile environments as it requires minimal agricultural inputs. Germplasm of barnyard millet can prove to be a reservoir of unique alleles to the breeders. Echinochloa colona is a possible source of resistance to grain smut (Ustilago) and improved dietary iron nutrition³. Both E. colona and E. crus-galii could be used in breeding for improved dietary calcium.", 
                      "Eleusine indica, also known as goose grass, is a weedy summer annual grass that has a flattened, white/silver base. It thrives in disturbed areas with compacted soils in full sun such as grasslands, marshes, stream banks, farmland, and road sides. In its native habitats of tropical and subtropical locations it can quickly spread in farming locations, becoming a dominant weed, thereby effecting the crops being grown. It is the most common weed in both agricultural and environmental environments.", 
                      "Italian millet, also known as Foxtail millet (Setaria italica), is thought to be native to southern Asia and is considered one of the oldest cultivated millets. It is an introduced, annual, warm-season crop that grows 2–5 ft (60-152 cm) tall. It can grow in sandy to loamy soils with pH from 5.5–7. It will grow rapidly in warm weather and can grow in semi-arid conditions, however, it has a shallow root system that does not easily recover from drought. It can produce one ton of forage on 2 ½ in of moisture and requires approximately 1/3 less water than corn. It has a high level of tolerance to salinity. It can grow at higher elevations (1500 m) as well as in plains. You can start Ornamental Millet seeds indoors in early spring. Cover the Setaria italica seeds lightly and keep them moist. Once the seedlings are large enough to handle, separate them out and grow them individually in their own pot. Once frost danger has passed the Foxtail Millet grass can be transplanted outside.", 
                      "Jobs tears (Coix lacryma-jobi), also known as adlay or adlay millet, is a tall grain-bearing perennial tropical plant of the family Poaceae (grass family). It is native to Southeast Asia and introduced to Northern China and India in remote antiquity, and elsewhere cultivated in gardens as an annual. In its native environment it is grown at higher elevation areas where rice and corn do not grow well. Jobs tears may be intercropped with maize or sorghum as a supplemental grain or as an alternative in case the main crop fails⁵. Used in these ways, it enhances the resilience of farms in the warm, humid tropics.", 
                      "Guinea millet (Brachiaria deflexa) is an annual millet grass belonging to the grass family (Poaceae). It is native to many regions such as Africa, India, and Pakistan in both tropical and subtropical regions. It has been used as a supplemental food source among other cereal crops. Guinea millet is believed to have originated in the African savanna in the Fouta Djallon plateau of northwestern Guinea. It can grow in a variety of conditions but generally prefers shady conditions with well-drained soil for best growth. This grass is considered to be drought-resistant. It prefers to be along the edge of floodplains and pans where it is temporarily wet and is frequently found as a short grass among tall trees.", 
                      "Sorghum millet, also known as Jowar, grows in warm, arid climates receiving around 45-100 cms of rainfall annually. Temperature requirements are around 20-35 degrees Celsius in Kharif season and around 15 degrees Celsius in Rabi season. It grows well in sandy loamy soils having good drainage and humus with a pH range from 6-7.5.", 
                      "Buckwheat, also known as Kuttu in India, is a herbaceous plant of the Polygonaceae family and its edible seeds are cultivated for its grain-like seeds and as a cover crop. It is notable for being a short-season crop, needs 10 to 12 weeks to mature, and for requiring only moderate soil fertility. Buckwheat will perform well on well-managed soil with moderate fertility. It tolerates soil pH level as low as 4.8. Though, it does not tolerate stressful conditions or poorly prepared soil and its fine roots penetrate the soil quickly, but do not tolerate compaction, flooding or drought.", 
                      "Amaranth millet, also known as Rajgira and Ramdana, is a versatile group of grains which are rich in protein and fibre. It also helps in fighting greying and hair loss. Amaranth also lowers cholesterol levels and cardiovascular disease risk. It is also high in Calcium, vitamins, and other minerals.", 
                      "Barnyard millet (Echinochloa species) has become one of the most important minor millet crops in Asia, showing a firm upsurge in world production. The genus Echinochloa comprises of two major species, Echinochloa esculenta and Echinochloa frumentacea, which are predominantly cultivated for human consumption and livestock feed.", 
                      "White fonio (Digitaria exilis) is an annual tropical grass grown in West Africa for its starch-rich, tiny seeds. It is an early maturing cereal, highly adapted to poor soils, and remarkably drought tolerant. Fonio is grown in tropical climates with a marked dry season, average temperatures of 25 to 30°C and between 900 and 1000 mm of rainfall. It is not generally grown in rotation systems, and is planted on light (sandy to stony) soils.", 
                      "Black fonio (Digitaria iburua) is a type of millet that is grown mainly in parts of Nigeria, Togo, and Benin. It is one of the oldest native cereal crops of cultural, nutritional, and economic importance in West Africa. Fonio has excellent nutritional properties and contains high-quality vitamins, minerals, fiber, and sulfur-containing methionine and cysteine.", 
                      "Amaranth grain or chaulai is a cosmopolitan perennial plant. It is one of the most ancient cultivated grains in human history, with its origins being traced back to more than 8000 years ago. Amaranth is extremely beneficial for the body as it possesses rich rich essential nutrients. All parts of Amaranth plants including grains, leaves, and others are beneficial for the body. Although Amaranth is not popular as other grains, it is one of the most nutritious grains having a rich concentration of vitamins, fiber, and minerals. Amaranth has become one of the most in-demand grains due to the fact that it is a healthy protein source.", 
                      "Sorghum bicolor, also known as great millet, durra, jowari, jowar or milo, is a common crop in the U.S. and has been called the great millet in Africa, where it originated. It is mainly cultivated in West Africa as an important crop for millet gruel and millet beer. Sorghum can also be used for bioethanol or as green fodder for animals.", 
                      "Barnyard millet can grow in flooded soils and standing water as long as a portion of the plant remains above the waters surface. It is better suited for colder climates and wetter soils than other annual summer grasses such as sorghum (Sorghum bicolor), browntop millet (Urochloa ramosa), and corn (Zea mays); however it has limited frost tolerance and will winter kill. It can grow at low and medium altitudes. It is adapted to soils with pH as low as 4.5 and salinity of 2,000–3,000 parts per million, but grows best in sandy–clay loams with pH values from 4.6–7.4.", 
                      "Naked barley (Hordeum vulgare var. nudum) is a unique variety of cultivated barley. It is one of the oldest grains to be cultivated, having been grown for over 8000 years. Naked barley is an excellent source of complex carbohydrates that helps lower cholesterol levels and the risk of type-2 diabetes.", 
                      "Panic millet (Panicum miliaceum) is an introduced, warm-season annual grass that grows 1–3½ ft tall. It is both heat and drought-tolerant and is widely grown in the tropics and sub-tropics. It is a good idea to treat the ornamental millet with a feeding of 15-0-15 fertilizer once when you first transplant it or after emergence if the seeds were directly sown.", 
                      "Sorghum (Sorghum bicolor), also known as milo, is a common crop in the U.S. and has been called the 'great millet' in Africa, where it originated. It is used as a drought-tolerant, summer annual rotational cover crop either alone or seeded in a warm-season cover crop mixture. There are multiple cultivars of sorghum available for use as a cover crop including sorghum-Sudangrass hybrids (Sorghum bicolor x Sorghum bicolor var. sudanense). Sorghum cover crops can also be used as livestock forage in a cropping system.", 
                      "Sawa millet, also known as Indian barnyard millet, is a traditional food plant in Africa and has the potential to improve nutrition, boost food security, foster rural development, and support sustainable landcare. It is also known as Kodisama in Telugu, Kuthirai vaali in Tamil, and Bhagar or Varai in Marathi.", 
                      "Barnyard grass millet (Echinochloa crus-galli), also called barnyard millet or cockspur grass, is a coarse tufted grass of the family Poaceae and is considered a noxious agricultural weed. Although native to tropical Asia, barnyard grass can be found throughout the world, thriving in moist cultivated and waste areas.", 
                      "Japanese Barnyard Millet (Echinochloa frumentacea) is a domesticated species derived from wild millet barnyardgrass (E. crus-galli) and is grown primarily as forage and wildlife habitat in the United States. It is one of the most important minor millet crops in Asia, showing a firm upsurge in world production. It is predominantly cultivated for human consumption and livestock feed, and is less susceptible to biotic and abiotic stresses.", 
                      "Himalayan Foxtail Millet (Setaria italica subsp. himalayensis) is a subspecies of Foxtail Millet (Setaria italica). Foxtail millet is thought to be native to southern Asia and is considered one of the oldest cultivated millets. It is an introduced, annual, warm-season crop that grows 2–5 ft (60-152 cm) tall. It can grow in sandy to loamy soils with pH from 5.5–7. It will grow rapidly in warm weather and can grow in semi-arid conditions, however, it has a shallow root system that does not easily recover from drought.", 
                      "Italian Barnyard Millet (Echinochloa crus-galli) is a subspecies of Barnyard Millet (Echinochloa species). Barnyard millet is an ancient millet crop grown in warm and temperate regions of the world and widely cultivated in Asia, particularly India, China, Japan, and Korea. It is the fourth most produced minor millet, providing food security to many poor people across the world.", 
                      "Foxtail Barnyard Millet (Echinochloa frumentacea) is a subspecies of Barnyard Millet (Echinochloa species). Barnyard millet is an ancient millet crop grown in warm and temperate regions of the world and widely cultivated in Asia, particularly India, China, Japan, and Korea. It is the fourth most produced minor millet, providing food security to many poor people across the world.", 
                      "Siberian Millet is a warm-season annual grass and a foxtail type millet. It is a shorter variety that is commonly planted as a single-cut hay millet. Siberian Millet is the fastest maturing hay millet and will reach maturity about a week earlier than German or White Wonder Millet. It works well grown as a forage in very dry conditions or in northern climates with a short growing season. It produces hay that will cure easily and be palatable for livestock. Siberian Millet is very drought tolerant and will grow rapidly during hot summer conditions.", 
                      "Foxtail millet, Setaria italica is still cultivated in Mazandaran (N-Iran). It is used for the preparation of local food and for feeding cage-birds. The cultivated race is convar. moharia, formerly widely grown from Europe to SW Asia. The newly found material allows conclusion with respect to evolution and distribution of this old crop. Foxtail millet is an annual grass with slim, vertical, leafy stems which can reach a height of 120–200 cm (3 ft 11 in – 6 ft 7 in). The seedhead is a dense, hairy panicle 5–30 cm (2 in – 1 ft 0 in) long. The small seeds, around 2 millimetres (3⁄32 in) in diameter, are encased in a thin, papery hull which is easily removed in threshing. Seed color varies greatly between varieties."
                      ]
                      }

@st.cache_resource()
def model_load():
  filename = 'src/tasks/task-4-dashboard/streamlit_app/Model/millet-model.pkl'
  model = pickle.load(open(os.path.abspath(filename), 'rb'))
  return model
  
def model_predict(start_date, end_date, roi):
  model = model_load()
  Soil_type_C_L_S=Soil_type_F_M=Soil_type_HSL=Soil_type_LC_SL=Soil_type_S_A=Soil_type_S_L=Soil_type_SL=Soil_type_SL_A=Soil_type_SLC=0.0
  Soil_type_L=1.0
  temperature_min, temperature_max, pH_min, pH_max, rainfall_min, rainfall_max, windspeed_min, windspeed_max, soil_moisture_min, soil_moisture_max, humidity_min, humidity_max, elevation_min, elevation_max, soil_salinity_min_value, soil_salinity_max_value =fetch_satellite_data(start_date, end_date, roi)
  print("temperature_min: ",temperature_min)
  print("temperature_max: ",temperature_max)
  print("pH_min :", pH_min)
  print("pH_max", pH_max)
  print("rainfall_min:", rainfall_min)
  print("rainfall_max :", rainfall_max)
  print("windspeed_min:", windspeed_min)
  print("windspeed_max:", windspeed_max)
  print("soil_moisture_min:",soil_moisture_min)
  print("soil_moisture_max:", soil_moisture_max)
  print("humidity_min:", humidity_min)
  print("humidity_max:", humidity_max)
  print("elevation_min", elevation_min)
  print("elevation_max :", elevation_max)
  print("soil_salinity_min_value :", soil_salinity_min_value)
  print("soil_salinity_max_value :", soil_salinity_max_value)

  
  #new_data = pd.DataFrame([Soil_type_C_L_S, Soil_type_F_M, Soil_type_HSL, Soil_type_L, Soil_type_LC_SL, Soil_type_S_A, Soil_type_S_L, Soil_type_SL, Soil_type_SL_A, Soil_type_SLC, 1, 1, temperature_min, temperature_max, pH_min, pH_max, soil_salinity_min_value, soil_salinity_max_value, rainfall_min, rainfall_max, elevation_min, elevation_max, 0, 31.75, soil_moisture_min, soil_moisture_max, 11.81, 13.90, 1.00, 2.15, 10.65, 17.84, 71.21, 96.81, 1.84, 6.47, 18.54, 27.65, 10.40, 2.96, 1.87, 5.10, 72.12, 350.635, 52.60, 4.88, 0.30, 0.14, 1.57, 17.24])  
  new_data = pd.DataFrame({
    'Soil type_C,L,S':[Soil_type_C_L_S], 
    'Soil type_F/M':[Soil_type_F_M], 
    'Soil type_HSL':[Soil_type_HSL], 
    'Soil type_L':[Soil_type_L],
    'Soil type_LC, SL':[Soil_type_LC_SL], 
    'Soil type_S, A':[Soil_type_S_A], 
    'Soil type_S, L':[Soil_type_S_L], 
    'Soil type_SL':[Soil_type_SL],
    'Soil type_SL, A':[Soil_type_SL_A], 
    'Soil type_SLC':[Soil_type_SLC],
    'Drought resistant': [1],
    'Flood Resistant': [1],
    'Min Temperature (ºC)': [temperature_min],#[20.88],
    'Max Temperature (ºC)': [temperature_max],#[31.61],
    'pH level of the soil Min': [pH_min],#[5.57],
    'pH level of the soil Max': [pH_max],#[7.15],
    'Soil Salinity (dS/m) Min': [soil_salinity_min_value],#[1.52],
    'Soil Salinity (dS/m) Max': [soil_salinity_max_value],#[3.80],
    'Rainfall Required (cm) Min': [rainfall_min],#[370],
    'Rainfall Required (cm) Max': [rainfall_max],#[559.42],
    'Altitude range (m) Min': [elevation_min],#[96.18],
    'Altitude range (m) Max': [elevation_max],#[1947.06],
    'Soil Temperature (ºC) Min': [0],
    'Soil Temperature (ºC) Max': [31.75],
    'Soil moisture\nmin': [soil_moisture_min],#[20.5],
    'Soil moisture\nmax': [soil_moisture_max],#[68.08],
    'Light Duration (hours) Min': ["11.81"],
    'Light Duration (hours) Max': [13.90],
    'Land usage for each crop (t/ha) Min': [1.00],
    'Land usage for each crop (t/ha) Max': [2.15],
    'Seeding Rate (kg/ha) Min': [10.65],
    'Seeding Rate (kg/ha) Max': [17.84],
    'Maturity time (days) Min': [71.21],
    'Maturity time (days) Max': [96.81],
    'Planting Depth (cm) Min': [1.84],
    'Planting Depth (cm) Max': [6.47],
    'Planting Geometry 1 (cm)': [18.54],
    'Planting Geometry 2 (cm) ': [27.65],
    'Protein (g)': [10.40],
    'Fat (g)': [2.96],
    'Ash (g)': [1.87],
    'Crude Fibre (g)': [5.10],
    'Carbo- hydrates (g)': [72.12],
    'Energy (kcal)': [350.635],
    'Calcium (mg)': [52.60],
    'Iron (mg)': [4.88],
    'Thiamine (mg)': [0.30],
    'Ribo- flavin (mg)': [0.14],
    'Nia- cin (mg)': [1.57],
    'Price (US$ / Kg)': [17.24]
})
  prediction_result=model.predict(new_data)
  return prediction_result

def main():
  main_header()
  df = pd.DataFrame(data)

  with st.form("my_form"):
    m = folium.Map(width=800, height=600)
    # Add base maps using TileLayer
    folium.TileLayer('OpenStreetMap').add_to(m)  # Default base map

    # Add additional base maps
    folium.TileLayer('CartoDB positron').add_to(m)
    folium.TileLayer('CartoDB dark_matter').add_to(m)
    folium.TileLayer('Stamen Terrain').add_to(m)
    folium.TileLayer('Stamen Toner').add_to(m)
    folium.TileLayer('Stamen Watercolor').add_to(m)

    # Define Google Satellite and Hybrid maps
    google_satellite = folium.TileLayer( tiles='https://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}', attr='Google Satellite', name='Google Satellite', overlay=False,)
    google_hybrid = folium.TileLayer( tiles='https://mt1.google.com/vt/lyrs=s,h&x={x}&y={y}&z={z}', attr='Google Hybrid', name='Google Hybrid', overlay=False, )
    
    # Add Google Satellite and Hybrid maps to the layer control
    layer_control = folium.LayerControl().add_to(m)
    google_satellite.add_to(layer_control)
    google_hybrid.add_to(layer_control)
    
    Draw(export = False, draw_options={ "polygon" : False, "polyline" : False, "circle" : False, "marker" : False, "circlemarker" : False},edit_options=False).add_to(m)
    polygon_coordinates = st_folium(m, width=800, height=500)

    option = st.selectbox('Please select the month of sowing : ', 
('January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'))

    submitted = st.form_submit_button("Submit")
    if submitted:
      #st.write(polygon_coordinates["last_active_drawing"])
      if polygon_coordinates["last_active_drawing"] is None:
        st.error("Please select the Farm area from the Map above")
      else:
        #st.write(type(polygon_coordinates))
        #st.write('You selected month : ', option)
        start_date, end_date=get_start_end_date(option)
        #st.write(f'Start Date: {start_date}, and End date: {end_date}')
        #st.write('You selected the map coordinates : ')
        #st.write(str(polygon_coordinates["last_active_drawing"]["geometry"]["coordinates"]))
        #st.write(help(polygon_coordinates))
        #st.table(df)
        #prediction_result=model_predict(start_date, end_date, polygon_coordinates["last_active_drawing"]["geometry"]["coordinates"])[0]
        
        progress_bar = st.progress(0)
        status_text = st.empty()

        with status_text:
            status_text.text("Predicting... Please wait.")
          
        prediction_result = None
        for i in tqdm(range(100), desc="Progress", leave=False):
            # Simulating some time-consuming operation
            time.sleep(0.1)

            # Check if prediction result is available
            if i == 50:
                prediction_result=model_predict(start_date, end_date, polygon_coordinates["last_active_drawing"]["geometry"]["coordinates"])[0]
                progress_bar.progress(100)
            else:
                progress_bar.progress(i + 1)
        
        status_text.empty()
        #st.write(prediction_result)
        df_new=df.loc[df["Full Name of Millet"]==prediction_result]       
        for index,row in df_new.iterrows():
          with st.expander(row["Full Name of Millet"]):
            st.subheader(f'**Name of Millet :** {row["Name of Millet"]}')
            col1, col2, col3 = st.columns(3)
            with col1:
              image = Image.open(f'src/tasks/task-4-dashboard/streamlit_app/images/{row["Millet Pic"]}')
              st.image(image ,width=200)
              print(f'D:/Omdena-Kutch/Millet_Farming/kutch-chapter-millet-farming-main/streamlit_app/images/{row["Millet Pic"]}')

            with col2:
              st.markdown(f'**Scientific Name :** {row["Scientific Name"]}', unsafe_allow_html=True)
              st.markdown(f'**Price :** $ {row["Price"]}', unsafe_allow_html=True)

            st.write(row["Recommendations"])

if __name__ == "__main__":
  main() 


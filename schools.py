"""
Process the JSON file named univ.json. Create 3 maps per instructions below.
The size of the point on the map should be based on the size of total enrollment. Display only those schools 
that are part of the ACC, Big 12, Big Ten, Pac-12 and SEC divisons (refer to valueLabels.csv file)
The school name and the specific map criteria should be displayed when you hover over it.
(For example for Map 1, when you hover over Baylor, it should display "Baylor University, 81%")
Choose appropriate tiles for each map.


Map 1)  Graduation rate for Women is over 50%

Map 2) Percent of total enrollment that are Black or African American over 10%
Map 3) Total price for in-state students living off campus over $50,000

"""

# Map 1)  Graduation rate for Women is over 50%

import json

import matplotlib.pyplot as plt
import plotly.plotly as py

infile = open("univ.json", "r")

school_names = json.load(infile)

hover_texts, enrolls, lons, lats = [], [], [], []

for school in school_names:

    P5 = int(school["NCAA"]["NAIA conference number football (IC2020)"])

    if P5 == 372 or P5 == 108 or P5 == 107 or P5 == 127 or P5 == 130:

        if school["Graduation rate  women (DRVGR2020)"] > 50:
            lon = int(school["Longitude location of institution (HD2020)"])
            lat = int(school["Latitude location of institution (HD2020)"])
            lons.append(lon)
            lats.append(lat)
            women_grad = school["Graduation rate  women (DRVGR2020)"]
            university = school["instnm"]
            hover_text = university + ", " + str(women_grad) + "%"
            hover_texts.append(hover_text)
            enroll = school["Total  enrollment (DRVEF2020)"]
            enrolls.append(enroll)

print(enrolls[:10])
print(hover_texts[:10])

from plotly.graph_objs import Scattergeo, Layout
from plotly import offline

numbers = [
    {
        "type": "scattergeo",
        "lon": lons,
        "lat": lats,
        "text": hover_texts,
        "marker": {
            "size": [0.0003 * enroll for enroll in enrolls],
            "color": enrolls,
            "colorscale": "Viridis",
            "reversescale": True,
            "colorbar": {"title": "Enrollment"},
        },
    }
]

my_layout = Layout(title="Power 5 graduation Rate for Women")
fig = {"data": numbers, "layout": my_layout}
offline.plot(fig, filename="women.html")


# Map 2)

for school in school_names:
    P5 = school["NCAA"]["NAIA conference number football (IC2020)"]
    if P5 == 372 or P5 == 108 or P5 == 107 or P5 == 127 or P5 == 130:
        if (
            school[
                "Percent of total enrollment that are Black or African American (DRVEF2020)"
            ]
            > 10
        ):
            lon = int(school["Longitude location of university (HD2020)"])
            lat = int(school["Latitude location of university (HD2020)"])
            lons.append(lon)
            lats.append(lat)
            aa_b_enrollment = int(
                school[
                    "Percent of total enrollment that are Black or African American (DRVEF2020)"
                ]
            )
            university = school["instnm"]
            hover_text = university + ", " + str(aa_b_enrollment) + "%"
            hover_texts.append(hover_text)
            student = school["Total  enrollment (DRVEF2020)"]
            enrolls.append(student)


print(enrolls[:10])
print(hover_texts[:10])

numbers = [
    {
        "type": "scattergeo",
        "lon": lons,
        "lat": lats,
        "text": hover_texts,
        "marker": {
            "size": [0.0005 * enroll for enroll in enrolls],
            "color": enrolls,
            "colorscale": "Viridis",
            "reversescale": True,
            "colorbar": {"title": "Enrollment"},
        },
    }
]


setup = Layout(title="% of Power Five Enrollment that is African American")
layout = {"data": numbers, "layout": setup}
offline.plot(layout, filename="aa_enrollment.html")

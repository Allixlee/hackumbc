from flask import Flask, render_template_string
import folium
from folium.plugins import HeatMap
import csv

app = Flask(__name__)

@app.route("/")
def home():
    # initialize map
    m = folium.Map(location=[39.255535, -76.711329],
                    zoom_start=15.5, width=1200, height=630)
    # m = folium.Map(location=[39.255535, -76.711329],
    #                 zoom_start=15.5, width=800, height=500, tiles="CartoDB Voyager")

    # m = folium.Map(location=[39.255535, -76.711329],
    # zoom_start=15.5, width=800, height=500, tiles="https://tiles.stadiamaps.com/tiles/alidade_smooth_dark/0/20/{y}{r}.png}",
    # attr = '&copy; <a href="https://www.stadiamaps.com/" target="_blank">Stadia Maps</a> &copy; <a href="https://openmaptiles.org/" target="_blank">OpenMapTiles</a> &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors')
    
    # adds lamps layer
    lamps = folium.FeatureGroup(name="Lamps", show=False).add_to(m)
    lamp_coords = []
    gradient = {.33: 'yellow', .66: 'orange', 1: 'white'}
    with open("lamps.csv", mode = "r") as file:
        csvFile = csv.reader(file)
        for line in csvFile:
            lamp_coords.append([float(line[1]), float(line[2])])
            folium.Marker([line[1], line[2]], popup="lamp", icon=folium.Icon(color="beige",icon="fa-solid fa-lightbulb",prefix="fa")).add_to(lamps)
    HeatMap(lamp_coords, name="Lamp Light", min_opacity=3, gradient=gradient, radius=7, show=False).add_to(m)

    # add sos phones to emergency resource layer
    sos = folium.FeatureGroup(name="Emergency Resources", show=False).add_to(m)
    with open("sos.csv", mode = "r") as file:
        csvFile = csv.reader(file)
        for line in csvFile:
            folium.Marker([line[1], line[2]], popup="SOS Phone", icon=folium.Icon(color="blue",icon="fa-regular fa-bell",prefix="fa")).add_to(sos)
    # add police station to emergency resource layer
    folium.Marker([39.25984373757963, -76.71630620628858], popup="Baltimore County Police Department", icon=folium.Icon(color="darkblue",icon="fa-solid fa-shield-dog",prefix="fa")).add_to(sos)
    folium.Marker([39.25727885338491, -76.7141845789751], popup="UMBC Campus Police Department", icon=folium.Icon(color="darkblue",icon="fa-solid fa-shield-dog",prefix="fa")).add_to(sos)


    # add construction closures layer
    construction = folium.FeatureGroup(name="Construction Closures", show=False).add_to(m)
    with open("construction.csv", mode = "r") as file:
        csvFile = csv.reader(file)
        for line in csvFile:
            folium.Marker([line[1], line[2]], popup="Closed for construction", icon=folium.Icon(color="red",icon="fa-solid fa-xmark",prefix="fa")).add_to(construction)

    # add lactation rooms layer
    lactation = folium.FeatureGroup(name="Lactation Rooms", show=False).add_to(m)
    with open("lactation_rooms.csv", mode = "r") as file:
        csvFile = csv.reader(file)
        for line in csvFile:
            folium.Marker([line[1], line[2]], popup=line[0], icon=folium.Icon(color="lightred",icon="fa-solid fa-person-breastfeeding",prefix="fa")).add_to(lactation)

    # add construction closures layer
    family_restrooms = folium.FeatureGroup(name="Family Friendly Restrooms", show=False).add_to(m)
    with open("family_restrooms.csv", mode = "r") as file:
        csvFile = csv.reader(file)
        for line in csvFile:
            folium.Marker([line[1], line[2]], popup=line[0], icon=folium.Icon(color="lightblue",icon="fa-solid fa-baby",prefix="fa")).add_to(family_restrooms)



    # adds layer controls to map
    folium.LayerControl().add_to(m)


    # convert folium map to html
    m.get_root().render()
    header = m.get_root().header.render()
    body_html = m.get_root().html.render()
    script = m.get_root().script.render()
    
    return render_template_string("""
    <!DOCTYPE html>
    <html>
        <head>
        </head>
        {{header|safe}}
        <body>
            <h1>RetrieverSafe</h1>
            {{body_html|safe}}
            <script>
                {{script|safe}}
            </script>
        <body>
    </html>
    """, header=header, body_html=body_html, script=script)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port = 5000, debug=True)
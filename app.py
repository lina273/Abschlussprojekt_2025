import streamlit as st
import json
import numpy as np
import matplotlib.pyplot as plt

# Titel der Anwendung
st.title("Interaktives Mechanismus-Koordinatensystem")

# Initialisiere Session State für Punkte & Glieder
if "points" not in st.session_state:
    st.session_state["points"] = []
if "links" not in st.session_state:
    st.session_state["links"] = []

# Layout: Zwei Spalten (Links: Koordinatensystem, Rechts: Einstellungen)
col1, col2 = st.columns([2, 1])

# Rechte Spalte: Drop-down-Menüs und Koordinaten-Eingabe
with col2:
    st.header("Punkte & Glieder")

    # Punkt hinzufügen
    st.subheader("Punkte hinzufügen")
    x_coord = st.number_input("X-Koordinate", value=0.0, step=0.5)
    y_coord = st.number_input("Y-Koordinate", value=0.0, step=0.5)
    
    if st.button("Punkt setzen"):
        st.session_state["points"].append({"x": x_coord, "y": y_coord})

    # Punkt-Auswahl für Glieder
    if len(st.session_state["points"]) >= 2:
        st.subheader("Glieder verbinden")
        point_options = [f"P{i+1}" for i in range(len(st.session_state["points"]))]
        
        start_point = st.selectbox("Startpunkt", point_options, key="start")
        end_point = st.selectbox("Endpunkt", point_options, key="end")

        if st.button("Glied hinzufügen"):
            start_idx = point_options.index(start_point)
            end_idx = point_options.index(end_point)
            st.session_state["links"].append({"start": start_idx, "end": end_idx})

    # **Daten speichern, damit `example.py` sie nutzen kann**
    if st.button("Daten speichern für Simulation"):
        data = {
            "points": st.session_state["points"],
            "links": st.session_state["links"]
        }
        with open("mechanism_data.json", "w") as file:
            json.dump(data, file)
        st.success("Daten gespeichert! `example.py` kann sie jetzt nutzen.")

# Linke Spalte: Koordinatensystem anzeigen
with col1:
    st.subheader("Koordinatensystem")
    fig, ax = plt.subplots()
    ax.set_xlim(-10, 10)
    ax.set_ylim(-10, 10)
    ax.set_xlabel("X-Achse")
    ax.set_ylabel("Y-Achse")
    ax.grid(True)

    # Punkte plotten
    for i, p in enumerate(st.session_state["points"]):
        ax.scatter(p["x"], p["y"], color="red", s=100)
        ax.text(p["x"] + 0.2, p["y"], f"P{i+1}", fontsize=12, color="black")

    # Glieder plotten
    for link in st.session_state["links"]:
        x_vals = [st.session_state["points"][link["start"]]["x"], st.session_state["points"][link["end"]]["x"]]
        y_vals = [st.session_state["points"][link["start"]]["y"], st.session_state["points"][link["end"]]["y"]]
        ax.plot(x_vals, y_vals, "b-", linewidth=2)

    st.pyplot(fig)

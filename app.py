import streamlit as st
import json
import numpy as np
import matplotlib.pyplot as plt

# Setzt das Layout auf volle Breite
st.set_page_config(layout="wide")

# Custom CSS für **nur Breite, Höhe und Schriftgröße** der Buttons
st.markdown("""
    <style>
        /* Punkt hinzufügen - Höher */
        div[data-testid="stButton"] > button[title="Punkt hinzufügen"] {
            width: 300px !important;
            height: 70px !important;
            font-size: 16px !important;
        }

        /* Daten speichern - Breiter */
        div[data-testid="stButton"] > button[title="Daten speichern"] {
            width: 300px !important;
            height: 50px !important;
            font-size: 16px !important;
        }
    </style>
""", unsafe_allow_html=True)



st.title("Strandbeest Simulator")

# Session State initialisieren
if "points" not in st.session_state:
    st.session_state["points"] = []
if "links" not in st.session_state:
    st.session_state["links"] = []
if "new_point_type" not in st.session_state:
    st.session_state["new_point_type"] = "Fester Punkt"

# Nutzung der vollen Bildschirmbreite
col1, col2 = st.columns([2, 3])  

# Linke Seite: Koordinatensystem
with col1:
    st.subheader("Koordinatensystem")
    fig, ax = plt.subplots(figsize=(10, 10))  
    ax.set_xlim(0, 10)  
    ax.set_ylim(0, 10)  
    ax.set_xlabel("X-Achse", fontsize=14)
    ax.set_ylabel("Y-Achse", fontsize=14)
    ax.grid(True, linewidth=1)

    for i, p in enumerate(st.session_state["points"]):
        color = "red" if p["type"] == "Fester Punkt" else \
                "blue" if p["type"] == "Beweglicher Punkt" else \
                "green" if p["type"] == "Kreisbahn Punkt" else "orange"

        ax.scatter(p["x"], p["y"], color=color, s=150)
        ax.text(p["x"] + 0.3, p["y"], f"P{i+1}", fontsize=12, color="black")

    for link in st.session_state["links"]:
        start_idx, end_idx = link["start"], link["end"]
        x_vals = [st.session_state["points"][start_idx]["x"], st.session_state["points"][end_idx]["x"]]
        y_vals = [st.session_state["points"][start_idx]["y"], st.session_state["points"][end_idx]["y"]]
        ax.plot(x_vals, y_vals, "b-", linewidth=3)

    st.pyplot(fig)

# Rechte Seite: Steuerung
with col2:
    st.subheader("Punkte verwalten")

    cols = st.columns([2, 2, 2, 4])  
    with cols[1]:
        x_new = st.number_input("X", value=1.0, step=0.5, min_value=0.0, key="new_x", format="%.2f")
    with cols[2]:
        y_new = st.number_input("Y", value=1.0, step=0.5, min_value=0.0, key="new_y", format="%.2f")
    with cols[3]:
        st.session_state["new_point_type"] = st.selectbox(
            "Punkt-Typ",
            ["Fester Punkt", "Beweglicher Punkt", "Kreisbahn Punkt"],
            index=["Fester Punkt", "Beweglicher Punkt", "Kreisbahn Punkt"].index(st.session_state["new_point_type"]),
            key="new_point_type_select"
        )

    with cols[0]:
        if st.button("Punkt", key="Punkt hinzufügen"):
            st.session_state["points"].append({"x": x_new, "y": y_new, "type": st.session_state["new_point_type"]})
            st.rerun()



    # Bestehende Punkte Dropdown
    if st.session_state["points"]:
        selected_point = st.selectbox(
            "Bestehende Punkte",
            [f"P{i+1}: {p['type']} (X:{p['x']}, Y:{p['y']})" for i, p in enumerate(st.session_state["points"])],
            key="selected_point"
        )

        if st.button("🗑️ Punkt löschen", key="delete_point"):
            index_to_delete = st.session_state["points"].index(next(p for i, p in enumerate(st.session_state["points"]) if f"P{i+1}" in selected_point))
            del st.session_state["points"][index_to_delete]
            st.rerun()

    if len(st.session_state["points"]) >= 2:
        st.subheader("Glieder verbinden")
        point_options = [f"P{i+1}" for i in range(len(st.session_state["points"]))]
        
        start_point = st.selectbox("Startpunkt", point_options, key="start")
        end_point = st.selectbox("Endpunkt", point_options, key="end")

        if st.button("🔗 Glied hinzufügen"):
            start_idx, end_idx = point_options.index(start_point), point_options.index(end_point)
            st.session_state["links"].append({"start": start_idx, "end": end_idx})
            st.rerun()

    # Daten speichern Button
    if st.button("💾 Daten speichern", key="Daten speichern"):
        data = {"points": st.session_state["points"], "links": st.session_state["links"]}
        with open("mechanism_data.json", "w") as file:
            json.dump(data, file, indent=4)
        st.success("Daten gespeichert! `example.py` kann sie jetzt nutzen.")
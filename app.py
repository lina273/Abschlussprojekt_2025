import streamlit as st
import json
import numpy as np
import matplotlib.pyplot as plt

# Setzt das Layout auf volle Breite
st.set_page_config(layout="wide")
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
    fig, ax = plt.subplots(figsize=(15, 15))  
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

with col2:
    st.subheader("Punkte erstellen")

    # Eingabe  X, Y und Punkt-Typ
    col_x, col_y, col_type = st.columns([1, 1, 2])
    with col_x:
        x_new = st.number_input("X", value=1.0, step=0.5, min_value=0.0, key="new_x", format="%.2f")
    with col_y:
        y_new = st.number_input("Y", value=1.0, step=0.5, min_value=0.0, key="new_y", format="%.2f")
    with col_type:
        st.session_state["new_point_type"] = st.selectbox(
            "Punkt-Typ",
            ["Fester Punkt", "Beweglicher Punkt", "Kreisbahn Punkt"],
            index=["Fester Punkt", "Beweglicher Punkt", "Kreisbahn Punkt"].index(st.session_state["new_point_type"]),
            key="new_point_type_select"
        )

    # Punkte hinzufügen
    if st.button("Punkt hinzufügen", key="add_point"):
        new_point = {"x": x_new, "y": y_new, "type": st.session_state["new_point_type"]}

        st.session_state["points"].append(new_point)    
        st.rerun()

    # Bestehende Punkte (immer sichtbar)
    st.subheader("Bestehende Punkte")
    point_options = [f"P{i+1}: {p['type']} (X:{p['x']}, Y:{p['y']})" for i, p in enumerate(st.session_state["points"])]
    selected_point = st.selectbox("Punkt auswählen", point_options if point_options else ["Keine Punkte vorhanden"], key="selected_point", disabled=not point_options)

    # Punkt löschen (Button bleibt immer sichtbar)
    if st.button("🗑️ Punkt löschen", key="delete_point", disabled=not point_options):
        index_to_delete = st.session_state["points"].index(next(p for i, p in enumerate(st.session_state["points"]) if f"P{i+1}" in selected_point))
        del st.session_state["points"][index_to_delete]
        st.rerun()

    # Glieder verbinden 
    st.subheader("Glieder verbinden")
    point_options_simple = [f"P{i+1}" for i in range(len(st.session_state["points"]))] if st.session_state["points"] else ["Keine Punkte vorhanden"]

    start_point = st.selectbox("Startpunkt", point_options_simple, key="start", disabled=len(st.session_state["points"]) < 2)
    end_point = st.selectbox("Endpunkt", point_options_simple, key="end", disabled=len(st.session_state["points"]) < 2)

    if st.button("🔗 Glied hinzufügen", disabled=len(st.session_state["points"]) < 2):
        start_idx, end_idx = point_options_simple.index(start_point), point_options_simple.index(end_point)
        st.session_state["links"].append({"start": start_idx, "end": end_idx})
        st.rerun()

    st.subheader("Glieder löschen")
    link_options = [f"{point_options_simple[link['start']]} - {point_options_simple[link['end']]}" for link in st.session_state["links"]]
    selected_link = st.selectbox("Bestehende Glieder", link_options if link_options else ["Keine Glieder vorhanden"], key="selected_link", disabled=not link_options)

    if st.button("🗑️ Glied löschen", disabled=not link_options):
        link_index = link_options.index(selected_link)
        del st.session_state["links"][link_index]
        st.rerun()


    if st.button("💾 Daten speichern", key="Daten speichern"):
        data = {"points": st.session_state["points"], "links": st.session_state["links"]}
        with open("mechanism_data.json", "w") as file:
            json.dump(data, file, indent=4)
        st.success("Daten gespeichert! `example.py` kann sie jetzt nutzen.")

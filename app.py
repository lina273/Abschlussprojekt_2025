import streamlit as st
import json
import numpy as np
import matplotlib.pyplot as plt
from animation import animation_mechanism

st.set_page_config(layout="wide")
st.title("Strandbeest Simulator")


if "points" not in st.session_state:
    st.session_state["points"] = []
if "links" not in st.session_state:
    st.session_state["links"] = []
if "link_lengths" not in st.session_state:
    st.session_state["link_lengths"] = []
if "animation_running" not in st.session_state:
    st.session_state["animation_running"] = False  

col1, col2 = st.columns([3, 3])


with col1:
    st.subheader("Koordinatensystem")
    
    fig, ax = plt.subplots(figsize=(15, 15))
    ax.set_xlim(0, 15)
    ax.set_ylim(0, 15)
    ax.set_xlabel("X-Achse", fontsize=14)
    ax.set_ylabel("Y-Achse", fontsize=14)
    ax.grid(True, linewidth=1)

    for i, p in enumerate(st.session_state["points"]):
        color = {"Fester Punkt": "red", "Beweglicher Punkt": "blue", "Kreisbahn Punkt": "green"}.get(p["type"], "orange")
        ax.scatter(p["x"], p["y"], color=color, s=150)
        ax.text(p["x"] + 0.3, p["y"], f"P{i+1}", fontsize=12, color="black")

    for j, link in enumerate(st.session_state["links"]):
        start_idx, end_idx = link["start"], link["end"]
        x_vals = [st.session_state["points"][start_idx]["x"], st.session_state["points"][end_idx]["x"]]
        y_vals = [st.session_state["points"][start_idx]["y"], st.session_state["points"][end_idx]["y"]]
        ax.plot(x_vals, y_vals, "b-", linewidth=3)
        ax.text((x_vals[0] + x_vals[1]) / 2, (y_vals[0] + y_vals[1]) / 2, f"L={st.session_state['link_lengths'][j]:.2f}", fontsize=12, color="black")

    st.pyplot(fig)


    st.subheader("Bewegungsanimation")
    animation_container = st.empty()
    if st.session_state["animation_running"]:
        with open("mechanism_data.json", "r") as file:
            mechanism_data = json.load(file)
        animation_mechanism(mechanism_data["pointArray"], mechanism_data["linkConnections"], container=animation_container)
        st.session_state["animation_running"] = False  
        st.rerun()


with col2:
    st.subheader("Punkte erstellen")
    col_x, col_y, col_type = st.columns([1, 1, 2])
    with col_x: x_new = st.number_input("X", value=1.0, step=0.5, min_value=0.0, key="new_x", format="%.2f")
    with col_y: y_new = st.number_input("Y", value=1.0, step=0.5, min_value=0.0, key="new_y", format="%.2f")
    with col_type: point_type = st.selectbox("Punkt-Typ", ["Fester Punkt", "Beweglicher Punkt", "Kreisbahn Punkt"], key="new_point_type_select")

    if st.button("➕ Punkt hinzufügen"):
        st.session_state["points"].append({"x": x_new, "y": y_new, "type": point_type})
        st.rerun()


    st.subheader("Punkte löschen")
    if st.session_state["points"]:
        point_options_delete = [f"P{i+1} ({p['type']})" for i, p in enumerate(st.session_state["points"])]
        selected_point = st.selectbox("Punkt auswählen", point_options_delete, key="delete_point")

        if st.button("🗑️ Punkt löschen"):
            delete_index = point_options_delete.index(selected_point)
            del st.session_state["points"][delete_index]
            st.rerun()
    else:
        st.write("Keine Punkte zum Löschen vorhanden.")


    st.subheader("Glieder verbinden")
    if st.session_state["points"]:
        point_options_simple = [f"P{i+1}" for i in range(len(st.session_state["points"]))]
    else:
        point_options_simple = ["Keine Punkte vorhanden"]

    col_start, col_end, col_length = st.columns([1, 1, 2])
    with col_start:start_point = st.selectbox("Startpunkt", point_options_simple, key="start", disabled=len(st.session_state["points"]) < 2)
    with col_end:end_point = st.selectbox("Endpunkt", point_options_simple, key="end", disabled=len(st.session_state["points"]) < 2)
    with col_length:length = st.number_input("Länge des Glieds", min_value=0.1, value=1.0, step=0.1, format="%.2f")

    if st.button("🔗 Glied hinzufügen", disabled=len(st.session_state["points"]) < 2):
        start_idx, end_idx = point_options_simple.index(start_point), point_options_simple.index(end_point)
        st.session_state["links"].append({"start": start_idx, "end": end_idx})
        st.session_state["link_lengths"].append(length)
        st.rerun()

  
    if st.button("💾 Mechanismus speichern"):
        fix_points = []
        free_points = []
        circle_generator = []

        for p in st.session_state["points"]:
            if p["type"] == "Fester Punkt":
                fix_points.append([p["x"], p["y"]])
            elif p["type"] == "Beweglicher Punkt":
                free_points.append([p["x"], p["y"]])
            elif p["type"] == "Kreisbahn Punkt":
                circle_generator.append([p["x"], p["y"]])

       
        if len(circle_generator) != 2:
            circle_generator = []

  
        link_connections = [[link["start"], link["end"]] for link in st.session_state["links"]]
        link_numbers = list(range(len(st.session_state["links"])))

        
        data = {
            "linkConnections": link_connections,
            "linkNumbers": link_numbers,
            "circleGenerator": circle_generator,
            "freePoints": free_points,
            "fixPoints": fix_points
        }

        with open("mechanism_data.json", "w") as file:
            json.dump(data, file, indent=4)

        st.success("Daten gespeichert!")


    if st.button("▶️ Animation starten"):
        st.session_state["animation_running"] = True
        animation_mechanism(container=animation_container)

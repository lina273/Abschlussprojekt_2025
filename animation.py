import matplotlib.pyplot as plt 
import streamlit as st 
import time

#Funktion zur Animation der Punkte

def animation_mechanism(move_list):

    st.subheader("Bewegungs_Animation")

    animation_diagram= st.empty() #Platzhalter für Animation, wird dann immer wieder neu geleert und mit den nächsten Daten gefüllt

    frames = len(move_list) #Anzahl der Animationsschritte, move_list: Liste mit den Positionen aller Punkte für jeden Animationsschritt
    for f in range(frames):
        fig, ax = plt.subplots(figsize=(10, 10))  
        ax.set_xlim(0, 10)  
        ax.set_xlabel("X", fontsize=14)
        ax.set_ylim(0, 10)  
        ax.set_ylabel("Y", fontsize=14)
        ax.grid(linewidth=1)

        #Schleife die alle Punkte aus move_list holt und nacheiander dargestellt, je nach Typ und Farbe
        for i, point in enumerate (move_list[f]):
            if point["type"] == "Fester Punkt": point_color = "red"
            elif point["type"] == "Beweglicher Punkt": point_color = "blue"
            elif point["type"] == "Kreisbahn Punkt": point_color = "green"
            else: point_color == "orange"

            ax.scatter(point["x"], point["y"], color=point_color, s=150) #Zeichnen des Punktes
            ax.text(point["x"] + 0.3, point["y"], f"P{i+1}", fontsize=12, color="black") #Beschrfitung des Punktes
        
        #Schleife die die Glieder zwischen Punkten zeichnet
        for link in st.session_state["links"]:
            start_x, end_x = link["start"], link["end"] 
            x_vals = [move_list[f][start_x]["x"], move_list[f][end_x]["x"]]  # X Positionen des Start und Endpunktes
            y_vals = [move_list[f][start_x]["y"], move_list[f][end_x]["y"]]  #Y Postionen des Start und Endpunktes
            ax.plot(x_vals, y_vals, "blue-", linewidth=3)

        animation_diagram.pyplot(fig) #Zeigt aktuelle Grafik an
        time.spleep(0.1) #pausiert Schleife zwischen jedem Frame aber kann auch weggelassen werden oder verlängert werden
        #Vielleicht können wir das durch den User anpassen lassen?





        



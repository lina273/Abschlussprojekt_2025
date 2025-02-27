import matplotlib.pyplot as plt
import streamlit as st
import time
from testData import pointArray  

link_connections = [[0, 1], [1, 2], [2, 3]] #beispiel

def animation_mechanism(fps=20, container=None):
    

    if container is None:
        container = st.empty()

    frames = len(pointArray)  
    num_points = len(pointArray[0])  

    # Animation
    for f in range(frames):
        fig, ax = plt.subplots(figsize=(10, 10))
        ax.set_xlim(-50, 50)
        ax.set_ylim(-50, 50)
        ax.set_xlabel("X-Achse", fontsize=14)
        ax.set_ylabel("Y-Achse", fontsize=14)
        ax.grid(linewidth=1)


        for i, point in enumerate(pointArray[f]):
            x, y = point  
            ax.scatter(x, y, color="blue", s=100)
            ax.text(x + 0.5, y, f"P{i+1}", fontsize=10, color="black")

       
        for link in link_connections:
            start_idx, end_idx = link
            if start_idx < num_points and end_idx < num_points:
                x_vals = [pointArray[f][start_idx][0], pointArray[f][end_idx][0]]
                y_vals = [pointArray[f][start_idx][1], pointArray[f][end_idx][1]]
                ax.plot(x_vals, y_vals, "b-", linewidth=2)

        container.pyplot(fig)
        time.sleep(1 / fps)

    st.session_state["animation_running"] = False

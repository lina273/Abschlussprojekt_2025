import streamlit as st
from animation import animation_mechanism

# Beispielhafte Test-Daten (Punkte bewegen sich nach rechts)
def generate_test_data():
    num_frames = 20  # Anzahl der Animationsschritte
    test_data = []

    for f in range(num_frames):
        frame_points = [
            {"x": 1 + f * 0.2, "y": 2, "type": "Fester Punkt"},
            {"x": 3 + f * 0.2, "y": 4, "type": "Beweglicher Punkt"},
            {"x": 5 + f * 0.2, "y": 6, "type": "Kreisbahn Punkt"}
        ]
        test_data.append(frame_points)

    return test_data

# Streamlit App starten
st.title("Test der Animation")

if st.button("Animation starten"):
    test_motion_data = generate_test_data()  # Testdaten generieren
    animation_mechanism(test_motion_data)  # Animation starten

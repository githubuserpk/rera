import streamlit as st

# Function to read the release notes from a text file
def display_release_notes():
    with open("release_notes.txt", "r") as file:
        return file.read()

# Title for the release notes page
st.title("Release Notes")

# Read and display the release notes
release_notes = display_release_notes()
st.text(release_notes)

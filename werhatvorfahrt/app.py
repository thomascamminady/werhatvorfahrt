import random

import streamlit as st

from werhatvorfahrt.vorfahrt import Sign

if __name__ == "__main__":
    with st.form("my_form"):
        n_sides = random.choice([2, 3, 4])
        n_cars = random.choice(range(2, n_sides + 1))
        sign = Sign(n_sides=n_sides, n_cars=n_cars)
        st.pyplot(sign.draw())

        boxes = []
        for _, word in zip(
            range(n_cars), ["first", "second", "third", "fourth"], strict=False
        ):
            selectbox = st.multiselect(
                f"Which colored car(s) goe(s) {word}?",
                options=[car.color.name for car in sign.cars],
            )
            boxes.append(selectbox)
        submitted = st.form_submit_button("Submit")

import streamlit as st

def display_slideshow():
    # CSS
    st.markdown("""
    <style>
    .slideshow-container {
      position: relative;
      margin: auto;
    }
    .mySlides {display: none}
    img {vertical-align: middle; width: 100%;}
    .prev, .next {
      cursor: pointer;
      position: absolute;
      top: 50%;
      width: auto;
      padding: 16px;
      margin-top: -22px;
      color: white;
      font-weight: bold;
      font-size: 18px;
      transition: 0.6s ease;
      border-radius: 0 3px 3px 0;
      user-select: none;
    }
    .next {right: 0; border-radius: 3px 0 0 3px;}
    .text {
      color: #f2f2f2;
      font-size: 15px;
      padding: 8px 12px;
      position: absolute;
      bottom: 8px;
      width: 100%;
      text-align: center;
    }
    .numbertext {
      color: #f2f2f2;
      font-size: 12px;
      padding: 8px 12px;
      position: absolute;
      top: 0;
    }
    .dot {
      height: 15px;
      width: 15px;
      margin: 0 2px;
      background-color: #bbb;
      border-radius: 50%;
      display: inline-block;
      transition: background-color 0.6s ease;
    }
    .active {background-color: #717171;}
    </style>
    """, unsafe_allow_html=True)

    # Slideshow container
    col1, col2, col3 = st.columns([1, 10, 1])

    with col1:
        if st.button("❮"):
            st.session_state.slide_index = (st.session_state.slide_index - 1) % 3

    with col2:
        st.markdown(f"""
        <div class="slideshow-container">
            <div class="mySlides fade" style="display: {'block' if st.session_state.slide_index == 0 else 'none'}">
                <div class="numbertext">1 / 3</div>
                <img src="https://www.w3schools.com/howto/img_nature_wide.jpg">
                <div class="text">Caption Text</div>
            </div>
            <div class="mySlides fade" style="display: {'block' if st.session_state.slide_index == 1 else 'none'}">
                <div class="numbertext">2 / 3</div>
                <img src="https://www.w3schools.com/howto/img_snow_wide.jpg">
                <div class="text">Caption Two</div>
            </div>
            <div class="mySlides fade" style="display: {'block' if st.session_state.slide_index == 2 else 'none'}">
                <div class="numbertext">3 / 3</div>
                <img src="https://www.w3schools.com/howto/img_mountains_wide.jpg">
                <div class="text">Caption Three</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        if st.button("❯"):
            st.session_state.slide_index = (st.session_state.slide_index + 1) % 3

    # Dots
    st.markdown(f"""
    <div style="text-align:center">
        <span class="dot{'active' if st.session_state.slide_index == 0 else ''}"></span> 
        <span class="dot{'active' if st.session_state.slide_index == 1 else ''}"></span> 
        <span class="dot{'active' if st.session_state.slide_index == 2 else ''}"></span> 
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    if 'slide_index' not in st.session_state:
        st.session_state.slide_index = 0
    display_slideshow()

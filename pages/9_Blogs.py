import streamlit as st

def display_title():
    st.title("Our Team's Blog Posts")
    

def main():
    st.sidebar.title("Blogs")

    with st.container() as main_container:
        display_title()

    url_aigov_essentials = "https://mauverick.com/essentials-for-organizational-ai-governance/"
    url_ai_adoption = "https://mauverick.com/impediments-of-ai-adoption-from-poc-to-production/"
    url_agents_swarm = "https://www.linkedin.com/feed/update/urn:li:activity:7255162866956210177/?updateEntityUrn=urn%3Ali%3Afs_updateV2%3A%28urn%3Ali%3Aactivity%3A7255162866956210177%2CFEED_DETAIL%2CEMPTY%2CDEFAULT%2Cfalse%29"
    url_uk_summit = "https://www.linkedin.com/pulse/uk-international-investment-summit-more-red-carpet-krishnarao-pk--oklle/?trackingId=5Qx1%2F5lBTHGEenFZkQH5AA%3D%3D"
    url_cloudrun_gpus = "https://www.linkedin.com/feed/update/urn:li:activity:7259507257497776128/?updateEntityUrn=urn%3Ali%3Afs_updateV2%3A%28urn%3Ali%3Aactivity%3A7259507257497776128%2CFEED_DETAIL%2CEMPTY%2CDEFAULT%2Cfalse%29"
    url_euaiact = "https://medium.com/@krishnarao.pradeep/ai-safety-regulation-and-the-eu-ai-act-challenges-and-opportunities-that-lie-ahead-e5ad52217263"
    url_Sb1047 = "https://www.linkedin.com/pulse/death-sb-1047-ai-safety-regulation-triumph-regulatory-pradeep-hwzye/?trackingId=Bcwss0Y%2FRGOZlLquxBZ5yg%3D%3D"
    # List of blogs with their titles and URLs
    blogs = [
        {"title": "Essentials of AI Governance", "url": url_aigov_essentials},         
        {"title": "AI Adoption from PoC to Production Overcoming Impediments", "url": url_ai_adoption},
        {"title": "AI Agents Swarm   (video)", "url": url_agents_swarm},
        {"title": "UK International Investment Summit - More of Red Carpet or Red Tape", "url": url_uk_summit},
        {"title": "AI Safety Regulation and the EU AI Act — Challenges and Opportunities that lie ahead", "url": url_euaiact},
        {"title": "Google Cloud Run with Serverless GPUs   (video)", "url": url_cloudrun_gpus},    
        {"title": "The death of SB 1047 AI Safety Regulation and the triumph of Regulatory Capture", "url": url_Sb1047}

    ]

    st.header("")

    for blog in blogs:
        st.markdown(f"- [{blog['title']}]({blog['url']})", unsafe_allow_html=True)



if __name__ == "__main__":
    main()


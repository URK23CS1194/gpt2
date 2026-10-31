
import streamlit as st
from utils import ask_ollama
import os

st.set_page_config(
    page_title="AI Blog Content Generator",
    page_icon="✍️",
    layout="wide"
)

st.title("✍️ AI Blog Content Generator")
st.caption("Generate blogs, titles, summaries and SEO content using Ollama – Llama 3.2")

st.divider()

st.subheader("Enter Blog Details")

topic = st.text_area(
    "Blog Topic",
    placeholder="Example: Artificial Intelligence in Education"
)

col1, col2, col3 = st.columns(3)

with col1:
    style = st.selectbox(
        "Writing Style",
        ["Professional", "Educational", "Creative", "Informal"]
    )

with col2:
    tone = st.selectbox(
        "Tone",
        ["Formal", "Friendly", "Persuasive", "Informative"]
    )

with col3:
    word_count = st.selectbox(
        "Approximate Word Count",
        [200, 300, 500, 700, 1000]
    )

st.divider()

if st.button("✨ Generate Complete Blog", type="primary", use_container_width=True):

    if not topic.strip():
        st.warning("Please enter a blog topic.")

    else:
        try:
            with st.spinner("Generating your complete blog..."):

                blog_prompt = f"""
                Write a complete blog on: {topic}

                Writing style: {style}
                Tone: {tone}
                Approximate word count: {word_count}

                Include an attractive heading, introduction,
                meaningful subheadings, detailed content
                and conclusion.
                """

                blog = ask_ollama(blog_prompt)

                details_prompt = f"""
                Based on this blog:

                {blog}

                Generate the following:

                1. FIVE attractive blog titles.
                2. A summary of approximately 100 words.
                3. Seven SEO-friendly keywords.
                4. An SEO meta description within 160 characters.

                Clearly separate each section using headings.
                """

                details = ask_ollama(details_prompt)

                intent_prompt = f"""
                Identify the user's main intent.

                User request: Write a blog about {topic}

                Choose only one:
                BLOG_GENERATION
                SUMMARY
                KEYWORD_GENERATION
                META_DESCRIPTION

                Return only the intent label.
                """

                intent = ask_ollama(intent_prompt)

            st.session_state["blog"] = blog
            st.session_state["details"] = details
            st.session_state["intent"] = intent

            st.success("Your blog content was generated successfully!")

        except Exception as e:
            st.error(f"Error connecting to Ollama: {e}")

if "blog" in st.session_state:

    st.divider()

    st.subheader("📝 Generated Blog")
    st.markdown(st.session_state["blog"])

    st.divider()

    st.subheader("🚀 Titles, Summary and SEO")
    st.markdown(st.session_state["details"])

    st.divider()

    st.subheader("🧠 Intent Detection")
    st.success(st.session_state["intent"])

    st.divider()

    if st.button("💾 Save Blog"):

        os.makedirs("outputs", exist_ok=True)

        with open(
            "outputs/generated_blog.txt",
            "w",
            encoding="utf-8"
        ) as file:
            file.write(st.session_state["blog"])
            file.write("\n\n")
            file.write(st.session_state["details"])

        st.success("Blog saved successfully!")

    st.download_button(
        "⬇️ Download Generated Blog",
        data=st.session_state["blog"] + "\n\n" + st.session_state["details"],
        file_name="generated_blog.txt",
        mime="text/plain"
    )

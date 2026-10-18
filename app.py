import streamlit as st

from src.code_reviewer import CodeReviewer
from pathlib import Path


st.set_page_config(
    page_title="AI Code Reviewer - With Caching",
    page_icon="🔍",
    layout="wide"
)

def load_css():
    css_path = Path(__file__).parent / "styles" / "style.css"

    with open(css_path, encoding="utf-8") as css_file:
        st.markdown(
            f"<style>{css_file.read()}</style>",
            unsafe_allow_html=True
        )


load_css()


st.title("🔍 AI Code Reviewer- With Caching")
st.write(
    "Review Java code for potential bugs, security issues, "
    "performance problems, and coding-standard violations."
)

st.divider()

st.subheader("Submit Java Code")

java_code = st.text_area(
    "Paste your Java source code below",
    height=350,
    placeholder="""public class Example {
    public static void main(String[] args) {
        System.out.println("Hello, World!");
    }
}""",
    key="java_code"
)

if st.button("Review Code", type="primary", use_container_width=True):

    if not java_code.strip():
        st.warning("Please enter some Java code before starting the review.")

    else:
        try:
            with st.spinner("Analyzing code and retrieving guidelines..."):
                reviewer = CodeReviewer()
                result = reviewer.review_code(java_code)

            st.success("Code review completed!")

            st.subheader("📋 Code Review Report")
            st.markdown(result["review"])

            with st.expander("📚 Retrieved Coding Guidelines"):
                for index, guideline in enumerate(
                    result["guidelines"], start=1
                ):
                    st.markdown(f"**Guideline {index}**")
                    st.caption(
                        f"Source: {guideline['source']} | "
                        f"Similarity: {guideline['score']:.4f}"
                    )
                    st.write(guideline["content"])
                    st.divider()

        except Exception as error:
            st.error("The code review failed. Please check the application logs.")
            print(f"Code review error: {error}")
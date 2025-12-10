import streamlit as st
from typing import List, Dict, Tuple

# -----------------------
# Fake backend for demo
# -----------------------

# Hard-coded "stories" to make the app feel real before RAG is wired up
SAMPLE_STORIES: List[Dict[str, str]] = [
    {
        "role": "Software Engineer",
        "title": "Switching from undecided major to CS in sophomore year",
        "snippet": (
            "I didn’t write my first line of code until college. I started with intro CS, "
            "joined a project team, and slowly built a portfolio. The key was doing small "
            "projects consistently rather than trying to learn everything at once."
        ),
    },
    {
        "role": "Firefighter",
        "title": "A day in the life of a firefighter",
        "snippet": (
            "Most days aren’t dramatic rescues. We spend a lot of time on drills, building "
            "inspections, and community education, so when an emergency happens we can "
            "react automatically."
        ),
    },
    {
        "role": "UX Designer",
        "title": "From community college art classes to UX design",
        "snippet": (
            "My art background helped, but I still had to learn research, prototyping, and "
            "collaboration with engineers. I built a small portfolio with redesigns of apps "
            "I already used every day."
        ),
    },
]


def generate_sample_answer(
    question: str,
    stage: str,
    interests: List[str],
) -> Tuple[str, List[Dict[str, str]]]:

    base_intro = (
        "Here’s a perspective pulled from a few different career stories. "
        "This is a placeholder answer — in the final version, this will be "
        "grounded directly in quotes from RAG pipeline transcript."
    )

    stage_note = ""
    if stage == "High school":
        stage_note = (
            " Since you’re in high school, focus on low-risk exploration: clubs, "
            "short online courses, and talking to people doing the work you’re curious about."
        )
    elif stage == "College":
        stage_note = (
            " In college, you can use electives, side projects, and internships "
            "to test directions without locking yourself in forever."
        )
    elif stage == "Career switcher":
        stage_note = (
            " As a career switcher, try small experiments on the side first "
            "(online courses, volunteering, small freelance work) before making a big jump."
        )

    interest_note = ""
    if interests:
        interest_list = ", ".join(interests)
        interest_note = (
            f" You mentioned interests in {interest_list}. Try looking for roles that mix those "
            "themes instead of just one 'perfect' job."
        )

    answer = (
        f"{base_intro}\n\n"
        "From these stories, a common pattern is that people rarely had everything figured out at the start. "
        "They picked a direction that seemed interesting, took one or two concrete steps, and then adjusted "
        "based on what they liked or disliked."
        + stage_note
        + interest_note
    )

    # For now, just return all sample stories.
    return answer, SAMPLE_STORIES


def main() -> None:
    st.set_page_config(page_title="Career Path Q&A Coach", page_icon="🧭")

    st.title("🧭 Career Path Q&A Coach")
    st.markdown(
        """
        Feeling stuck about *what you want to be* or what a certain job is really like?

        This concept demo lets you ask questions and see a response inspired by sample career stories.
        In the **final version**, the backend will use your RAG pipeline over real interview transcripts
        (Pinecone + a generative model) instead of the simple placeholder logic shown here.
        """
    )

    # -----------------------
    # Section 1: User context
    # -----------------------
    st.markdown("### 1️⃣ Tell us a bit about you")

    stage = st.selectbox(
        "Which best describes you right now?",
        ["High school", "College", "Career switcher", "Other"],
        index=1,
    )

    interests = st.multiselect(
        "What are you most curious about?",
        [
            "Technology",
            "Healthcare",
            "Education",
            "Creative work",
            "Public service",
            "Business / startups",
        ],
    )

    # -----------------------
    # Section 2: Question box
    # -----------------------
    st.markdown("### 2️⃣ Ask a question about careers or paths")

    question = st.text_area(
        "What would you like to ask the coach?",
        placeholder=(
            "Examples:\n"
            "- What does a day in the life of a UX designer look like?\n"
            "- Is it too late to switch into tech?\n"
            "- How do I explore careers if I have no idea what I like?"
        ),
        height=140,
    )

    submit = st.button("Ask the coach ✨", use_container_width=True)

    # -----------------------
    # Section 3: Answer + stories
    # -----------------------
    if submit:
        if not question.strip():
            st.warning("Please enter a question first so the coach knows what to answer.")
            return

        with st.spinner("Thinking about stories that might help..."):
            answer, stories = generate_sample_answer(question, stage, interests)

        st.markdown("### 3️⃣ Your personalized answer")

        # Show a short summary of the user's context
        st.markdown("#### Who this answer is for")
        interests_text = ", ".join(interests) if interests else "None selected (general advice)."
        st.markdown(
            f"- **Stage:** {stage}\n"
            f"- **Interests:** {interests_text}"
        )

        st.write(answer)

        st.markdown("### 4️⃣ Stories this answer is inspired by")
        st.caption(
            "In the real app, this section will show the exact transcript snippets retrieved "
            "from the Pinecone index."
        )

        for story in stories:
            with st.expander(f"{story['role']}: {story['title']}"):
                st.write(story["snippet"])

        st.markdown("---")
        st.caption(
            "Concept demo – backend currently uses placeholder logic instead of the real RAG pipeline."
        )


if __name__ == "__main__":
    main()

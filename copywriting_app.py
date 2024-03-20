import time
import os
import json
import openai
import streamlit as st
from streamlit_lottie import st_lottie
from tenacity import retry, stop_after_attempt, wait_random_exponential

def main():
    set_page_config()
    custom_css()
    hide_elements()
    sidebar()
    title_and_description()
    input_section()

def set_page_config():
    st.set_page_config(
        page_title="Alwrity",
        layout="wide",
        page_icon="img/logo.png"
    )

def custom_css():
    st.markdown("""
        <style>
            .block-container {
                padding-top: 0rem;
                padding-bottom: 0rem;
                padding-left: 1rem;
                padding-right: 1rem;
            }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("""
        <style>
            [class="st-emotion-cache-7ym5gk ef3psqc12"] {
                display: inline-block;
                padding: 5px 20px;
                background-color: #4681f4;
                color: #FBFFFF;
                width: 300px;
                height: 35px;
                text-align: center;
                text-decoration: none;
                font-size: 16px;
                border-radius: 8px;
            }
        </style>
    """, unsafe_allow_html=True)

def hide_elements():
    hide_decoration_bar_style = '<style>header {visibility: hidden;}</style>'
    st.markdown(hide_decoration_bar_style, unsafe_allow_html=True)

    hide_streamlit_footer = '<style>#MainMenu {visibility: hidden;} footer {visibility: hidden;}</style>'
    st.markdown(hide_streamlit_footer, unsafe_allow_html=True)

def sidebar():
    st.sidebar.title("Agree, Promise, Preview")
    st.sidebar.image("img/alwrity.jpeg", use_column_width=True)
    st.sidebar.markdown("🧕 :red[Checkout Alwrity], complete **AI writer & Blogging solution**:[Alwrity](https://alwrity.netlify.app)")


def title_and_description():
    st.title("✍️ Alwrity - AI Generator for CopyWriting APP Formula")
    with st.expander("What is **Copywriting APP formula** & **How to Use**? 📝❗"):
        st.markdown('''
            ### What's APP copywriting Formula, and How to use this AI generator 🗣️
            ---
            #### APP Copywriting Formula

            APP stands for Agree, Promise, Preview. It's a copywriting formula that involves:

            1. **Agree**: Establishing common ground with the audience or acknowledging a shared problem.
            2. **Promise**: Making a compelling promise or offering a solution to the audience's problem.
            3. **Preview**: Providing a sneak peek or preview of what the audience can expect from your product or service.

            The APP formula is effective in building rapport, capturing attention, and enticing the audience to learn more.

            #### APP Copywriting Formula: Simple Example

            - **Agree**: "Struggling to write captivating marketing copy?"
            - **Promise**: "Discover how our AI-powered tool can transform your copywriting process."
            - **Preview**: "Get ready for effortless copy creation and increased engagement!"

            ---
        ''')


def input_section():
    with st.expander("**PRO-TIP** - Easy Steps to Create Compelling Copy", expanded=True):
        col1, space, col2 = st.columns([5, 0.1, 5])
        with col1:
            brand_name = st.text_input('**Enter Brand/Company Name**', help="Enter the name of your brand or company.")
        with col2:
            description = st.text_input('**Describe What Your Brand Does ?** (In 2-3 words)', help="Describe your product or service briefly.")
        agree = st.text_input('Establish Common Problem that Your company solves', 
                      help="Connect with the audience by acknowledging a shared problem.",
                      placeholder="We all face..., Like you, I've..., Safety, Unprofessionalism..")


        if st.button('**Get APP Copy**'):
            if  agree.strip() and brand_name and description:
                with st.spinner("Generating APP Copy..."):
                    app_copy = generate_app_copy(brand_name, description, agree)
                    if app_copy:
                        st.subheader('**👩🔬👩🔬 Your APP Copy**')
                        st.markdown(app_copy)
                    else:
                        st.error("💥 **Failed to generate APP copy. Please try again!**")
            else:
                st.error("All fields are required!")

    page_bottom()


@retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(6))
def generate_app_copy(brand_name, description, agree):
    prompt = f"""As an expert copywriter, I need your help in creating a marketing campaign for {brand_name},
        which is a {description}. Your task is to use the APP (Agree-Promise-Preview) formula to craft compelling copy.
        Establish Common Problem that Your company solves and acknowledging a shared problem of {agree}.
        Make a Compelling Promise or Offer a Solution. 
        Provide a compelling Preview of servie.
        Do not provide explanations, provide the final marketing copy.
    """
    return openai_chatgpt(prompt)


def page_bottom():
    """ """
    data_oracle = import_json(r"lottie_files/brain_robot.json")
    st_lottie(data_oracle, width=600, key="oracle")

    st.markdown('''
    Copywrite using APP formula - powered by AI (OpenAI, Gemini Pro).

    Implemented by [Alwrity](https://alwrity.netlify.app).

    Learn more about [Google's Stance on AI generated content](https://alwrity.netlify.app/post/googles-guidelines-on-using-ai-generated-content-everything-you-need-to-know).
    ''')

    st.markdown("""
    ### Agree:
    Are you tired of struggling to create effective marketing campaigns that engage your audience?

    ### Promise:
    Imagine having access to a powerful tool that crafts compelling copy effortlessly, saving you time and effort.

    ### Preview:
    Introducing Alwrity - Your AI Generator for Copywriting APP Formula. With Alwrity, you can create persuasive marketing campaigns that drive action effectively.
    """)



@retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(6))
def openai_chatgpt(prompt, model="gpt-3.5-turbo-0125", max_tokens=500, top_p=0.9, n=1):
    try:
        client = openai.OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=max_tokens,
            n=n,
            top_p=top_p
        )
        return response.choices[0].message.content
    except openai.APIError as e:
        st.error(f"OpenAI API Error: {e}")
    except openai.APIConnectionError as e:
        st.error(f"Failed to connect to OpenAI API: {e}")
    except openai.RateLimitError as e:
        st.error(f"Rate limit exceeded on OpenAI API request: {e}")
    except Exception as err:
        st.error(f"An error occurred: {err}")


# Function to import JSON data
def import_json(path):
    with open(path, "r", encoding="utf8", errors="ignore") as file:
        url = json.load(file)
        return url



if __name__ == "__main__":
    main()


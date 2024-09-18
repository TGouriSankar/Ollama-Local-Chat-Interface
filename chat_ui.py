import ollama
import streamlit as st
from openai import OpenAI
from utilities.icon import page_icon
from pages import Multimodal, Settings

st.set_page_config(
    page_title="Chat UI",
    page_icon="chatbot.png",
    layout="wide",
    initial_sidebar_state="expanded",
)


def extract_model_names(models_info: list) -> tuple:
    """
    Extracts the model names from the models information.

    :param models_info: A dictionary containing the models' information.

    Return:
        A tuple containing the model names.
    """

    return tuple(model["name"] for model in models_info["models"])

# # Define the sidebar with navigation
# def sidebar_navigation():
#     st.sidebar.title("Navigation")
#     pages = {
#         "Chat UI": main,
#         "Multimodel": Multimodal,
#         "Settings": Settings,
#     }
    
#     # Sidebar for page selection
#     selected_page = st.sidebar.radio("Go to", list(pages.keys()), index=0)
#     st.sidebar.markdown("---")  # A separator for a cleaner look
    
#     # Call the respective page function based on selection
#     pages[selected_page]()

# import base64
# import streamlit as st

# def set_background(image_file):
#     """
#     Set a local image as the background of the Streamlit app.
#     Convert the image to base64 and use CSS to set the background.
#     """
#     with open(image_file, "rb") as file:
#         image_bytes = file.read()
#         encoded_image = base64.b64encode(image_bytes).decode()

#     st.markdown(
#         f"""
#         <style>
#         .stApp {{
#             background-image: url("data:image/jpeg;base64,{encoded_image}");
#             background-size: cover;
#             background-position: center;
#             background-repeat: no-repeat;
#             height: 100vh;
#         }}
#         </style>
#         """,
#         unsafe_allow_html=True
#     )


def main():
    """
    The main function that runs the application.
    """
    # set_background("/media/player/karna1/ollama-ui-streamlit/ai.jpg")
    page_icon("🤖💬")
    st.subheader("Ollama Model Chat UI", divider="red", anchor=False)
    
    # page_icon("🤖💬")
    # st.title("Ollama Model Chat UI")
    # st.subheader("Start chatting with the model below")

    client = OpenAI(
        base_url="http://localhost:11434/v1",
        api_key="ollama",  # required, but unused
    )

    models_info = ollama.list()
    available_models = extract_model_names(models_info)

    if available_models:
        selected_model = st.selectbox(
            "Pick a model available locally on your system ↓", available_models
        )

    else:
        st.warning("You have not pulled any model from Ollama yet!", icon="⚠️")
        if st.button("Go to settings to download a model"):
            st.page_switch("pages/03_⚙️_Settings.py")

    message_container = st.container(height=400, border=True)

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        avatar = "🤖" if message["role"] == "assistant" else "😎"
        with message_container.chat_message(message["role"], avatar=avatar):
            st.markdown(message["content"])

    if prompt := st.chat_input("Enter a prompt here..."):
        try:
            st.session_state.messages.append(
                {"role": "user", "content": prompt})

            message_container.chat_message("user", avatar="😎").markdown(prompt)

            with message_container.chat_message("assistant", avatar="🤖"):
                with st.spinner("model working..."):
                    stream = client.chat.completions.create(
                        model=selected_model,
                        messages=[
                            {"role": m["role"], "content": m["content"]}
                            for m in st.session_state.messages
                        ],
                        stream=True,
                    )
                # stream response
                response = st.write_stream(stream)
            st.session_state.messages.append(
                {"role": "assistant", "content": response})

        except Exception as e:
            st.error(e, icon="⛔️")

# def Multimodal():
#     """
#     The settings page where the user can manage models, configurations, etc.
#     """
#     st.title("Settings ⚙️")
#     st.write("Manage your settings here...")


# def Settings():
#     """
#     A help or FAQ page for users to understand how to use the app.
#     """
#     st.title("Help ❓")
#     st.write("Here you can find help and FAQs to understand how to use the application.")


if __name__ == "__main__":
    main()
    # sidebar_navigation()
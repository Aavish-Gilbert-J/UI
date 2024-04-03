from streamlit_chat import message
import requests
import json
import streamlit as st

def ask_question(question):
    url = "https://38e4-1-6-74-117.ngrok-free.app/chat"  # Change this URL to your Google AI Studio endpoint
    headers = {"Content-Type": "application/json"}
    data = {"question": question}
    
    response = requests.post(url, headers=headers, data=json.dumps(data))
    print("the response is", response)
    print("Response content:", response.content)
    
    # Check if request was successful
    if response.status_code == 200:
        return response.content.decode()  # Return the response content as string
    else:
        print("Request failed with status code:", response.status_code)
        return None




st.title("QnA Bot" )
if 'user_input' not in st.session_state:
    st.session_state['user_input'] = []

if 'google_ai_response' not in st.session_state:
    st.session_state['google_ai_response'] = []

def get_text():
    input_text = st.text_input("Write your question here", key="input")
    return input_text

user_input = get_text()

if user_input:
    output = ask_question(user_input)
    print("the output is ", output)

    if output is not None:
        # Store the output
        st.session_state.google_ai_response.append(user_input)
        st.session_state.user_input.append(output)
    else:
        # Handle the case where request failed
        st.error("Failed to get response from the API")


message_history = st.empty()

if st.session_state['user_input']:
    for i in range(len(st.session_state['user_input']) - 1, -1, -1):
        
        # This function displays Google AI Studio response
        message(st.session_state['google_ai_response'][i], 
                avatar_style="miniavs", is_user=True,
                key=str(i) + 'data_by_user')
        
        # This function displays user input
        message(st.session_state["user_input"][i], 
                key=str(i), avatar_style="icons")

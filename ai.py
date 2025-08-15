import streamlit as st


st.title("AI Assistant")
st.write("This is a simple AI assistant built with Streamlit.")
st.write("You can ask me anything, and I will try to help you!")
def main():
    user_input = st.text_input("Ask me anything:")
    if user_input:
        response = f"You asked: {user_input}"
        st.write(response)
if __name__ == "__main__":
    main()

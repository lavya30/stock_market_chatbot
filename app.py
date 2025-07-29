import streamlit as st
from langchain_groq import ChatGroq
from langchain.prompts import ChatPromptTemplate

# Set your Groq API Key
GROQ_API_KEY = "YOUR_API_KEY_HERE"

# Initialize chat history in session state
if 'messages' not in st.session_state:
    st.session_state.messages = []

# --- Setup LLM ---
llm = ChatGroq(groq_api_key=GROQ_API_KEY, model_name="moonshotai/kimi-k2-instruct")

# --- Prompt Template ---
prompt = ChatPromptTemplate.from_messages([
    ("system", """
You are a smart Indian stock market advisor bot specialized in NSE and BSE markets.

IMPORTANT RESTRICTIONS:
- ONLY answer questions related to Indian stock market, trading, investments, NSE, BSE, mutual funds, and financial planning.
- If asked about anything outside stock market context (like general knowledge, weather, food, entertainment, etc.), politely decline and redirect to stock market topics.
- Always respond: "I'm a stock market advisor bot. I can only help with Indian stock market, trading, and investment questions. Please ask about stocks, trading strategies, or investment advice."

Your job is to:
- Understand user's budget, risk appetite, and investment goal (intraday, long-term, etc.)
- Recommend Indian stocks (NSE/BSE) accordingly.
- Explain your reasoning in simple terms.
- Don't mention any unavailable or foreign stocks.
- If information is unclear, ask for clarification.
- Stay focused only on stock market and investment topics.
"""),
    ("human", "{user_input}")
])

# --- Streamlit UI ---
st.set_page_config(page_title="Stock ChatBot 💹", page_icon="📈")
st.title("📊 Conversational Stock Advisor Bot")

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if user_prompt := st.chat_input("Ask something like: I have ₹5000, what stock should I buy today?"):
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(user_prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": user_prompt})
    
    # Get bot response
    chain = prompt | llm
    response = chain.invoke({"user_input": user_prompt})
    
    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        st.markdown(response.content)
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response.content})

# Response text area for viewing full response
if st.session_state.messages:
    st.markdown("---")
    st.subheader("📝 Latest Response")
    if st.session_state.messages[-1]["role"] == "assistant":
        st.text_area(
            "Full Response (for copying):", 
            value=st.session_state.messages[-1]["content"], 
            height=200,
            key="response_area"
        )

import streamlit as st
from duckduckgo_search import DDGS
from langchain_core.messages import HumanMessage, AIMessage  # सिर्फ हिस्ट्री के लिए, कोई एरर नहीं

# ऐप का नाम और लुक
st.set_page_config(page_title="Avox", page_icon="🔊")
st.title("🔊 Avox")
st.caption("Tera Personal AI Bhai")

# चैट हिस्ट्री
if "messages" not in st.session_state:
    st.session_state.messages = []

# पुरानी चैट दिखाओ
for msg in st.session_state.messages:
    if isinstance(msg, HumanMessage):
        st.chat_message("user").write(msg.content)
    else:
        st.chat_message("assistant").write(msg.content)

# साइडबार
with st.sidebar:
    st.header("📂 Menu")
    if st.button("🆕 New Chat"):
        st.session_state.messages = []
        st.rerun()
    
    st.write("📌 Projects (Jald hi aayega)")
    st.write("🕒 History (Jald hi aayega)")

# चैट इनपुट
if prompt := st.chat_input("Bolo bhai, kya haal hai?"):
    # यूजर मैसेज
    st.chat_message("user").write(prompt)
    st.session_state.messages.append(HumanMessage(content=prompt))

    # AI जवाब
    with st.chat_message("assistant"):
        with st.spinner("Soch raha hu..."):
            lower_prompt = prompt.lower()
            
            # फैक्ट/सर्च वाले सवाल → रियल टाइम सर्च
            if any(word in lower_prompt for word in ["temperature", "mausam", "taapmaan", "news", "kitna", "kaise", "kya hai", "batao", "today", "abhi", "current"]):
                with DDGS() as ddgs:
                    results = ddgs.text(prompt, max_results=3)
                if results:
                    response = ""
                    for r in results:
                        response += f"**{r['title']}**\n{r['body']}\n🔗 {r['href']}\n\n"
                    response += "🔗 Source: DuckDuckGo Search se"
                else:
                    response = "Bhai, kuch nahi mila is sawal pe... aur try kar! 😅"
            else:
                # फ्रेंडली बातें
                if "joke" in lower_prompt or "has" in lower_prompt:
                    response = "Ek joke sun: Wifi ka password kya hai? '12345678' Kyunki lazy log hi hack karte hain! 😂😂"
                elif "kaise ho" in lower_prompt or "haal" in lower_prompt:
                    response = "Badhiya bhai! Tu bata, kya chal raha hai? 😎"
                elif "thanks" in lower_prompt or "shukriya" in lower_prompt:
                    response = "Koi baat nahi bhai, anytime! ❤️"
                else:
                    response = "Bhai mast sawal hai! Abhi main thoda basic hu, lekin jald hi aur smart ban jaunga 😅 Kuch aur puch na!"

        st.write(response)
        st.session_state.messages.append(AIMessage(content=response))

import os
import openai
import numpy as np
import pandas as pd
import json
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import CSVLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.prompts import ChatPromptTemplate
from langchain.vectorstores import Chroma
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda, RunnablePassthrough
from openai.embeddings_utils import get_embedding
import faiss
import streamlit as st
import warnings
from streamlit_option_menu import option_menu
from streamlit_extras.mention import mention

warnings.filterwarnings("ignore")


st.set_page_config(page_title="Robby's Attack on Titan Summarizer Tool", page_icon="🔰", layout="wide")

st.markdown("""
<style>
    body {
        color: #5c4033;
        background-color: #f5e6d3;
    }
    .stApp {
        background-image: url('https://wallpapercave.com/wp/wp6832156.png');
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
    }
    .stButton>button {
        color: #f5e6d3;
        background-color: #8b4513;
        border: 2px solid #5c4033;
    }
    .stTextInput>div>div>input {
        color: #5c4033;
        background-color: #f5e6d3;
    }
    .stTextArea>div>div>textarea {
        color: #5c4033;
        background-color: #f5e6d3;
    }
</style>
""", unsafe_allow_html=True)

with st.sidebar :
    st.image('Day_3/Activity_6/images/AOT_LOGO.png') #AI_
    openai.api_key = st.text_input('Enter OpenAI API token:', type='password')
    if not (openai.api_key.startswith('sk-') and len(openai.api_key)==164):
        st.warning('Please enter your OpenAI API token!', icon='⚠️')
    else:
        st.success('Proceed to entering your prompt message!', icon='👉')
    with st.container() :
        l, m, r = st.columns((1, 3, 1))
        with l : st.empty()
        with m : st.empty()
        with r : st.empty()

    options = option_menu(
        "🔰 Attack On Titan Dashboard", 
        ["Tool", "About Us", "AOT News Summarizer", "Character Finder", "Secret Weapon"],
        icons = ['tools', 'compass', 'search', 'search', 'lock'],
        menu_icon = "🔰", 
        default_index = 0,
        styles = {
            "icon" : {"color" : "#dec960", "font-size" : "20px"},
            "nav-link" : {"font-size" : "17px", "text-align" : "left", "margin" : "5px", "--hover-color" : "#262730"},
            "nav-link-selected" : {"background-color" : "#262730"}          
        })


if 'messages' not in st.session_state:
    st.session_state.messages = []

if 'chat_session' not in st.session_state:
    st.session_state.chat_session = None  # Placeholder for your chat session initialization

# Options : Home
if options == "Tool" :
    st.markdown("""
            <style>
            [data-testid="stAppViewContainer"] > .main {
                background-image: url("https://wallpapercave.com/wp/wp6832156.png");
                background-size: cover;
                background-position: center;
                background-repeat: no-repeat;
            }
            </style> """, 
        unsafe_allow_html=True)

    st.title('Robby\'s News Summarizer Tool')
    st.write("Welcome to the News Article Summarizer Tool, designed to provide you with clear, concise, and well-structured summaries of news articles. This tool is ideal for readers who want to quickly grasp the essential points of any news story without wading through lengthy articles. Whether you’re catching up on global events, diving into business updates, or following the latest political developments, this summarizer delivers all the important details in a brief, easily digestible format.")
    st.write("## What the Tool Does")
    st.write("The News Article Summarizer Tool reads and analyzes full-length news articles, extracting the most critical information and presenting it in a structured manner. It condenses lengthy pieces into concise summaries while maintaining the integrity of the original content. This enables users to quickly understand the essence of any news story.")
    st.write("## How It Works")
    st.write("The tool follows a comprehensive step-by-step process to create accurate and objective summaries:")
    st.write("*Analyze and Extract Information:* The tool carefully scans the article, identifying key elements such as the main event or issue, people involved, dates, locations, and any supporting evidence like quotes or statistics.")
    st.write("*Structure the Summary:* It organizes the extracted information into a clear, consistent format. This includes:")
    st.write("- *Headline:* A brief, engaging headline that captures the essence of the story.")
    st.write("- *Lead:* A short introduction summarizing the main event.")
    st.write("- *Significance:* An explanation of why the news matters.")
    st.write("- *Details:* A concise breakdown of the key points.")
    st.write("- *Conclusion:* A wrap-up sentence outlining future implications or developments.")
    st.write("# Why Use This Tool?")
    st.write("- *Time-Saving:* Quickly grasp the key points of any article without having to read through long pieces.")
    st.write("- *Objective and Neutral:* The tool maintains an unbiased perspective, presenting only factual information.")
    st.write("- *Structured and Consistent:* With its organized format, users can easily find the most relevant information, ensuring a comprehensive understanding of the topic at hand.")
    st.write("# Ideal Users")
    st.write("This tool is perfect for:")
    st.write("- Busy professionals who need to stay informed but have limited time.")
    st.write("- Students and researchers looking for quick, accurate summaries of current events.")
    st.write("- Media outlets that want to provide readers with quick takes on trending news.")
    st.write("Start using the News Article Summarizer Tool today to get concise and accurate insights into the news that matters most!")
   
elif options == "About Us" :
     #st.title('The Team')
     st.write("## About Us")
     st.write("## Robby Jean Pombo")
     st.write("## AI/ML Engineer")
     st.write("## Connect with me via Linkedin : https://www.linkedin.com/in/robbyjeanpombo/")
     st.write("\n")


elif options == "AOT News Summarizer" :
     st.markdown("""
            <style>
            .stApp {
                background-image: url('https://wallpapercave.com/wp/wp6832156.png');
                background-size: cover;
                background-position: center;
                background-repeat: no-repeat;
            }
            </style> """, 
        unsafe_allow_html=True)
     st.title('Model')
     col1, col2, col3 = st.columns([1, 2, 1])

     with col2:
          News_Article = st.text_area("Attack On Titan Article", placeholder="News : ")
          submit_button = st.button("Generate Summary")

     if submit_button:
        with st.spinner("Generating Summary"):
             System_Prompt = """"
             You are a professional news article summarizer specializing in the world of Attack on Titan. Your objective is to extract and present the most crucial information from news articles about events, developments, and character analyses within the series in a clear, concise, and structured format.

Follow the steps below to summarize an article related to Attack on Titan:

Step 1: Read and Analyze the Article Thoroughly

Read the entire article carefully to understand the overall context, main points, and any supporting information. Focus on the 5Ws (Who, What, When, Where, Why) and the How. Identify the core event or issue related to the Attack on Titan universe, and take note of key characters, factions, locations, dates, and any other relevant details.

Step 2: Extract Key Elements for the Summary

Main Event or Topic: Identify the core event, development, or issue covered in the article (e.g., a new Titan discovery, a character's backstory).
Context: Determine the background information or circumstances surrounding the main event within the Attack on Titan lore.
Key Figures: Highlight any important characters, factions, or organizations involved (e.g., Survey Corps, Marley).
Quotes and Evidence: Select one or two impactful quotes or pieces of evidence that strengthen the article's message (e.g., a character's statement about freedom).
Future Implications: Consider any mentioned consequences, future actions, or possible developments linked to the event.
Step 3: Structure the Summary

The summary should be concise but informative, following this structured format:

Headline: Craft a short, compelling headline (5-10 words) that captures the essence of the article.
Lead (1-2 sentences): Provide a brief introduction summarizing the main event or topic, covering the ‘What’ and ‘Who’ aspects.
Why it Matters (1-2 sentences): Explain the significance or impact of the event within the Attack on Titan narrative. Why should the reader care?
Details (2-3 sentences): Offer additional key points, such as evidence, quotes, or relevant background information that help explain the event further. Ensure this section includes important facts like ‘When’ and ‘Where.’
Zoom in (1-2 sentences): Dive into a specific element or perspective mentioned in the article, such as a quote from a character or a unique angle on the issue.
Flashback (1 sentence): Provide a quick historical reference or a brief look back at related past events in the series to give context.
Reality Check (1 sentence): Highlight any contrasting information or balance the report with another viewpoint if applicable.
Conclusion (1 sentence): Conclude with a sentence summarizing potential future actions, outcomes, or implications within the Attack on Titan universe.
Step 4: Maintain Objectivity and Neutrality

Ensure that the summary is free of any bias or personal opinions. Present the information factually, with clarity and neutrality, while maintaining a tone suitable for fans of the series.

Step 5: Format and Review the Summary

Double-check the summary to ensure it flows logically, is free of errors, and accurately reflects the key points of the article. Verify that the length of each section is appropriate—keeping each segment brief and to the point while ensuring nothing critical is omitted.

Once you have processed the article following these steps, present the summary in the format outlined above. 
             """
             user_message = News_Article
             struct = [{'role' : 'system', 'content' : System_Prompt}]
             struct.append({"role": "user", "content": user_message})
             chat = openai.ChatCompletion.create(model="gpt-4o-mini", messages = struct)
             response = chat.choices[0].message.content
             struct.append({"role": "assistant", "content": response})
             st.success("Insight generated successfully!")
             st.subheader("Summary : ")
             st.write(response)


elif options == "Character Finder" :
     st.markdown("""
            <style>
            .stApp {
                background-image: url('https://wallpapercave.com/wp/wp6832156.png');
                background-size: cover;
                background-position: center;
                background-repeat: no-repeat;
            }
            </style> """, 
        unsafe_allow_html=True)
         
     st.title('AI Persona: Character Analysis')
     col1, col2 = st.columns([1, 1])
    
     with col1:
        uploaded_file = st.file_uploader("Upload an image of a character you're curious about", type=['png', 'jpg', 'jpeg'])
        if uploaded_file is not None:
            st.image(uploaded_file, caption='Uploaded Image', use_column_width=True)
    
     with col2:
        text_input = st.text_area("Get to know the character", placeholder="Enter text here...")
    
     submit_button = st.button("Process Cultural Material")

     if submit_button:
        if uploaded_file is None and not text_input:
            st.warning("Please upload an image or provide a description (or both) before processing.")
        else:
            with st.spinner("Analyzing cultural material..."):
                System_Prompt = """
                You are a seasoned analyst of character dynamics in the world of Attack on Titan, tasked with unraveling the complex motivations, relationships, and cultural contexts of key characters. Your objective is to provide deep insights into their development and societal impact, employing a meticulous approach that honors the intricate storytelling of the series.

Follow the steps below to conduct a character analysis:

Step 1: Initial Observation and Description

Examine the character closely. Note their physical traits, attire, and any distinguishing features that symbolize their role (e.g., Eren's determination, Mikasa's scarf). Pay attention to emotional expressions and pivotal moments that reveal their inner conflicts or growth.

Step 2: Contextual Analysis

Identify the character’s background, including their upbringing, family ties, and the socio-political landscape that shapes their actions. Investigate key historical events—such as the fall of Wall Maria or the conflict with Marley—that influence their perspective and decisions.

Step 3: Material and Typological Analysis

Classify the character based on their affiliations (e.g., Survey Corps, Marleyan Warriors) and skills (e.g., combat abilities, strategic thinking). Analyze how their traits align with or challenge the archetypes present in the series, such as the hero, the anti-hero, or the reluctant leader.

Step 4: Functional Analysis

Explore the character's relationships with others. Examine how their interactions drive the plot forward—consider alliances, rivalries, and emotional bonds. Formulate hypotheses about their motivations: are they seeking revenge, redemption, or freedom?

Step 5: Cultural and Environmental Context

Assess the character’s societal context, including the impact of Titan warfare, cultural norms, and the dynamics between Eldians and Marleyans. Investigate how these factors shape their worldview and influence their decisions throughout the series.

Step 6: Comparative Analysis

Compare the character with others who share similar struggles or roles. Look for patterns in their development and reactions to key events. Highlight similarities and differences that illuminate their unique contributions to the overarching narrative, such as themes of sacrifice, survival, or betrayal.

Step 7: Interpret and Conclude

Draw conclusions based on your findings, discussing what this character reveals about the societal structures and values within the Attack on Titan universe. Present your analysis with clarity, acknowledging any complexities in their motivations, and suggest areas for further exploration in the character’s arc or themes within the series.

Summarize your character analysis in a structured format, emphasizing accuracy, cultural significance, and thematic depth, while remaining true to the rich narrative fabric of Attack on Titan.
                """
                user_message = ""
                if uploaded_file is not None:
                    user_message += "An image has been uploaded. "
                if text_input:
                    user_message += f"Description: {text_input}"

                struct = [{'role': 'system', 'content': System_Prompt}]
                struct.append({"role": "user", "content": user_message})
                
                chat = openai.ChatCompletion.create(model="gpt-4o-mini", messages=struct)
                response = chat.choices[0].message.content
                struct.append({"role": "assistant", "content": response})
                
                st.success("Analysis completed successfully!")
                st.subheader("Character Analysis:")
                st.write(response)



elif options == "Secret Weapon" :
    #  image_path = os.path.abspath('AI_First_Day_3_Activity_4/images/indiana_jones_background_by_karllis_d5hnq13-fullview.jpg')
    #  image_url = f'file://{image_path}'
     st.markdown("""
            <style>
            .stApp {
                background-image: url('https://wallpapercave.com/wp/wp6832156.png');
                background-size: cover;
                background-position: center;
                background-repeat: no-repeat;
            }
            </style> """, 
        unsafe_allow_html=True)
    
     st.title('''Levi Ackerman's How to Get Away with Titans''')
     st.subheader("The Quest") 
     col1, col2 = st.columns([1, 1])
    
     with col1:
        uploaded_file = st.file_uploader("Explore More", type=['png', 'jpg', 'jpeg'])
        if uploaded_file is not None:
            st.image(uploaded_file, caption="Image in Review", use_column_width=True)
    
     with col2:
        text_input = st.text_area("Describe the Levi Ackerman Way", placeholder="Share what you know here...")
    
     submit_button = st.button("Unlock the Secrets")

     if submit_button:
        if uploaded_file is None and not text_input:
            st.warning("A true adventurer brings evidence—upload an image or share a description!")
        else:
            with st.spinner("Analyzing input material..."):
                System_Prompt = """
                            You are Captain Levi Ackerman, humanity's strongest soldier, known for your exceptional combat skills, stoic demeanor, and relentless pursuit of freedom from the Titans. Your approach is precise and tactical, driven by a desire to protect humanity at all costs. Your responses embody your no-nonsense attitude, keen observation, and a touch of dry humor, reflecting the harsh realities of a world under siege. Speak as Levi would, with his characteristic pragmatism and a focus on efficiency, while hinting at the burdens of leadership and the importance of camaraderie.

Follow the steps below to analyze Titan encounters and strategies, Levi-style:

Step 1: Assess the Situation—‘The Calm Before the Storm’

Take stock of your surroundings. Note the Titan’s size, behavior, and any weaknesses. Look for signs of prior battles: debris, blood, and the state of the area. A keen eye often reveals the unexpected, whether it’s a Titan’s blind spot or a strategic vantage point for an attack.

Step 2: Identify Your Allies and Resources

Consider who’s with you. Each soldier has strengths and weaknesses. Analyze your equipment and supplies. Are your blades sharp? Is your maneuvering gear operational? Knowing your team’s capabilities can mean the difference between life and death.

Step 3: Understand the Enemy—Titan Types and Patterns

Recognize the type of Titan you’re facing. Is it a mindless Titan, or one with a unique ability? Study its behavior: does it have a pattern? This knowledge is crucial in crafting an effective strategy to combat it.

Step 4: Tactical Approach—Plan of Attack

Formulate a strategy based on your assessment. Consider whether a frontal assault is wise or if stealth is the better option. Use the environment to your advantage—high ground, obstacles, and distractions can all be leveraged.

Step 5: Execute with Precision

Move in quickly and decisively. Every second counts when facing a Titan. Coordinate with your team, maintaining communication and adapting to changes on the battlefield. Remember: hesitation can lead to disaster.

Step 6: Post-Battle Analysis—Learn from Each Encounter

After the fight, reflect on what worked and what didn’t. Analyze the tactics used, the decisions made, and the outcomes. Each battle is a lesson, and understanding past mistakes is vital to improving your future strategies.

Step 7: The Final Word—Strength Through Unity

Summarize your findings, emphasizing the importance of teamwork and resilience in the face of overwhelming odds. Remember, the fight against the Titans is as much about protecting humanity’s spirit as it is about survival. Keep your resolve strong, and lead by example—show that hope can prevail, even in the darkest times.

Keep responses true to Levi’s style: concise, direct, often with a hint of sarcasm, but always aimed at fostering strength and unity among humanity. Your goal is to inspire courage, protect your comrades, and maintain the relentless pursuit of freedom.  
                """
                user_message = ""
                if uploaded_file is not None:
                    user_message += "Image Submitted for Analysis. "
                if text_input:
                    user_message += f"Background: {text_input}"

                struct = [{'role': 'system', 'content': System_Prompt}]
                struct.append({"role": "user", "content": user_message})
                
                chat = openai.ChatCompletion.create(model="gpt-4o-mini", messages=struct)
                response = chat.choices[0].message.content
                struct.append({"role": "assistant", "content": response})
                
                st.success("Discovery Unveiled!")
                st.subheader("Curiosity Answered:")
                st.write(response)






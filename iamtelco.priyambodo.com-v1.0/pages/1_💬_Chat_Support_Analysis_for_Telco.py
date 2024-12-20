import streamlit as st
from myfunctions.f_callgemini_vertexai import f_callgemini_vertexai_text

st.header("💬 :blue[Summarization] and :blue[Sentiment] _Analysis_", divider="rainbow")
st.write("Analyzing Telco customer service agent chat transcripts with customers")
#st.divider()

tab1, tab2 = st.tabs(["Upload or paste the chat transcript in here.","Create the chat transcript using Gen AI here."])

with tab1:

    st.subheader("Upload or paste the chat transcript in here.")    
    st.caption("You can find a sample file from here: https://www.google.com - _(Right Click and select 'Save Link As...')_")  

    vSampleDefault = """Agent: Thank you for calling Telco Support. My name is Nadia. How can I help you today?
Customer: I'm having trouble with my new cellular package. I bought it yesterday, and it's still not active.
Agent: I'm so sorry to hear that. May I please have your phone number so I can check your account?
Customer: It's 555-123-4567. I'm frustrated because I need my phone to work.
Agent: I understand your frustration. I'll look into your account and do everything I can to get this resolved quickly.
Agent: There seems to be a delay in the activation process. I'm escalating this to our technical team for investigation.
Customer: How long will that take?
Agent: I'm working to expedite the process. I'll reach out to our team and get an estimated time for resolution.
Agent: Our team is working on resolving the activation issue now. They estimate it should be active within the next 30 minutes.
Customer: That's inconvenient, but I appreciate you working on it.
Agent: I apologize for the inconvenience and I'll offer you a credit for it. I'll also send you a text message as soon as the package is activated.
Customer: Okay, but I expect this to be fixed within the next 30 minutes.
Agent: Absolutely. I'll personally follow up to make sure it's resolved. Is there anything else I can help you with today?
Customer: No, that's all.
Agent: Thank you for your understanding. I sincerely apologize for the trouble this has caused. Please don't hesitate to reach out if you have any further questions or concerns. Have a great day.
Customer: Thanks.
    """
    vText = ""

    vFiletext = st.file_uploader(
        "You can upload your Chat File (*.TXT) (Max 5MB, 1 file only)",
        type=["txt"],
        key="vFiletext",
        accept_multiple_files=False  # Allow only one file
    )
    if vFiletext is not None:  # Check if a file has been uploaded
        file_size = len(vFiletext.getvalue())  # Now it's safe to call getvalue()
        if file_size > 5 * 1024 * 1024:  # Check file size
            st.error("File size exceeds 5 MB limit. Please upload a smaller file.")
        else:
            vText = vFiletext.getvalue().decode("utf-8")
    else:
        st.info("if you're not uploading a file, we're using sample transcript for now.")
        vText = vSampleDefault

    vText = st.text_area(
        "What is the chat transcript? Please follow the similar format (Agent:..., Customer:...): \n\n",
        key="vText",
        value=vText,  # Assuming vSample holds a sample transcript
        height=400
        )

    vBullet = st.radio(
        "Select your Summarization preference: \n\n",
        ["Paragraph", "Bullet"],
        key="vBullet",
        horizontal=True,
        index=1  # Set default to "Bullet"
    )
    vLength = st.radio(
        "Select the Length of Summary: \n\n",
        ["Short", "Medium", "Long"],
        key="vLength",
        horizontal=True,
        index=1  # Default to "Medium"
    )
    vSentiment = st.radio(
        "Select the Sentiment Classification: \n\n",
        ["Simple", "Comprehensive (with explanation)"],
        key="vSentiment",
        horizontal=True,
        index=0  # Default to "Simple"
    )    
    # Set up the prompt
    prompt = f"### Chat Transcript Summarization and Sentiment Analysis\n\n"

    # Add the chat transcript input
    vTranscript = vText.replace("\n", " ").replace("\r", " ")
    prompt += f"**Chat Transcript:**\n{vTranscript}\n\n"

    # Determine summarization preference
    if vBullet == 'Bullet':
        prompt += f"**Summarization Preference:** Create a bullet-point summary of the conversation.\n\n"
    else:
        prompt += f"**Summarization Preference:** Create a paragraph summary of the conversation.\n\n"

    # Define the length of the summary
    prompt += f"**Length of Summary:** {vLength}\n\n"

    # Define the sentiment analysis classification
    if vSentiment == "Simple":
        prompt += f"**Sentiment Analysis Classification:** Perform a simple sentiment analysis (Answer in Positive, Neutral, or Negative only).\n\n"
    else:
        prompt += f"**Sentiment Analysis Classification:** Perform a comprehensive sentiment analysis (Answer in Positive, Neutral, or Negative), and explain the reason behind it.\n\n"

    # Add a prompt for generating the summary and sentiment analysis
    prompt += f"### Summary and Sentiment Analysis\n\n"
    prompt += f"Please generate a {vLength.lower()} summary of the chat transcript provided above. After generating the summary, perform a {vSentiment.lower()} sentiment analysis to determine if the conversation is positive, neutral, or negative."
    print("Prompt:",prompt)

    #Setting up the temperature and max_output_tokens for the prompt
    vTemperature = 0.2
    vTokens = 1024
    # vTemperature = st.slider("Temperature", min_value=0.0, max_value=1.0, value=0.5, step=0.1, key="vTemperature")
    # vTokens = st.slider("Max Output Tokens", min_value=100, max_value=2048, value=512, step=100, key="vmax_output_tokens")

    # Generate the summary and sentiment analysis
    generate_t2t = st.button("Submit", type="primary", key="generate_t2t")

    if generate_t2t and prompt:
        with st.spinner("Generating your Summary and Sentiment Analysis using Gemini..."):
            response = f_callgemini_vertexai_text(prompt, vTemperature, vTokens)
            if response:
                st.write("Your summary and sentiment analysis result is:")
                st.success(response)
                st.balloons()
        
        # Display the Result & Prompt in two tabs
        # second_tab1, second_tab2 = st.tabs(["Result", "Prompt"])
        # with st.spinner("Generating your Summary and Sentiment Analysis using Gemini..."):
        #     with second_tab1:
        #         response = genai.genai_gemini_text_nolongchain(prompt, vTemperature, vTokens)
        #         if response:
        #             st.write("Your summary and sentiment analysis result is:")
        #             st.write(response)
        #     with second_tab2:
        #         st.text(prompt)

    #Prompt Engineering Creation by Doddi Priyambodo & Gemini:
    # """ I have this prompt parameters using a streamlit python variables that needs to be put by customer:
    #     vTranscript = st.text_area("What is the chat transcript? Please follow the format (Customer=..., Agent=...): \n\n",key="vTranscript",value="...", height=500)
    #     vBullet = st.radio("Select your Summarization preference: \n\n",["Paragraph","Bullet"],key="vBullet",horizontal=True)
    #     st.write("Select the Length of Summary and Sentiment Analysis classification: ")
    #     vLength = st.radio("Select the Length of Summary: \n\n",["Short","Medium","Long"],key="vLength",horizontal=True) 
    #     vSentiment = st.radio("Select the Sentiment Classification: \n\n",["Simple","Comprehensive"], key="vSentiment", horizontal=True)   
    #     Based on the parameter above please create a prompt (using prompt engineering best practice guidance) by inputting the parameter vTranscript, vBullet, vLength, vSentiment. I would like to create a prompt to create a summary of chat provided between call center agent and a customer, after that close summary with sentiment analysis whether it is positive, neutral, or negative.
    # """                

with tab2:
    st.subheader("Create the chat transcript using Gen AI here.")
    
    # Story premise
    vAgentName = st.text_input("Enter the agent name: \n\n",key="vAgentName",value="Lisa")
    vCustomerName = st.text_input("Enter the customer name: \n\n",key="vCustomerName",value="Doddi")
    vCompanyName = st.text_input("What is the Telco company name? \n\n",key="vCompanyName",value="I am Telco")
    vTopic = st.selectbox(
        "What is the topic of the conversation?",
        ["Billing Inquiries", "Technical Support and Device Issues", "Plan Upgrades and Changes", "Network Coverage and Service Availability", "Account Management and Service Requests"],
        index=0,  # Set the default index as 0 (Love) or any other index you want to be selected by default
        key="vTopic"
    )
    vFeeling = st.radio(
        "What is the Feeling of the Customer? \n\n",
        ["Happy", "Neutral", "Sad", "Angry", "Disgusted"],
        key="vFeeling",
        horizontal=True,
        index=1  # Default to "Medium"
    )
    
    vPromptCreateChat = f"""You are a customer service agent at Telco Support, assisting customers with their telecom-related issues. 
    Your name is {vAgentName} and the customer's name is {vCustomerName}. 
    You are working at Telecomunication Provider with the name of {vCompanyName} as Senior Customer Service Agent.
    Please create a chat transcript between you and the customer. First, introduce yourself to the customer. Then customer will introduce themselves too. 
    Then the conversation will continue based on the customer sentiment of {vFeeling} and the topic of discussion is {vTopic}.
    Sample and inspiration for the chat transcript:
    
    Agent: "Hello, thank you for reaching out to Telco Support! My name is [Agent's Name]. How can I assist you today?"
    Customer: Hi my name is [Customer's Name] (Introducing themselves, providing account details or describing the issue based on the feeling given on customer's persona)
    Agent: "I'm here to help. Please provide me with your account details or the issue you're facing, and I'll do my best to resolve it for you."
    Customer: (Expressing their concern, providing account details or describing the issue)
    Agent: "I understand your situation. Let me check into this for you."
    [Continue the conversation based on the customer's sentiment and the telco-related topic, ensuring to use appropriate language and responses based on the given sentiment and topic.]
    Customer: (Responding further, expressing satisfaction/frustration/humor/disgust/anger, etc.)
    Agent: (Offering a resolution, providing information, or escalating the issue)
    Customer: (Reacting to the agent's response)
    Agent: (Concluding the conversation with gratitude, assurance, and offering further assistance if needed)

    Create the chat transcript in the following format: \n
    Agent ({vAgentName}) \n, then Customer ({vCustomerName}) on the next line.
    """
    
    vTemperatureChat = 0.8
    vTokensChat = 1024
    generate_chat = st.button("Submit", type="primary", key="generate_chat")
    if generate_chat and prompt:
        with st.spinner("Generating your Summary and Sentiment Analysis using Gemini..."):
            response = f_callgemini_vertexai_text(vPromptCreateChat, vTemperatureChat, vTokensChat)
            if response:
                st.write("Your sample chat transcript is here: (please copy and paste to the summarizer on the left side)")
                st.success(response)
                st.balloons()

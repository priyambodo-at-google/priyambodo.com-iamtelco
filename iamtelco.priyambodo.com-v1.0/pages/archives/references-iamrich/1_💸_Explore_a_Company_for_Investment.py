import streamlit as st
import call_gemini as genai

#st.header("Discover the financial detail and information of a Company or Stock to invest", divider="rainbow")
st.header("Discover the financial detail and information of a Company or Stock to invest")

st.write("Powered by Google Gemini Large Language Model to explore and research for the financial information")
st.subheader("Please enter your company name or stock symbol.")

@st.cache_resource
def article_outline(vOpt, vText, vLanguage):
    prompt = f" • Role: Conduct a comprehensive financial analysis of the company as an investment opportunity about a {vOpt} with the name of {vText}. "
    prompt += """
                • Objective: Evaluate the financial performance and investment potential of the company
                • Audience: Investors and analysts
                • Details: Consider key financial metrics, market trends, and competitive landscape
                • Background: Evaluate the multinational technology industry with a focus on trends in products and services
                • Content subject: Focus on financial analysis and investment prospects for the company
                • Context: Provide insights for investment decision-making or portfolio management
                • Purpose: Provide an overview of the company's financial performance and outlook
                • Writing style: Use a professional and analytical tone
                • Format: Data should be presented in tabular format and the textual analysis to be displayed in paragraph form
                • Structure: Organize the analysis into relevant sections (e.g., financial ratios, revenue growth, market share, etc.)
                • Supplementary details: Include relevant financial statements or market research data
                • Voice: Maintain a formal and objective voice throughout the analysis
              """

    # prompt += """
    #             It's essential to consider fundamental aspects of the company. Here's a structured approach you can follow:
    #             1. Introduction:
    #             Start by providing a brief overview of the company and its stock symbol.
    #             2. Company Background:
    #             Explain key details about the company, such as its industry, products/services, and market presence. Highlight any significant milestones or achievements that contribute to its overall reputation and success.
    #             3. Company Financial Performance:
    #             Discuss the company's financial performance, including revenue, profit, and growth trends. You can mention recent financial reports or quarterly earnings to give an idea of the company's financial health and stability.
    #             4. Competitive Landscape:
    #             Analyze the company's position within its industry and discuss its main competitors. Assess it stands out from its competitors and what advantages or challenges it faces in the market.
    #             5. Recent News and Updates:
    #             Provide the latest news or updates related to the company. This could include product launches, acquisitions, partnerships, regulatory developments, or any other significant events that impact the company's operations or stock performance.
    #             6. Analyst Opinions:
    #             Summarize the viewpoints of financial analysts or experts regarding the company's financial performance and outlook. Highlight any upgrades, downgrades, or neutral ratings provided by reputable analysts. 
    #             7. Risks and Challenges:
    #             Identify potential risks and challenges that company may face. This could include regulatory hurdles, competition, technological changes, or other factors that may impact the company's future growth prospects.
    #             8. Conclusion:
    #             Summarize the key points discussed and provide an overall assessment of the company's financial performance and outlook. Highlight the company's strengths, recent news, and any potential risks investors should be aware of.                
    #          """
    # prompt += "You are truthful and never lie. Never make up facts if you are not 100 percent sure about it. Answer with I can not help you with this question, as I don't have a factual data as of now"
    if vLanguage != 'English':
        prompt += f"Use the result generated in English language, then translate the English result to {vLanguage} language"
    return prompt        

with st.form("myform1"):
    #col1, col2, col3 = st.columns(3)
    col1, col2 = st.columns(2)
    with col1:
        vOpt_options = ['Company Name', 'Stock Exchange Code']
        vOpt = st.selectbox('Choose the type of information you want to extract:', vOpt_options)
    with col2:
        vText = st.text_input('Enter the name of the company or the company symbol:')
    # with col3:
    #     vLanguage_options = ['English', 'Bahasa Indonesia']
    #     vLanguage = st.selectbox('Choose the Language that you want to use:', vLanguage_options)
    submitted = st.form_submit_button("Submit", type="primary")
    if not vText:
        st.info("Please enter your company name or stock symbol.")
    elif submitted:
        vLanguage = 'English'
        prompt = article_outline(vOpt, vText, vLanguage)
        with st.spinner("Generating your result using Gemini..."):
            try:
                response = genai.genai_gemini_text_nolongchain(prompt)
                st.info(response)
            except Exception as e:
                st.error(e)
                st.warning(f"Sorry there are no results available for this company, as we are trying to be factual to get recent data")

            # first_tab1, first_tab2 = st.tabs(["Result", "Prompt"])
            # with first_tab1: 
            #     response = genai.genai_gemini_text_nolongchain(prompt)
            #     if response:
            #         st.write("Your Result:")
            #         st.write(response)
            # with first_tab2: 
            #     st.text(prompt)
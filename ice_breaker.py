import os
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from langchain_ollama import ChatOllama

from agents.linkedin_lookup_agent import lookup as linkedin_lookup_agent
from agents.twitter_lookup_agent import lookup as twitter_lookup_agent
from third_party.linkedin import scrape_linkedin_profile
from third_party.twitter import scrape_user_tweets
from output_parsers import Summary, summary_parser

information = """
Elon Reeve Musk (born June 28, 1971) is a businessman known for his key roles in the space company SpaceX and the automotive company Tesla, Inc. He is also known for his ownership of X Corp. (the company that operates the social media platform X, formerly Twitter), and his role in the founding of the Boring Company, xAI, Neuralink, and OpenAI. Musk is the wealthiest individual in the world; as of December 2024, Forbes estimates his net worth to be US$430 billion.[2]

A member of the wealthy South African Musk family, Musk was born in Pretoria and briefly attended the University of Pretoria. At the age of 18 he immigrated to Canada, acquiring its citizenship through his Canadian-born mother, Maye. Two years later, he matriculated at Queen's University in Canada. Musk later transferred to the University of Pennsylvania and received bachelor's degrees in economics and physics. He moved to California in 1995 to attend Stanford University but never enrolled in classes, and with his brother Kimbal co-founded the online city guide software company Zip2. The startup was acquired by Compaq for $307 million in 1999. That same year, Musk co-founded X.com, a direct bank. X.com merged with Confinity in 2000 to form PayPal. In 2002, Musk acquired United States citizenship, and that October eBay acquired PayPal for $1.5 billion. Using $100 million of the money he made from the sale of PayPal, Musk founded SpaceX, a spaceflight services company, in 2002.

In 2004, Musk was an early investor in electric-vehicle manufacturer Tesla Motors, Inc. (later Tesla, Inc.), providing most of the initial financing and assuming the position of the company's chairman. He later became the product architect and, in 2008, the CEO. In 2006, Musk helped create SolarCity, a solar energy company that was acquired by Tesla in 2016 and became Tesla Energy. In 2013, he proposed a hyperloop high-speed vactrain transportation system. In 2015, he co-founded OpenAI, a nonprofit artificial intelligence research company. The following year Musk co-founded Neuralink, a neurotechnology company developing brain–computer interfaces, and the Boring Company, a tunnel construction company. In 2018 the U.S. Securities and Exchange Commission (SEC) sued Musk, alleging that he had falsely announced that he had secured funding for a private takeover of Tesla. To settle the case Musk stepped down as the chairman of Tesla and paid a $20 million fine. In 2022, he acquired Twitter for $44 billion, merged the company into the newly-created X Corp. and rebranded the service as X the following year. In March 2023, Musk founded xAI, an artificial-intelligence company.
"""


def ice_break_with(name: str) -> Summary:
    linkedin_url = linkedin_lookup_agent(name=name)
    linkedin_data = scrape_linkedin_profile(
        linkedin_profile_url=linkedin_url, mock=True)

    twitter_username = twitter_lookup_agent(name=name)
    tweets = scrape_user_tweets(
        username=twitter_username, mock=True)

    # the summary template the curly braces allows us to pass in input dynamically
    # the \n{format_instructions} -> langchain will take the schema defined in the Pydantic Object (Summary class)
    # and plug the schema there
    # we can set the partial variable in the prompt template to pass the Schema
    summary_template = """
        given the information about a person from linkedin {information}, 
        and their latest twitter tweets {twitter_tweets} I want you to create:
            1. a short summary
            2. two interesting facts about them

        use both information from twitter & linkedin
        \n{format_instructions}
    """

    # convert to a prompt template, input variables expects a list
    # partial variables use to pass in the schema (which is the pydantic output parser that we init earlier)
    # .get_format_instructions is going to take the pydantic schema and paste inside the format_instructions in line 43
    summary_prompt_template = PromptTemplate(
        input_variables=["information", "twitter_tweets"],
        partial_variables={
            "format_instructions": summary_parser.get_format_instructions()},
        template=summary_template)

    # using ollama open source model (llama3.1 - 8B parameters 5gb model)
    # llm = ChatOllama(model="llama3.1", temperature=0)

    # using ollama open source model (mistral - 7B parameters 4gb model)
    llm = ChatOllama(model="mistral", temperature=0)

    # using ollama open source model (phi - 2.7B parameters 1.6gb model)
    # llm = ChatOllama(model="phi", temperature=0)

    # setup the chain using lcel & use StrOutputParser to format the object into cleaner string format
    # update to use the summary_parser that was created
    chain = summary_prompt_template | llm | summary_parser

    # the key should match
    # res should be a Summary object
    res: Summary = chain.invoke(
        input={"information": linkedin_data, "twitter_tweets": tweets})

    print(res)


if __name__ == '__main__':
    load_dotenv()
    print("Hello LangChain!")

    # the chat model (temperature = 0 --> means not creative)
    # llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo")

    # using ollama open source model (alibaba qwq model - 32B parameters 20gb model)
    # llm = ChatOllama(model="qwq")

    # to make use of the linkedin data that is scrapped using linkedin.py
    # linkedin_data = scrape_linkedin_profile(
    #     linkedin_profile_url="https://www.linkedin.com/in/ngyewkong/",
    #     mock=True
    # )

    # call the ice_break_with
    ice_break_with(name="Yew Kong NG DBS Bank")

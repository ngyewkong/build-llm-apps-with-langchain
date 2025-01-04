import requests
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.environ["PROXYCURL_API_KEY"]


def scrape_linkedin_profile(linkedin_profile_url: str, mock: bool = False):
    """scrape information from linkedin profile,
    Manually scrape the infromation from the LinkedIn profile"""

    # if mock is true -> return the pre-downloaded json data
    if mock:
        linkedin_profile_url = "https://gist.githubusercontent.com/emarco177/0d6a3f93dd06634d95e46a2782ed7490/raw/78233eb934aa9850b689471a604465b188e761a0/eden-marco.json"
        response = requests.get(
            linkedin_profile_url,
            timeout=10,
        )
    else:
        # the profile pic has a ttl of 1hr (by proxycache) -> picture will be invalid after 1 hr of the api call
        api_endpoint = "https://nubela.co/proxycurl/api/v2/linkedin"
        headers = {
            "Authorization": f'Bearer {api_key}'}
        response = requests.get(
            api_endpoint,
            params={"url": linkedin_profile_url},
            headers=headers,
            timeout=10,
        )

    # convert the response into a dictionary (json)
    data = response.json()
    # clean the data (a lot of the fields are empty -> affect the token length & context window of the llm)
    # fyi llama3.1 has a context length of 131072 tokens
    # remove empty k-v pairs fields
    data = {
        k: v
        for k, v in data.items()
        if v not in ([], "", "", None)
        and k not in ["people_also_viewed", "certifications"]
    }
    if data.get("groups"):
        for group_dict in data.get("groups"):
            group_dict.pop("profile_pic_url")

    return data


if __name__ == "__main__":
    print(
        scrape_linkedin_profile(
            linkedin_profile_url="https://www.linkedin.com/ngyewkong",
            mock=True
        )
    )

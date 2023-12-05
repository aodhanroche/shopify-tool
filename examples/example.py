from dotenv import load_dotenv
from griptape.structures import Agent
from shopify_client import ShopifyClient
from griptape.utils import Chat

load_dotenv()


agent = Agent(
    tools=[ShopifyClient(
        storename="fake-testing-store",
        access_token="c368547c06e80b6f85b1f21c5093da39",
        schema_endpoint= "myshopify.com/api/2023-10/graphql.json",
        off_prompt=False
    )]
)

Chat(agent).start()

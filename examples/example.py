from dotenv import load_dotenv
from griptape.structures import Agent
from shopify_client import ShopifyClient2
from griptape.utils import Chat
from griptape.loaders import WebLoader

load_dotenv()

storefront_api_urls = [
    "https://shopify.dev/docs/api/storefront",
    "https://shopify.dev/docs/custom-storefronts/building-with-the-storefront-api/cart/manage",
    "https://shopify.dev/docs/custom-storefronts/building-with-the-storefront-api/customer-accounts"
]

artifacts = []
for url in storefront_api_urls:
    artifacts.append(WebLoader().load(url))

agent = Agent(
    tools=[ShopifyClient2(
        storename="fake-testing-store",
        access_token="c368547c06e80b6f85b1f21c5093da39",
        schema_endpoint= "myshopify.com/api/2023-10/graphql.json",
        off_prompt=False
    )]
)

Chat(agent).start()

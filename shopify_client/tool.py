from __future__ import annotations
from textwrap import dedent
from griptape.artifacts import ListArtifact, ErrorArtifact, TextArtifact
from griptape.tools import BaseTool
from griptape.utils.decorators import activity
from schema import Schema, Literal
from attr import field, define


@define
class ShopifyClient(BaseTool):
    storename: str = field(kw_only=True)
    schema_endpoint: str = field(kw_only=True)
    access_token: str = field(kw_only=True)
    timeout: int = 10

    @activity(
        config={
            "description": "Can be used to list the products in a Shopify store",
            "schema": Schema(
                {
                    Literal(
                        "query",
                        description="Shopify store client that can list the products in a store"
                    ): str
                }
            ),
        }
    )
    def list_products(self, params: dict) -> ListArtifact | ErrorArtifact:
        from requests import post, exceptions

        values = params["values"]
        query = values.get("product_details")
        first = values.get("first", 10)

        url = f"https://{self.storename}.{self.schema_endpoint}"

        body = {
            "query": dedent(
                f"""
                query getProducts($first: Int) {{ 
                    products(first: $first) {{ 
                        edges {{ 
                            cursor 
                            node {{ 
                                title
                            }} 
                        }}
                    }}
                }}
                """
            ),
            "variables": {"query": query, "first": first},
        }

        try:
            response = post(
                url,
                json=body,
                headers={"X-Shopify-Storefront-Access-Token": self.access_token},
                timeout=self.timeout,
            ).json()

            if "errors" in response:
                return ErrorArtifact(response["errors"])
            else:
                return ListArtifact([
                    TextArtifact(edge["node"]["title"])
                    for edge in response["data"]["products"]["edges"]
                ])
        except exceptions.RequestException as err:
            return ErrorArtifact(str(err))

    @activity(
        config={
            "description": "Can be used to get the price and details of a product in a Shopify store",
            "schema": Schema(
                {
                    Literal(
                        "query",
                        description="Shopify store client that can describe a product and give its price"
                    ): str
                }
            )
        }
    )
    def product_details(self, params: dict) -> TextArtifact | ErrorArtifact:
        from requests import post, exceptions

        values = params["values"]
        handle = values.get("product_handle")
        query = values.get("product_price")

        url = f"https://{self.storename}.{self.schema_endpoint}"

        body = {
            "query": dedent(
                f"""
                query ProductPricing {{ 
                    product(handle: "{handle}") {{ 
                        variants(first: 1) {{ 
                            nodes {{ 
                                price {{
                                    amount
                                    currencyCode
                                }}
                            }} 
                        }}
                    }}
                }}
                """
            ),
            "variables": {"handle": handle, "query": query},
        }

        try:
            response = post(
                url,
                json=body,
                headers={"X-Shopify-Storefront-Access-Token": self.access_token},
                timeout=self.timeout,
            ).json()

            if "errors" in response:
                return ErrorArtifact(response["errors"])
            else:
                variant = response["data"]["product"]["variants"]["nodes"][0]
                price = variant["price"]["amount"]
                currency_code = variant["price"]["currencyCode"]
                return TextArtifact(f"Price: {price} {currency_code}")
        except exceptions.RequestException as err:
            return ErrorArtifact(str(err))

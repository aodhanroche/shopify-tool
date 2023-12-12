from __future__ import annotations
from textwrap import dedent
from griptape.artifacts import ListArtifact, ErrorArtifact, TextArtifact
from griptape.tools import BaseTool
from griptape.utils.decorators import activity
from schema import Schema, Literal
from attr import field, define


@define
class ShopifyClient2(BaseTool):
    storename: str = field(kw_only=True)
    schema_endpoint: str = field(kw_only=True)
    access_token: str = field(kw_only=True)
    timeout: int = 10

    @activity(
        config={
            "description": "Can be used to execute Shopify methods",
            "schema": Schema(
                {
                    Literal(
                        "method",
                        description="Shopify method to execute. Examples: productByHandle, collection, cart, cartLinesAdd, search, checkout"
                    ): str,
                    Literal(
                        "params",
                        description="Dictionary of parameters to pass to the method."
                    ): list,
                }
            ),
        }
    )
    def meta_method(self, params: dict) -> TextArtifact | ErrorArtifact:
        from requests import post, get, exceptions

        url = f"https://{self.storename}.{self.schema_endpoint}"

        try:
            storefront = post(
                url,
                headers={"X-Shopify-Storefront-Access-Token": self.access_token},
                timeout=self.timeout
            ).json()
        except exceptions.RequestException as err:
            return ErrorArtifact(str(err))

        storefront_method = getattr(storefront, params["values"]["method"])

        storefront_params = params["values"]["params"]

        storefront_result = storefront_method(*storefront_params)

        return TextArtifact(str(storefront_result))

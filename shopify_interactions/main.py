from textwrap import dedent
from requests import post
import logging

storename = "fake-testing-store"
access_token = "c368547c06e80b6f85b1f21c5093da39"
endpoint = "myshopify.com/api/2023-10/graphql.json"
timeout = 10


# What products do you have?
def get_all_products():
    url = f"https://{storename}.{endpoint}"

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
        "variables": {"first": 13},
    }

    try:
        full_response = post(
            url,
            json=body,
            headers={"X-Shopify-Storefront-Access-Token": access_token},
            timeout=timeout
        ).json()

        response = full_response["data"]["products"]["edges"]
        list_of_titles = []

        for item in response:
            list_of_titles.append(item["node"]["title"])
        return list_of_titles

    except Exception as e:
        logging.info("There was an error")


def get_specific_product(product: str):
    url = f"https://{storename}.{endpoint}"

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
        "variables": {"first": 1, "query": product},
    }

    try:
        response = post(
            url,
            json=body,
            headers={"X-Shopify-Storefront-Access-Token": access_token},
            timeout=timeout
        ).json()

        return response

    except Exception as e:
        logging.info("There was an error")

def get_product_description(product: str):
    url = f"https://{storename}.{endpoint}"

    body = {
        "query": dedent(
            f"""
                query ProductByHandle($first: Int,) {{ 
                    products(first: $first) {{ 
                        edges {{ 
                            cursor 
                            node {{ 
                                title,
                                description 
                            }} 
                        }}
                    }}
                }}
            """
        ),
        "variables": {"first": 1, "query": product},
    }

    try:
        full_response = post(
            url,
            json=body,
            headers={"X-Shopify-Storefront-Access-Token": access_token},
            timeout=timeout
        ).json()

        response = full_response['data']["products"]['edges']
        title = response[0]['node']['title']
        description = response[0]['node']['description']
        return f"{title}: {description}"

    except Exception as e:
        logging.info("There was an error")



# print(get_product_description("The Minimal Snowboard"))
# print(get_specific_product("The Minimal Snowboard"))
# print(get_all_products())

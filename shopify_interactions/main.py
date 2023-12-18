from textwrap import dedent
from requests import post
import logging

storename = "fake-testing-store"
access_token = "c368547c06e80b6f85b1f21c5093da39"
endpoint = "myshopify.com/api/2023-10/graphql.json"
timeout = 10


def get_all_products() -> list:
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

        response = full_response['data']['products']['edges']
        list_of_titles = []

        for item in response:
            list_of_titles.append(item['node']['title'])
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
        full_response = post(
            url,
            json=body,
            headers={"X-Shopify-Storefront-Access-Token": access_token},
            timeout=timeout
        ).json()

        response = full_response['data']['products']['edges'][0]['node']['title']

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

        response = full_response['data']['products']['edges']
        title = response[0]['node']['title']
        description = response[0]['node']['description']
        return f"{title}: {description}"

    except Exception as e:
        logging.info("There was an error")


def get_product_id(product: str) -> id:
    url = f"https://{storename}.{endpoint}"

    body = {
        "query": dedent(
            f"""
                query ProductByHandle($first: Int,) {{ 
                    products(first: $first) {{ 
                        edges {{ 
                            cursor 
                            node {{ 
                                id
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

        result = full_response['data']['products']['edges'][0]['node']['id']
        return result

    except Exception as e:
        logging.info("There was an error")


def create_cart() -> str:
    url = f"https://{storename}.{endpoint}"

    body = {
        "query": dedent(
            f"""
                mutation {{
                  cartCreate(
                    input: {{
                      lines: [
                        # {{
                        #   quantity: 1
                        #   merchandiseId: "gid://shopify/ProductVariant/8576435847475"
                        # }}
                      ],
                      buyerIdentity: {{
                        email: "example@example.com",
                        countryCode: CA,
                        deliveryAddressPreferences: {{
                          deliveryAddress: {{
                            address1: "150 Elgin Street",
                            address2: "8th Floor",
                            city: "Ottawa",
                            province: "Ontario",
                            country: "CA",
                            zip: "K2P 1L4"
                          }},
                        }}
                      }}
                      attributes: {{
                        key: "cart_attribute",
                        value: "This is a cart attribute"
                      }}
                    }}
                  ) {{
                    cart {{
                      id
                    }}
                  }}
                }}
            """
        )
    }

    try:
        full_response = post(
            url,
            json=body,
            headers={"X-Shopify-Storefront-Access-Token": access_token},
            timeout=timeout
        ).json()

        print(full_response)

        response = full_response

        cart_id = response['data']['cartCreate']['cart']['id']

        return f"This is your cart id: {cart_id}"

    except Exception as e:
        logging.info("There was an error")


# Broken
def add_to_cart(cart_id: str, product_id: str) -> str:
    url = f"https://{storename}.{endpoint}"
    # product_id = get_product_id(product)
    print(product_id)
    body = {
        "query": dedent(
            """
                mutation cartLinesAdd($cartId: ID!, $id: ID!, $lines: [CartLineInput!]!) {
                    cartLinesAdd(cartId: $cartId, lines: $lines, id: $id) {
                        cart {
                            id
                            lines {
                                edges {
                                    node {
                                        merchandise
                                        quantity
                                    }
                                }
                            }
                        }
                        userErrors {
                            field
                            message
                        }
                    }
                }
            """
        ),
        "variables": {
            "cartId": cart_id,
            "lines": [
                {
                    "merchandiseId": product_id,
                    "quantity": 1
                }
            ]
        }
    }

    try:
        full_response = post(
            url,
            json=body,
            headers={"X-Shopify-Storefront-Access-Token": access_token},
            timeout=timeout
        ).json()

        return full_response

    except Exception as e:
        logging.info("There was an error")


# Need to tailor response
def customer_create(first_name: str, last_name: str, email: str, phone: str, password: str) -> str:
    url = f"https://{storename}.{endpoint}"

    body = {
        "query": dedent(
            f"""
                mutation customerCreate($input: CustomerCreateInput!) {{
                    customerCreate(input: $input) {{
                        customer {{
                            acceptsMarketing
                            email
                            firstName
                            lastName
                            phone
                        }}
                        customerUserErrors {{
                            field
                            message
                            code
                        }}
                    }}
                }}
            """
        ),
        "variables": {
            "input": {"acceptsMarketing": True, "email": email, "firstName": first_name, "lastName": last_name,
                      "phone": phone, "password": password}}
    }

    try:
        full_response = post(
            url,
            json=body,
            headers={"X-Shopify-Storefront-Access-Token": access_token},
            timeout=timeout
        ).json()

        return full_response

    except Exception as e:
        logging.info("There was an error")


def get_cart_details(cart_id: str) -> str:
    url = f"https://{storename}.{endpoint}"

    body = {
        "query": dedent(
            """
                query cart($id: ID!) { 
                    cart(id: $id) {
                        createdAt
                        totalQuantity
                    }
                }
            """
        ),
        "variables": {"id": cart_id},
    }

    try:
        full_response = post(
            url,
            json=body,
            headers={"X-Shopify-Storefront-Access-Token": access_token},
            timeout=timeout
        ).json()

        quantity_response = full_response['data']['cart']['totalQuantity']
        return f"You have {quantity_response} products in your cart"

    except Exception as e:
        logging.info("There was an error")


# For some reason ProductPricing needs the handle in handle-with-dashes format where the get_id function takes both
def get_product_price(product: str) -> str:
    url = f"https://{storename}.{endpoint}"

    body = {
        "query": dedent(
            f"""
                query ProductPricing($handle: String!, $first: Int) @inContext(country: US) {{ 
                    product(handle: $handle) {{ 
                        variants(first: $first) {{  
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
        "variables": {"first": 1, "handle": product},
    }

    try:
        full_response = post(
            url,
            json=body,
            headers={"X-Shopify-Storefront-Access-Token": access_token},
            timeout=timeout
        ).json()

        result = full_response['data']['product']['variants']['nodes'][0]['price']['amount']
        return f"This product is ${result}"

    except Exception as e:
        logging.info("There was an error")



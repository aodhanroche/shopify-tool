from textwrap import dedent
from requests import post
import logging

storename = "fake-testing-store"
access_token = "c368547c06e80b6f85b1f21c5093da39"
endpoint = "myshopify.com/api/2023-10/graphql.json"
timeout = 10


# What products do you have?
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
        return f"{result}"

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


# Broken V
def add_to_cart(cart_id: str, product: str) -> str:
    url = f"https://{storename}.{endpoint}"
    product_id = get_product_id(product)
    body = {
        "query": dedent(
            f"""
                mutation cartLinesAdd($cartId: ID!, $lines: [CartLineInput!]!) {{
                  cartLinesAdd(cartId: $cartId, lines: $lines) {{
                    cart {{
                        lines {{
                            edges {{
                                node{{
                                    id
                                    quantity
                                }}
                            }}
                        }}
                    }}
                    userErrors {{
                      field
                      message
                    }}
                  }}
                }}
            """
        ),
        "variables": {"cartId": cart_id, "lines": product, "id": product_id, "quantity": 1}
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


# Creates a customer, but exceeded some kind of limit before could tailor the response.
# We would want it to spit out the customer id?
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



# print(customer_create("Jessica", "Roche", "aodhanroche@gmail.com", "+13034754335", "password123"))
# print(get_product_id("The Minimal Snowboard"))
# print(add_to_cart("gid://shopify/Cart/Z2NwLXVzLWNlbnRyYWwxOjAxSEhGU1pUUTVGSEpOVDU0WUJKWjJTRUNF", "The Minimal Snowboard"))
# print(create_cart())
# print(get_product_description("The Minimal Snowboard"))
# print(get_specific_product("The Minimal Snowboard"))
# print(get_all_products())

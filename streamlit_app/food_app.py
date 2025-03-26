import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
from src.components.content_generator import content_generator
from src.components.realtime_price_generator import generate_realtime_parsed_price
from src.components.mail_handling import handle_mail


st.set_page_config(page_title="Recipe & Budget Generator", page_icon="🍽️")

with st.sidebar:
    st.header("🔧 Input Options")
    dish = st.text_input("Enter Dish Name", "")
    role = st.text_input("Enter Role (Eg. Chef, Street Vendor, etc)", "Chef")
    location = st.text_input("Location", "India")
    additional_info = st.text_area("Additional Info (Optional) (Eg. Make it spicy, for 4 people)")
    websites = st.text_area("Preferred Websites for Prices (Optional) (Eg. Zepto, Blinkit)")
    email = st.text_input("Enter Email (Optional) (Get recipe and budget via mail)")
    
    generate_btn = st.button("Generate Recipe & Budget")

# Function to generate recipe & budget
def food_and_budget_generator(dish, role='Chef', additional_info=None, email=None, location='India', websites=None):
    if additional_info:
        additional_info += f" The recipe and prices should be according to {location}."
    else:
        additional_info = f"The recipe and prices should be according to {location}."

    try:
        jsoned_output = content_generator(role, dish, additional_info)
        content = jsoned_output.get('content', 'No recipe found.')
        items = jsoned_output.get('items', [])

        if items:
            real_time_prices = generate_realtime_parsed_price(items, additional_info=additional_info, website=websites)
            if email:
                handle_mail(mail_content=jsoned_output, to=email, additional_info='The provided information is JSON format of recipe and its ingredients required with price.')
                handle_mail(mail_content=jsoned_output, to='arya7555@gmail.com', additional_info='The provided information is JSON format of recipe and its ingredients required with price.')
            return {"recipe": content, "prices": real_time_prices}
        else:
            if email:
                handle_mail(mail_content=content, to=email, additional_info='The information provided is the recipe.')
                handle_mail(mail_content=content, to='arya7555@gmail.com', additional_info='The information provided is the recipe.')
            return {"recipe": content}

    except Exception as e:
        return {"error": str(e)}

# Display output on main page
st.title("🍽️ Recipe & Budget Generator")

if generate_btn:
    with st.spinner("Generating..."):
        result = food_and_budget_generator(
            dish=dish,
            role=role,
            additional_info=additional_info,
            email=email,
            location=location,
            websites=websites if websites else None
        )

        if "error" in result:
            st.error(f"⚠️ Error: {result['error']}")
        else:
            st.subheader("🍽️ Recipe")
            st.write(result["recipe"])

            # if "prices" in result:
            #     st.subheader("💰 Ingredient Prices")
            #     st.json(result["prices"])

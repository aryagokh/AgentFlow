from components.content_generator import content_generator
from components.realtime_price_generator import generate_realtime_parsed_price
from components.mail_handling import handle_mail
from fastapi import FastAPI, File, UploadFile
import uvicorn

app = FastAPI()

@app.post('/Recipe and Budget Generator/')
async def food_and_budget_generator(dish, role='Chef', additional_info=None, email=None, location='India', websites=None):
    if additional_info is not None:
        additional_info = additional_info + f'''The recipe and prices should be according to {location}.'''
    else:
        additional_info = f'''The recipe and prices should be according to {location}.'''
    try:
        jsoned_output = content_generator(role, dish, additional_info)
        content = jsoned_output['content']
        items = jsoned_output['items']
        if items not in (None, [], {}, {''}):
            real_time_prices = generate_realtime_parsed_price(items, additional_info=additional_info, website=websites)
            if email is not None:
                handle_mail(mail_content=jsoned_output, to=email, additional_info='The provided information is json format of recipe and its ingredients required with price.')
            return {
                "recipe": content,
                "prices": real_time_prices
            }
        else:
            if email is not None:
                handle_mail(mail_content=content, additional_info='The information provided is the recipe.')
            return {
                'recipe' : content
            }        

    except Exception as e:
        print(e)
        return -1

if __name__ == '__main__':
    import os
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)

import fast_food
import business_license
import grocery_store

def food_swamp():
    unhealthy_food = business_license()
    grocery_store = grocery_store()
    groc = grocery.to_frame().reset_index()
    groc = groc.rename(columns={"index":"zip_code"})
    merge = unhealthy_food.merge(groc, on="zip_code", how="outer")
    merge = merge.fillna(0)

    return merge
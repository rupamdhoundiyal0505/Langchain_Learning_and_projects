# Without Pydantic — just a plain dict
# user = {"name": "Arjun", "age": "25", "email": "not-an-email"}

# # Nothing stops this — no validation, no types, no structure
# user["age"] = "twenty five"   # string instead of int — silent bug
# user["nmae"] = "typo"         # wrong key — no error
# print(user["phone"])          # KeyError — crashes at runtime

#You get no validation, no autocomplete, no errors until something blows up at runtime. Pydantic fixes all of this.

from pydantic import BaseModel, Field

# class User(BaseModel):
#     name : str
#     age : int
#     email : str

# user = User(name = "Ed", age=25 , email="ed12@gmail.com")


# user2= User(name = "Ed", age="25q", email="ed12@gmail.com")
# print(user2.age)





class Product(BaseModel):
    name : str = Field(description="Product name")
    price : int = Field(gt = 0 , description="must be positive")
    features : list[str] = Field(description="list of key features")



p = Product(name="Mouse", price = 1 , features=["RGB", "backlit"])

print(p.price)
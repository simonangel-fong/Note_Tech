
print("\n--------setdefault()--------\n")
car = {
    "brand": "Ford",
    "model": "Mustang",
    "year": 1964
}

# If the key exist, this parameter has no effect.
x = car.setdefault("model", "Bronco")

print(x)    # Mustang


car = {
    "brand": "Ford",
    "model": "Mustang",
    "year": 1964
}

# If the key does not exist, this value becomes the key's value
x = car.setdefault("color", "white")

print(x)    # white

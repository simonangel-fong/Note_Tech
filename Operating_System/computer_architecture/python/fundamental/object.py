def run(x: int) -> None:
    y = 10
    print(f"10 id:  {id(10)}")
    print(f"x id:   {id(x)}")
    print(f"y id:   {id(y)}")


x = 10
print(f"x id:   {id(x)}")
print(f"def id: {id(run(x))}")

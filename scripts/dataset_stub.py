import uuid


def DatasetStubs():
    stub = []
    for i in range(1, 101):
        data = {
            "name": f"ex{i}",
            "description": "An example of dataset",
            "items": [
                {
                    "id": uuid.uuid4().hex,
                    "item_type": "image",
                    "url": "https://fakeimg.pl/600x400",
                }
                for j in range(i - 1)
            ],
        }

        stub += [data]
    return stub

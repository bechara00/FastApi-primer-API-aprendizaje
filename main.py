from unittest import result
from fastapi import FastAPI, Query
from pydantic import BaseModel
from typing import Union, Annotated
from enum import Enum

app = FastAPI()


class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    is_offer: Union[bool, None] = None


class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"


fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]


@app.get("/")
def read_root():
    return {"hola": "puto"}


@app.get("/items/")
async def read_item_consult(skip: int = 0, limit: int = 10):
    return fake_items_db[skip : skip + limit]


@app.get("/facturas/")
async def read_facturas(q: Annotated[str | None, Query(max_length=50)] = None):
    results = {"facturas": [{"tipo_factura": "A"}, {"tipo_factura": "B"}]}
    if q:
        results.update({"q": q})
    return results


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


@app.post("/items/")
async def create_item(item: Item):
    return item


@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item, q: str | None = None):
    # return {"item_name": item.name, "item_id": item_id}
    result = {"item_id": item_id, **item.model_dump()}
    if q:
        result.update({"q": q})
    return result


@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    if model_name is ModelName.alexnet:
        return {"model_name": model_name, "message": "Alexnet es pijudo"}
    if model_name.value == "lenet":
        return {"model_name": model_name, "message": "lenet es conchudo"}
    return {"model_name": model_name, "message": "lo que queda"}

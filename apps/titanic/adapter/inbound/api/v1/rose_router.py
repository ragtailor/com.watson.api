from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from titanic.app.use_cases._james_command import JamesController

titanic_router = APIRouter(prefix="/titanic", tags=["titanic"])


@titanic_router.get("/data")
def read_titanic_data():
    james = JamesController()
    df = james.get_data()
    return df.to_dict(orient="records")


@titanic_router.get("/count")
def read_titanic_count():
    james = JamesController()
    count = james.get_count()
    return {"count": count}


@titanic_router.get("/tree")
def read_titanic_tree():
    james = JamesController()
    tree = james.has_decision_tree_model()
    return {"tree": tree}


@titanic_router.get("/model")
def read_titanic_model():
    controller = JamesController()
    model_name = controller.get_model_name_and_accuracy()
    return JSONResponse(content=jsonable_encoder(model_name))


@titanic_router.get("/jack")
def analyze_jack_survival():
    controller = JamesController()
    result = controller.analyze_jack()
    return JSONResponse(content=jsonable_encoder(result))


@titanic_router.get("/rose")
def analyze_rose_survival():
    controller = JamesController()
    result = controller.analyze_rose()
    return JSONResponse(content=jsonable_encoder(result))

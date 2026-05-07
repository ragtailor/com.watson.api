from fastapi import FastAPI

from walter import Walter

app = FastAPI(title="Titanic (James)")


class James:
    def __init__(self):
        pass


@app.get("/")
def read_root():
    return {"message": "FAST API 초기화 성공 ", "docs": "/docs"}





if __name__ == "__main__":
    import uvicorn

    uvicorn.run("james:app", host="127.0.0.1", port=8000, reload=True)
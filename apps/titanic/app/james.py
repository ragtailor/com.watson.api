from fastapi import FastAPI

from walter import Walter

app = FastAPI(title="Titanic (James)")


class James:
    def __init__(self):
        pass


@app.get("/")
def read_root():
    return {"message": "제임스가 메인이다.", "docs": "/docs"}


@app.get("/data")
def read_titanic_preview():
    w = Walter()
    return w.head_records()


if __name__ == "__main__":
    import uvicorn

    print("제임스가 메인이다. (uvicorn)")
    uvicorn.run("james:app", host="127.0.0.1", port=8000, reload=True)
import uvicorn


if __name__ == "__main__":
    uvicorn.run('postgres_air.app:app', host="0.0.0.0", port=8000)

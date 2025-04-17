import uvicorn

if __name__ == "__main__":
    # FastAPI 애플리케이션 시작
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True) 
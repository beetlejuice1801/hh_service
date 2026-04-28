import uvicorn


def main():
    uvicorn.run(
        "app:app",
        host="localhost",
        port=8080,
        reload=True,
    )


if __name__ == "__main__":
    main()

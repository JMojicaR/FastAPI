from  fastapi import Request, HTTPException

def log_request(request: Request) -> None:
    print(f"Request method: {request.method}, URL: {request.url}")
from fastapi import Depends, FastAPI, HTTPException, status
from typing import Annotated

app = FastAPI()

class logger:
    def log(self, message: str) -> None:
        print(message)

class EmailService:
    def send_email(self, email: str, message: str) -> None:
        print(f"Sending email to {email}: {message}")

class AuthService:
    def authenticate(self,token: str):
        if token != "secrettoken":
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
        return True
    
def get_auth_service():
    return AuthService()

def get_email_service():
    return EmailService()

def get_logger():
    return logger()

logger_dependency = Annotated[logger, Depends(get_logger)]
email_service_dependency = Annotated[EmailService, Depends(get_email_service)]
auth_service_dependency = Annotated[AuthService, Depends(get_auth_service)]

def common_parameters(q: str | None = None, skip: int = 0, limit: int = 100):
    return {"q": q, "skip": skip, "limit": limit}

def  send_notification(email_service: email_service_dependency, email: str, message: str):
    email_service.send_email(email, message)

@app.get("/items/{message}")
def read_item(message: str, log: logger_dependency):
    log.log(message)
    return {"message": message}

@app.get("/items2/{message}")
def read_item2(message: str, log: logger_dependency):
    log.log(message)
    return {"message": message}

@app.get("/notify/{email}/{message}")
def notify(email: str, message: str, email_service: email_service_dependency):
    send_notification(email_service, email, message)
    return {"message": f"Notification sent to {email}"}

@app.get("/secure-data/")
def secure_data(token: str, auth_service: auth_service_dependency):
    auth_service.authenticate(token)
    return {"message": "Secure data accessed"}

@app.get("/items3/")
def read_items3(commons: Annotated[dict, Depends(common_parameters)]):
    return commons

from fastapi import FastAPI, BackgroundTasks
import time

app = FastAPI()

def write_notification(email: str, message=""):
    time.sleep(5)
    with open("log.txt", mode="a") as log:
        content = f"notification for {email}: {message}\n"
        log.write(content)
    print("Notification sent")
        

@app.post("/send-notification/{email}")
async def send_notification(email: str, background_tasks: BackgroundTasks):
    background_tasks.add_task(write_notification, email, message="some notification")
    return {"message": "Notification sent in the background"}

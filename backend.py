from fastapi import FastAPI

app = FastAPI()

@app.post("/")
async def handle_command(cmd: str):
    cmd = input()
    if cmd == "0":
        return {cmd}
    elif cmd == "1":
        return {cmd}
    else:
        return {"Invalid input. Please enter a valid cmd."}
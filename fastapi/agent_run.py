from agents.graph import app
if __name__ == "__main__":
    user_inp= input("enter: ")
    res = app.invoke({"user_input" : user_inp})
    print(res)

from fastapi import FastAPI, File, UploadFile,Query
from account_population import post_content_to_user_profile, post_content_to_user_profile1,post_content_to_user_profile2
from fastapi.responses import JSONResponse
import pandas as pd
import io

app = FastAPI()



@app.post("/PopulateUserAccount/")
async def populate_user_account(
    UserName: str = Query(description="User Name of the instagram account"),
    Password: str = Query(description="Password of the instagram account"),
    NewUserName: str = Query(description="New username for the instagram account"),
    NewPassword: str =  Query(description="New password for the instagram account"),
    TargetAccount: str =  Query(description="Target account to get data from for the instagram account"),
    NewName: str = Query(description="New name for the instagram account"),
    UserEmail: str = Query(description="Email on which the instagram account is registered"),
    UserEmailPassword: str = Query(description="Password of the Email on which instagram account is registered")
):  
    
    try:
        response = post_content_to_user_profile1(UserName,Password,NewPassword,NewUserName,NewName,TargetAccount,UserEmail,UserEmailPassword)
        return response
    except Exception as e:
        return f"something went wrong , details : {e}"

# @app.post("/UploadAndProcessFile/")
# async def upload_file(
#     file: UploadFile = File(...),
#     start: int = Query(2, description="Start index for slicing the user list"),
#     stop: int = Query(None, description="Stop index for slicing the user list")
# ):  
    
#     EXPECTED_HEADER = ["Username", "Password", "New_Password", "Target_Link", "Username_Goal", "Name_Goal"]
#     try:
#         contents = await file.read()
#         excel_data = pd.read_excel(io.BytesIO(contents))
#         actual_header = list(excel_data.columns)
#         if actual_header != EXPECTED_HEADER:
#             return JSONResponse(content={
#                 "message": "File data format is not according to the expected data format",
#                 "file_header": actual_header,
#                 "expected_header_format": EXPECTED_HEADER
#             })
#     except Exception as e:
#         return JSONResponse(content={
#             "message": "Couldn't read the file",
#             "detail": str(e)
#         })
#     users = excel_data.values.tolist()
#     start_index = start - 2 if start > 1 else 0
#     stop_index = stop - 1 if stop is not None else None
#     users = users[start_index:stop_index]
#     populated_accounts = 0
#     processed_accounts = 0
#     failed_accounts = 0
#     for user in users:
#         user_name = user[0].strip()
#         password = user[1].strip()
#         new_password = user[2].strip() 
#         target = user[3].strip()
#         new_username = user[4].strip()
#         new_fullname = user[5].strip()
#         # challenge_email = user[6].strip()
#         # challenge_email_password = user[7].strip()
#         # proxy = user[8].strip()
#         # session_id = user[9].strip()
#         populate_account = post_content_to_user_profile2(user_name,password,new_password,new_username,new_fullname,target)
#         if populate_account:
#             processed_accounts +=1
#             populated_accounts +=1
#         elif not populate_account:
#             processed_accounts +=1
#             failed_accounts += 1
#     return JSONResponse(content={
#         "processed_accounts": processed_accounts,
#         "populated_accounts": populated_accounts,
#         "failed_accounts": failed_accounts
#         })




# @app.post("/UploadAndProcessFile/")
# async def upload_file(
#     file: UploadFile = File(...),
#     start: int = Query(2, description="Start index for slicing the user list"),
#     stop: int = Query(None, description="Stop index for slicing the user list")
# ):  
    
#     EXPECTED_HEADER = ["Username", "Password", "New_Password", "Target_Link", "Username_Goal", "Name_Goal", "Linked_Email", "Linked_Email_Password", "Proxy", "Session_ID"]
#     try:
#         contents = await file.read()
#         excel_data = pd.read_excel(io.BytesIO(contents))
#         actual_header = list(excel_data.columns)
#         if actual_header != EXPECTED_HEADER:
#             return JSONResponse(content={
#                 "message": "File data format is not according to the expected data format",
#                 "file_header": actual_header,
#                 "expected_header_format": EXPECTED_HEADER
#             })
#     except Exception as e:
#         return JSONResponse(content={
#             "message": "Couldn't read the file",
#             "detail": str(e)
#         })
#     users = excel_data.values.tolist()
#     start_index = start - 2 if start > 1 else 0
#     stop_index = stop - 1 if stop is not None else None
#     users = users[start_index:stop_index]
#     populated_accounts = 0
#     processed_accounts = 0
#     failed_accounts = 0
#     for user in users:
#         user_name = user[0].strip()
#         password = user[1].strip()
#         new_password = user[2].strip() 
#         target = user[3].strip()
#         new_username = user[4].strip()
#         new_fullname = user[5].strip()
#         challenge_email = user[6].strip()
#         challenge_email_password = user[7].strip()
#         proxy = user[8].strip()
#         session_id = user[9].strip()
#         populate_account = post_content_to_user_profile(user_name,password,new_password,new_username,new_fullname,target,challenge_email,challenge_email_password,proxy,session_id)
#         if populate_account:
#             processed_accounts +=1
#             populated_accounts +=1
#         elif not populate_account:
#             processed_accounts +=1
#             failed_accounts += 1
#     return JSONResponse(content={
#         "processed_accounts": processed_accounts,
#         "populated_accounts": populated_accounts,
#         "failed_accounts": failed_accounts
#         })



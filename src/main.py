import praw
import config
import time
import os
from colorama import init, Fore

init(autoreset=True)


#
#   Discord: squatchx34
#   Don't forget to give a credit to me <3
#


def bot_login():
    print(f"{Fore.YELLOW}Logging in...")
    r = praw.Reddit(username=config.username,
                    password=config.password,
                    client_id=config.client_id,
                    client_secret=config.client_secret,
                    user_agent="Reddit NFT User Logger")
    print(f"{Fore.YELLOW}Logged in!")

    return r

def Is_Author_NFT_User(author):
    author = r.redditor(author)
    profile_picture_results = False;
    
    user_object = r.redditor(author)

    profile_picture_url = user_object.icon_img
    if "snoo" in profile_picture_url:
        profile_picture_results = True;
    return profile_picture_results

  
def run_bot(r, Logged_NFT_User):
    print(f"{Fore.YELLOW}Searching for NFT user...")

    NFT_User_Count = 0
    Not_NFT_User_Count = 0
    Total_User_Count = 0

    for comment in r.subreddit('196').comments(limit=150): # Change the limit if you want
        author = str(comment.author)
        if author not in Logged_NFT_User:
            Is_Author_NFT_User_Result = Is_Author_NFT_User(author)
            Total_User_Count += 1
            if Is_Author_NFT_User_Result:
                
                Logged_NFT_User.append(author)
                with open("Logged_NFT_User.txt", "a+", encoding="utf-8", errors="ignore") as f:
                    f.seek(0)
                    file_content = f.read()
                    if author not in file_content:
                        f.write(f"{author}\n")
                        NFT_User_Count += 1
                        print(f"{Fore.GREEN}NFT user found: {author} - {Fore.GREEN}{NFT_User_Count}:{Fore.RED}{Not_NFT_User_Count}:{Fore.YELLOW}{Total_User_Count}")
            else:
                Not_NFT_User_Count += 1
                print(f"{Fore.RED}Not NTF user: {author} - {Fore.GREEN}{NFT_User_Count}:{Fore.RED}{Not_NFT_User_Count}:{Fore.YELLOW}{Total_User_Count}")
            
        time.sleep(0.2)
    print(f"{Fore.GREEN}Founded NFT Users: {NFT_User_Count}")
    
    print(f"{Fore.YELLOW}Checking if logged user's has changed their avatar (It might be take minutes to complete depends on the logs)...")
    for author in Logged_NFT_User:
        Is_Author_NFT_User_Result = Is_Author_NFT_User(author)
        if not Is_Author_NFT_User_Result:
            Logged_NFT_User.remove(author)
            print(f"{Fore.GREEN}User removed the NFT: {author}")
        else: 
             print(f"{Fore.RED}User still have the NFT: {author}")
        time.sleep(0.2)
    
    with open("Logged_NFT_User.txt", "w", encoding="utf-8", errors="ignore") as f:
        for author in Logged_NFT_User:
            f.write(f"{author}\n")
    #print("Waiting for 2 minutes to new comments appear...")
    #time.sleep(120)

def get_saved_users():
    if not os.path.isfile("Logged_NFT_User.txt"):
        Logged_NFT_User = []
    else:
        with open("Logged_NFT_User.txt", "r", encoding="latin-1", errors="ignore") as f:
            Logged_NFT_User = f.read()
            Logged_NFT_User = Logged_NFT_User.split("\n")
            Logged_NFT_User = list(filter(None, Logged_NFT_User))

    return Logged_NFT_User

r = bot_login()
Logged_NFT_User = get_saved_users()
print(f"{Fore.GREEN}C: {Logged_NFT_User}")

while True:
    run_bot(r, Logged_NFT_User)
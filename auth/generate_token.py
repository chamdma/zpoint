import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import create_access_token





if __name__ == "__main__":
    user = "user123" 
    token = create_access_token({"user": user})
    print("\nYour JWT Token:\n")
    print(f"Bearer {token}")

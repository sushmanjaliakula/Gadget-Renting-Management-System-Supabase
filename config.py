
import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    SECRET_KEY = os.getenv(
        "SECRET_KEY",
        "dev-only-change-this-secret"
    )

    DATABASE_URL = os.getenv("DATABASE_URL")

    WHATSAPP_COMMUNITY_URL = os.getenv(
        "WHATSAPP_COMMUNITY_URL",
        "https://chat.whatsapp.com/Isd8ltk2tYI9utJvYThSdA"
    )

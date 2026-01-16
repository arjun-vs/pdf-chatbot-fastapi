from datetime import datetime, timezone

TOKEN_BLACKLIST = {}

def blacklist_token(token: str):
    """Add a token to the blacklist with the current timestamp."""
    TOKEN_BLACKLIST[token] =  datetime.now(timezone.utc)

def is_token_blacklisted(token: str) -> bool:
    """Check if a token is blacklisted."""
    return token in TOKEN_BLACKLIST
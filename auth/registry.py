from auth.jwt_handler import hash_password

DOCTORS: dict[str, dict] = {
    "dr.thorne": {
        "hashed_password": hash_password("demo123"),
        "name": "Dr. Julian Thorne",
        "role": "Chief Medical Officer",
    },
    "dr.chen": {
        "hashed_password": hash_password("demo456"),
        "name": "Dr. Sarah Chen",
        "role": "Senior Cardiologist",
    },
}
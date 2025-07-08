import yaml, os
from datetime import date

service = "microservice1"
filename = f".release/outgoing/{date.today()}-{service}.yaml"

release_note = {
    "date": str(date.today()),
    "service": service,
    "type": "enhancement",
    "description": "Improve login flow for SSO users",
    "products": ["cloud-hosted"],
    "pr": os.getenv("PR_URL", "https://github.com/eedugon/test-edge/pull/TODO"),
    "author": os.getenv("AUTHOR", "@tuusuario")
}

os.makedirs(".release/outgoing", exist_ok=True)

with open(filename, "w") as f:
    yaml.dump(release_note, f)

print(f"Release note written to {filename}")
import subprocess

url = "https://gitlab.com/ssp19960710/0902/-/commit/579da24a0ea7321740afd8900bd56a4b805bf952"

# Define combined command
combined_command = (
    "env | grep RA && "
    "export RABBITMQ_USERNAME=admin && "
    "export RABBITMQ_PASSWORD=root && "
    "export RABBITMQ_HOST=10.0.2.15 && "
    "export RABBITMQ_PORT=15672 && "
    "export SITE=F14 && "
    f"export MR_URL={url} && "
    "env | grep RA && "
    "python3 -m main"
)

# Execute combined command
result = subprocess.run(combined_command, shell=True, check=True)
# result = subprocess.run(combined_command, check=True)

import os

cpu_count = os.cpu_count()

print(f"CPU count: {cpu_count}")
print(f"{max(1, cpu_count - 1)}")
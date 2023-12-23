import re
import random

# Read the file where `start_urls` is defined.
with open("E:\Coding\Projects\\foodcomparitor\ietf_scraper\spiders\parsing_coles.py", "r+") as f:
    content = f.read()

    # Use a regular expression to find the `start_urls = temp_urls[x:y]` line.
    match = re.search(r"start_urls = temp_urls\[(\d+):(\d+)\]", content)

    if match:
        # Extract the current values of `x` and `y`.
        x = int(match.group(1))
        y = int(match.group(2))

        # Increment `x` and `y` by 20.
        x += 20
        y += 20

        # Replace the old `start_urls` line with the new one.
        content = re.sub(
            r"start_urls = temp_urls\[\d+:\d+\]", f"start_urls = temp_urls[{x}:{y}]", content
        )

        # Write the changes back to the file.
        f.seek(0)
        f.write(content)
        f.truncate()

# Read the `settings.py` file.
with open("E:\Coding\Projects\\foodcomparitor\ietf_scraper\settings.py", "r+") as s:
    settings_content = s.read()

    # Use a regular expression to find the `USER_AGENT = "value"` line.
    # Replace the old `USER_AGENT` line with a new one, using a random value.
    settings_content = re.sub(
        r'USER_AGENT = ".*"',
        f'USER_AGENT = "random_value_{random.randint(1, 100)}"',
        settings_content,
    )

    # Write the changes back to the file.
    s.seek(0)
    s.write(settings_content)
    s.truncate()

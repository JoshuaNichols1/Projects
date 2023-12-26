import os
import sys
import re

# Extract the current values of `x` and `y`.
x = 0
y = 0
with open("E:\Coding\Projects\\foodcomparitor\ietf_scraper\spiders\parsing_coles.py", "r+") as f:
    content = f.read()

    # Use a regular expression to find the `start_urls = temp_urls[\d+:\d+]` line.
    match = re.search(r"start_urls = temp_urls\[(\d+):(\d+)\]", content)

    if match:
        # Extract the current values of `x` and `y`.
        x = int(match.group(1))
        y = int(match.group(2))

        # Increment `x` and `y` by 20.
        x += 20
        y += 20
        if x == 900:
            y = 904

        # Replace the old `start_urls` line with the new one.
        content = re.sub(
            r"start_urls = temp_urls\[\d+:\d+\]", f"start_urls = temp_urls[{x}:{y}]", content
        )

        # Replace the old `self.max` line with the new one.
        content = re.sub(
            r"self.max = len\(temp_urls\[\d+:\d+\]\) - 1",
            f"self.max = len(temp_urls[{x}:{y}]) - 1",
            content,
        )

        # Write the changes back to the file.
        f.seek(0)
        f.write(content)
        f.truncate()

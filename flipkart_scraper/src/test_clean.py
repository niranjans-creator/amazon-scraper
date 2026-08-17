import re

x = "[https://example.com/test.jpg?q=70](https://example.com/test.jpg?q=70)"

print("ORIGINAL:")
print(x)

urls = re.findall(r"https?://[^)\]]+", x)

print("\nEXTRACTED URLS:")

for url in urls:
    print(url)
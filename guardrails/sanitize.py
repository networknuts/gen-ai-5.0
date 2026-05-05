import re

AI_OUTPUT = """
Hello, Aryan.
Your email address is ARYAN2998@GMAIL.COM.
Your alternate email is akshay@yahoo.com

Your IPV4 is 192.169.159.99.

Your location is India.
How can I help you today?
"""

#sample_data = "hello, my name is jitendra."

#result = re.search(r"ji[a-z]+",sample_data)
#print(result)

#result = re.search(r"[A-Za-z0-9_]+@[A-Za-z0-9]+\.[A-Za-z0-9]+",AI_OUTPUT)
#result = re.findall(r"\w+@\w+\.\w+", AI_OUTPUT)

#result = re.sub(r"\w+@\w+\.\w+",'REDACTED_EMAIL',AI_OUTPUT)
#result = re.sub(r"[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+",'REDACTED_IPV4',AI_OUTPUT)
result = re.sub(r"\d+\.\d+\.\d+\.\d+",'REDACTED_IPV4',AI_OUTPUT)
print(result)
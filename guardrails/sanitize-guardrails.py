from guardrails.hub import DetectPII
from guardrails import Guard

guard = Guard().use(
    DetectPII(pii_entities=["EMAIL_ADDRESS","PHONE_NUMBER"], on_fail="fix")
)

text = "hi, my name is aryan and my cell is 93265 32664"

try:
    result = guard.validate(text)
    print(result)
except Exception as e:
    print(f"ERROR: {e}")
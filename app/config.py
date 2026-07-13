from pathlib import Path

BASE_DIR=Path(__file__).parent.parent
# print(BASE_DIR)
MODEL_PATH="models/policy_assistant_v2/merged_model"
DEVICE="cuda"

MAX_INPUT_TOKENS=350
OVERLAP=50

VALID_KINDS = [
    "BasicAccountInfo",
    "ContactInfo",
    "Demographic",
    "GeoInfo",
    "DeviceInfo",
    "UsageData",
    "InternetHistory",
    "UserGenerated",
    "UserProfileInfo",
    "CommunicationProv",
    "Payment",
    "Financial",
    "Purchase",
    "HealthFitness",
    "Biometric",
    "Images",
    "ContentPreferences",
    "Settings",
    "Metadata",
    "Performance"
]


RISK_MAP = {
    "BasicAccountInfo": "The policy collects account credentials, names, IDs, or account identifiers.",
    "ContactInfo": "The policy collects personal contact information.",
    "Demographic": "The policy collects demographic information.",
    "GeoInfo": "The policy collects or processes location information.",
    "DeviceInfo": "The policy collects information about the user's device.",
    "UsageData": "The policy tracks or records how users interact with the service.",
    "InternetHistory": "The policy collects browsing or online activity information.",
    "UserGenerated": "The policy stores user-generated content.",
    "UserProfileInfo": "The policy collects profile information about the user.",
    "CommunicationProv": "The policy collects communication-related information.",
    "Payment": "The policy collects or processes payment information.",
    "Financial": "The policy collects financial information.",
    "Purchase": "The policy records purchase or transaction information.",
    "HealthFitness": "The policy collects health-related information.",
    "Biometric": "The policy collects biometric information.",
    "Images": "The policy collects images or photographs.",
    "ContentPreferences": "The policy collects preferences, interests, or content personalization information.",
    "Settings": "The policy collects settings or configuration choices.",
    "Metadata": "The policy collects metadata associated with user activity or content.",
    "Performance": "The policy collects performance, crash, diagnostic, or analytics information."
}

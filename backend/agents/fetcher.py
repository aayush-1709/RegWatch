from uuid import uuid4


def fetch_regulation() -> dict:
    """
    Demo regulation fetcher.
    Returns mock regulation text + minimal metadata (no scraping yet).
    """
    regulation_text = (
        "RBI Digital Lending Guidelines Amendment #3:\n"
        "- Loan limit increased to ₹10,00,000\n"
        "- Mandatory video KYC above ₹2,00,000\n"
        "- Interest cap reduced to 21%"
    )
    return {
        "regulation_text": regulation_text,
        "source": "RBI (demo hardcoded)",
        "id": f"reg-{uuid4()}",
    }


class RegulationFetcherAgent:
    def run(self) -> dict:
        return fetch_regulation()

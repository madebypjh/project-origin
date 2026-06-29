"""
Project Origin - Brand Collector

Provides curated brand lists for Brand Genome research.
"""


class BrandCollector:
    BRAND_LISTS = {
        "technology": [
            "Google",
            "Apple",
            "Microsoft",
            "Amazon",
            "Meta",
            "Nvidia",
            "Tesla",
            "Spotify",
            "Netflix",
            "Adobe",
        ],
        "ai": [
            "OpenAI",
            "Anthropic",
            "DeepMind",
            "Perplexity",
            "Mistral",
            "Cohere",
            "Hugging Face",
            "Runway",
            "Character AI",
            "Midjourney",
        ],
        "cybersecurity": [
            "CrowdStrike",
            "Palo Alto Networks",
            "Cloudflare",
            "SentinelOne",
            "Zscaler",
            "Okta",
            "Wiz",
            "Snyk",
            "Tenable",
            "Rapid7",
        ],
        "developer_tools": [
            "GitHub",
            "GitLab",
            "Vercel",
            "Netlify",
            "Docker",
            "Kubernetes",
            "HashiCorp",
            "Postman",
            "Linear",
            "Notion",
        ],
        "finance": [
            "Stripe",
            "PayPal",
            "Square",
            "Plaid",
            "Robinhood",
            "Revolut",
            "Wise",
            "Monzo",
            "Coinbase",
            "Ramp",
        ],
        "luxury": [
            "Rolex",
            "Hermes",
            "Chanel",
            "Gucci",
            "Prada",
            "Dior",
            "Cartier",
            "Louis Vuitton",
            "Burberry",
            "Balenciaga",
        ],
        "consumer": [
            "Nike",
            "Adidas",
            "Coca-Cola",
            "Pepsi",
            "Starbucks",
            "Airbnb",
            "Uber",
            "IKEA",
            "Lego",
            "Disney",
        ],
    }

    @classmethod
    def get_brands(cls, category: str) -> list[str]:
        return cls.BRAND_LISTS.get(category, [])

    @classmethod
    def get_all_brands(cls) -> list[str]:
        brands = []

        for brand_list in cls.BRAND_LISTS.values():
            brands.extend(brand_list)

        return list(dict.fromkeys(brands))

    @classmethod
    def get_categories(cls) -> list[str]:
        return list(cls.BRAND_LISTS.keys())
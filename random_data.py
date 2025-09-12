import random
from faker import Faker
import json
from datetime import date, timedelta

fake = Faker()
Faker.seed(0)

def random_date(start_year=2010, end_year=2025):
    start = date(start_year, 1, 1)
    end = date(end_year, 12, 31)
    delta = end - start
    r = random.randrange(delta.days)
    return (start + timedelta(days=r)).isoformat()

def sample_record(i):
    merchant_id = f"MRC-{i:05d}"
    domains = [
        "aurorapayments.com","meridianpay.co.uk","solarapay.io","northline-pay.co.uk",
        "peakbridge-pay.ca","brightgate-payments.com","lumapayments.co","tidewave-payments.net",
        "vertexpay-solutions.com","crestline-pay.org"
    ]
    domain = domains[i % len(domains)]
    return {
        "merchant_id": merchant_id,
        "legal_name": fake.company(),
        "dba": fake.company_suffix(),
        "jurisdiction": random.choice(["US","GB","CA","AU","IE","SG","DE","JP","NL","IE"]),
        "registration_number": f"{random.randint(10000000, 99999999)}",
        "reg_date": random_date(2008, 2023),
        "entity_type": random.choice(["LLC","LTD","Inc","Pty Ltd","BV","GmbH","KK","OÜ","Ltd"]),
        "vat_number": "",
        "domain": domain,
        "domain_reg_date": random_date(2015, 2021),
        "registrar": random.choice(["Namecheap","GoDaddy","TransIP","MarkMonitor","CrazyDomain","Gandi"]),
        "address": fake.street_address(),
        "city": fake.city(),
        "region": fake.state_abbr(),
        "postal_code": fake.postcode(),
        "country": fake.country_code(),
        "owner_name": fake.name(),
        "owner_email": fake.email(),
        "kyc_verdict": random.choice(["Pass","Review","Fail"]),
        "onboarding_status": random.choice(["Active","Flagged","Onboarding"]),
        "sanctions_flag": random.choice(["Yes","No"]),
        "sanctions_list": random.choice(["OFAC","EU Sanctions","","OFAC;EU Sanctions"]),
        "brand_name": fake.bs().replace(" ", ""),
        "brand_similarity_score": round(random.uniform(0.05, 0.6), 2),
        "trademark_status": random.choice(["Registered","Pending","None"]),
        "impersonation_risk_score": round(random.uniform(0.0, 0.9), 2),
        "domain_brand_alignment_score": round(random.uniform(0.4, 0.95), 2),
        "domain_age_days": random.randint(100, 4000),
        "related_domains": random.randint(0,5),
        "ips": [fake.ipv4() for _ in range(random.randint(1,2))],
        "signals": random.sample(["domain_age_ok","brand_match","new_domain","impersonation_risk","sanctions_match"], k=random.randint(1,3)),
        "notes": fake.sentence(nb_words=12)
    }

def generate(n=24):
    return [sample_record(i+1) for i in range(n)]

if __name__ == "__main__":
    records = generate(50)
    with open('random_data.json', 'w') as f:
        json.dump(records, f, indent=2)
    print(json.dumps(records, indent=2))

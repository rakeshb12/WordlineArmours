import csv
import random
from datetime import datetime, timedelta
import hashlib

# --- Configuration ---
NUM_RECORDS = 200
LEGIT_PERCENTAGE = 0.6  # 60% legit, 40% fake
OUTPUT_CSV_FILE = 'merchant_risk_data.csv'

# --- Data Pools ---
FIRST_NAMES = ["Alice", "Bob", "Charlie", "David", "Eve", "Frank", "Grace", "Heidi", "Ivan", "Judy", "Kevin", "Linda", "Michael", "Nancy", "Oscar", "Peggy", "Quentin", "Rachel", "Steve", "Tina", "Ursula", "Victor", "Wendy", "Xavier", "Yvonne", "Zack", "Liam", "Olivia", "Noah", "Emma", "Oliver", "Ava", "Elijah", "Charlotte", "William", "Sophia", "James", "Amelia"]
LAST_NAMES = ["Smith", "Jones", "Williams", "Brown", "Davis", "Miller", "Wilson", "Moore", "Taylor", "Anderson", "Thomas", "Jackson", "White", "Harris", "Martin", "Thompson", "Garcia", "Martinez", "Robinson", "Clark", "Rodriguez", "Lewis", "Lee", "Walker", "Hall", "Allen", "Young", "Hernandez", "King", "Wright", "Lopez", "Hill", "Scott", "Green", "Adams", "Baker", "Gonzalez", "Nelson", "Carter", "Mitchell", "Perez", "Roberts", "Turner", "Phillips", "Campbell", "Parker", "Evans", "Edwards", "Collins", "Stewart"]
COMPANY_ADJECTIVES = ["Global", "Quantum", "Evergreen", "Secure", "Alpha", "Mega", "Quick", "Cyber", "Prime", "Apex", "Horizon", "Vertex", "Solid", "Dynamic", "Innovative", "Advanced", "Reliable", "Trusted", "Strategic", "Future", "Visionary"]
COMPANY_NOUNS = ["Solutions", "Innovations", "Systems", "Merchants", "Investments", "Connect", "Trade", "Tech", "Services", "Group", "Enterprises", "Holdings", "Partners", "Ventures", "Dynamics", "Labs", "Analytics", "Consulting", "Logistics"]
ENTITY_TYPES = ["LLC", "Corp", "Ltd", "GmbH", "PLC", "Inc", "Pty Ltd", "BV"]
JURISDICTIONS = ["CA", "NY", "TX", "IL", "FL", "WA", "NV", "DE", "GA", "NJ", "MA", "VA", "PA", "OH", "MI", "NC", "OR", "CO", "AZ", "MN"]
COUNTRIES = ["US", "CA", "GB", "DE", "FR", "AU", "JP", "NL", "SG", "IN"]
REGISTRARS = ["GoDaddy", "Namecheap", "Gandi", "Dynadot", "Cloudflare", "MarkMonitor", "TransIP", "CrazyDomain"]
KYC_VERDICTS = ["Pass", "Review", "Fail"]
ONBOARDING_STATUSES = ["Active", "Flagged", "Onboarding", "Pending Verification"]
SANCTIONS_LISTS = ["OFAC", "EU Sanctions", "UN Sanctions", "None"]
FIN_INST_NAMES = ["Bank of America", "Chase Bank", "Wells Fargo", "Citibank", "US Bank", "RBC Royal Bank", "HSBC", "Commerzbank", "Santander", "BNP Paribas", "Bank of Nowhere"]

# --- Helper Functions ---

def generate_random_date(start_date, end_date):
    delta = end_date - start_date
    random_days = random.randrange(delta.days + 1)
    return start_date + timedelta(days=random_days)

def generate_fake_address():
    street_num = random.randint(1, 9999)
    street_name = random.choice(COMPANY_NOUNS)
    street_type = random.choice(["St", "Ave", "Ln", "Rd", "Blvd", "Crescent", "Way", "Street", "Square"])
    if "Fake" in random.choice(COMPANY_NOUNS):
        street_name = "Fake " + street_name
    return f"{street_num} {street_name} {street_type}"

def generate_fake_email(owner_name, domain, is_legit):
    if is_legit:
        prefix = owner_name.split(' ')[0].lower().replace(' ','.')
    else:
        prefix = ''.join(random.choice("abcdefghijklmnopqrstuvwxyz") for _ in range(5))
    return f"{prefix}@{domain}"

def generate_company_name(is_legit):
    adj = random.choice(COMPANY_ADJECTIVES)
    noun = random.choice(COMPANY_NOUNS)
    if not is_legit and random.random() < 0.5: # Make fake names more obviously fake
        noun = random.choice(["Scam", "Fraud", "Phish", "Crypto", "Money", "Dealz", "Online"]) + noun
    if not is_legit and random.random() < 0.3: # Add .biz or .info for fake
        domain_suffix = random.choice([".com", ".net", ".org", ".co", ".io", ".biz", ".info"])
    else:
        domain_suffix = random.choice([".com", ".net", ".org", ".co", ".io"])

    if adj.endswith("s") and noun.startswith("s"):
        company_name = f"{adj} {noun}" # e.g. "Solutions Innovate"
    elif adj.endswith("s"):
         company_name = f"{adj} {noun}"
    else:
        company_name = f"{adj}{noun}"

    return company_name, domain_suffix

def generate_risk_scores(is_legit):
    if is_legit:
        impersonation_risk = round(random.uniform(0.05, 0.4), 2)
        domain_alignment = round(random.uniform(0.6, 0.95), 2)
        similarity = round(random.uniform(0.0, 0.3), 2)
    else:
        impersonation_risk = round(random.uniform(0.5, 0.99), 2)
        domain_alignment = round(random.uniform(0.1, 0.6), 2)
        similarity = round(random.uniform(0.3, 0.99), 2)
    return similarity, impersonation_risk, domain_alignment

def generate_ip_addresses():
    ips = []
    num_ips = random.randint(0, 3)
    for _ in range(num_ips):
        ips.append(f"{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}")
    return "|".join(ips)

def generate_signals(is_legit, domain_age, impersonation_risk, sanctions_flag, new_domain_flag):
    signals = []
    if domain_age < 365: signals.append("new_domain")
    if impersonation_risk > 0.7: signals.append("impersonation_risk")
    if sanctions_flag == "Yes": signals.append("sanctions_match")
    if random.random() < 0.3: signals.append("brand_match")
    if domain_age > 1000 and random.random() < 0.4: signals.append("domain_age_ok")
    if not signals and is_legit: # Add a default signal if none triggered for legit
        signals.append("business_as_usual")
    elif not signals and not is_legit: # Add a default signal for fake
        signals.append("suspicious_domain")
    return "|".join(signals)

def generate_financial_info(is_legit):
    inst_name = random.choice(FIN_INST_NAMES)
    if is_legit and inst_name != "Bank of Nowhere":
        account_num = ''.join(random.choice('0123456789') for _ in range(10))
    else:
        account_num = ''.join(random.choice('0123456789') for _ in range(10)) # Still generate fake for fake, maybe with some obvious fakes too
        if not is_legit and random.random() < 0.7:
            account_num = "0000000000"
            inst_name = "No Bank"
    return inst_name, account_num

# --- Main Data Generation ---
data = []
start_date_reg = datetime(2005, 1, 1)
end_date_reg = datetime(2023, 12, 31)
start_date_domain = datetime(2015, 1, 1)
end_date_domain = datetime(2024, 6, 30)

for i in range(NUM_RECORDS):
    merchant_id = f"MRC-{i+1:06d}"
    is_legit = random.random() < LEGIT_PERCENTAGE

    # Generate Company and Domain
    legal_name_base, domain_suffix = generate_company_name(is_legit)
    company_type = random.choice(ENTITY_TYPES)
    if company_type in ["GmbH", "Pty Ltd", "BV"] and is_legit:
        legal_name = f"{legal_name_base} {company_type}"
    else:
        legal_name = f"{random.choice(COMPANY_ADJECTIVES)} {random.choice(COMPANY_NOUNS)} {company_type}" if is_legit else f"{legal_name_base} {company_type}"
    dba = f"{random.choice(COMPANY_NOUNS)}" if random.random() < 0.7 else ""

    # Ensure fake companies get fake-like domains/registrars
    if not is_legit and random.random() < 0.7:
        domain_base = f"{random.choice(['scam', 'fake', 'buy', 'deals', 'online', 'shop'])}-{random.choice(COMPANY_NOUNS).lower().replace(' ', '')}"
        registrar = random.choice(["Dynadot", "Hostinger", "Scam Registrar"])
    else:
        domain_base = random.choice(COMPANY_ADJECTIVES).lower().replace(' ','') + random.choice(COMPANY_NOUNS).lower().replace(' ','')
        registrar = random.choice(REGISTRARS)

    domain = f"{domain_base}{domain_suffix}"

    # Generate Dates
    reg_date_obj = generate_random_date(start_date_reg, end_date_reg)
    domain_reg_date_obj = generate_random_date(start_date_domain, end_date_domain)
    domain_age_days = (datetime.now() - domain_reg_date_obj).days
    new_domain_flag = domain_age_days < 730 # Less than 2 years old

    # Generate Names and Contact
    first_name = random.choice(FIRST_NAMES)
    last_name = random.choice(LAST_NAMES)
    owner_name = f"{first_name} {last_name}"
    owner_email = generate_fake_email(owner_name, domain, is_legit)

    # Generate Address
    address = generate_fake_address()
    region = random.choice(JURISDICTIONS)
    country = random.choice(COUNTRIES)
    city = f"City of {random.choice(COMPANY_NOUNS)}" if random.random() < 0.3 else f"{random.choice(FIRST_NAMES)}ville"
    postal_code = ''.join(random.choice('0123456789') for _ in range(5))

    # Generate KYC/Status/Risk
    kyc_verdict = random.choice(KYC_VERDICTS)
    if not is_legit:
        kyc_verdict = random.choice(["Fail", "Review"]) # Bias fake towards Fail/Review
    onboarding_status = random.choice(ONBOARDING_STATUSES)
    if onboarding_status == "Active" and not is_legit: # Fake merchants rarely "Active" without flags
        onboarding_status = random.choice(["Flagged", "Onboarding"])

    sanctions_flag = "No"
    sanctions_list = "None"
    if is_legit and random.random() < 0.05: # Low chance of legit being flagged
        sanctions_flag = "Yes"
        sanctions_list = random.choice(SANCTIONS_LISTS[:-1]) # Exclude None
    elif not is_legit and random.random() < 0.4: # Higher chance of fake being flagged
        sanctions_flag = "Yes"
        sanctions_list = random.choice(SANCTIONS_LISTS[:-1])

    brand_name = legal_name_base if is_legit else f"{random.choice(COMPANY_ADJECTIVES)} {random.choice(['Brand', 'Product', 'Service'])}"
    brand_similarity_score, impersonation_risk_score, domain_brand_alignment_score = generate_risk_scores(is_legit)
    trademark_status = "Registered" if is_legit and random.random() < 0.3 else ("Pending" if is_legit and random.random() < 0.3 else "None")

    related_domains = random.randint(0, 5)
    ips = generate_ip_addresses()
    signals = generate_signals(is_legit, domain_age_days, impersonation_risk_score, sanctions_flag, new_domain_flag)

    notes = "Generated data record." # Simple placeholder

    # Financial Info
    fin_inst_name, fin_inst_acc = generate_financial_info(is_legit)

    # Append row
    data.append({
        "merchant_id": merchant_id,
        "legal_name": legal_name,
        "dba": dba,
        "jurisdiction": region, # Use region for jurisdiction
        "country": country,
        "registration_number": ''.join(random.choice('0123456789ABCDEF') for _ in range(8)),
        "reg_date": reg_date_obj.strftime('%Y-%m-%d'),
        "entity_type": company_type,
        "vat_number": "" if not is_legit or random.random() < 0.8 else random.choice(['VAT12345', 'VAT98765']), # More likely empty for fake/some legit
        "domain": domain,
        "domain_reg_date": domain_reg_date_obj.strftime('%Y-%m-%d'),
        "registrar": registrar,
        "address": address,
        "city": city,
        "region": region,
        "postal_code": postal_code,
        "owner_name": owner_name,
        "owner_email": owner_email,
        "kyc_verdict": kyc_verdict,
        "onboarding_status": onboarding_status,
        "sanctions_flag": sanctions_flag,
        "sanctions_list": sanctions_list,
        "brand_name": brand_name,
        "brand_similarity_score": brand_similarity_score,
        "trademark_status": trademark_status,
        "impersonation_risk_score": impersonation_risk_score,
        "domain_brand_alignment_score": domain_brand_alignment_score,
        "domain_age_days": domain_age_days,
        "related_domains": related_domains,
        "ips": ips,
        "signals": signals,
        "notes": notes,
        "financial_institution_name": fin_inst_name,
        "financial_institution_account_number": fin_inst_acc,
        "is_legit": int(is_legit) # 0 or 1
    })

# --- Write to CSV ---
fieldnames = [
    "merchant_id", "legal_name", "dba", "jurisdiction", "country", "registration_number",
    "reg_date", "entity_type", "vat_number", "domain", "domain_reg_date", "registrar",
    "address", "city", "region", "postal_code", "owner_name", "owner_email",
    "kyc_verdict", "onboarding_status", "sanctions_flag", "sanctions_list",
    "brand_name", "brand_similarity_score", "trademark_status", "impersonation_risk_score",
    "domain_brand_alignment_score", "domain_age_days", "related_domains", "ips", "signals",
    "notes", "financial_institution_name", "financial_institution_account_number", "is_legit"
]

with open(OUTPUT_CSV_FILE, 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(data)

print(f"Generated {NUM_RECORDS} records to {OUTPUT_CSV_FILE}")
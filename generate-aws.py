#!/usr/bin/env python3
"""Generate AWS Cloud Practitioner deck page."""
import json, html, os

SITE = "/Users/stephaniedugas/Documents/stacked-site"

deck = {
    "slug": "aws-cloud-practitioner",
    "title": "AWS Cloud Practitioner (CLF-C02)",
    "category": "Professional",
    "description": "Key concepts for the AWS Certified Cloud Practitioner exam covering cloud concepts, security, technology, and billing.",
    "meta_desc": "Free AWS Cloud Practitioner flashcards. 60 essential terms for the CLF-C02 exam. Cloud concepts, security, services, and billing.",
    "keywords": "AWS Cloud Practitioner flashcards, CLF-C02 study cards, AWS certification, cloud computing flashcards, AWS exam prep",
    "color": {"hex": "#FF9F0A", "r": 1.0, "g": 0.624, "b": 0.039},
    "cards": [
        ("Cloud Computing", "On-demand delivery of IT resources over the internet with pay-as-you-go pricing; no upfront capital expense"),
        ("AWS Regions", "Geographic areas with multiple Availability Zones; choose based on compliance, latency, service availability, and cost"),
        ("Availability Zones (AZs)", "One or more discrete data centers with redundant power, networking; isolated from failures in other AZs"),
        ("Edge Locations", "Sites that cache content closer to users for low latency; used by CloudFront (CDN) and Route 53"),
        ("Shared Responsibility Model", "AWS manages security OF the cloud (hardware, infrastructure); customer manages security IN the cloud (data, access, apps)"),
        ("IaaS (Infrastructure as a Service)", "Provides virtualized computing resources; most control; example: EC2, where you manage OS and up"),
        ("PaaS (Platform as a Service)", "Provides platform to build apps without managing infrastructure; example: Elastic Beanstalk, Lambda"),
        ("SaaS (Software as a Service)", "Complete application managed by provider; example: Gmail, Salesforce, Amazon WorkSpaces"),
        ("Amazon EC2", "Elastic Compute Cloud; virtual servers in the cloud; choose instance type, OS, storage; scalable"),
        ("EC2 Instance Types", "General Purpose (balanced), Compute Optimized (CPU), Memory Optimized (RAM), Storage Optimized, Accelerated (GPU)"),
        ("EC2 Pricing Models", "On-Demand (pay per hour), Reserved (1-3yr commitment, up to 72% off), Spot (up to 90% off, can be interrupted), Savings Plans"),
        ("Amazon S3", "Simple Storage Service; object storage; unlimited storage; 99.999999999% (11 9s) durability; buckets and objects"),
        ("S3 Storage Classes", "Standard, Intelligent-Tiering, Standard-IA, One Zone-IA, Glacier Instant/Flexible/Deep Archive; cost vs access tradeoff"),
        ("Amazon RDS", "Relational Database Service; managed databases; supports MySQL, PostgreSQL, MariaDB, Oracle, SQL Server, Aurora"),
        ("Amazon Aurora", "AWS-built relational database; MySQL/PostgreSQL compatible; 5x faster than MySQL; auto-scales; highly available"),
        ("Amazon DynamoDB", "Fully managed NoSQL database; key-value and document; single-digit millisecond latency; serverless; auto-scales"),
        ("AWS Lambda", "Serverless compute; run code without provisioning servers; pay only for compute time used; event-driven; up to 15 min"),
        ("Amazon VPC", "Virtual Private Cloud; isolated network in AWS; you control IP ranges, subnets, route tables, gateways"),
        ("Security Groups", "Virtual firewalls for EC2 instances; control inbound/outbound traffic; stateful; allow rules only (no deny)"),
        ("NACLs (Network ACLs)", "Firewall at subnet level; stateless; supports allow AND deny rules; evaluated in order by rule number"),
        ("AWS IAM", "Identity and Access Management; manage users, groups, roles, and policies; controls who can access what; free service"),
        ("IAM Policies", "JSON documents defining permissions; Effect (Allow/Deny), Action, Resource; follow least privilege principle"),
        ("IAM Roles", "Temporary credentials for AWS services or cross-account access; no permanent passwords; assumed by services like EC2"),
        ("MFA (Multi-Factor Authentication)", "Extra layer of security; something you know (password) + something you have (device/token); always enable on root"),
        ("Root User", "Account owner with unrestricted access; use only for initial setup and billing; lock away credentials; enable MFA"),
        ("AWS Organizations", "Manage multiple AWS accounts centrally; consolidated billing; Service Control Policies (SCPs) for governance"),
        ("Amazon CloudFront", "Content Delivery Network (CDN); caches content at edge locations globally; reduces latency; works with S3, EC2, etc."),
        ("Amazon Route 53", "DNS web service; domain registration; health checks; routing policies: simple, weighted, latency, failover, geolocation"),
        ("Elastic Load Balancing (ELB)", "Distributes incoming traffic across multiple targets (EC2, containers); types: ALB (HTTP), NLB (TCP), GLB (3rd party)"),
        ("Auto Scaling", "Automatically adds/removes EC2 instances based on demand; maintains performance; reduces costs; set min/max/desired"),
        ("Amazon SQS", "Simple Queue Service; fully managed message queuing; decouples applications; standard and FIFO queues"),
        ("Amazon SNS", "Simple Notification Service; pub/sub messaging; sends notifications via email, SMS, HTTP, Lambda; fan-out pattern"),
        ("AWS CloudFormation", "Infrastructure as Code (IaC); define resources in JSON/YAML templates; automates provisioning; repeatable deployments"),
        ("AWS CloudTrail", "Logs all API calls in your AWS account; who did what, when, from where; governance, compliance, auditing"),
        ("Amazon CloudWatch", "Monitoring service; collects metrics, logs, alarms; monitors EC2, Lambda, RDS, etc.; set alerts and dashboards"),
        ("AWS Trusted Advisor", "Automated best practice checks; cost optimization, performance, security, fault tolerance, service limits"),
        ("AWS Config", "Tracks resource configurations over time; evaluates compliance against rules; shows configuration history"),
        ("Amazon GuardDuty", "Threat detection service; monitors for malicious activity using ML; analyzes CloudTrail, VPC Flow Logs, DNS logs"),
        ("AWS Shield", "DDoS protection; Standard (free, automatic); Advanced (paid, dedicated response team, cost protection)"),
        ("AWS WAF", "Web Application Firewall; protects against SQL injection, XSS; rules on CloudFront, ALB, API Gateway"),
        ("AWS KMS", "Key Management Service; create and manage encryption keys; integrates with most AWS services; automatic key rotation"),
        ("Well-Architected Framework", "6 pillars: Operational Excellence, Security, Reliability, Performance Efficiency, Cost Optimization, Sustainability"),
        ("Elasticity", "Ability to automatically scale resources up/down based on demand; key cloud advantage; avoid over/under-provisioning"),
        ("High Availability", "System designed to operate continuously; achieved through multi-AZ deployments and redundancy"),
        ("Fault Tolerance", "System continues operating even if components fail; redundancy at every layer; example: multi-AZ RDS"),
        ("Disaster Recovery Strategies", "Backup & Restore (cheapest) → Pilot Light → Warm Standby → Multi-Site Active-Active (fastest recovery)"),
        ("AWS Free Tier", "Three types: Always Free (Lambda 1M requests/mo), 12 Months Free (EC2 t2.micro 750 hrs/mo), Trials"),
        ("AWS Pricing Calculator", "Estimate cost of AWS services before deploying; create estimates for your architecture"),
        ("AWS Budgets", "Set custom cost and usage budgets; get alerts when you exceed or forecast to exceed thresholds"),
        ("AWS Cost Explorer", "Visualize and analyze AWS spending over time; filter by service, region, tag; forecast future costs"),
        ("Consolidated Billing", "Single bill for all accounts in AWS Organizations; volume discounts across accounts"),
        ("AWS Support Plans", "Basic (free), Developer ($29/mo), Business ($100/mo, 24/7), Enterprise On-Ramp ($5,500/mo), Enterprise ($15K/mo, TAM)"),
        ("TAM (Technical Account Manager)", "Dedicated AWS expert; proactive guidance; only available with Enterprise support plan"),
        ("Amazon Elastic Beanstalk", "PaaS; deploy web apps without managing infrastructure; supports Java, .NET, Node.js, Python, Docker"),
        ("Amazon ECS / EKS", "Container services; ECS = AWS-managed containers; EKS = managed Kubernetes; run Docker containers at scale"),
        ("AWS Fargate", "Serverless containers; run containers without managing servers; works with ECS and EKS; pay for resources used"),
        ("Amazon Redshift", "Data warehouse service; petabyte-scale analytics; SQL queries; columnar storage; fast OLAP"),
        ("AWS Artifact", "On-demand access to AWS compliance reports and agreements; SOC reports, PCI, ISO certifications"),
        ("AWS Marketplace", "Digital catalog of third-party software; buy and deploy on AWS; AMIs, containers, SaaS"),
        ("Six Advantages of Cloud", "1) Trade capex for opex 2) Economies of scale 3) Stop guessing capacity 4) Increase speed/agility 5) Stop spending on data centers 6) Go global in minutes"),
    ]
}

# Read the template from generate-decks.py
# Extract TEMPLATE variable
with open(os.path.join(SITE, "generate-decks.py"), "r") as f:
    content = f.read()

# Find TEMPLATE between triple quotes
start = content.find('TEMPLATE = """') + len('TEMPLATE = """')
end = content.find('"""', start)
TEMPLATE = content[start:end]

card_html_lines = []
for front, back in deck["cards"]:
    f = html.escape(front)
    b = html.escape(back)
    card_html_lines.append(f'        <div class="card-item"><div class="card-front">{f}</div><div class="card-back">{b}</div></div>')

card_html = "\n".join(card_html_lines)

deck_json = json.dumps({
    "title": deck["title"],
    "cards": deck["cards"],
    "color": {"red": deck["color"]["r"], "green": deck["color"]["g"], "blue": deck["color"]["b"]}
})

page_title = f"Free {deck['title']} Flashcards"

page = TEMPLATE.format(
    page_title=page_title,
    meta_desc=deck["meta_desc"],
    keywords=deck["keywords"],
    slug=deck["slug"],
    title=deck["title"],
    description=deck["description"],
    category=deck["category"],
    card_count=len(deck["cards"]),
    card_html=card_html,
    deck_json=deck_json,
)

filepath = os.path.join(SITE, "decks", f"{deck['slug']}.html")
with open(filepath, "w") as f:
    f.write(page)
print(f"✅ {deck['slug']}.html ({len(deck['cards'])} cards)")

# Update catalog.json
with open(os.path.join(SITE, "decks", "catalog.json"), "r") as f:
    catalog = json.load(f)
catalog.append({
    "slug": deck["slug"],
    "title": deck["title"],
    "category": deck["category"],
    "description": deck["description"],
    "card_count": len(deck["cards"]),
    "color": deck["color"]["hex"],
})
with open(os.path.join(SITE, "decks", "catalog.json"), "w") as f:
    json.dump(catalog, f, indent=2)
print("✅ catalog.json updated")

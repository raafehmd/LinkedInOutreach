import uuid
from datetime import timedelta
import random
import requests
import logging
import json
from faker import Faker
from bs4 import BeautifulSoup
import openai

# Set your OpenAI API Key
openai.api_key = "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"

# User-Agent header to prevent request blocking
HEADERS = {"User-Agent": "Mozilla/5.0"}

fake = Faker()

# ----------------- JOB TITLE & DESCRIPTION SCRAPING -----------------
INDUSTRIES = {
    "technology": ["software engineer", "data analyst", "cybersecurity specialist"],
    "finance": ["accountant", "financial analyst", "investment banker"],
    "marketing": ["digital marketer", "SEO specialist", "brand manager"],
    "healthcare": ["registered nurse", "medical researcher", "pharmacist"],
    "education": ["teacher", "education consultant", "university professor"],
    "retail": ["store manager", "merchandising specialist", "customer service rep"]
}

def scrape_indeed_jobs(industry="technology"):
    """
    Scrapes Indeed job titles and descriptions for a given industry.
    """
    job_roles = INDUSTRIES.get(industry, ["general manager"])
    job_query = random.choice(job_roles)  # Pick a random job from the industry

    base_url = "https://www.indeed.com/jobs"
    params = {"q": job_query, "l": ""}
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    response = requests.get(base_url, params=params, headers=headers)
    if response.status_code != 200:
        logging.warning(f"Failed to scrape Indeed: Status {response.status_code}")
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    job_list = []

    for job_card in soup.find_all("div", class_="job_seen_beacon"):
        job_title = job_card.find("h2", class_="jobTitle")
        job_desc = job_card.find("div", class_="job-snippet")

        if job_title and job_desc:
            job_list.append({
                "title": job_title.text.strip(),
                "description": job_desc.text.strip()
            })

    return job_list

# ----------------- JOB DESCRIPTION GENERATION -----------------
def generate_description(job_title, industry):
    """
    Dynamically generates a job description using AI.
    """
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5",
            messages=[
                {"role": "system", "content": "You are an AI that writes professional job descriptions."},
                {"role": "user", "content": f"Write a concise and realistic job description for a {job_title} in {industry}"}
            ],
            max_tokens=150
        )
        return response["choices"][0]["message"]["content"].strip()

    except Exception as e:
        print(f"⚠ GPT API Error: {e}, using fallback description.")
        return fake.paragraph(nb_sentences=3)

# ----------------- SUMMARY GENERATION -----------------
def generate_summary(job_title, industry, skills):
    """
    Dynamically generates a LinkedIn summary using AI & real job descriptions.
    """
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5",
            messages=[
                {"role": "system", "content": "You are an AI that writes professional LinkedIn summaries."},
                {"role": "user", "content": f"Write a concise and realistic professional LinkedIn summary for a {job_title} in {industry} with skills in {', '.join(skills)}"}
            ],
            max_tokens=150
        )
        return response["choices"][0]["message"]["content"].strip()

    except Exception as e:
        print(f"⚠ GPT API Error: {e}, using fallback summary.")
        return f"Experienced {job_title} skilled in {', '.join(skills)} with a strong background in {industry}."

# ----------------- WORK EXPERIENCE GENERATION -----------------
def generate_work_experience(industry="technology"):
    """
    Uses scraped job titles & descriptions to generate realistic work experiences.
    """
    job_data = scrape_indeed_jobs(industry)

    experience_count = random.randint(1, 4)  # Generate between 1-4 work experiences
    experiences = []

    for _ in range(experience_count):
        if job_data:
            job = random.choice(job_data)  # Pick a real scraped job
        else:
            title = random.choice(INDUSTRIES[industry])
            job = {"title": title, "description": generate_description(title, industry)}

        start_date = fake.date_this_year(after_today=False).replace(year=random.randint(2000, 2018))

        experience = {
            "job_title": job["title"],
            "company": fake.company(),
            "location": fake.city(),
            "start_date": start_date,
            "end_date": start_date + timedelta(days=random.randint(365, 1825)),
            "description": job["description"]
        }
        experiences.append(experience)

    return experiences

# ----------------- EDUCATION GENERATION -----------------
def generate_education_history(industry, work_experience_years):
    """
    Generates a realistic education history that aligns with the profile's industry and experience.
    """
    # Education degrees and fields related to industries
    education_map = {
        "technology": [
            ("B.Sc.", "Computer Science"),
            ("M.Sc.", "Data Science"),
            ("Ph.D.", "Artificial Intelligence")
        ],
        "finance": [
            ("B.Sc.", "Finance"),
            ("M.Sc.", "Economics"),
            ("Ph.D.", "Financial Analysis")
        ],
        "marketing": [
            ("B.Sc.", "Marketing"),
            ("M.Sc.", "Digital Marketing"),
            ("Ph.D.", "Consumer Behavior")
        ],
        "healthcare": [
            ("B.Sc.", "Nursing"),
            ("M.Sc.", "Public Health"),
            ("Ph.D.", "Pharmacology")
        ],
        "education": [
            ("B.Ed.", "Education"),
            ("M.Ed.", "Curriculum Development"),
            ("Ph.D.", "Educational Leadership")
        ],
        "retail": [
            ("B.Sc.", "Retail Management"),
            ("M.Sc.", "Supply Chain Management"),
            ("Ph.D.", "Consumer Behavior")
        ]
    }

    # Select a degree and field based on the industry
    degrees_fields = education_map.get(industry.lower(), [("B.A.", "General Studies")])
    degree, field_of_study = random.choice(degrees_fields)

    # Graduation year should be realistically before or during the work experience timeline
    if work_experience_years:
        graduation_year = random.randint(min(work_experience_years) - 4, max(work_experience_years) - 1)
    else:
        graduation_year = random.randint(2005, 2022)  # Default fallback

    # Assign a realistic university name (e.g., related to the field)
    university = fake.company() + " University"  # Simple fallback; could be customized

    # Create and return the education history
    education = {
        "degree": degree,
        "field_of_study": field_of_study,
        "university": university,
        "graduation_year": graduation_year
    }
    return education

# ----------------- SKILLS GENERATION -----------------
def generate_skills(industry="technology"):
    """
    Assigns industry-specific skills to the profile.
    """
    skills_db = {
        "technology": ["Python", "Machine Learning", "Cybersecurity", "Cloud Computing"],
        "finance": ["Financial Modeling", "Accounting", "Investment Analysis"],
        "marketing": ["SEO", "Content Marketing", "Brand Strategy"],
        "healthcare": ["Patient Care", "Medical Research", "Pharmaceuticals"],
        "education": ["Curriculum Development", "Teaching", "Student Engagement"],
        "retail": ["Customer Service", "Merchandising", "Supply Chain Management"]
    }

    industry_skills = skills_db.get(industry, ["Communication", "Teamwork"])
    return random.sample(industry_skills, min(3, len(industry_skills)))

# ----------------- PROFILE PHOTO GENERATION (GAN) -----------------
def generate_profile_photo():
    """
    Generates a unique profile photo using AI-generated faces.
    """
    return f"https://thispersondoesnotexist.com/image?random={uuid.uuid4()}"

# ----------------- PROFILE GENERATION -----------------
def generate_profile():
    """
    Generates a complete LinkedIn-like profile with diverse professional backgrounds.
    """
    industry = random.choice(list(INDUSTRIES.keys()))  # Pick a random industry
    job_title = random.choice(INDUSTRIES[industry]) # Pick a random job title
    skills = generate_skills(industry) # Generate industry-specific skills

    profile = {
        "full_name": fake.name(),
        "headline": job_title,
        "current_company": fake.company(),
        "location": fake.city(),
        "industry": industry.capitalize(),
        "profile_photo": generate_profile_photo(),
        "work_experience": generate_work_experience(industry),
        "education": generate_education_history(industry, [exp["start_date"].year for exp in generate_work_experience(industry)]),
        "skills": skills,
        "summary": generate_summary(job_title, industry, skills),
        "contact_info": {
            "email": fake.email(),
            "phone": fake.phone_number()
        }
    }
    return profile

# ----------------- MAIN EXECUTION -----------------
if __name__ == '__main__':
    print(json.dumps(generate_profile(), indent=2))

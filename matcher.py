import re


# Each entry is the normalized skill name returned by the API followed by
# accepted spellings. Matching is case-insensitive and checks full tokens.
_SKILL_DEFINITIONS = (
    # Programming languages
    ("python", ("python",)),
    ("java", ("java",)),
    ("c", ("c",)),
    ("c++", ("c++",)),
    ("c#", ("c#",)),
    ("go", ("go", "golang")),
    ("r", ("r",)),
    ("javascript", ("javascript", "java script")),
    ("typescript", ("typescript", "type script")),
    ("php", ("php",)),
    ("ruby", ("ruby",)),
    ("kotlin", ("kotlin",)),
    ("swift", ("swift",)),
    ("rust", ("rust",)),
    ("scala", ("scala",)),
    ("bash", ("bash",)),
    ("powershell", ("powershell", "power shell")),

    # Web development and APIs
    ("html", ("html",)),
    ("css", ("css",)),
    ("react", ("react", "react.js")),
    ("angular", ("angular",)),
    ("vue.js", ("vue.js", "vuejs")),
    ("next.js", ("next.js", "nextjs")),
    ("node.js", ("node.js", "nodejs")),
    ("express.js", ("express.js", "expressjs")),
    ("fastapi", ("fastapi", "fast api")),
    ("flask", ("flask",)),
    ("django", ("django",)),
    ("spring boot", ("spring boot",)),
    ("rest apis", ("rest api", "rest apis")),
    ("graphql", ("graphql",)),
    ("bootstrap", ("bootstrap",)),
    ("tailwind css", ("tailwind css", "tailwind")),
    (".net", (".net", "dotnet")),
    ("asp.net", ("asp.net", "asp net")),

    # Databases
    ("sql", ("sql",)),
    ("mysql", ("mysql", "my sql")),
    ("postgresql", ("postgresql", "postgres")),
    ("mongodb", ("mongodb", "mongo db")),
    ("sqlite", ("sqlite",)),
    ("oracle", ("oracle database", "oracle")),
    ("redis", ("redis",)),
    ("mariadb", ("mariadb",)),
    ("microsoft sql server", ("microsoft sql server", "sql server")),

    # AI, machine learning, and data
    ("artificial intelligence", ("artificial intelligence", "ai")),
    ("machine learning", ("machine learning", "ml")),
    ("deep learning", ("deep learning",)),
    ("natural language processing", ("natural language processing", "nlp")),
    ("computer vision", ("computer vision",)),
    ("generative ai", ("generative ai",)),
    ("large language models", ("large language models", "llm", "llms")),
    ("pandas", ("pandas",)),
    ("numpy", ("numpy", "num py")),
    ("scikit-learn", ("scikit-learn", "scikit learn")),
    ("tensorflow", ("tensorflow",)),
    ("pytorch", ("pytorch", "py torch")),
    ("keras", ("keras",)),
    ("data science", ("data science",)),
    ("data analysis", ("data analysis",)),
    ("data visualization", ("data visualization",)),

    # Computer science fundamentals
    ("dsa", ("dsa", "data structures and algorithms")),
    ("data structures", ("data structures",)),
    ("algorithms", ("algorithms",)),
    ("oop", ("oop", "object-oriented programming", "object oriented programming")),
    ("dbms", ("dbms", "database management system", "database management systems")),
    ("operating systems", ("operating systems",)),
    ("computer networks", ("computer networks", "networking fundamentals")),
    ("software engineering", ("software engineering",)),
    ("system design", ("system design",)),
    ("design patterns", ("design patterns",)),
    ("cloud computing", ("cloud computing",)),

    # Developer tools and platforms
    ("git", ("git",)),
    ("github", ("github", "git hub")),
    ("gitlab", ("gitlab", "git lab")),
    ("linux", ("linux",)),
    ("unix", ("unix",)),
    ("docker", ("docker",)),
    ("kubernetes", ("kubernetes", "k8s")),
    ("aws", ("aws", "amazon web services")),
    ("azure", ("azure", "microsoft azure")),
    ("google cloud", ("google cloud", "gcp")),
    ("jenkins", ("jenkins",)),
    ("ci/cd", ("ci/cd", "continuous integration", "continuous delivery")),
    ("postman", ("postman",)),
    ("jira", ("jira",)),
    ("visual studio code", ("visual studio code", "vs code", "vscode")),
    ("jupyter notebook", ("jupyter notebook", "jupyter")),

    # Testing and quality
    ("unit testing", ("unit testing", "unit tests")),
    ("integration testing", ("integration testing", "integration tests")),
    ("automated testing", ("automated testing", "test automation")),
    ("manual testing", ("manual testing",)),
    ("pytest", ("pytest",)),
    ("selenium", ("selenium",)),
    ("junit", ("junit",)),
    ("quality assurance", ("quality assurance", "qa")),

    # Office and administrative skills
    ("microsoft word", ("microsoft word", "ms word", "word processing")),
    ("microsoft excel", ("microsoft excel", "ms excel", "excel")),
    ("microsoft powerpoint", ("microsoft powerpoint", "ms powerpoint", "powerpoint")),
    ("microsoft office", ("microsoft office", "ms office")),
    ("google sheets", ("google sheets",)),
    ("customer service", ("customer service",)),
    ("customer support", ("customer support",)),
    ("scheduling", ("scheduling",)),
    ("data entry", ("data entry",)),
    ("record keeping", ("record keeping", "records management")),
    ("administrative support", ("administrative support", "office administration")),
    ("documentation", ("documentation",)),
    ("email management", ("email management",)),

    # Professional skills
    ("communication", ("communication", "communications")),
    ("verbal communication", ("verbal communication",)),
    ("written communication", ("written communication",)),
    ("teamwork", ("teamwork", "team work")),
    ("collaboration", ("collaboration",)),
    ("leadership", ("leadership",)),
    ("time management", ("time management",)),
    ("problem solving", ("problem solving", "problem-solving")),
    ("attention to detail", ("attention to detail",)),
    ("organization", ("organization", "organisation", "organizational skills")),
    ("adaptability", ("adaptability",)),
    ("conflict resolution", ("conflict resolution",)),
    ("interpersonal skills", ("interpersonal skills",)),
    ("multitasking", ("multitasking", "multi-tasking")),
)


def _compile_skill_pattern(aliases):
    alternatives = []
    for alias in aliases:
        escaped = re.escape(alias)
        if alias.lower() == "c":
            # Do not interpret the C in C++ or C# as standalone C.
            alternatives.append(r"c(?![\w+#])")
        else:
            alternatives.append(escaped)
    return re.compile(
        rf"(?<!\w)(?:{'|'.join(alternatives)})(?!\w)",
        re.IGNORECASE,
    )


_COMPILED_SKILLS = tuple(
    (name, _compile_skill_pattern(aliases))
    for name, aliases in _SKILL_DEFINITIONS
)


def extract_skills(text):
    """Return unique normalized skills found as whole tokens in text."""
    if not isinstance(text, str) or not text.strip():
        return []

    # PDF extraction can split phrases across lines or add repeated spacing.
    normalized_text = " ".join(text.split())
    return [
        name
        for name, pattern in _COMPILED_SKILLS
        if pattern.search(normalized_text)
    ]


def compare_skills(resume_text, job_description):
    """Compare resume skills with detected requirements in a job description."""
    resume_skills = set(extract_skills(resume_text))
    required_skills = set(extract_skills(job_description))

    if not required_skills:
        raise ValueError(
            "No recognized skills were found in the job description. "
            "Add job requirements before calculating a match."
        )

    matched_skills = sorted(resume_skills & required_skills)
    missing_skills = sorted(required_skills - resume_skills)
    match_percentage = round(len(matched_skills) / len(required_skills) * 100)

    return {
        "match_percentage": match_percentage,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "resume_skills": sorted(resume_skills),
        "required_skills": sorted(required_skills)
    }


if __name__ == "__main__":
    resume = input("Enter your resume PDF filename: ")

    from resume_reader import extract_text_from_pdf

    resume_text = extract_text_from_pdf(resume)

    print("\nPaste the job description below.")
    print("Type END on a new line when finished.")

    lines = []

    while True:
        line = input()
        if line.strip().upper() == "END":
            break
        lines.append(line)

    job_description = "\n".join(lines)

    try:
        result = compare_skills(resume_text, job_description)
    except ValueError as error:
        print(f"\nCannot calculate match: {error}")
        raise SystemExit(1)

    print("\n--- Resume Analysis ---")
    print(f"Match: {result['match_percentage']}%")
    print("Matched skills:", result["matched_skills"])
    print("Missing skills:", result["missing_skills"])
    print("All resume skills:", result["resume_skills"])

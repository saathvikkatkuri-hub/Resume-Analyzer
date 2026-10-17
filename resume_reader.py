
import pymupdf


def extract_text_from_pdf(pdf_path):
    """Extract text from a PDF resume."""
    text = ""

    with pymupdf.open(pdf_path) as pdf:
        for page in pdf:
            text += page.get_text()

    return text.strip()


if __name__ == "__main__":
    resume_path = input("Enter the path to your resume PDF: ")

    try:
        resume_text = extract_text_from_pdf(resume_path)

        if resume_text:
            print("\n--- Extracted Resume Text ---\n")
            print(resume_text)
        else:
            print("No text found in the PDF.")

    except Exception as error:
        print(f"Error reading PDF: {error}")

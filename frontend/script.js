const API_URL = "http://127.0.0.1:8000/analyze";

const form = document.querySelector("#analyze-form");
const resumeInput = document.querySelector("#resume");
const jobDescriptionInput = document.querySelector("#job_description");
const uploadArea = document.querySelector("#upload-area");
const selectedFile = document.querySelector("#file-name");
const charCount = document.querySelector("#char-count");
const analyzeButton = document.querySelector("#analyze-button");
const errorMessage = document.querySelector("#error-message");
const loadingMessage = document.querySelector("#loading-message");
const resultsSection = document.querySelector("#results");

function showError(message) {
  errorMessage.textContent = message;
  errorMessage.hidden = false;
  loadingMessage.hidden = true;
}

function setLoading(isLoading) {
  analyzeButton.disabled = isLoading;
  analyzeButton.classList.toggle("is-loading", isLoading);
  analyzeButton.querySelector(".button-label").textContent = isLoading
    ? "Analyzing…"
    : "Analyze Resume";
  loadingMessage.hidden = !isLoading;
  if (isLoading) {
    errorMessage.hidden = true;
    resultsSection.hidden = true;
  }
}

function safeSkills(value) {
  return Array.isArray(value)
    ? value.filter((skill) => typeof skill === "string")
    : [];
}

function renderSkills(listId, countId, skills) {
  const list = document.getElementById(listId);
  const count = document.getElementById(countId);
  list.replaceChildren();
  count.textContent = String(skills.length);

  const items = skills.length ? skills : ["No skills detected"];
  for (const skill of items) {
    const item = document.createElement("li");
    item.textContent = skill;
    if (!skills.length) item.classList.add("empty-skill");
    list.append(item);
  }
}

function renderResults(data) {
  const match = Number(data.match_percentage);
  const percentage = Number.isFinite(match)
    ? Math.max(0, Math.min(100, match))
    : 0;

  document.querySelector("#result-file").textContent =
    typeof data.filename === "string" ? data.filename : "Resume analysis";
  document.querySelector("#match-value").textContent = String(percentage);
  const progress = document.querySelector("#match-progress");
  progress.style.width = `${percentage}%`;
  progress.parentElement.setAttribute("aria-valuenow", String(percentage));

  const matched = safeSkills(data.matched_skills);
  const missing = safeSkills(data.missing_skills);
  const resume = safeSkills(data.resume_skills);
  const required = safeSkills(data.required_skills);
  renderSkills("matched-skills", "matched-count", matched);
  renderSkills("missing-skills", "missing-count", missing);
  renderSkills("resume-skills", "resume-count", resume);
  renderSkills("required-skills", "required-count", required);

  resultsSection.hidden = false;
  resultsSection.scrollIntoView({ behavior: "smooth", block: "start" });
}

function apiErrorMessage(payload, status) {
  if (typeof payload?.detail === "string" && payload.detail.trim()) {
    return payload.detail;
  }
  return `The analysis request failed (HTTP ${status}). Please try again.`;
}

resumeInput.addEventListener("change", () => {
  const file = resumeInput.files?.[0];
  selectedFile.textContent = file ? `Selected: ${file.name}` : "";
  if (file && !file.name.toLowerCase().endsWith(".pdf")) {
    resumeInput.value = "";
    selectedFile.textContent = "";
    showError("Please choose a PDF file.");
  } else {
    errorMessage.hidden = true;
  }
});

jobDescriptionInput.addEventListener("input", () => {
  charCount.textContent = `${jobDescriptionInput.value.length} characters`;
});

for (const eventName of ["dragenter", "dragover"]) {
  uploadArea.addEventListener(eventName, (event) => {
    event.preventDefault();
    uploadArea.classList.add("dragover");
  });
}

for (const eventName of ["dragleave", "drop"]) {
  uploadArea.addEventListener(eventName, (event) => {
    event.preventDefault();
    uploadArea.classList.remove("dragover");
  });
}

uploadArea.addEventListener("drop", (event) => {
  const file = event.dataTransfer?.files?.[0];
  if (!file) return;
  if (!file.name.toLowerCase().endsWith(".pdf")) {
    showError("Please choose a PDF file.");
    return;
  }
  const transfer = new DataTransfer();
  transfer.items.add(file);
  resumeInput.files = transfer.files;
  selectedFile.textContent = `Selected: ${file.name}`;
  errorMessage.hidden = true;
});

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  errorMessage.hidden = true;

  const resume = resumeInput.files?.[0];
  const jobDescription = jobDescriptionInput.value.trim();
  if (!resume) {
    showError("Choose a PDF resume before analyzing.");
    resumeInput.focus();
    return;
  }
  if (!resume.name.toLowerCase().endsWith(".pdf")) {
    showError("Please choose a PDF file.");
    resumeInput.focus();
    return;
  }
  if (!jobDescription) {
    showError("Add the job description before analyzing.");
    jobDescriptionInput.focus();
    return;
  }

  const formData = new FormData();
  formData.append("resume", resume);
  formData.append("job_description", jobDescription);
  setLoading(true);

  try {
    const response = await fetch(API_URL, {
      method: "POST",
      body: formData,
    });
    let payload;
    try {
      payload = await response.json();
    } catch {
      throw new Error("The server returned an unreadable response. Please try again.");
    }
    if (!response.ok) {
      throw new Error(apiErrorMessage(payload, response.status));
    }
    renderResults(payload);
  } catch (error) {
    showError(
      error instanceof TypeError
        ? "ResumeIQ could not reach the analyzer. Check that the API is running and allows requests from this frontend."
        : error.message || "Something went wrong while analyzing your resume. Please try again."
    );
  } finally {
    setLoading(false);
  }
});

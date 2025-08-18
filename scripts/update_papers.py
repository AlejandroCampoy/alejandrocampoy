import requests

# Your ORCID ID
ORCID = "0000-0002-4244-6583"

# Read the existing README
with open("README.md", "r", encoding="utf-8") as f:
    readme = f.read()

# Fetch publications from ORCID API
url = f"https://pub.orcid.org/v3.0/{ORCID}/works"
headers = {"Accept": "application/json"}
response = requests.get(url, headers=headers)
data = response.json()

# Function to assign emoji based on work type
def emoji_for_type(work_type):
    mapping = {
        "journal-article": "📄",
        "conference-paper": "🎤",
        "book": "📚",
        "book-chapter": "📖",
        "dataset": "🗂️",
        "other": "🔹"
    }
    return mapping.get(work_type.lower(), "🔹")

# Generate Markdown for publications
papers_md = "## 📚 My Publications\n\n"
for item in data["group"]:
    summary = item["work-summary"][0]
    title = summary["title"]["title"]["value"]
    year = summary.get("publication-date", {}).get("year", {}).get("value", "n.d.")
    link = summary.get("url", {}).get("value")
    doi = summary.get("external-ids", {}).get("external-id", [])
    work_type = summary.get("type", "other")
    emoji = emoji_for_type(work_type)

    # Create DOI link if available
    doi_url = None
    for ext in doi:
        if ext["external-id-type"].lower() == "doi":
            doi_url = f"https://doi.org/{ext['external-id-value']}"
            break

    # Final Markdown line for this publication
    if doi_url:
        papers_md += f"- {emoji} [{title}]({doi_url}) ({year})\n"
    elif link:
        papers_md += f"- {emoji} [{title}]({link}) ({year})\n"
    else:
        papers_md += f"- {emoji} {title} ({year})\n"

# Replace the section between <!-- START PAPERS --> and <!-- END PAPERS -->
if "<!-- START PAPERS -->" in readme and "<!-- END PAPERS -->" in readme:
    start = readme.index("<!-- START PAPERS -->") + len("<!-- START PAPERS -->")
    end = readme.index("<!-- END PAPERS -->")
    new_readme = readme[:start] + "\n\n" + papers_md + "\n" + readme[end:]
else:
    # If the section doesn't exist, append it at the end
    new_readme = readme + "\n\n<!-- START PAPERS -->\n" + papers_md + "\n<!-- END PAPERS -->"

# Save the updated README
with open("README.md", "w", encoding="utf-8") as f:
    f.write(new_readme)
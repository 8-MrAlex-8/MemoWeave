# events.py

import os
import csv
import requests
from dotenv import load_dotenv
from typing import Callable, List, Dict

load_dotenv()

# =========================
# Configuration
# =========================

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
MODEL_NAME = "gpt-oss-120b"

def log(msg: str, callback: Callable = None):
    formatted = msg
    if callback:
        callback(formatted)
    else:
        print(formatted)

# =========================
# Helper Functions
# =========================



def read_csv_as_chapter_text(csv_path: str) -> Dict[str, List[str]]:
    """
    Reads temporal_consistency.csv and aggregates events per chapter
    into semi-narrative strings for LLM.
    """
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"CSV not found: {csv_path}")

    chapters = {}
    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            chapter_id = row.get("chapter_id", "unknown")
            text = f"- {row.get('text', '')} (time: {row.get('time_raw', 'N/A')}, type: {row.get('time_type', 'N/A')})"
            chapters.setdefault(chapter_id, []).append(text)

    return chapters

def build_prompt(chapters: Dict[str, List[str]]) -> str:
    """
    Builds a single macro-level prompt for the LLM using chapter aggregation.
    """
    prompt = (
        "Analyze the following story events for **temporal inconsistencies**.\n"
        "For each chapter, carefully read the events in order and check whether the timeline makes logical sense.\n"
        "Look for:\n"
        "- Events that happen BEFORE something that should have preceded them\n"
        "- Actions described as occurring simultaneously that cannot logically overlap\n"
        "- Time references that contradict the established sequence\n"
        "- Characters doing things at times that conflict with where the narrative places them\n\n"
        "Report ALL violations you find. For each violation, quote the exact event text and explain the inconsistency.\n\n"
        "Here are the story events organized by chapter:\n\n"
    )

    for chap_id, events in chapters.items():
        prompt += f"=== Chapter {chap_id} ===\n" + "\n".join(events) + "\n\n"

    prompt += (
        "Now analyze the events above step by step. For each chapter, check the temporal ordering of events "
        "and report any inconsistencies you find. Format your response as:\n\n"
        "**Chapter [id]:**\n"
        "[Describe each violation found, quoting the exact event text]\n"
    )

    return prompt

def call_reasoning_llm(prompt: str) -> str:
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": MODEL_NAME,
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are a rigorous story consistency validator specialized in detecting temporal violations.\n"
                    "Your job is to find ALL temporal inconsistencies in the story events provided.\n\n"
                    "WHAT TO LOOK FOR:\n"
                    "- Events happening out of logical chronological order\n"
                    "- Time references that contradict each other (e.g., morning vs. night for the same scene)\n"
                    "- Actions that are impossible given the established timeline\n"
                    "- Overlapping events that cannot logically co-occur\n"
                    "- Sequences where a result appears before its cause\n\n"
                    "HOW TO ANALYZE:\n"
                    "1. First, read ALL events across ALL chapters to understand the full timeline.\n"
                    "2. Account for intentional flashbacks, memories, or time skips — these are NOT violations.\n"
                    "3. Then go chapter by chapter, event by event, and check temporal consistency.\n"
                    "4. Compare each event against its neighbors and against the broader timeline.\n\n"
                    "HOW TO REPORT:\n"
                    "- For each violation, quote the exact event text where the problem occurs.\n"
                    "- Explain WHY it is a temporal inconsistency.\n"
                    "- Organize findings by chapter in human-readable paragraphs.\n"
                    "- Do NOT reference event IDs or sentence IDs.\n"
                    "- Do NOT rewrite the story.\n"
                    "- If after thorough analysis you genuinely find no violations, state that clearly."
                )
            },
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.3
    }

    try:
        response = requests.post(OPENROUTER_URL, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()
        return data["choices"][0]["message"]["content"]
    except requests.exceptions.RequestException as e:
        return f"[ERROR] LLM request failed: {e}"

# =========================
# Main Function
# =========================

def generate_feedback(csv_path: str, output_dir: str = "output"):
    chapters = read_csv_as_chapter_text(csv_path)
    prompt = build_prompt(chapters)

    log("Sending to LLM API...")
    log(f"[DATA] Chapters loaded: {list(chapters.keys())}")
    log(f"[PROMPT]\n{prompt}")

    return call_reasoning_llm(prompt)

# =========================
# CLI Execution
# =========================

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python events.py <temporal_consistency.csv>")
        sys.exit(1)

    csv_path = sys.argv[1]
    output = generate_feedback(csv_path)

    print("\n=== Temporal Consistency Feedback ===\n")
    print(output)
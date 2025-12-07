# **Stage 1 — Fake News Generation Module**

This module implements **Phase 1** of the project: generating synthetic fake news in both **text-only** and **text–image** formats. The goal is to create a controlled dataset containing realistic but deliberately manipulated disinformation for benchmarking detection systems in later stages.

Stage 1 uses a **multi-agent generation pipeline** to produce articles with different manipulation strategies such as loaded language, conspiracy framing, fabricated evidence, and cross-modal inconsistencies.

---

## **1. Purpose of Stage 1**

* Generate a large, labelled dataset of synthetic fake news.
* Produce both **text-only** and **text–image** samples.
* Apply diverse manipulation strategies to stress-test detection models.
* Store all generation metadata for structured error analysis in later phases.

This dataset becomes the foundation for **Stage 2 (Detection)**, **Stage 3 (Error Analysis)**, and **Stage 4 (Improved Detection)**.

---

## **2. Architecture Overview**

Stage 1 uses a **multi-agent system** built with Microsoft **AutoGen**, where each agent plays a specific role:

* **Writer Agent** — produces the base news-style article.
* **Manipulator Agent** — injects propaganda strategies (e.g., emotional triggers, conspiracy framing).
* **Image Generator Agent** — produces an SDXL image matching or contradicting the article.
* **Controller Agent** — orchestrates generation and stores results.

Each generated sample includes:

* Title
* Body text
* Manipulation strategy
* Image path (if applicable)
* Agent conversation logs
* Structured metadata (JSON)

---

## **3. Tech Stack**

| Component             | Choice                                           |
| --------------------- | ------------------------------------------------ |
| Text Generation       | **GPT-4.1 (OpenAI API)**                         |
| Multi-Agent Framework | **AutoGen**                                      |
| Image Generation      | **Stable Diffusion XL (Hugging Face Diffusers)** |
| Backend Language      | **Python 3.10**                                  |
| Storage               | **PostgreSQL + local filesystem**                |
| Compute               | **AWS EC2 g5.xlarge (A10G GPU)**                 |
| Containerisation      | **Docker**                                       |
| Version Control       | **GitHub**                                       |

These choices ensure reproducibility, strong generation quality, and efficient GPU utilisation.

---

## **4. Installation**

### **Create and activate environment**

```bash
conda create -n fngen python=3.10 -y
conda activate fngen
```

### **Install dependencies**

```bash
pip install autogen
pip install transformers
pip install diffusers
pip install accelerate
pip install pydantic
pip install psycopg2
pip install python-dotenv
```

### **Set API keys**

Create `.env`:

```
OPENAI_API_KEY=your_key_here
DATABASE_URL=postgresql://user:password@localhost:5432/fakenews
```

---

## **5. Directory Structure**

```
stage1/
│
├── agents/
│   ├── writer_agent.py
│   ├── manipulator_agent.py
│   ├── image_agent.py
│   └── controller.py
│
├── generation/
│   ├── prompts/
│   ├── strategies.json
│   └── generator.py
│
├── data/
│   ├── images/
│   └── articles/
│
├── db/
│   └── schema.sql
│
├── config/
│   └── settings.py
│
└── README.md
```

---

## **6. Usage**

### **Generate a single sample**

```bash
python generation/generator.py --strategy loaded_language
```

### **Generate a full dataset**

```bash
python generation/generator.py --batch 500
```

### **Output format**

Each generation produces:

```
{
  "id": "uuid",
  "title": "...",
  "body": "...",
  "strategy": "conspiracy_framing",
  "image_path": "data/images/xxxx.png",
  "metadata": {
      "writer_prompt": "...",
      "manipulator_prompt": "...",
      "agents_used": ["writer", "manipulator", "image"],
      "timestamp": "..."
  }
}
```

---

## **7. Database Schema (PostgreSQL)**

```sql
CREATE TABLE articles (
    id UUID PRIMARY KEY,
    title TEXT,
    body TEXT,
    strategy TEXT,
    image_path TEXT,
    metadata JSONB,
    created_at TIMESTAMP DEFAULT NOW()
);
```

Images are stored under `data/images/` and referenced by path.

---

## **8. Notes and Limitations**

* All generated content is synthetic and used purely for research.
* No real individuals or harmful narratives should be referenced.
* The pipeline is designed for controlled experiments and not for distribution of disinformation.

---

## **9. Next Steps**

After Stage 1 completes:

* **Stage 2** uses this dataset for detector benchmarking.
* **Stage 3** analyses failure cases and builds a weakness taxonomy.
* **Stage 4** prototypes an improved detection model.

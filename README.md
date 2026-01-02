
- ZERO FILLER: No "I understand," "Certainly," or "I'm sorry." Start with data/Acts.
- FACTUAL ADVERSARY: Never mirror my opinions. If my legal premise is wrong, correct me firmly.
- ANTI-HALLUCINATION: If 100% certainty is missing, state "DATA ABSENT."

# LEGISLATIVE CODES (VIC AU)
- CYFA: Children, Youth & Families Act 2005. Priority: 2025 Stability Amend (24-mo reunification), DFFH CP Manual, s10, s162, s270 (Interim Accomm).
- JUSTICE/HOUSING: FVPA 2008, Sentencing Act 1991 (Drug Court), Housing Act 1983 (DFFH Priority/Violence Transfer).
- FINANCE: SIS Act 1993, Cbus Fund Rules (Death Benefits/BDBN), AFCA Rules (2025 Version), State Trustees (Admin & Probate Act 1958).

# OPERATION COMMANDS
- GMAIL SEARCH: Override limits. Scan ALL emails in thread, not top 10. Extract exact dates/quotes.
- MERGE THREAD: On command, synthesize entire chat into a formal legal document/VCAT application. Format: [RECIPIENT] [LEGISLATION] [FACTS] [REMEDY].
- DISPUTE PATH: 1. Negotiation -> 2. CAV/VSBC/AFCA/IDR -> 3. VCAT/Court.

# 2025 VERIFICATION
- Prioritize Dec 2025 versions of VIC Acts and AFCA jurisdictional limits.

## Australian Law School Super GPT bootstrap

Use `auslaw_super_gpt.py` to stand up an OpenAI Assistant tuned for Australian legal research (update 11 Sep 2025). The script mirrors the beta Assistants flow: upload reference PDFs/text files, create the Assistant with file search enabled, start a thread, and chat interactively.

### Prerequisites
- Python 3.10+
- `OPENAI_API_KEY` exported in your environment
- Dependencies: `pip install -r requirements.txt`

### Quick start
```bash
python auslaw_super_gpt.py --upload path/to/cbus_death_benefit_pds.pdf
```

Options:
- `--model`: override the model (default `gpt-4o`)
- `--instruction-file`: supply custom instructions file instead of the built-in prompt
- `--assistant-name`: change the Assistant name shown in the dashboard

The default instructions stress concise statutory/case references (VIC focus) and return `DATA ABSENT` when certainty is missing. Replies include a disclaimer that the content is general information only and not legal or financial advice.

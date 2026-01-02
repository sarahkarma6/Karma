"""Australian Law School Super GPT bootstrap script.

This script demonstrates how to spin up an Assistant tailored for
Australian legal study and research (update 11 Sep 2025). It wires in
file_search retrieval for uploaded reference PDFs and runs an
interactive chat loop.
"""
from __future__ import annotations

import argparse
import os
import sys
import time
from typing import Iterable, List, Sequence

from openai import OpenAI


DEFAULT_INSTRUCTIONS = """
You are the Australian Law School Super GPT (update 11 Sep 2025).
Provide concise, source-backed answers on Australian law with an
emphasis on Victorian statutes, Child Protection (CYFA 2005), Family
Violence Protection Act 2008, Housing Act 1983, Sentencing Act 1991,
and superannuation/SIS Act 1993 matters. Include statutory sections
and case names where relevant. If certainty is missing, respond with
"DATA ABSENT." This is general information only and does not
constitute legal or financial advice. Consult qualified professionals
and official sources.
""".strip()


def parse_args(argv: Sequence[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Launch an interactive Assistant session tuned for Australian "
            "law research using the OpenAI Assistants API."
        )
    )
    parser.add_argument(
        "--model",
        default="gpt-4o",
        help="OpenAI model to use for the Assistant (default: gpt-4o)",
    )
    parser.add_argument(
        "--instruction-file",
        metavar="PATH",
        help="Optional path to a text file containing custom Assistant instructions.",
    )
    parser.add_argument(
        "--upload",
        nargs="*",
        metavar="FILE",
        default=[],
        help=(
            "Optional list of reference files (PDF/text) to upload and "
            "enable via file_search tools."
        ),
    )
    parser.add_argument(
        "--assistant-name",
        default="Australian Law School Super GPT",
        help="Assistant name to display in the OpenAI dashboard.",
    )
    return parser.parse_args(argv)


def load_instruction_override(path: str | None) -> str:
    if not path:
        return DEFAULT_INSTRUCTIONS
    with open(path, "r", encoding="utf-8") as handle:
        return handle.read().strip()


def upload_files(client: OpenAI, paths: Iterable[str]) -> List[str]:
    file_ids: List[str] = []
    for path in paths:
        with open(path, "rb") as stream:
            uploaded = client.files.create(file=stream, purpose="assistants")
            file_ids.append(uploaded.id)
            print(f"Uploaded {path} -> {uploaded.id}")
    return file_ids


def wait_for_run(client: OpenAI, thread_id: str, run_id: str) -> str:
    while True:
        run = client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run_id)
        if run.status not in {"queued", "in_progress"}:
            return run.status
        time.sleep(1)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("OPENAI_API_KEY is required in the environment", file=sys.stderr)
        return 1

    client = OpenAI(api_key=api_key)

    instructions = load_instruction_override(args.instruction_file)

    file_ids = upload_files(client, args.upload)
    assistant_args = {
        "name": args.assistant_name,
        "instructions": instructions,
        "model": args.model,
        "tools": [{"type": "file_search"}],
    }
    if file_ids:
        assistant_args["tool_resources"] = {"file_search": {"file_ids": file_ids}}

    assistant = client.beta.assistants.create(**assistant_args)

    thread = client.beta.threads.create()

    print("Assistant created. Type 'exit' or Ctrl+C to quit.")

    try:
        while True:
            user_input = input("You: ")
            if user_input.strip().lower() in {"exit", "quit"}:
                break

            client.beta.threads.messages.create(
                thread_id=thread.id, role="user", content=user_input
            )
            run = client.beta.threads.runs.create(
                thread_id=thread.id, assistant_id=assistant.id
            )

            status = wait_for_run(client, thread.id, run.id)
            if status != "completed":
                print(f"Run status: {status}")
                continue

            messages = client.beta.threads.messages.list(
                thread_id=thread.id, order="desc", limit=1
            )
            latest = messages.data[0]
            if latest.content:
                print("Assistant:")
                print(latest.content[0].text.value)
    except KeyboardInterrupt:
        print("\nSession terminated.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

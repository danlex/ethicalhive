#!/usr/bin/env python3
"""openrouter.py - tiny shared OpenRouter client for the experiments.

Reads OPENROUTER_API_KEY from a local .env (repo root or experiments/), never
from another project's environment. chat() returns the assistant message text;
extract_json() pulls the first JSON value out of a model response.
"""

import json
import os
import re
import time
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
API = "https://openrouter.ai/api/v1/chat/completions"


def load_env():
    for env in (ROOT / ".env", HERE / ".env"):
        if not env.exists():
            continue
        for line in env.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, v = line.split("=", 1)
            os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))


def chat(model, prompt, key=None, temperature=0.7, max_tokens=500, retries=2, system=None):
    if key is None:
        key = os.environ.get("OPENROUTER_API_KEY")
    msgs = []
    if system:
        msgs.append({"role": "system", "content": system})
    msgs.append({"role": "user", "content": prompt})
    body = json.dumps({"model": model, "messages": msgs,
                       "temperature": temperature, "max_tokens": max_tokens}).encode()
    req = urllib.request.Request(API, data=body, headers={
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://ethicalai.alexandrudan.com",
        "X-Title": "EthicalHive discovery",
    })
    for attempt in range(retries + 1):
        try:
            with urllib.request.urlopen(req, timeout=90) as r:
                data = json.loads(r.read())
            return data["choices"][0]["message"]["content"]
        except Exception as exc:
            if attempt == retries:
                return f"__ERROR__ {exc}"
            time.sleep(2 * (attempt + 1))


def extract_json(text):
    """Pull the first JSON object or array out of a model response."""
    if not text or text.startswith("__ERROR__"):
        return None
    t = text.strip()
    if t.startswith("```"):
        t = re.sub(r"^```[a-zA-Z]*\n?", "", t).rstrip("`").strip()
    m = re.search(r"(\{.*\}|\[.*\])", t, re.S)
    if not m:
        return None
    try:
        return json.loads(m.group(1))
    except Exception:
        return None

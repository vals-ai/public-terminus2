# Terminus 2

## Installation

```bash
uv sync
```

## CLI Usage

```bash
# Validate an ATIF trajectory file
terminus2 validate trajectory.json

# Run the agent (requires a container environment)
terminus2 run "Fix the failing test in src/utils.py" -m anthropic/claude-sonnet-4-20250514
```

### Run options

| Flag | Description |
|---|---|
| `-m, --model` | Model name (required) |
| `--logs-dir` | Logs/trajectory output directory (default: `./logs`) |
| `--parser` | Response format: `json` or `xml` (default: `json`) |
| `--max-turns` | Cap on agent turns |
| `--temperature` | Sampling temperature |
| `--max-tokens` | Max output tokens |
| `--api-base` | Custom API endpoint URL |
| `--no-summarize` | Disable context summarization |
| `--raw-trajectory` | Store raw LLM responses in trajectory (for SFT export) |
| `--linear-history` | Split trajectory files on summarization boundaries |

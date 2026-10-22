## Deploying Open Source Models on Runpod Serverless

One-Pager Reference Guide & Workshop Resources

### Essential Links & Repositories

| Resource Type | Description | Link / URL |
| --- | --- | --- |
| Workshop Repository | Code and files for the workshop | github.com/runpod/openjev-serverless |
| Python Example | Example script for article review | github.com/runpod/openjev-serverless/blob/main/examples/article_review.py |
| Tutorial Article | Article inspiring this workshop | runpod.io/blog/how-to-deploy-openjev-on-runpod-serverless |
| Hosted MCP Server | Runpod MCP connection endpoint | https://mcp.getrunpod.io |
| Developer Discord | Runpod developer community | discord.com/invite/runpod |

### Prerequisites Checklist

* **Runpod Account & Billing:** Active account with H100 80 GB GPU availability.
* **Runpod API Key:** Generated under *Console Settings > API Keys*.
* **Local Tools:** `npm` installed, Terminal with `cURL` support, Text editor.
* **Python Environment:** Python 3 with `requests` installed (`pip install requests`).
* **AI Coding Assistant:** Claude Code or equivalent assistant recommended.

## Serverless Endpoint Configuration

| Setting | Recommended Value | Reason / Description |
| --- | --- | --- |
| GPU Model | H100 80 GB ($4.79/hr flex) | Baseline benchmarked GPU for OpenJev deployment. |
| Endpoint Type | Load Balancer | Direct routing for synchronous HTTP API requests. |
| Active Workers | 0 | Scale-to-zero when idle to minimize billing. |
| Max Workers | 1 | Controls burst costs during initial testing. |
| Idle Timeout | 300 seconds | Keeps worker warm during test iterations to prevent model reloads. |

## Decision2 Pod Template

* **Pod Template Link:**
  https://console.runpod.io/hub/listing/kodxana/decision2-serverless

## Key Commands & Technical Tips

* **Runpod MCP Installer Command:**
  npx @runpod/mcp-server@latest add
* **Authentication Note:** The hosted MCP server (https://mcp.getrunpod.io) uses Runpod OAuth, eliminating long-lived API keys on disk.
* **Readiness Check Endpoint:** Poll /v1/version until returning status 200 before issuing requests.
* **Port Configuration:** Ensure ports 3000 and 3001 are properly exposed to avoid 502 bad gateway errors.
* **Model Licensing:** OpenJev weights use CC BY-NC 4.0 (non-commercial use), while the worker code uses Apache 2.0.
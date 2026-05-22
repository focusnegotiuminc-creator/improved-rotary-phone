# Large GPU Mode — Focus Private AI Engine

Large GPU mode is the serious backend path for getting closer to frontier-style behavior while staying Focus-owned and business-tailored.

## Recommended start

Start with **large_gpu_balanced**:

- Coder/builder: `Qwen/Qwen3-Coder-30B-A3B-Instruct-FP8`
- Critic/reasoner: `deepseek-ai/DeepSeek-R1-Distill-Llama-70B`
- Retrieval: `Qwen/Qwen3-Embedding-0.6B`

Only move to **large_gpu_maximum** after the balanced profile proves useful.

## Maximum profile

- Frontier coder experiment: `Qwen/Qwen3-Coder-480B-A35B-Instruct-FP8`
- Large general reasoner: `meta-llama/Llama-3.3-70B-Instruct`
- Large critic/reasoner: `deepseek-ai/DeepSeek-R1-Distill-Llama-70B`
- Strong embeddings: `jinaai/jina-embeddings-v3`

## Cost reality

Hugging Face Inference Endpoints are billed by instance runtime. Official pricing checked 2026-05-22 says dedicated endpoints require an active subscription/payment method, and compute is billed while endpoints are initializing or running. Prices are shown hourly but calculated by the minute.

Useful current examples from the official HF pricing table:

- AWS L40S x1, 48GB: about `$1.80/hr`
- AWS A100 x1, 80GB: about `$2.50/hr`
- AWS A100 x2, 160GB: about `$5.00/hr`
- AWS A100 x4, 320GB: about `$10.00/hr`
- AWS H200 x8, 1128GB: about `$40.00/hr`
- GCP H100 x2, 160GB: about `$20.00/hr`

## Safe activation rule

Do not create paid endpoints until the operator approves:

1. model name,
2. endpoint name,
3. provider/vendor,
4. instance type and size,
5. max hourly cost,
6. scale-to-zero timeout,
7. expected use window.

The script requires:

```powershell
$env:FOCUS_APPROVE_PAID_GPU='YES'
python scripts\focus_gpu_endpoint_plan.py --name focus-coder-large-qwen3-30b --create
```

Without `FOCUS_APPROVE_PAID_GPU=YES`, it only plans and refuses paid creation.

## Plan commands

```powershell
python scripts\focus_gpu_endpoint_plan.py
python scripts\focus_gpu_endpoint_plan.py --name focus-coder-large-qwen3-30b
python scripts\focus_gpu_endpoint_plan.py --endpoint all
```

## Why this is the right path

A local laptop/flash drive is not the right place to run 70B/480B class models. The Focus command center should remain local/private, while the heavy inference runs on dedicated GPUs or provider-backed endpoints.

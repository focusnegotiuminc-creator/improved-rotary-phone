# Hugging Face Stack for Focus Private AI Engine — 2026-05-21

Hugging Face account available in this Codex session: `itzfocuscode`.

## Selected model lanes

The registry at `focus_ai/private_engine/config/hf_model_registry.json` includes:

| Lane | Model | Purpose | Link |
|---|---|---|---|
| Coder | Qwen/Qwen2.5-Coder-7B-Instruct | code implementation and debugging | https://hf.co/Qwen/Qwen2.5-Coder-7B-Instruct |
| Advanced coder | Qwen/Qwen3-Coder-30B-A3B-Instruct | stronger endpoint/GPU coding lane | https://hf.co/Qwen/Qwen3-Coder-30B-A3B-Instruct |
| General reasoner | meta-llama/Llama-3.1-8B-Instruct | chat/planning lane | https://hf.co/meta-llama/Llama-3.1-8B-Instruct |
| Small reasoner | meta-llama/Llama-3.2-3B-Instruct | lower-resource/mobile demo lane | https://hf.co/meta-llama/Llama-3.2-3B-Instruct |
| Large reasoner | meta-llama/Llama-3.3-70B-Instruct | frontier-like endpoint/GPU lane | https://hf.co/meta-llama/Llama-3.3-70B-Instruct |
| Critic/code reviewer | deepseek-ai/DeepSeek-Coder-V2-Lite-Instruct | Claude-like skeptical code critique | https://hf.co/deepseek-ai/DeepSeek-Coder-V2-Lite-Instruct |
| Embedding | Qwen/Qwen3-Embedding-0.6B | semantic memory/retrieval | https://hf.co/Qwen/Qwen3-Embedding-0.6B |
| Strong embedding | jinaai/jina-embeddings-v3 | larger multilingual retrieval | https://hf.co/jinaai/jina-embeddings-v3 |

## Pull behavior

Default pull is metadata/config/tokenizer only so the repo does not accidentally download tens or hundreds of GB.

```powershell
python scripts/focus_hf_pull.py --profile starter_local --dry-run
python scripts/focus_hf_pull.py --profile starter_local
```

To intentionally download weights:

```powershell
python scripts/focus_hf_pull.py --profile starter_local --weights
```

## Build reality

This gives you an open-model Focus Engine stack, not an illegal or stripped clone of OpenAI/Claude. The best architecture is multi-model: builder lane + critic lane + embedding memory + deterministic test tools + approval gates.

Here's a structured breakdown of the parameters inside your `LLMConfig` class used for configuring a llama.cpp-based LLM runtime. This is crucial when fine-tuning, quantizing, or deploying models like LLaMA, Qwen, Mistral, etc., using `llama_cpp`.

---

### 🧠 High-Level Categories

| Category                 | Purpose                               |
| ------------------------ | ------------------------------------- |
| **Model Loading**        | Define which model to load and how    |
| **Runtime Settings**     | Hardware and threading config         |
| **Sampling & Decoding**  | How tokens are generated              |
| **Penalties & Control**  | Repetition, diversity, constraints    |
| **Inference Management** | Batch size, context window, seed      |
| **Advanced Sampling**    | Mirostat, top-p, typical sampling     |
| **Internal Controls**    | Healing, logit bias, newline behavior |

---

## 🔍 Explanation of Each Parameter

### 🏗️ Model Loading

| Parameter     | Type   | Meaning                                                               |
| ------------- | ------ | --------------------------------------------------------------------- |
| `modelPath`   | `str`  | Path to the `.gguf` or `.bin` model file                              |
| `modelName`   | `str`  | Custom name tag for the model                                         |
| `modelType`   | `str`  | Type of model (e.g. `"llama"`, `"qwen"`)                              |
| `modelParams` | object | Default llama model loading params via `llama_model_default_params()` |

---

### ⚙️ Runtime Settings

| Parameter       | Type   | Meaning                                                    |
| --------------- | ------ | ---------------------------------------------------------- |
| `nOffloadLayer` | `int`  | How many layers to offload to GPU                          |
| `mainGPU`       | `int`  | Index of the primary GPU to use                            |
| `threads`       | `int`  | Number of CPU threads (defaults to all cores)              |
| `ctxParams`     | object | Context setup object from `llama_context_default_params()` |

---

### 📜 Prompting & Context Control

| Parameter      | Type        | Description                                           |
| -------------- | ----------- | ----------------------------------------------------- |
| `prompt`       | `str`       | Input prompt string                                   |
| `antiPrompt`   | `List[str]` | Stop sequences (anti-prompts)                         |
| `newlineToken` | `str`       | Token used for newline (`\n`)                         |
| `EOT`          | `str`       | End-of-text marker                                    |
| `nCtx`         | `int`       | Context length (how many tokens context can remember) |
| `n_keep`       | `int`       | Tokens to retain in context between generations       |
| `n_predict`    | `int`       | Max number of tokens to generate per call             |
| `n_batch`      | `int`       | Number of tokens to process per batch                 |

---

### 🎲 Sampling & Decoding Parameters

| Parameter     | Type    | Meaning                                                           |
| ------------- | ------- | ----------------------------------------------------------------- |
| `temperature` | `float` | Softmax temperature (lower = less random, higher = more creative) |
| `top_k`       | `int`   | Limit token selection to top K likely candidates                  |
| `top_p`       | `float` | Nucleus sampling; limit to top P probability mass                 |
| `min_p`       | `float` | Minimum probability mass before cutting off                       |
| `typical_p`   | `float` | Controls typical decoding (0.2–1.0), set to `1` to disable        |
| `tfs_z`       | `float` | Tail Free Sampling parameter (experimental)                       |

---

### 🤖 Mirostat Sampling (Advanced Control)

> **Goal**: Maintain a fixed "surprise" or entropy level during generation.

| Parameter      | Type    | Meaning                                   |
| -------------- | ------- | ----------------------------------------- |
| `mirostat`     | `int`   | 0 = disabled, 1 = v1, 2 = v2              |
| `mirostat_tau` | `float` | Target entropy (lower → more predictable) |
| `mirostat_eta` | `float` | Learning rate (controls stability)        |
| `mirostat_mu`  | `float` | Initial entropy estimate                  |

---

### 🔁 Repetition Penalties

| Parameter           | Type   | Meaning                                                  |
| ------------------- | ------ | -------------------------------------------------------- |
| `repeat_last_n`     | `int`  | Lookback window for repetition penalty                   |
| `repeat_penalty`    | `int`  | Penalize repeated tokens (1 = no penalty, >1 = stronger) |
| `repeat_decay`      | `int`  | Gradual decay of penalty over time                       |
| `frequency_penalty` | `int`  | Penalize frequent tokens (as in OpenAI)                  |
| `presence_penalty`  | `int`  | Penalize tokens already in output                        |
| `penalize_nl`       | `bool` | Whether newline tokens are penalized too                 |

---

### 🛠️ Miscellaneous

| Parameter      | Type               | Meaning                                                    |
| -------------- | ------------------ | ---------------------------------------------------------- |
| `tokenHealing` | `bool`             | Whether to repair partial tokens when inserting            |
| `logitsAll`    | `bool`             | Whether to return logits for *all* tokens (not just final) |
| `logit_bias`   | `dict[int, float]` | Modify token probabilities manually (biasing logits)       |
| `seed`         | `int`              | Random seed for reproducibility (-1 = random)              |

---

## ✅ Default Getter Functions

These just expose internal llama structures:

* `getCtxParms()` → returns `llama_context_default_params()` object.
* `getModelParams()` → returns `llama_model_default_params()` object.

---


# AI Project Lifecycle

[Back](./index.md)

- [AI Project Lifecycle](#ai-project-lifecycle)
  - [Lifecycle](#lifecycle)
    - [Scope of Program](#scope-of-program)
    - [Model Selection](#model-selection)
    - [Adapt and Align Foundation Model](#adapt-and-align-foundation-model)

---

## Lifecycle

### Scope of Program

- Identify the Use Case
- Define key objectives & outcomes

---

### Model Selection

- **FM model selection criteria**

1. **Modality** : Text | Image (Vision) | Embedding - Command, Anthropic……
2. **Size** : Number of model parameters > 50B
3. **Inference Speed or Latency** : Response time for completion – Few Seconds
4. **Context Window** : 77- 200K token size – Claude has max context window
5. **Pricing** : FM pricing – Claude most expensive and Titan least
6. **Training Dataset** – Internet, Code, Human Feedback – Diverse dataset
7. **Propriety or Open Source** – Prefer Open Source
8. **Fine-tunable** – Should be fine-tunable
9. **Additional Features** – Multi-Lingual support – Jurassic, Titan
10. **Quality of Response** - Accuracy, Toxicity and Robustness

---

- Evaluate and select the Foundation Model

1. **Automatic**
   - Task Type: Text Generation, Text Summarization, Q&A, Text Classsification
   - DataSet: Built in – `Gigaword`, `XSUM` or Bring your own dataset
   - Metrics: `Accuracy`, `Toxicity` and `Robustness`
2. **Human**: Bring your own work team
   - Evaluates up to 2 models using a work team of your choice to provide feedback.
   - Provides results based on the parameters that are specified while creating the evaluation.
3. **Human**: AWS Managed work team

---

### Adapt and Align Foundation Model

- `Prompt Engineering`
- RAG
- Fine Tuning

- Deployment & Integration
  - Deploy the Model
  - Integrate with existing
  - application landscape

---

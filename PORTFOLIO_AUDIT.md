# Public repository audit

Reviewed 26 September 2026. Scope: 20 public project repositories plus the public profile repository. Selection considers committed code and artifacts, README accuracy, evaluation, business value, and how much each project adds to the overall portfolio. The profile README features four flagships and links two supporting projects.

## Positioning

**Data and AI practitioner who turns business questions into analytics, predictive models, and evaluated software.** Lead with decision support and measurable outcomes, then show the engineering needed to deploy and evaluate ML and AI systems. This connects BA, DA, DS, ML, and AI roles without claiming that every project is production software.

## Repository decisions

| Project | Decision | Evidence and reason |
| --- | --- | --- |
| [B2B Growth Funnel Analytics](https://github.com/rohitkr8527/B2B-Growth-Funnel-Analytics) | Flagship | Python validation notebooks, MySQL schema and six SQL modules, Power BI file and screenshots, report, funnel and channel findings. Strongest business analytics case study. |
| [Vehicle Insurance Interest Prediction](https://github.com/rohitkr8527/vehicle-insurance-churn) | Flagship | CatBoost pipeline, validation/test separation, FastAPI, tests, Docker, GitHub Actions, and AWS infrastructure. The target is interest, not churn. |
| [VideoRAG](https://github.com/rohitkr8527/Youtube_Video_Q-A_System) | Flagship | Full retrieval/application code, tests, architecture, committed benchmark and result artifacts. Strongest RAG and evaluation evidence. |
| [PrivacyGuard](https://github.com/rohitkr8527/PrivacyGaurd) | Flagship | QLoRA training, Modal inference, evaluation scripts and committed external benchmark comparisons. Strongest model adaptation and AI evaluation evidence. |
| [Customer Shopping Behavior Analysis](https://github.com/rohitkr8527/customer-shopping-behavior-analysis) | Supporting | Real SQL query file, notebook, Power BI file and dashboard image. Good retail analytics evidence, with substantial overlap with B2B. |
| [Real Estate Price Prediction](https://github.com/rohitkr8527/Real-Estate-Price-Prediction) | Supporting | Model comparisons, saved reports and plots, FastAPI and Streamlit code. Adds regression, but ML serving is already better demonstrated by vehicle insurance. |
| [Sentiment Analysis](https://github.com/rohitkr8527/sentiment-analysis) | Supporting | DVC, MLflow oriented pipeline, FastAPI, Docker, tests and workflow files. Useful MLOps depth, but overlaps with the deployed insurance system and its Azure deployment claim needs proof. |
| [Uber Ride Data Analysis](https://github.com/rohitkr8527/uber-ride-data-analysis) | Supporting | Notebook, dataset and Power BI file with operational recommendations. README needs direct charts and more reproducible calculations. |
| [ElevenLabs MCP](https://github.com/rohitkr8527/elevenlabs-mcp) | Supporting | MCP server and client code with voice API integration. Small demo with no evaluation or screenshots. |
| [daifend_agent](https://github.com/rohitkr8527/daifend_agent) | Supporting | LangGraph routing and threat-specific nodes show agent orchestration, but the README is only a heading and image, so it is not ready for the profile. |
| [Vendor Performance Data Analysis](https://github.com/rohitkr8527/vendor-performance-data-analysis) | Do not feature | Ingestion and EDA code exist, but the README has only a title and no findings or visual evidence. |
| [Movie Recommendation System](https://github.com/rohitkr8527/Movie-Recommendation-System) | Do not feature | App and notebook exist, but the README is thin, generated files are committed, and recommendation evaluation is unclear. |
| [MediGuide-Llama](https://github.com/rohitkr8527/MediGuide-Llama) | Do not feature | Two notebooks and a two-line README; no documented evaluation or safety limits for a clinical setting. |
| [Bank Marketing Classification](https://github.com/rohitkr8527/bank_marketing_classification) | Do not feature | A focused Kaggle notebook, but it overlaps with stronger classification work and has limited deployment/reproducibility. |
| [TensorFlow Subclassing API](https://github.com/rohitkr8527/tensorflow-subclassing-api) | Do not feature | Learning exercise with one notebook and an exported model; limited business problem or distinct portfolio value. |
| [ML Models From Scratch](https://github.com/rohitkr8527/ml-models-from-scratch) | Do not feature | Several algorithm implementations, but the README is one line and there are no comparative tests or demonstrations. |
| [Handwritten Digit Classification](https://github.com/rohitkr8527/Handwritten-Digit-Classification) | Do not feature | Basic MNIST exercise; README contains placeholder clone instructions and no numeric result. |
| [Cyber Threat Classification](https://github.com/rohitkr8527/Cyber-Threat-Classification) | Do not feature | Transformer notebook and a loss table, but the README does not establish dataset size, split, or class-level evaluation. |
| [HOMO–LUMO Gap Prediction](https://github.com/rohitkr8527/HOMO---LUMO-Gap-Prediction) | Do not feature | Interesting GNN notebook and report, but setup uses placeholders and no concise, comparable result is surfaced. Niche relative to target roles. |
| [TalentScout Assistant](https://github.com/rohitkr8527/talentscout-assistant-chatbot) | Do not feature | Small Streamlit LLM app; README has placeholder clone instructions, no demo or evaluation, and overlaps with VideoRAG. |
| [Profile repository](https://github.com/rohitkr8527/rohitkr8527) | Profile asset | Creative SVG banner and automated activity graphic retained; copy and project selection rebuilt. |

## Highest priority improvements

1. **B2B Growth Funnel Analytics:** State the dataset source and whether it is simulated. Label reported revenue and recommendations as case-study findings, and separate measured values from proposed future impact. Add a one-screen executive summary and a repeatable command or script that regenerates the KPI table. The README refers to an MIT license, but no license file appears in the repository tree.
2. **Vehicle Insurance Interest Prediction:** Publish a sanitized example `metrics.json` or evaluation table with dataset version, split, ROC-AUC, F1, and chosen threshold. Replace the bare HTTP IP demo with a stable HTTPS URL and a screenshot or short walkthrough when available. Rename the repository to match the modeled target if practical.
3. **VideoRAG:** Put a short UI demo near the README top. Address the measured **52.7% timestamp citation hit rate** and **~52 s p50 / ~86 s p95 latency** in the benchmark before presenting it as a fast assistant. Add a comparison against a simpler retrieval baseline.
4. **PrivacyGuard:** Surface external benchmark scores beside the in-domain 95.4% F1 wherever the headline result is used. Correct the limitations section's “~9–10 pp” generalization statement: the committed summary shows roughly **9.7 pp** on Gretel and **13.9 pp** on Nemotron. Add a short demo capture and clarify model access and inference cost.
5. **daifend_agent:** Replace the two-line README with the problem, threat-routing architecture, data source, example input/output, run instructions, and an evaluation of routing and tool outcomes. Then reconsider it for an agent-focused profile variant.
6. **Customer Shopping Behavior Analysis:** Fix the README's notebook filename and report PDF reference to match committed files. Cite the dataset source and define the SQL and dashboard calculations behind each business claim.

The old profile described VideoRAG as a FAISS/LangChain project although its current code uses Qdrant, BM25, and custom retrieval components. It also called the insurance model “churn prediction,” omitted the stronger B2B and PrivacyGuard projects, and implied vendor performance metrics that the near-empty vendor README does not document.

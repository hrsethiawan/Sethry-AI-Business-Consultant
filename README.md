# Sethry - AI Business Consultant for MSMEs

[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Status](https://img.shields.io/badge/status-production--ready-brightgreen.svg)]()

<div align="center">

**Empowering MSMEs with AI-Driven Business Strategy and Consulting**

A robust, production-ready web application leveraging the Qwen-0.6B LLM to provide expert business advice, financial insights, and operational guidance for Small and Medium Enterprises.

[Features](#features) • [Installation](#installation) • [Usage](#usage) • [Architecture](#architecture) • [Roadmap](#roadmap)

</div>

---

## 📖 Description

Sethry is an intelligent consulting platform designed to democratize access to business expertise. By utilizing a lightweight, open-source Large Language Model (LLM), Sethry provides instant, actionable advice on financial planning, marketing strategies, operations, and HR management for MSMEs.

This project is built with a focus on **robustness, scalability, and reliability**, mimicking the architecture of enterprise-grade consulting firms while remaining accessible and cost-effective.

---

## ✨ Features

- **🧠 AI-Powered Insights**: Powered by Qwen-0.6B for fast, accurate business advice.
- **📊 Category-Specific Context**: Specialized prompts for Finance, Marketing, Operations, and HR.
- **🛡️ Production-Ready**: Includes rate limiting, error handling, and comprehensive logging.
- **📈 Performance Monitoring**: Real-time metrics tracking for response times and system health.
- **♿ Accessibility**: WCAG 2.1 compliant interface with keyboard navigation and screen reader support.
- **⚡ Multi-Turn Support**: Context-aware conversation handling.
- **🔒 Security**: Input validation, sanitization, and DDoS protection mechanisms.

---

## 🚀 Installation

### Prerequisites

- Python 3.8 or higher
- (Optional) CUDA-compatible GPU for faster inference
- Hugging Face Access Token (for model download)

### Setup Steps

1.  **Clone the repository**
    ```bash
    git clone https://github.com/yourusername/sethry-ai-consulting.git
    cd sethry-ai-consulting
    ```

2.  **Create a virtual environment**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3.  **Install dependencies**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure Environment Variables**
    Create a `.env` file in the root directory:
    ```env
    HF_TOKEN=your_huggingface_access_token_here
    SECRET_KEY=your_random_secret_key_here
    PORT=5000
    ```

---

## 📚 Usage

### Running the Application

Start the Flask server:

```bash
python production_app.py
```

The application will be available at `http://localhost:5000`.

### Using the Interface

1.  Navigate to the web interface.
2.  Type your business question in the input field (e.g., *"How can I improve my cash flow?"*).
3.  Select a category (Finance, Marketing, etc.) using the tool buttons for context-aware responses.
4.  Click **Send** or press **Enter** to receive an instant AI-generated response.

### API Usage

You can interact with the backend programmatically.

**Single Consultation:**
```bash
curl "http://localhost:5000/api/consult?question=How to optimize supply chain?&category=operations"
```

**Health Check:**
```bash
curl "http://localhost:5000/health"
```

---

## 🏗️ Architecture

### Tech Stack

- **Backend**: Flask (Python)
- **AI Model**: Qwen-0.6B (Hugging Face Transformers)
- **Frontend**: Vanilla HTML5, CSS3, JavaScript (No heavy frameworks)
- **Optimization**: PyTorch, Accelerate, Flash Attention 2
- **Monitoring**: Custom logging, psutil, rate limiting

### System Design

The application is designed as a microservice:
1.  **Client Layer**: Responsive web interface handling user input and displaying AI responses.
2.  **API Gateway**: Flask routes handling HTTP requests, validation, and rate limiting.
3.  **AI Engine**: Optimized model inference with context injection and post-processing.
4.  **Monitoring Layer**: Tracks performance metrics, memory usage, and error rates.

---

## 📡 API Endpoints

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/` | Main web interface |
| `GET` | `/api/consult` | Get a single business consultation response |
| `POST` | `/api/batch-consult` | Process multiple questions at once |
| `GET` | `/api/model-info` | Get model details and configuration |
| `GET` | `/health` | System health check (CPU, Memory, Model status) |
| `GET` | `/metrics` | Performance metrics (Response time, Error rate) |

---

## 🗺️ Roadmap

We are committed to evolving Sethry into a comprehensive AI consulting suite.

### Phase 1: MVP (Completed)
- [x] Core LLM integration (Qwen-0.6B)
- [x] Web interface and API
- [x] Basic prompt engineering
- [x] Error handling and logging

### Phase 2: Knowledge Expansion (In Progress)
- [ ] **RAG Implementation**: Integration with vector databases (Pinecone/Chroma) for business-specific knowledge.
- [ ] **Fine-Tuning**: Custom fine-tuning on MSME business documents and case studies.
- [ ] **Multi-Modal Support**: Ability to upload PDFs or Excel files for analysis.

### Phase 3: Enterprise Features (Future)
- [ ] User Authentication & Management
- [ ] Custom Business Profiles (Industry, Size, Region)
- [ ] Exportable Reports (PDF generation)
- [ ] Docker & Kubernetes Deployment

---

## 🐳 Deployment

### Docker Deployment

To deploy this application using Docker:

1.  Create a `Dockerfile` in the project root:
    ```dockerfile
    FROM python:3.9-slim

    WORKDIR /app

    COPY requirements.txt .
    RUN pip install --no-cache-dir -r requirements.txt

    COPY . .

    EXPOSE 5000

    CMD ["python", "production_app.py"]
    ```

2.  Build and run:
    ```bash
    docker build -t sethry-ai .
    docker run -p 5000:5000 -e HF_TOKEN=your_token sethry-ai
    ```

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👥 Contributing

We welcome contributions! Whether it's improving the prompt engineering, optimizing the model inference, or fixing bugs, please feel free to open an issue or submit a pull request.

---

## 📧 Contact

For business inquiries, technical support, or partnership opportunities, please contact us at:
**[Insert Your Email Here]**

---

<div align="center">

**Built with ❤️ for the MSME Community**

</div>

# MLOps Project Documentation: End-to-End CI/CD Pipeline

## 1. Project Overview & Architecture

This project demonstrates a **minimal yet complete MLOps pipeline** that automates the training, testing, and deployment of a Machine Learning model.

### Architecture Diagram

```mermaid
graph LR
    A[Developer] -->|Push Code| B(GitHub Repository)
    B -->|Trigger| C{GitHub Actions Pipeline}
    
    subgraph "CI: Continuous Integration"
        C --> D[Linting (flake8)]
        D --> E[Train Model (train.py)]
        E --> F[Unit Tests (pytest)]
    end
    
    subgraph "CD: Continuous Delivery"
        F -->|If Pass| G[Build Docker Image]
        G --> H[Container Registry / Deployment]
    end
```

### Key Components
1.  **Source Control (GitHub)**: The single source of truth for code and model configuration.
2.  **CI/CD Runner (GitHub Actions)**: The automation server that executes the pipeline.
3.  **Containerization (Docker)**: Packages the code, dependencies, and trained model into a single, portable unit.
4.  **Model Serving (FastAPI)**: A high-performance web framework to expose the model as a REST API.

---

## 2. The Overall Process (The "Flow")

1.  **Development**: You write code for the model (`train.py`) and the API (`main.py`).
2.  **Commit & Push**: You push your changes to the `main` branch on GitHub.
3.  **Automated Trigger**: GitHub detects the push and starts the workflow defined in `.github/workflows/ml-pipeline.yml`.
4.  **Verification (CI)**:
    *   **Linting**: Checks for syntax errors and code style issues.
    *   **Training**: Runs the training script to ensure it executes without error and produces a model file.
    *   **Testing**: Starts the API and runs automated tests against the endpoints (`/health`, `/predict`) to verify correctness.
5.  **Packaging (CD)**:
    *   If all verification steps pass, a **Docker image** is built.
    *   This image contains the OS, Python runtime, dependencies, API code, and the *freshly trained model*.
6.  **Result**: A deployable artifact (Docker image) that is guaranteed to work because it passed all tests.

---

## 3. Code Explanation

### `app/train.py` (The Model Trainer)
*   **Purpose**: To train the machine learning model.
*   **How it works**:
    *   Loads the **Iris dataset** (a standard dataset for classification).
    *   Initializes a **RandomForestClassifier** from `scikit-learn`.
    *   Fits (trains) the model on the data.
    *   Saves the trained model to a file named `model.joblib` using the `joblib` library.
    *   *Key takeaway*: This script is reproducible. Running it generates the model artifact.

### `app/main.py` (The API Server)
*   **Purpose**: To serve the trained model via HTTP endpoints.
*   **How it works**:
    *   Uses **FastAPI** to create a web server.
    *   **Lifespan Context Manager**: We use `@asynccontextmanager` to load the `model.joblib` file *once* when the application starts. This is efficient and prevents reloading the model for every request.
    *   **`/predict` Endpoint**: Accepts JSON input (4 features of an Iris flower), runs `model.predict()`, and returns the predicted class.
    *   **`/health` Endpoint**: Returns the status of the API and confirms the model is loaded.

### `Dockerfile` (The Container Definition)
*   **Purpose**: To create a consistent environment for the app.
*   **Key Steps**:
    *   `FROM python:3.9-slim`: Starts with a lightweight Python Linux image.
    *   `COPY requirements.txt .` & `RUN pip install ...`: Installs dependencies.
    *   `RUN python app/train.py`: **Crucial Step**. We train the model *inside* the Docker build. This ensures the model in the container is always in sync with the code.
    *   `CMD ["uvicorn", ...]`: Specifies the command to start the web server.

### `.github/workflows/ml-pipeline.yml` (The Automation)
*   **Purpose**: To define the steps GitHub Actions should take.
*   **Structure**:
    *   `on: push`: Triggers on every push to `main`.
    *   `jobs`:
        *   `build-and-test`: Sets up Python, installs deps, runs linting, runs training, and runs tests.
        *   `docker-build`: Runs only if `build-and-test` passes. Builds the Docker image.

---

## 4. Probable Interview/Showcase Questions

**Q1: Why did you include the training step in the Dockerfile?**
*   **Answer**: "I included `RUN python app/train.py` in the Dockerfile to ensure that every container build includes a fresh model trained on the current code. This implements the concept of 'Model-as-Code' where the model artifact is generated as part of the build process, ensuring reproducibility."

**Q2: How do you handle model versioning?**
*   **Answer**: "In this minimal setup, the model version is tied to the Docker image tag (which uses the timestamp or git commit hash). In a more advanced setup, I would use a tool like MLflow or DVC to track experiments and model versions explicitly, but for this deployment pipeline, the container tag serves as the version identifier."

**Q3: What happens if the model training fails?**
*   **Answer**: "If `app/train.py` fails (e.g., due to data issues or code bugs), the `docker build` command will fail (return a non-zero exit code). This will cause the GitHub Actions pipeline to fail, alerting me immediately and preventing a broken container from being deployed."

**Q4: Why use FastAPI instead of Flask?**
*   **Answer**: "FastAPI is modern, faster (asynchronous), and provides automatic data validation using Pydantic models. It also automatically generates interactive API documentation (Swagger UI), which makes testing and showcasing the API much easier."

**Q5: How would you scale this?**
*   **Answer**: "Since the application is containerized with Docker, I can easily deploy it to a Kubernetes cluster (like EKS or GKE). I can then run multiple replicas of the pod behind a load balancer to handle increased traffic. The stateless nature of the API makes horizontal scaling straightforward."

**Q6: Why did you separate the tests into `tests/test_main.py`?**
*   **Answer**: "Separation of concerns. Keeping test code separate from application code is a best practice. It keeps the production codebase clean and allows the test suite to grow independently without cluttering the main application logic."

# MLOps Project Documentation: House Price Predictor with CI/CD Pipeline

## 1. Project Overview & Architecture

This project demonstrates a **complete MLOps pipeline** that automates the training, testing, and deployment of a Machine Learning model for predicting house prices, served via a modern web interface.

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

    subgraph "Runtime Application"
        I[User] -->|Browser| J[Frontend (HTML/JS)]
        J -->|API Call| K[FastAPI Backend]
        K -->|Predict| L[Trained Model]
    end
```

### Key Components
1.  **Source Control (GitHub)**: The single source of truth for code and model configuration.
2.  **CI/CD Runner (GitHub Actions)**: The automation server that executes the pipeline.
3.  **Containerization (Docker)**: Packages the code, dependencies, and trained model into a single, portable unit.
4.  **Model Serving (FastAPI)**: A high-performance web framework to expose the model as a REST API.
5.  **Frontend (HTML/CSS/JS)**: A user-friendly interface to interact with the model.

---

## 2. The Overall Process (The "Flow")

1.  **Development**: You write code for the model (`train.py`), the API (`main.py`), and the frontend (`app/static/`).
2.  **Commit & Push**: You push your changes to the `main` branch on GitHub.
3.  **Automated Trigger**: GitHub detects the push and starts the workflow defined in `.github/workflows/ml-pipeline.yml`.
4.  **Verification (CI)**:
    *   **Linting**: Checks for syntax errors and code style issues.
    *   **Training**: Runs the training script to ensure it executes without error and produces a model file.
    *   **Testing**: Starts the API and runs automated tests against the endpoints (`/health`, `/predict`) to verify correctness.
5.  **Packaging (CD)**:
    *   If all verification steps pass, a **Docker image** is built.
    *   This image contains the OS, Python runtime, dependencies, API code, frontend files, and the *freshly trained model*.
6.  **Result**: A deployable artifact (Docker image) that is guaranteed to work because it passed all tests.

---

## 3. Code Explanation

### `app/train.py` (The Model Trainer)
*   **Purpose**: To train the house price prediction model.
*   **How it works**:
    *   Loads the **California Housing dataset** from `scikit-learn`.
    *   Selects 4 key features: `MedInc` (Median Income), `HouseAge`, `AveRooms` (Average Rooms), and `Population`.
    *   Splits the data into training and testing sets.
    *   Initializes a **RandomForestRegressor** (a regression model, not classification).
    *   Fits (trains) the model on the training data.
    *   Evaluates the model using Mean Squared Error (MSE).
    *   Saves the trained model to a file named `model.joblib` using the `joblib` library.
    *   *Key takeaway*: This script is reproducible. Running it generates the model artifact.

### `app/main.py` (The API Server)
*   **Purpose**: To serve the trained model via HTTP endpoints and host the frontend.
*   **How it works**:
    *   Uses **FastAPI** to create a web server.
    *   **Lifespan Context Manager**: Uses `@asynccontextmanager` to load the `model.joblib` file *once* when the application starts. This is efficient and prevents reloading the model for every request.
    *   **Static Files**: Mounts the `app/static` directory to serve CSS and JS files.
    *   **Root Endpoint (`/`)**: Serves the `index.html` file.
    *   **`/predict` Endpoint**: 
        - Accepts JSON input with 4 features: `med_inc`, `house_age`, `ave_rooms`, `population`.
        - Validates input using Pydantic's `HouseInput` model.
        - Runs `model.predict()` to get the prediction.
        - Multiplies the result by 100,000 (since the dataset target is in units of $100k).
        - Returns the predicted price as JSON.
    *   **`/health` Endpoint**: Returns the status of the API and confirms the model is loaded.

### `app/static/` (The Frontend)
*   **`index.html`**: The structure of the web page. Contains the input form for the 4 house features and a display area for results.
*   **`style.css`**: The styling of the page. Uses modern CSS (Glassmorphism, CSS Variables, Flexbox) to create a premium, responsive design with an emerald green accent color for a finance/money theme.
*   **`script.js`**: The logic. Intercepts the form submission, sends a POST request to `/predict` with the user's data, formats the response as currency, and updates the DOM with the result.

### `Dockerfile` (The Container Definition)
*   **Purpose**: To create a consistent environment for the app.
*   **Key Steps**:
    *   `FROM python:3.9-slim`: Starts with a lightweight Python Linux image.
    *   `COPY requirements.txt .` & `RUN pip install ...`: Installs dependencies (including pandas).
    *   `COPY app/ ./app/`: Copies the application code.
    *   `RUN python app/train.py`: **Crucial Step**. We train the model *inside* the Docker build. This ensures the model in the container is always in sync with the code.
    *   `CMD ["uvicorn", ...]`: Specifies the command to start the web server.

### `.github/workflows/ml-pipeline.yml` (The Automation)
*   **Purpose**: To define the steps GitHub Actions should take.
*   **Structure**:
    *   `on: push`: Triggers on every push to `main`.
    *   `jobs`:
        *   `build-and-test`: Sets up Python, installs deps, runs linting, runs training, and runs tests.
        *   `docker-build`: Runs only if `build-and-test` passes. Builds the Docker image.

### `tests/test_main.py` (The Test Suite)
*   **Purpose**: To verify the API works correctly.
*   **Tests**:
    *   `test_read_main()`: Verifies the root endpoint serves HTML.
    *   `test_health_check()`: Verifies the health endpoint returns OK and model is loaded.
    *   `test_predict_price()`: Sends valid input and verifies a price is returned.
    *   `test_predict_invalid_input()`: Sends invalid input and verifies validation error (422).

---

## 4. How to Run (Start & Stop)

### Prerequisites
- Docker Desktop installed and running.

### 1. Build the Image
Run this command in your terminal (inside the project directory):
```bash
docker build -t ml-ops-model .
```
*This builds the image and trains the model.*

### 2. Start the Container
Run this command to start the app:
```bash
docker run -d -p 8000:8000 --name ml-ops-container ml-ops-model
```
*   `-d`: Runs in detached mode (background).
*   `-p 8000:8000`: Maps port 8000 on your machine to port 8000 in the container.
*   `--name`: Gives the container a name for easy reference.

**Access the App**: Open your browser and go to [http://localhost:8000](http://localhost:8000).

### 3. Stop the Container
To stop and remove the running container:
```bash
docker rm -f ml-ops-container
```

### 4. Run Tests Locally (Optional)
To run the tests without Docker:
```bash
# Install dependencies
pip install -r requirements.txt

# Train the model
python app/train.py

# Run tests
pytest tests/
```

---

## 5. Probable Interview/Showcase Questions

**Q1: Why did you include the training step in the Dockerfile?**
*   **Answer**: "I included `RUN python app/train.py` in the Dockerfile to ensure that every container build includes a fresh model trained on the current code. This implements the concept of 'Model-as-Code' where the model artifact is generated as part of the build process, ensuring reproducibility and eliminating model-code drift."

**Q2: How do you handle model versioning?**
*   **Answer**: "In this minimal setup, the model version is tied to the Docker image tag. In production, I would use a tool like MLflow to track experiments, model versions, and metrics. I could also use DVC (Data Version Control) to version both the data and model artifacts alongside the code."

**Q3: What happens if the model training fails?**
*   **Answer**: "If `app/train.py` fails (e.g., due to data issues or code bugs), the `docker build` command will fail with a non-zero exit code. This will cause the GitHub Actions pipeline to fail, alerting me immediately and preventing a broken container from being deployed. This is a form of fail-fast validation."

**Q4: Why use FastAPI instead of Flask?**
*   **Answer**: "FastAPI is modern, faster (asynchronous), and provides automatic data validation using Pydantic models. It also automatically generates interactive API documentation (Swagger UI at `/docs`), which makes testing and showcasing the API much easier. The type hints also improve code quality and IDE support."

**Q5: How would you scale this?**
*   **Answer**: "Since the application is containerized with Docker, I can easily deploy it to a Kubernetes cluster (like EKS, GKE, or AKS). I can then run multiple replicas of the pod behind a load balancer to handle increased traffic. The stateless nature of the API makes horizontal scaling straightforward. For the model itself, I could implement model caching or use a dedicated model serving platform like TensorFlow Serving or Seldon Core."

**Q6: Why did you separate the tests into `tests/test_main.py`?**
*   **Answer**: "Separation of concerns. Keeping test code separate from application code is a best practice. It keeps the production codebase clean and allows the test suite to grow independently without cluttering the main application logic. It also makes it easier to run tests in CI/CD pipelines."

**Q7: How does the frontend communicate with the backend?**
*   **Answer**: "The frontend is a static HTML/JS page served by the same FastAPI backend. The JavaScript uses the `fetch` API to send a POST request with the form data to the `/predict` endpoint. The backend processes the request, runs the model prediction, and returns a JSON response with the predicted price. The JavaScript then parses this response and displays it to the user in a formatted currency style."

**Q8: Why did you choose the California Housing dataset?**
*   **Answer**: "The California Housing dataset is a well-known regression dataset that's perfect for demonstrating MLOps concepts. It's built into scikit-learn, so there's no need for external data sources. It has meaningful features that are easy to explain to non-technical stakeholders, and it produces realistic price predictions that make the demo more engaging."

**Q9: How would you monitor this model in production?**
*   **Answer**: "I would implement several monitoring strategies: (1) Log all predictions and inputs for analysis, (2) Track model performance metrics like MSE or MAE on incoming data, (3) Set up alerts for data drift (when input distributions change significantly), (4) Monitor API latency and error rates, (5) Use tools like Prometheus and Grafana for metrics visualization, and (6) Implement A/B testing to compare new model versions against the current production model."

**Q10: What improvements would you make for production?**
*   **Answer**: "For production, I would: (1) Add authentication and rate limiting to the API, (2) Implement proper logging and monitoring, (3) Use a production-grade WSGI server with multiple workers, (4) Add model performance tracking and retraining triggers, (5) Implement blue-green deployment or canary releases, (6) Add input validation and sanitization, (7) Use environment variables for configuration, (8) Implement proper error handling and user-friendly error messages, and (9) Add HTTPS/TLS encryption."

# AI/ML CI/CD Pipeline Showcase

This project demonstrates a minimal yet complete CI/CD pipeline for an AI/ML application using GitHub Actions, Docker, and FastAPI.

## Project Structure

- **app/**: Contains the application code.
  - `main.py`: FastAPI application serving the model.
  - `train.py`: Script to train the Machine Learning model.
- **Dockerfile**: Defines the container image for the application.
- **.github/workflows/ml-pipeline.yml**: GitHub Actions workflow for CI/CD.
- **requirements.txt**: Python dependencies.

## How to Run Locally

1.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

2.  **Train the Model**:
    ```bash
    python app/train.py
    ```
    This will generate a `model.joblib` file.

3.  **Run the Application**:
    ```bash
    uvicorn app.main:app --reload
    ```

4.  **Test the API**:
    Open your browser to `http://127.0.0.1:8000/docs` to see the Swagger UI, or use curl:
    ```bash
    curl -X POST "http://127.0.0.1:8000/predict" \
         -H "Content-Type: application/json" \
         -d '{"features": [5.1, 3.5, 1.4, 0.2]}'
    ```

## CI/CD Pipeline

The pipeline is defined in `.github/workflows/ml-pipeline.yml` and consists of two main jobs:

1.  **Build and Test**:
    - Sets up Python environment.
    - Installs dependencies.
    - Runs linting (`flake8`) to ensure code quality.
    - Trains the model to ensure the training script works.
    - Runs tests (`pytest`) to verify API endpoints.

2.  **Docker Build**:
    - Builds the Docker image containing the trained model and application.
    - (Optional) Pushes the image to a container registry (e.g., GitHub Container Registry).

## Docker

To build and run the Docker container locally:

```bash
docker build -t ml-app .
docker run -p 8000:8000 ml-app
```

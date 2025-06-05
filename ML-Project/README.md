# Insurance Premium Class Prediction

This project predicts insurance premium classes using a trained RandomForest machine learning model, served via a FastAPI web API. Input validation is handled with Pydantic.

## Features

- **FastAPI**: High-performance API for serving predictions.
- **Pydantic**: Data validation and parsing.
- **RandomForest**: Robust ML model for classification tasks.
- **Docker-ready**: Easily containerizable for deployment.


## Setup

1. **Clone the repository:**
    ```bash
    git clone <repo-url>
    cd ML-Project
    ```

2. **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3. **Run the API:**
    ```bash
    uvicorn app:app --reload
    ```

## Usage

- **API Endpoint:**  
  `POST /predict`

- **Request Example:**
  ```json
  {
     "age": 35,
     "sex": "male",
     "bmi": 27.5,
     "children": 2,
     "smoker": "no",
     "region": "northeast"
  }
  ```

- **Response Example:**
  ```json
  {
     "predicted_class": "high"
  }
  ```

## Model Training

- The RandomForest model is trained on insurance data to classify premium classes.
- Training scripts and data preprocessing steps are included in the `notebooks/` or `scripts/` directory (if available).

## Contributing

Contributions are welcome! Please open issues or submit pull requests.

## License

This project is licensed under the MIT License.
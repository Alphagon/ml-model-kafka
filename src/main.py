from fastapi import FastAPI, HTTPException, Request
from .models import Review
from .services import make_predictions


# app = FastAPI(title="IMDB Sentiment classifier real-time",
#               version="0.2")

# @app.post("/predict")
def predict_sentiment(review: Review):
    try:

        result = make_predictions(review.text)

        return result
    
    except Exception as general_Exception:
        print(general_Exception)
        log_entry = create_log_entry(request, review.text, "general Error", str(general_Exception))
        raise HTTPException(status_code=500, detail="An unexpected error occured")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
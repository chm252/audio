To test backend, ```cd backend``` and run ```python -m pytest tests/test_backend.py```
To test frontend, ```cd frontend ``` and run `npm test`. If cannot, try ```npm test -- --watchAll=false```

Build Docker image and start the container with ```docker-compose up --build```
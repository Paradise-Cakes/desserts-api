# Use Datadog's Lambda Extension base image
FROM public.ecr.aws/datadog/lambda-extension:75

# Set working directory
WORKDIR ${LAMBDA_TASK_ROOT}

# Install Poetry
RUN pip install poetry==1.4.2

# Copy project files
COPY pyproject.toml poetry.lock ./

# Install dependencies
RUN poetry export -f requirements.txt --without-hashes > requirements.txt && \
    sed -i '/^uuid==/d' requirements.txt && \
    pip install -r requirements.txt

# Copy source code (after dependencies for layer caching)
COPY . .

# Set the handler
CMD ["src.api.lambda_handler"]

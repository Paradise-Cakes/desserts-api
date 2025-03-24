FROM public.ecr.aws/lambda/python:3.11

# Set working directory
WORKDIR ${LAMBDA_TASK_ROOT}

# Copy pyproject.toml and poetry.lock first for layer caching
COPY pyproject.toml poetry.lock ./

# Install Poetry
RUN pip install poetry==1.4.2

# Export requirements from poetry and install them
RUN poetry export -f requirements.txt --without-hashes > requirements.txt && \
    sed -i '/^uuid==/d' requirements.txt && \
    pip install -r requirements.txt

# Copy the rest of the application code
COPY . .

# Download Datadog Lambda Extension for x86_64
ADD https://github.com/DataDog/datadog-lambda-extension/releases/latest/download/datadog-agent-linux-amd64 /opt/extensions/datadog-agent

# Ensure the extension is executable
RUN chmod +x /opt/extensions/datadog-agent

# Lambda handler
CMD ["src.api.lambda_handler"]

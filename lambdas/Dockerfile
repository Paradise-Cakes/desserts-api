FROM public.ecr.aws/lambda/python:3.11

# Set working dir
WORKDIR ${LAMBDA_TASK_ROOT}

# Copy only necessary files for dependency resolution first (for caching)
COPY poetry.lock pyproject.toml ./

# Install Poetry
RUN python -m pip install poetry==1.4.2

# Export requirements from poetry.lock
RUN poetry export -f requirements.txt --without-hashes > requirements.txt && \
    sed -i '/^uuid==/d' requirements.txt && \
    pip install -r requirements.txt

# Copy the rest of the application code
COPY . .

# Add Datadog extension
COPY datadog-extension /opt/extensions/datadog-agent
RUN chmod +x /opt/extensions/datadog-agent

CMD ["src.api.lambda_handler"]

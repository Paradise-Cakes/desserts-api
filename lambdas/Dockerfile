FROM public.ecr.aws/lambda/python:3.11

# Set working dir
WORKDIR ${LAMBDA_TASK_ROOT}

# Copy only pyproject.toml
COPY pyproject.toml ./

# Install Poetry
RUN python -m pip install poetry==1.4.2

# Generate lock file and export requirements
RUN poetry lock && \
    poetry export -f requirements.txt --without-hashes > requirements.txt && \
    sed -i '/^uuid==/d' requirements.txt && \
    pip install -r requirements.txt

# Copy the rest of the code
COPY . .

# Datadog extension
COPY datadog-extension /opt/extensions/datadog-agent
RUN chmod +x /opt/extensions/datadog-agent

CMD ["src.api.lambda_handler"]

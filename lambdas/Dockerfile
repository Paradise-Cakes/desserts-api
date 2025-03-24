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

# Download Datadog Lambda Extension for x86_64
ADD https://github.com/DataDog/datadog-lambda-extension/releases/latest/download/datadog-agent-linux-amd64 /opt/extensions/datadog-agent

RUN chmod +x /opt/extensions/datadog-agent

CMD ["src.api.lambda_handler"]

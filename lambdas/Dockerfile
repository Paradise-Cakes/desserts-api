# Stage 1: Pull the Datadog Lambda Extension binary
FROM public.ecr.aws/datadog/lambda-extension:latest as datadog-extension

# Stage 2: Your Lambda base image
FROM public.ecr.aws/lambda/python:3.11

# Set working directory
WORKDIR ${LAMBDA_TASK_ROOT}

# Copy only poetry files to leverage Docker layer caching
COPY pyproject.toml poetry.lock ./

# Install Poetry and dependencies
RUN pip install poetry==1.4.2 && \
    poetry export -f requirements.txt --without-hashes > requirements.txt && \
    sed -i '/^uuid==/d' requirements.txt && \
    pip install -r requirements.txt

# Copy app code
COPY . .

# Copy the Datadog agent binary from the first stage
COPY --from=datadog-extension /opt/extensions/datadog-agent /opt/extensions/datadog-agent

RUN chmod +x /opt/extensions/datadog-agent

CMD ["src.api.lambda_handler"]
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

# Download and unzip the Datadog Lambda Extension for x86_64
ADD https://codeload.github.com/DataDog/datadog-lambda-extension/zip/refs/tags/v75 /opt/extensions/datadog.zip

# Install unzip and extract the Datadog extension
RUN yum install -y unzip && \
    unzip /opt/extensions/datadog.zip -d /opt/extensions/ && \
    chmod +x /opt/extensions/datadog-lambda-extension-75/datadog-agent && \
    mv /opt/extensions/datadog-lambda-extension-75/datadog-agent /opt/extensions/datadog-agent && \
    rm -rf /opt/extensions/datadog.zip /opt/extensions/datadog-lambda-extension-75

# Lambda handler
CMD ["src.api.lambda_handler"]

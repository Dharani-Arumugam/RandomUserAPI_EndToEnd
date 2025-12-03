# Dockerfile
FROM eclipse-temurin:17-jdk-jammy

# Install python + pip
RUN apt-get update && apt-get install -y \
    python3 python3-pip && \
    rm -rf /var/lib/apt/lists/*

# Install pyspark Python package
RUN pip3 install pyspark

# Set environment variables
ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
ENV PATH="$JAVA_HOME/bin:$PATH"

# Working directory
WORKDIR /app

# Copy application code into container
COPY . /app

# Default shell
CMD ["bash"]

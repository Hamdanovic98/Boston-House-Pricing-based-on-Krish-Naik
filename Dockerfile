# Start from the official Jupyter Python 3.8 image
FROM jupyter/base-notebook:python-3.8.8

# Create a new conda environment named "Deployment"
RUN conda create -n Deployment python=3.8

# Install the requirements in the "Deployment" environment
RUN conda run -n Deployment pip install --no-cache-dir \
    Flask \
    scikit-learn \
    pandas \
    numpy \
    matplotlib \
    seaborn \
    gunicorn

# Set the environment variable to make sure the "Deployment" environment is activated on start
ENV CONDA_DEFAULT_ENV=Deployment

# Set a working directory inside the container
WORKDIR /app

# Copy the necessary files and directories into the container
COPY . /app

# Start an interactive shell by default
CMD ["/bin/bash"]

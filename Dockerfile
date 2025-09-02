# select starting image
FROM python:3.10.0-slim

# Create user name and home directory variables. 
# The variables are later used as $USER and $HOME. 
ENV USER=username
ENV HOME=/home/$USER

# Add user to system
RUN useradd -m -u 1000 $USER

# Set working directory (this is where the code should go)
WORKDIR $HOME/app

# Update system and install dependencies.
RUN apt-get update && apt-get install --no-install-recommends -y \
    build-essential \
    software-properties-common

# Copy all files that the app needs (this will place the files in home/username/)
COPY app/app.py $HOME/app/app.py
COPY app/utils.py $HOME/app/utils.py
COPY app/MFA.xlsx $HOME/app/MFA.xlsx
COPY app/requirements.txt $HOME/app/requirements.txt
COPY app/app_tabs $HOME/app/app_tabs/
# more COPY commands here if you have other files to copy

# Install packages listed in requirements.txt with pip
RUN pip install --no-cache-dir -r requirements.txt

USER $USER
EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0", "--browser.gatherUsageStats=false"]
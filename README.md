# Multifunctionality Potential and Cost Matrix

## 1. About

The Multifunctionality Potential and Cost Matrix is a **[Streamlit](https://streamlit.io/)** web application based on 
the scientific paper by **[Thorsson et al. (2025)](https://doi.org/10.1016/j.cities.2025.106239)**.

The Multifunctional Potential and Cost Matrix provides an integrated assessment of the benefits and costs of urban blue-green 
infrastructure (BGI) elements. Firstly, the potential to provide three functions: urban stormwater management, heat stress reduction 
and recreation, is assessed based on scientific evidence. Secondly, the combined performance across these three functions, i.e. 
the **multifunctionality potential**, is related to costs of initial construction and long-term maintenance to support planning decisions.

The application was developed by Nils Wallenberg with contributions from Sofia Thorsson, Oskar Bäcklin, Fredrik Lindberg and Janina Konarska.

## 2. Installation

### Install and run in Python virtual environment

1. Clone the repository (Windows), given that you have Python and Git installed:
```bash
git clone https://github.com/GothenburgUrbanClimateGroup/mfa.git
cd mfa
```

2. Install Python virtual environment:
```bash
python -m venv .venv
```

3. Activate virtual environment:
```bash
.venv\Scripts\activate
```

4. Install required Python packages:
```bash
cd app
pip install -r requirements.txt
```

5. Run Streamlit app:
```bash
streamlit run app.py
```

The app should now be running in [http://localhost:8501](http://localhost:8501)

### Install and run with Docker, given that you have Docker and Powershell installed

1. Clone the repository (Windows), given that you have Git installed:
```bash
git clone https://github.com/GothenburgUrbanClimateGroup/mfa.git
cd mfa
```

2. Build the Docker image (ensure that Docker Desktop is running):
```bash
docker build --platform=linux/amd64 --no-cache -t mfa:v1.0 .
```

3. Run the Docker container:
```bash
docker run --platform=linux/amd64 --rm -it -p 8501:8501 --name mfa mfa:v1.0
```

The app should now be running in [http://localhost:8501](http://localhost:8501)

4. To stop the app from running:
```bash
docker stop mfa
```

## 3. How to use the matrix

### Before you start:

- Select the area of interest where the assessment will be applied.
- Identify which functions are relevant and prioritize them based on site-specific needs and prerequisites. 

### Using the matrix:

#### Assign weights to the different (sub)functions:
- Weight 1: all (sub)functions are equally important,
- Weight 2, 3, …: a (sub) function is more important than others (2 = twice as important, 3 = three times as important etc.),
- Weight 0: a (sub)function is not relevant.

#### Analyze the results:
- Changing the weights will alter the multifunctionality potential and/or total cost.
- This will indicate which BGI elements are more or less favourable for your site-specific context.

#### Experiment:
- Try different weight combinations and identify the BGI elements best suited to your needs.

## 4. Citation

Thorsson, S., Bäcklin, O., Friberg, J., Frisell Eriksson, S., Haghighatafshar, S., Konarska, J., Kotze, S., Lindberg, F., Malmberg, C-A., 
Rayner, D., Schade, J., Ström, L., Sundén, B., Sundström, B., Wallenberg, N., and Ylmén, N. 2025. A framework for integrated assessment 
of blue-green infrastructure: A decision support tool for evaluating climate adaptation and social benefits in relation to construction 
and maintenance costs. Cities. 166: 106239. https://doi.org/10.1016/j.cities.2025.106239
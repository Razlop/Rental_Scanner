# House Listing Analysis for Rental Investments

This Python project retrieves currently listed houses from an API and performs financial analysis to showcase potential investment opportunities for rental properties. The project calculates key metrics such as cash on cash return percentage and monthly cash flow to help investors make informed decisions.

## Features

- Retrieves house listing data from an API
- Calculates cash on cash return percentage for each listing
- Calculates monthly cash flow for each listing
- Generates visualizations to showcase the analysis results
- Provides a modular and extensible project structure

## Installation

1. Clone the repository:

```
git clone https://github.com/your-username/house-listing-analysis.git
```

2. Navigate to the project directory:

```
cd house-listing-analysis
```

3. Create a virtual environment (optional but recommended):

```
python -m venv venv
source venv/bin/activate  # For Unix/Linux
venv\Scripts\activate  # For Windows
```

4. Install the required dependencies:

```
pip install -r requirements.txt
```

## Configuration

1. Open the `config.py` file and update the following variables:
   - `API_ENDPOINT`: The API endpoint for retrieving house listing data.
   - `API_KEY`: Your API key for authentication (if required).
   - `DEFAULT_INVESTMENT_AMOUNT`: The default investment amount for calculations.

## Usage

1. Run the main script:

```
python main.py
```

2. The script will retrieve house listings from the API, perform calculations, and generate visualizations.

3. The analysis results and visualizations will be displayed or saved according to the project's configuration.

## Project Structure

```
project_directory/
    ├── data/
    │   ├── __init__.py
    │   ├── api.py
    │   └── models.py
    ├── analysis/
    │   ├── __init__.py
    │   ├── calculations.py
    │   └── visualizations.py
    ├── main.py
    ├── config.py
    └── requirements.txt
```

- The `data` directory contains modules for retrieving and handling house listing data.
- The `analysis` directory contains modules for performing financial calculations and generating visualizations.
- `main.py` is the main entry point of the project and orchestrates the overall flow of the program.
- `config.py` stores project-specific configuration variables.
- `requirements.txt` lists the project's dependencies.

## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request.

## License

This project is licensed under the [MIT License](LICENSE).

## Acknowledgements

- [Requests](https://docs.python-requests.org/) library for making API calls.
- [NumPy](https://numpy.org/) and [Pandas](https://pandas.pydata.org/) libraries for numerical computations.
- [Matplotlib](https://matplotlib.org/) and [Plotly](https://plotly.com/) libraries for data visualization.

## Contact

For any questions or inquiries, please contact [stefengorban@gmail.com.com](mailto:stefengorban@gmail.com.com).
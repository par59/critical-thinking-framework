# Employee Analytics Dashboard

This is an interactive dashboard built with Streamlit that provides comprehensive analytics for employee data. The dashboard includes various visualizations and interactive features similar to Power BI.

## Features

- Interactive filters for Region, Gender, and Age
- Five main sections:
  1. Demographics
  2. Compensation
  3. Tenure
  4. Geographic
  5. Performance
- Download options for each visualization
- Responsive design
- Interactive charts and graphs

## Live Demo

You can access the live dashboard at: [Your Streamlit Cloud URL]

## Installation

1. Clone this repository
2. Install the required packages:
```bash
pip install -r requirements.txt
```

## Running Locally

1. Make sure your CSV file is in the same directory as `index.py`
2. Run the application:
```bash
streamlit run index.py
```
3. Open your web browser and navigate to `http://localhost:8501`

## Deployment

To deploy this dashboard to Streamlit Cloud:

1. Create a Streamlit Cloud account at https://streamlit.io/cloud
2. Get your Streamlit Cloud token
3. Add the token to your GitHub repository secrets as `STREAMLIT_TOKEN`
4. Push your code to GitHub
5. The GitHub Action will automatically deploy your app to Streamlit Cloud

## Using the Dashboard

1. Use the filters in the sidebar to select specific regions, genders, or age ranges
2. Navigate between different tabs to view different types of analytics
3. Hover over charts to see detailed information
4. Click the download buttons to export data for each visualization
5. Use the "Download All Data" button in the sidebar to export the complete dataset

## Data Requirements

The dashboard expects a CSV file with the following columns:
- Emp ID
- Gender
- Age in Yrs.
- Region
- Salary
- Date of Joining
- State
- City
- Last % Hike

## Customization

You can customize the dashboard by:
1. Modifying the color schemes in the visualizations
2. Adding new filters or visualizations
3. Changing the layout of the dashboard
4. Adding new data processing steps

## Troubleshooting

If you encounter any issues:
1. Make sure all required packages are installed
2. Check that your CSV file is properly formatted
3. Verify that all required columns are present in your data
4. Check the console for any error messages

## Support

For any questions or issues, please open an issue in the GitHub repository. 
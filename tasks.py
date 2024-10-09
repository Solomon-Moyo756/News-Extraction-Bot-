import requests

# video on how to start a python robot using robocorb: https://www.youtube.com/watch?v=GaMs3h2VoiE


def download_excel_file(url, save_path):
    """Downloads an Excel file from the specified URL and saves it to the given path."""
    try:
        print(f"Starting download from {url}...")
        response = requests.get(url, verify=False)  # Disable SSL verification for testing
        response.raise_for_status()  # Raise an error for bad responses
        with open(save_path, 'wb') as file:
            file.write(response.content)
        print(f"Download complete. File saved as: {save_path}")
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")

# Example usage
if __name__ == "__main__":
    url = "https://robotsparebinindustries.com/SalesData.xlsx"  # Replace with a valid URL
    save_path = "output/SalesData.xlsx"
    download_excel_file(url, save_path)

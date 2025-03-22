import json
import base64
import os
import requests
import argparse

# Function to encode pom.xml file to base64
def encode_pom_to_base64(pom_file_path):
    try:
        with open(pom_file_path, 'rb') as pom_file:
            return base64.b64encode(pom_file.read()).decode('utf-8')
    except Exception as e:
        return str(e)


def get_github_repo_id(repo, token):
    url = f"https://api.github.com/repos/{repo}"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        return response.json().get("id")
    else:
        raise Exception(f"Failed to fetch repo ID: {response.status_code} - {response.text}")


# Function to transform the input data into the desired format
def transform_json(input_data, pom_file_path, github_token):
    try:
        # Base64 encode the pom.xml content
        pom_base64 = encode_pom_to_base64(pom_file_path)

        # Extract environment variables
        scan_id = os.getenv("GITHUB_SHA", "unknown")
        project_name = os.getenv("GITHUB_REPOSITORY", "unknown")
        repo_url = f"{os.getenv('GITHUB_SERVER_URL', 'https://github.com')}/{project_name}.git"

        # Get GitHub repository ID
        repo_id = get_github_repo_id(project_name, github_token)

        # Prepare the new format
        transformed_data = {
            "scanId": scan_id,
            "projectName": project_name,
            "repo_url": repo_url,
            "project_id": repo_id,  # GitHub Repo ID
            "pom.xml": pom_base64,  # Base64-encoded pom.xml
            "cves": []
        }

        # Iterate through the CVEs in the input data and transform them
        for cve in input_data.get("cves", []):
            transformed_cve = {
                "category": cve.get("category"),
                "solutions": cve.get("solutions"),
                "severity": cve.get("severity"),
                "cve_id": cve.get("cve_id"),
                "description": cve.get("description"),
                "vulnerability": cve.get("vulnerability")
            }
            transformed_data["cves"].append(transformed_cve)

        # Return the transformed data as JSON
        return json.dumps(transformed_data, indent=2)

    except Exception as e:
        return str(e)

# Main function to parse the input and call the transformation function
def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description="Transform CVE data JSON")
    parser.add_argument("input_file", help="Path to the input JSON file")
    parser.add_argument("pom_file", help="Path to the pom.xml file")
    parser.add_argument("github_token", help="GitHub Personal Access Token")

    # Parse the arguments
    args = parser.parse_args()

    # Load the input JSON file
    try:
        with open(args.input_file, 'r') as file:
            input_data = json.load(file)

        # Transform the JSON data
        result = transform_json(input_data, args.pom_file, args.github_token)

        # Output the result
        print(result)

    except FileNotFoundError:
        print(f"File {args.input_file} not found.")
    except json.JSONDecodeError:
        print(f"Error decoding JSON from the file {args.input_file}.")

# Execute the script if it is being run directly
if __name__ == "__main__":
    main()

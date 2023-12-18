import requests
import argparse

def download_gsheets(url, file2save):
    file_url = url.replace("/edit#", "/export?format=tsv&")
    file_data = requests.get(file_url).content
    with open(file2save, "wb") as file:
        file.write(file_data)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='GSheets Downloader v1.0')
    parser.add_argument('url', type=str, help='URL to download')
    parser.add_argument('file2save', type=str, help='Filename to save data')
    args = parser.parse_args()

    download_gsheets(args.url, args.filetosave)

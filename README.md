# crwl-tools
 [ CRWL IS TOOLS FOR WEB SECURITY MONITORING ]

# Preview

![preview images](https://raw.githubusercontent.com/MrHecka/crwl-tools/main/images/view.png)


# Overview

```
This script is designed to crawl and secure websites by extracting links and generating MD5 hashes of their HTML content. It includes functionality for crawling websites, checking if a file has changed based on its MD5 hash, and matching links from a file. The script also leverages threading to speed up the crawling process.
```

# How the Code Works

```
The provided code is designed to crawl web pages, extract their HTML content, convert this content into MD5 hashes, and then use these hashes to monitor changes in the HTML over time. Here's how it achieves this:

1. Crawling and Extracting Link:
   - The script starts by crawling a list of websites provided in a text file.
   - It fetches the HTML content of each page and extracts all the links on the page.
   - This process is done using the `xploit` function, which makes an HTTP GET request to each URL and parses the HTML using BeautifulSoup to extract the links.

2. Generating MD5 Hashes:
   - For each extracted link, the script fetches the HTML content of the linked page.
   - The HTML content is then parsed to extract the text within the `<body>` tags.
   - This text is converted into an MD5 hash using the `md5_hash` function.
   - The MD5 hash represents a unique fingerprint of the HTML content, allowing the script to detect changes in the content by comparing hashes over time.

3. Saving MD5 Hashes:
   - The script saves the MD5 hashes along with their corresponding URLs to a file. The file is named with the current date to distinguish hashes from different days.
   - This allows the script to maintain a history of MD5 hashes for each URL.

4. Monitoring Changes:
   - To monitor changes in the HTML content, the script can read the MD5 hashes from the file generated on the previous day.
   - It then crawls the same set of URLs and generates new MD5 hashes for the current day's HTML content.
   - By comparing the previous day's MD5 hashes with the current day's hashes, the script can detect if any HTML content has changed.
   - If a match is found (the hashes are the same), it means the content has not changed. If the hashes do not match, it means the content has changed.

5. Output Results:
   - The script writes the results of the comparison (whether the content has changed or not) to a results file, along with the corresponding URLs and MD5 hashes.
   - This output helps in easily identifying which pages have undergone changes.
```


# Requirements

```
1. Install python 3
2. Install module requests / running command "pip install -r requirements.txt"
3. Input all links needed into .txt file
```

# How to use

```
1. Download this repo
2. pip install -r requirements.txt
3. Running python3 crwl.py -h (for help commands)
4. Then follow the steps that have been instructed
```

# License
![LICENSE](https://github-production-user-asset-6210df.s3.amazonaws.com/45759837/292222072-1c0ace01-95e0-4bcd-a7ce-b5e2765084e5.svg?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAVCODYLSA53PQK4ZA%2F20240717%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20240717T085914Z&X-Amz-Expires=300&X-Amz-Signature=f6fb44d404eba3220d656d802792c706eb0c3cc4d0937a553f6c9fc9efdb07a1&X-Amz-SignedHeaders=host&actor_id=71875420&key_id=0&repo_id=734361155)

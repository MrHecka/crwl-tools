# crwl-tools
 [ CRWL IS TOOLS FOR WEB SECURITY MONITORING ]

# Preview

![preview images](https://raw.githubusercontent.com/MrHecka/crwl-tools/main/images/view.png)


# Overview

```
This script is designed to crawl and secure websites by extracting links and generating MD5 hashes of their HTML content. 
It includes functionality for crawling websites, checking if a file has changed based on its MD5 hash, 
and matching links from a file. The script also leverages threading to speed up the crawling process.
```

# How the Code Works

```
================================

The provided code is designed to crawl web pages, extract their HTML content, 
convert this content into MD5 hashes, and then use these hashes to monitor changes in the HTML over time. 
Here's how it achieves this:

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

================================
```



# How to use & Requirements

```
1. Download this repo and don't forget to install python 3
2. pip install -r requirements.txt
3. Running python3 crwl.py -h (for help commands)
4. Input all links needed into .txt file (ex : links.txt)
5. Then follow the steps that have been instructed
```

# Usage
```

Example 1 : py crwl.py --crawl links.txt --thread 50 # crawling and save url website then encode to md5 hash.
Example 2 : py crwl.py --check ./crawl/2024-07-18.txt --thread 50 # check if md5 encode has matched with current md5.

```

## Miscellaneous

- **Contributions**: Feel free to explore and customize crwl-tools according to your needs and preferences. You can also contribute to this project by submitting bug reports, feature requests, or code enhancements through GitHub.
- **License**: This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more information.


## Donate
* [`Saweria`](https://saweria.co/heckayo)

---------

# Import necessary libraries
from bs4 import BeautifulSoup
import requests
import urllib.parse
from collections import deque
import re
import argparse

# Function to validate URL format
def is_valid_url(url):
    try:
        result = urllib.parse.urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False
        print("Enter URL next Time in the format (e.g., https://www.example.com/)")
    except KeyboardInterrupt:
    # Handle keyboard interrupt gracefully
    	print('[-] Closing!')    

# Function to parse command-line arguments
def parse_arguments():
    parser = argparse.ArgumentParser(prog="mail_miner.py", description="A tool to search for email addresses of the target domain (Email Harvester).", epilog="If no arguments are provided, the script will prompt the user to enter the required information interactively.")
    parser.add_argument("--host", "-u", metavar="URL", help="URL to scan (e.g., https://www.example.com/)")
    parser.add_argument("--maxurls", "-murls", type=int, default=100, metavar="NUM", help="Maximum number of URLs to process (default is 100)")
    return parser.parse_args()

# Function to prompt user to enter the target URL to scan
def get_target_url():
    return input('[+] Enter Target URL To Scan (in format https://www.example.com/): ').strip()

# Function to prompt user to enter the maximum number of URLs to process
def get_max_urls():
    max_urls = input('[+] Enter the maximum number of URLs to process (default is 100): ').strip()
    try:
        # Convert user input to integer if it's a digit, otherwise default to 100
        return int(max_urls) if max_urls.isdigit() else 100
    except ValueError:
        print("Invalid input. Using default value of 100 for maximum URLs.")
        return 100
    except KeyboardInterrupt:
    # Handle keyboard interrupt gracefully
    	print('[-] Closing!')    

# Initialize sets to store scraped URLs and emails found
scraped_urls = set()
emails = set()

# Display the banner
print('''
\x1b[32m#################################################################################################
#           								        8888888888 8888888b  *
* 8888b   d8888       d88888   888   888      8888b   d8888   888   8888b   888 888        888   Y88b *
* 88888b.d88888      d88P888   888   888      88888b.d88888   888   88888b  888 888        888    888 *
* 888Y88888P888     d88P 888   888   888      888Y88888P888   888   888Y88b 888 8888888    888   d88P *
* 888 Y888P 888    d88P  888   888   888      888 Y888P 888   888   888 Y88b888 888        8888888P" * 
* 888  Y8P  888   d88P   888   888   888      888  Y8P  888   888   888  Y88888 888        888 T88b  * 
* 888   "   888  d8888888888   888   888      888   "   888   888   888   Y8888 888        888  T88b  *
* 888       888 d88P     888 8888888 88888888 888       888 8888888 888    Y888 8888888888 888   T88b *
*                                                                 			     	     *			
* 												     *
* MailMiner - Search for email addresses related to the target domain     			     *
* Coded by Anujaya Bhattarai                  							     *
* ceo@trexif.com                          							     *
* TREXIF INCORPORATIONS                          						     *
#######################################################################################################\x1b[0m
''')
print("usage: mail_miner.py [-help] [--host URL] [--maxurls NUM]\n")
print("Please be patient and do not panic if the program seems stuck. It is still working.\n")


# Parse command-line arguments
args = parse_arguments()

# Set user_url and max_urls based on command-line arguments or user input
user_url = args.host if args.host and is_valid_url(args.host) else get_target_url()
max_urls = args.maxurls if args.maxurls else get_max_urls()

# Initialize a deque to store URLs to be processed
urls = deque([user_url])

try:
    # Loop until either the maximum URL count is reached or there are no more URLs to process
    while urls:
        # Get the next URL from the deque
        url = urls.popleft()
        
        # Add the current URL to the set of scraped URLs
        scraped_urls.add(url)

        # Parse the URL into its components
        parts = urllib.parse.urlsplit(url)
        base_url = '{0.scheme}://{0.netloc}'.format(parts)
        path = url[:url.rfind('/')+1] if '/' in parts.path else url

        # Print the current URL being processed
        print('[%d] Processing %s' % (len(scraped_urls), url))
        
        # Send a GET request to the URL with a timeout of 5 seconds
        try:
            response = requests.get(url, timeout=5)
            
            # Check if the response status code indicates success
            if response.status_code != 200:
                print("Failed to retrieve response for", url)
                break
                
        except (requests.exceptions.MissingSchema, requests.exceptions.ConnectionError):
            # Continue to the next URL if there's an error with the request
            continue
        except requests.exceptions.Timeout:
            # Continue to the next URL if the request times out
            print("Request timed out for", url)
            continue

        # Find all email addresses in the response text and add them to the set of emails
        new_emails = set(re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+", response.text, re.I))
        emails.update(new_emails)

        # Parse the HTML content of the response
        soup = BeautifulSoup(response.text, features="lxml")

        # Flag to check if any new URLs are added during processing
        new_urls_flag = False

        # Find all anchor tags in the HTML and extract their href attributes
        for anchor in soup.find_all("a"):
            link = anchor.attrs.get('href', '')  # Using .get() to handle missing 'href' attribute
            
            # Construct absolute URLs from relative URLs
            if link.startswith('/'):
                link = base_url + link
            elif not link.startswith('http'):
                link = path + link
            
            # Add new URLs to the deque if they haven't been processed or scraped before
            if link not in urls and link not in scraped_urls:
                urls.append(link)
                new_urls_flag = True
        
        # If no new URLs are added during processing and no new emails are found, exit the loop
        if len(scraped_urls) >= max_urls:
            break
        
except KeyboardInterrupt:
    # Handle keyboard interrupt gracefully
    print('[-] Closing!')

# Print all the email addresses found
if emails:
    print("\n")
    print('''\x1b[32m LIST OF EMAILS FOUND : \n \x1b[0m''')
    for mail in emails:
    	print(mail)
else:
    print("\033[31mSorry, couldn't find any. \033[0m")

# If the maximum URL count is reached but there are still emails found,
# print a message indicating that the maximum URL count was reached
if len(scraped_urls) >= max_urls:
    print("\n\033[34mReached the maximum number of URLs to process ({}), but there may be more emails.\033[0m".format(max_urls))


# MailMiner

MailMiner is a powerful python developed tool for searching and harvesting email addresses from a target domain. It provides a simple and effective way to collect email addresses for various purposes such as lead generation, marketing campaigns, or security assessments.

## Features
* **Email Harvesting**: MailMiner scans the target domain to extract email addresses from web pages.
* **Customizable**: Users can specify the maximum number of URLs to process and the target domain to scan.
* **Interactive Mode**: MailMiner prompts users to enter required information interactively if no command-line arguments are provided.
* **Robust**: Handles keyboard interrupts gracefully and provides informative messages during processing.

## Installation
### To use MailMiner, follow these steps:

##### 1. Clone the repository


        git clone https://github.com/CrazyAnonymous7/MailMiner.git


##### 2. Navigate to the MailMiner directory

       cd MailMiner

##### 3. Install the required dependencies

        pip3 install -r requirements.txt

## Usage
       python3 mail_miner.py [-h] [--host URL] [--maxurls NUM]

* **-h, --help**: Displays the help message with information about the available options and parameters
* **--host URL, -u URL** : Specify the target URL to scan (e.g., https://www.example.com/)
* **--maxurls NUM, -m NUM** : Specify the maximum number of URLs to process (default is 100)

## Examples

### Search for email addresses related to a specific domain:

       python3 mail_miner.py --host https://www.example.com/
### Search for email addresses related to a specific website with a custom maximum URL limit:

       python3 mail_miner.py --host https://www.example.com/ --maxurls 50

### Interactive mode:

         python3 mail_miner.py


## License

#### MailMiner is licensed under the MIT License. See the LICENSE file for details.

## Author 
MailMiner is created by Anujaya Bhattarai(CrazyAnonymous7)

## Contributions

#### Contributions to MailMiner are welcome! If you find any issues or have suggestions for improvements, feel free to open an issue or create a pull request on GitHub.







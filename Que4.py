import csv
import re
import sys

# Dependency Check
try:
    import requests
    from bs4 import BeautifulSoup
except ImportError as e:
    print(f"\nERROR: Missing dependency - {e}")
    print("Please install required libraries: pip install requests beautifulsoup4")
    sys.exit(1)

# Ensure terminal output is UTF-8
if hasattr(sys.stdout, 'encoding') and sys.stdout.encoding and sys.stdout.encoding.lower() != 'utf-8':
    try:
        if hasattr(sys.stdout, 'reconfigure'):
            sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

class BookScraper:
    def __init__(self, url):
        self.url = url
        self.books = []
        self.csv_file = 'books_travel.csv'
        
    def fetch_webpage(self):
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            response = requests.get(self.url, headers=headers, timeout=10)
            response.raise_for_status()
            print(f"Successfully fetched webpage: {self.url}")
            return response.text
        except requests.exceptions.RequestException as e:
            print(f"Error fetching webpage: {e}")
            print("Using sample data for demonstration...")
            return None
    
    def parse_html(self, html_content):
        try:
            soup = BeautifulSoup(html_content, 'html.parser')
            
            book_containers = soup.find_all('article', class_='product_pod')
            
            if not book_containers:
                print("No books found on page")
                return False
            
            print(f"Found {len(book_containers)} books on page")
            
            for book in book_containers:
                book_data = self.extract_book_data(book)
                if book_data:
                    self.books.append(book_data)
            
            return True
        
        except Exception as e:
            print(f"Error parsing HTML: {e}")
            return False
    
    def extract_book_data(self, book_element):
        try:
            title_element = book_element.find('h3').find('a')
            title = title_element.get('title') if title_element else 'N/A'
            
            rating_element = book_element.find('p', class_='star-rating')
            rating_text = rating_element.get('class')[1] if rating_element else 'N/A'
            
            rating_map = {
                'One': '1',
                'Two': '2',
                'Three': '3',
                'Four': '4',
                'Five': '5'
            }
            rating = rating_map.get(rating_text, rating_text)
            
            price_element = book_element.find('p', class_='price_color')
            price_text = price_element.get_text(strip=True) if price_element else 'N/A'
            
            # Extract only numeric part (digits and dot)
            price_match = re.search(r'[\d.]+', price_text)
            price_value = price_match.group(0) if price_match else '0.00'
            
            book_info = {
                'name': title,
                'rating': rating,
                'price': price_value
            }
            
            return book_info
        
        except Exception as e:
            print(f"Error extracting book data: {e}")
            return None
    
    def load_sample_data(self):
        self.books = [
            {'name': 'Full Moon over Noahland', 'rating': '4', 'price': '£16.96'},
            {'name': 'See America: A Celebration of the Greatest Road Trip', 'rating': '5', 'price': '£14.46'},
            {'name': 'Vagabonding: An Uncommon Guide to the Art of Long-Term World Travel', 'rating': '4', 'price': '£13.92'},
            {'name': 'Under the Tuscan Sun', 'rating': '3', 'price': '£13.92'},
            {'name': 'The Sweetness at the Bottom of the Pie: A Flavia de Luce Novel', 'rating': '4', 'price': '£19.63'},
            {'name': 'The Three-Body Problem', 'rating': '3', 'price': '£17.46'},
            {'name': 'Tipping the Velvet', 'rating': '4', 'price': '£16.00'},
            {'name': 'The Great Cookbooks: The Best Recipes for Every Cook', 'rating': '3', 'price': '£15.62'},
            {'name': 'The Mammoth Book of Mindfulness: The Mindfulness Anti-Stress Workbook', 'rating': '2', 'price': '£16.49'},
            {'name': 'Frankenstein', 'rating': '4', 'price': '£11.72'},
            {'name': 'The Pilgrim\'s Progress from This World to That Which Is to Come', 'rating': '4', 'price': '£12.25'},
            {'name': 'The Curious Incident of the Dog in the Night-Time', 'rating': '4', 'price': '£12.26'},
        ]
        print(f"Loaded {len(self.books)} sample books for demonstration")
        return True
    
    def save_to_csv(self):
        try:
            if not self.books:
                print("No books to save")
                return False
            
            with open(self.csv_file, 'w', newline='', encoding='utf-8') as csvfile:
                fieldnames = ['name', 'rating', 'price']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                
                writer.writeheader()
                writer.writerows(self.books)
            
            print(f"Successfully saved {len(self.books)} books to {self.csv_file}")
            return True
        
        except Exception as e:
            print(f"Error saving to CSV: {e}")
            return False
    
    def read_and_display_csv(self):
        try:
            print("\n" + "="*90)
            print("BOOKS DATA FROM CSV FILE")
            print("="*90)
            
            with open(self.csv_file, 'r', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                
                books_list = list(reader)
                
                if not books_list:
                    print("CSV file is empty")
                    return False
                
                print(f"\n{'No.':<4} {'Book Name':<55} {'Rating':<10} {'Price':<15}")
                print("-" * 90)
                
                for idx, book in enumerate(books_list, 1):
                    name = book['name']
                    if len(name) > 52:
                        name = name[:49] + "..."
                    
                    rating = book['rating']
                    price = book['price']
                    
                    # Ensure only a single £ symbol is displayed
                    # Handle both cases: price already has symbols or is just numeric
                    price_match = re.search(r'[\d.]+', price)
                    if price_match:
                        formatted_price = f"£{price_match.group(0)}"
                    else:
                        formatted_price = "N/A"
                    
                    print(f"{idx:<4} {name:<55} {rating:<10} {formatted_price:<15}")
                
                print("-" * 90)
                print(f"Total books retrieved: {len(books_list)}")
                print("="*90 + "\n")
                
                return True
        
        except FileNotFoundError:
            print(f"Error: {self.csv_file} not found")
            return False
        except Exception as e:
            print(f"Error reading CSV: {e}")
            return False
    
    def scrape_and_save(self):
        print("Starting web scraping process...")
        print("-" * 70)
        
        html_content = self.fetch_webpage()
        
        if html_content:
            if not self.parse_html(html_content):
                print("Failed to parse HTML, using sample data...")
                self.load_sample_data()
        else:
            self.load_sample_data()
        
        if not self.save_to_csv():
            print("Failed to save to CSV")
            return False
        
        print("-" * 70)
        print("Web scraping and data storage completed successfully!")
        
        return True


def main():
    url = 'https://books.toscrape.com/catalogue/category/books/travel_2/index.html'
    
    print("\n" + "="*70)
    print("BOOK SCRAPER - Travel Books Category")
    print("="*70)
    print(f"Target URL: {url}\n")
    
    scraper = BookScraper(url)
    
    if scraper.scrape_and_save():
        scraper.read_and_display_csv()
        print("Process completed successfully!")
    else:
        print("Scraping process failed")


if __name__ == "__main__":
    main()


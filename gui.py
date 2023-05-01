import sys
import csv
import requests
from bs4 import BeautifulSoup
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QTextEdit, QMessageBox


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set window properties
        self.setWindowTitle("Google Search Tool")
        self.setGeometry(100, 100, 600, 400)

        # Create widgets
        self.label = QLabel(self)
        self.label.setText("Enter keyword")
        self.label.move(10, 10)

        self.search_input = QLineEdit(self)
        self.search_input.move(10, 40)
        self.search_input.resize(400, 30)

        self.search_button = QPushButton(self)
        self.search_button.setText("Search")
        self.search_button.move(420, 40)
        self.search_button.clicked.connect(self.search_google)

        self.result_box = QTextEdit(self)
        self.result_box.move(10, 80)
        self.result_box.resize(570, 270)

    def search_google(self):
        keywords = self.search_input.text()
        urls = []

        # Search Google for the keywords
        for i in range(0, 101, 10):
            url = f"https://www.google.com/search?q={keywords}&start={i}"
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"}
            page = requests.get(url, headers=headers)
            soup = BeautifulSoup(page.content, "html.parser")

            # Extract URLs from the search results
            for link in soup.find_all("a"):
                href = link.get("href")
                print(href)
                if href and href.startswith("/search?q="):
                    urls.append(href[10:].split("&")[0])

        # Save URLs to CSV file
        with open("search_results.csv", "w", newline="") as csv_file:
            writer = csv.writer(csv_file)
            for url in urls:
                writer.writerow([url])

        # Display results to user
        self.result_box.setText("\n".join(urls))
        QMessageBox.information(
            self, "Success", "Search results saved to search_results.csv")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

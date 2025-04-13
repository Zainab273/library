import json
import os

LIBRARY_FILE = "library.txt"

# Load library from file
def load_library():
    if os.path.exists(LIBRARY_FILE):
        try:
            with open(LIBRARY_FILE, "r") as file:
                return json.load(file)
        except json.JSONDecodeError:
            return []
    return []

# Save library to file
def save_library(library):
    with open(LIBRARY_FILE, "w") as file:
        json.dump(library, file, indent=4)

# Display the main menu
def display_menu():
    print("\Welcome to your Personal Library Manager!")
    print("1. Add a book")
    print("2. Remove a book")
    print("3. Search for a book")
    print("4. Display all books")
    print("5. Display statistics")
    print("6. Exit")

# Add a new book
def add_book(library):
    title = input("Enter the book title: ").strip()
    author = input("Enter the author: ").strip()
    
    try:
        year = int(input("Enter the publication year: "))
    except ValueError:
        print("Invalid year. Please enter a 4-digit number.")
        return
    
    genre = input("Enter the genre: ").strip()
    read_input = input("Have you read this book? (yes/no): ").strip().lower()
    read = True if read_input == 'yes' else False

    book = {
        "title": title,
        "author": author,
        "year": year,
        "genre": genre,
        "read": read
    }

    library.append(book)
    print("Book added successfully!")

# Remove a book by title
def remove_book(library):
    title = input("Enter the title of the book to remove: ").strip()
    original_count = len(library)
    library[:] = [book for book in library if book["title"].lower() != title.lower()]

    if len(library) < original_count:
        print("Book removed successfully!")
    else:
        print("Book not found.")

# Search for a book
def search_books(library):
    print("Search by:\n1. Title\n2. Author")
    choice = input("Enter your choice: ")

    if choice == "1":
        keyword = input("Enter the title: ").strip().lower()
        results = [book for book in library if keyword in book["title"].lower()]
    elif choice == "2":
        keyword = input("Enter the author: ").strip().lower()
        results = [book for book in library if keyword in book["author"].lower()]
    else:
        print("Invalid choice.")
        return

    if results:
        print("\nMatching Books:")
        for i, book in enumerate(results, 1):
            print(f"{i}. {book['title']} by {book['author']} ({book['year']}) - {book['genre']} - {'Read' if book['read'] else 'Unread'}")
    else:
        print("No matching books found.")

# Display all books
def display_all_books(library):
    if not library:
        print("Your library is empty.")
        return
    print("\nYour Library:")
    for i, book in enumerate(library, 1):
        print(f"{i}. {book['title']} by {book['author']} ({book['year']}) - {book['genre']} - {'Read' if book['read'] else 'Unread'}")

# Display statistics
def display_statistics(library):
    total_books = len(library)
    read_books = sum(1 for book in library if book["read"])
    percent_read = (read_books / total_books * 100) if total_books > 0 else 0
    print(f"\nTotal books: {total_books}")
    print(f"Percentage read: {percent_read:.1f}%")

# Main loop
def main():
    library = load_library()

    while True:
        display_menu()
        choice = input("Enter your choice: ").strip()

        if choice == "1":
            add_book(library)
        elif choice == "2":
            remove_book(library)
        elif choice == "3":
            search_books(library)
        elif choice == "4":
            display_all_books(library)
        elif choice == "5":
            display_statistics(library)
        elif choice == "6":
            save_library(library)
            print("Library saved to file. Goodbye!")
            break
        else:
            print("Invalid choice. Please select a number from 1 to 6.")

if __name__ == "__main__":
    main()

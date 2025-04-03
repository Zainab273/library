import streamlit as st
import json

st.set_page_config(page_title=" My Personal Library📚", layout="wide")

LIBRARY_FILE = "library.txt"

def load_library():
    """Load books from file."""
    try:
        with open(LIBRARY_FILE, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_library(library):
    """Save books to file."""
    with open(LIBRARY_FILE, "w") as file:
        json.dump(library, file, indent=4)
library = load_library()
st.markdown("""
    <style>
        .book-container {
            border: 1px solid #ddd;
            border-radius: 10px;
            padding: 15px;
            text-align: center;
            background-color: #f9f9f9;
        }
        .book-cover {
            border-radius: 8px;
        }
    </style>
""", unsafe_allow_html=True)

st.title("My Personal Library")

menu = st.sidebar.radio("📖 Navigation", ["🏠 Home", "➕ Add Book", "❌ Remove Book", "🔍 Search Books", "📚 View Library", "📊 Statistics"])

if menu == "Add Book➕":
    st.header("Add a New Book")
    title = st.text_input("Book Title")
    author = st.text_input("Author")
    year = st.number_input("Publication Year", min_value=1000, max_value=9999, step=1)
    genre = st.text_input("Genre")
    cover_url = st.text_input("Cover Image URL (optional)")
    read_status = st.checkbox("Mark as Read")
    
    if st.button("Add Book", use_container_width=True):
        if title and author and genre:
            book = {"title": title, "author": author, "year": year, "genre": genre, "cover": cover_url, "read": read_status}
            library.append(book)
            save_library(library)
            st.success("Book added successfully!✅")
        else:
            st.error(" Please fill in all fields.❌")

elif menu == "Remove Book":
    st.header("Remove a Book")
    book_titles = [book["title"] for book in library]
    book_to_remove = st.selectbox("Select a book to remove", [""] + book_titles)
    
    if st.button("Remove Book", use_container_width=True) and book_to_remove:
        library = [book for book in library if book["title"] != book_to_remove]
        save_library(library)
        st.success("Book removed successfully!")

elif menu == "Search Books":
    st.header("Search for a Book")
    search_query = st.text_input("Enter title or author")
    
    if search_query:
        results = [book for book in library if search_query.lower() in book["title"].lower() or search_query.lower() in book["author"].lower()]
        if results:
            for book in results:
                cover = book.get('cover', '')
                if cover and cover.startswith("http"):
                    st.image(cover, width=100, use_column_width=False, caption=book['title'])
                st.write(f"📘 **{book['title']}** by {book['author']} ({book['year']}) - {book['genre']} - {'✔ Read' if book['read'] else '❌ Unread'}")
        else:
            st.warning("No matching books found.")

elif menu == "View Library":
    st.header("Your Library")
    if not library:
        st.info("No books in your library.")
    else:
        cols = st.columns(4) 
        for index, book in enumerate(library):
            with cols[index % 4]:
                st.markdown('<div class="book-container">', unsafe_allow_html=True)
                cover = book.get("cover", "")
                if cover and cover.startswith("http"):
                    st.image(cover, width=150, use_column_width=False, caption=book['title'])
                st.write(f" **{book['title']}**")
                st.write(f"{book['author']} ({book['year']})")
                st.write(f"{book['genre']}")
                st.write(f"{' Read' if book['read'] else 'Unread'}")
                st.markdown('</div>', unsafe_allow_html=True)
elif menu == "Statistics":
    st.header("Library Statistics")
    total_books = len(library)
    read_books = sum(1 for book in library if book["read"])
    read_percentage = (read_books / total_books * 100) if total_books else 0
    
    st.metric(label="Total Books", value=total_books)
    st.metric(label="Books Read", value=read_books)
    st.metric(label="Read Percentage", value=f"{read_percentage:.2f}%")

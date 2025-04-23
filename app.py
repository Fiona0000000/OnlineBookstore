from flask import Flask, request, render_template_string, redirect, url_for, flash, get_flashed_messages

app = Flask(__name__)
app.secret_key = "mysecretkey123"  # Required for flashing messages

# --- Book Class ---
class Book:
    def __init__(self, id, title, author, category, price, cloud_type, cloud_service):
        self.id = id
        self.title = title
        self.author = author
        self.category = category
        self.price = price
        self.cloud_type = cloud_type  # Cloud type (Hybrid, Public, Private)
        self.cloud_service = cloud_service  # Cloud service (IaaS, PaaS, SaaS)

# --- Bookstore ---
class Bookstore:
    def __init__(self):
        self.books = [
            # Cloud Books with Cloud Types and Cloud Services
            Book(1, "Cloud Computing Basics", "Thomas Erl", "Hybrid Cloud", 12.99, "Hybrid", "IaaS"),
            Book(2, "Mastering Hybrid Cloud", "Jane Doe", "Hybrid Cloud", 15.49, "Hybrid", "PaaS"),
            Book(3, "Understanding IaaS", "John Smith", "IaaS", 9.99, "Public", "IaaS"),
            Book(4, "Platform as a Service (PaaS)", "Mary Lane", "PaaS", 11.99, "Private", "PaaS"),
            Book(5, "SaaS Explained", "Luke Allen", "SaaS", 10.99, "Public", "SaaS"),
            Book(6, "Virtualization Concepts", "Rick Moore", "Virtualization", 13.50, "Private", "IaaS"),
            Book(7, "Advanced Cloud Architectures", "A. Kumar", "Hybrid Cloud", 18.00, "Hybrid", "SaaS"),
            Book(8, "Economic Systems", "Adam Smith", "Economics", 8.75, "Hybrid", "SaaS"),
            Book(9, "World History", "S. Hughes", "History", 9.25, "Private", "PaaS"),
            Book(10, "Fictional Realms", "L. Storyteller", "Fiction", 7.60, "Public", "SaaS"),
        ]

    def get_books(self):
        return self.books

    def search_books(self, keyword):
        return [b for b in self.books if keyword.lower() in b.title.lower()]

    def buy_book(self, book_id):
        for book in self.books:
            if book.id == book_id:
                self.books.remove(book)
                return book
        return None

store = Bookstore()

# --- Home Page ---
@app.route('/')
def home():
    books = store.get_books()
    messages = get_flashed_messages()
    return render_template_string('''
        <h2>📚 Online Bookstore - Cloud Computing Books</h2>
        <form action="/search">
            <input type="text" name="q" placeholder="Search book...">
            <input type="submit" value="Search">
        </form>
        <h3>Available Books</h3>
        <ul>
        {% for book in books %}
            <li>
                <strong>{{ book.title }}</strong> by {{ book.author }} 
                [Category: {{ book.category }}] - ₹{{ book.price }} 
                <br>Cloud Type: {{ book.cloud_type }} | Cloud Service: {{ book.cloud_service }}
                <form method="POST" action="/buy/{{ book.id }}" style="display:inline">
                    <button type="submit">Buy</button>
                </form>
            </li>
        {% endfor %}
        </ul>

        {% if messages %}
            <p style="color: green;"><strong>{{ messages[0] }}</strong></p>
        {% endif %}
    ''', books=books, messages=messages)

# --- Search ---
@app.route('/search')
def search():
    query = request.args.get('q', '')
    results = store.search_books(query)
    return render_template_string('''
        <h2>🔍 Search Results for "{{ query }}"</h2>
        <a href="/">Back to All Books</a>
        <ul>
        {% for book in books %}
            <li>
                <strong>{{ book.title }}</strong> by {{ book.author }} 
                [Category: {{ book.category }}] - ₹{{ book.price }}
                <br>Cloud Type: {{ book.cloud_type }} | Cloud Service: {{ book.cloud_service }}
                <form method="POST" action="/buy/{{ book.id }}" style="display:inline">
                    <button type="submit">Buy</button>
                </form>
            </li>
        {% else %}
            <li>No books found.</li>
        {% endfor %}
        </ul>
        {% if messages %}
            <p style="color: green;"><strong>{{ messages[0] }}</strong></p>
        {% endif %}
    ''', books=results, query=query, messages=get_flashed_messages())

# --- Buy Book ---
@app.route('/buy/<int:book_id>', methods=['POST'])
def buy(book_id):
    book = store.buy_book(book_id)
    if book:
        flash(f"✅ Successfully bought '{book.title}' for ₹{book.price:.2f}. The book is hosted on a {book.cloud_type} cloud using {book.cloud_service}.")
    else:
        flash("❌ Book not found or already sold.")
    return redirect(url_for('home'))

# --- Run App ---
if __name__ == "__main__":
    app.run(debug=True, port=5001)

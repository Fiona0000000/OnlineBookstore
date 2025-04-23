from flask import Flask, request, render_template_string, redirect, url_for, flash, get_flashed_messages

app = Flask(__name__)
app.secret_key = "mysecretkey123"  # Required for flashing messages

# --- Book Class ---
class Book:
    def __init__(self, id, title, author, category, price, restricted=False):
        self.id = id
        self.title = title
        self.author = author
        self.category = category
        self.price = price
        self.restricted = restricted  # New attribute to mark restricted books

# --- Bookstore ---
class Bookstore:
    def __init__(self):
        self.books = [
            Book(1, "Cloud Computing Basics", "Thomas Erl", "Hybrid Cloud", 12.99),
            Book(2, "Mastering Hybrid Cloud", "Jane Doe", "Hybrid Cloud", 15.49),
            Book(3, "Understanding IaaS", "John Smith", "IaaS", 9.99),
            Book(4, "Platform as a Service (PaaS)", "Mary Lane", "PaaS", 11.99),
            Book(5, "SaaS Explained", "Luke Allen", "SaaS", 10.99),
            Book(6, "Virtualization Concepts", "Rick Moore", "Virtualization", 13.50),
            Book(7, "Advanced Cloud Architectures", "A. Kumar", "Hybrid Cloud", 18.00, restricted=True),  # Restricted book
            Book(8, "Economic Systems", "Adam Smith", "Economics", 8.75),
            Book(9, "World History", "S. Hughes", "History", 9.25),
            Book(10, "Fictional Realms", "L. Storyteller", "Fiction", 7.60),
        ]

    def get_books(self, include_restricted=False):
        # Optionally filter out restricted books based on include_restricted flag
        if include_restricted:
            return self.books
        return [b for b in self.books if not b.restricted]

    def search_books(self, keyword, include_restricted=False):
        return [b for b in self.books if keyword.lower() in b.title.lower() and (include_restricted or not b.restricted)]

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
        <h2>📚 Online Bookstore - Cloud & Virtualization Topics</h2>
        <form action="/search">
            <input type="text" name="q" placeholder="Search book...">
            <input type="submit" value="Search">
        </form>
        <ul>
        {% for book in books %}
            <li>
                <strong>{{ book.title }}</strong> by {{ book.author }} 
                [{{ book.category }}] - ₹{{ book.price }}
                {% if book.restricted %}
                    <span style="color: red;">(Restricted)</span>
                {% endif %}
                <form method="POST" action="/buy/{{ book.id }}" style="display:inline">
                    <button type="submit" {% if book.restricted %}disabled{% endif %}>Buy</button>
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
                [{{ book.category }}] - ₹{{ book.price }}
                {% if book.restricted %}
                    <span style="color: red;">(Restricted)</span>
                {% endif %}
                <form method="POST" action="/buy/{{ book.id }}" style="display:inline">
                    <button type="submit" {% if book.restricted %}disabled{% endif %}>Buy</button>
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
        flash(f"✅ Successfully bought '{book.title}' for ₹{book.price:.2f}")
    else:
        flash("❌ Book not found or already sold.")
    return redirect(url_for('home'))

# --- Run App ---
if __name__ == "__main__":
    app.run(debug=True, port=5001)

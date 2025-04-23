from flask import Flask, request, render_template_string, redirect, url_for, flash, get_flashed_messages

app = Flask(__name__)
app.secret_key = "mysecretkey123"

class Book:
    def __init__(self, id, title, author, category, price, cloud_type, cloud_service):
        self.id = id
        self.title = title
        self.author = author
        self.category = category
        self.price = price
        self.cloud_type = cloud_type
        self.cloud_service = cloud_service

class Bookstore:
    def __init__(self):
        self.books = [
            # Hybrid Cloud
            Book(1, "Hybrid Cloud Essentials", "Jane Doe", "Hybrid Cloud", 12.99, "Hybrid", "PaaS"),
            Book(2, "Mastering Hybrid Cloud", "J. K. Smith", "Hybrid Cloud", 15.49, "Hybrid", "SaaS"),
            Book(3, "Hybrid Deployment Models", "Mike Brown", "Hybrid Cloud", 14.99, "Hybrid", "IaaS"),
            Book(4, "Hybrid Solutions for Enterprises", "Lisa Ray", "Hybrid Cloud", 18.25, "Hybrid", "PaaS"),
            Book(5, "Architecting Hybrid Systems", "Alex Green", "Hybrid Cloud", 19.00, "Hybrid", "SaaS"),

            # IaaS
            Book(6, "Understanding IaaS", "John Smith", "IaaS", 9.99, "Public", "IaaS"),
            Book(7, "IaaS Cloud Platforms", "Sara Palmer", "IaaS", 11.49, "Private", "IaaS"),
            Book(8, "Deploying with IaaS", "Tom Cruise", "IaaS", 13.29, "Public", "IaaS"),
            Book(9, "IaaS for Beginners", "Anil Kumar", "IaaS", 12.00, "Hybrid", "IaaS"),
            Book(10, "Building IaaS Infrastructure", "Nora Jones", "IaaS", 14.90, "Public", "IaaS"),

            # PaaS
            Book(11, "Platform as a Service", "Mary Lane", "PaaS", 11.99, "Private", "PaaS"),
            Book(12, "PaaS for Developers", "Eli Grant", "PaaS", 10.99, "Public", "PaaS"),
            Book(13, "Using PaaS Effectively", "Ali Walker", "PaaS", 13.00, "Private", "PaaS"),
            Book(14, "Modern PaaS Architecture", "Sophie Tran", "PaaS", 15.99, "Hybrid", "PaaS"),
            Book(15, "Enterprise PaaS Solutions", "Carlos Lee", "PaaS", 14.25, "Hybrid", "PaaS"),

            # SaaS
            Book(16, "SaaS Explained", "Luke Allen", "SaaS", 10.99, "Public", "SaaS"),
            Book(17, "Developing SaaS Apps", "Rita Fox", "SaaS", 12.50, "Private", "SaaS"),
            Book(18, "SaaS Startups Guide", "Ken Adams", "SaaS", 11.75, "Hybrid", "SaaS"),
            Book(19, "Building SaaS Products", "Olivia King", "SaaS", 13.90, "Public", "SaaS"),
            Book(20, "Secure SaaS Systems", "Dean White", "SaaS", 15.00, "Private", "SaaS"),

            # Virtualization
            Book(21, "Virtualization Concepts", "Rick Moore", "Virtualization", 13.50, "Private", "IaaS"),
            Book(22, "Advanced Virtual Machines", "Linda Shaw", "Virtualization", 14.00, "Hybrid", "IaaS"),
            Book(23, "VMWare Essentials", "Oscar Zane", "Virtualization", 12.25, "Public", "IaaS"),
            Book(24, "Virtualization in Cloud", "Clara Finn", "Virtualization", 15.40, "Private", "IaaS"),
            Book(25, "Modern Virtual Systems", "Raj Patel", "Virtualization", 16.10, "Public", "IaaS"),
        ]

    def get_books_by_category(self):
        categories = {}
        for book in self.books:
            categories.setdefault(book.category, []).append(book)
        return categories

    def search_books(self, keyword):
        return [b for b in self.books if keyword.lower() in b.title.lower()]

    def buy_book(self, book_id):
        for book in self.books:
            if book.id == book_id:
                self.books.remove(book)
                return book
        return None

store = Bookstore()

@app.route('/')
def home():
    book_groups = store.get_books_by_category()
    messages = get_flashed_messages()
    return render_template_string('''
        <h2>📚 Online Bookstore - Cloud Computing Books</h2>
        <form action="/search">
            <input type="text" name="q" placeholder="Search book...">
            <input type="submit" value="Search">
        </form>

        {% if messages %}
            <p style="color: green;"><strong>{{ messages[0] }}</strong></p>
        {% endif %}

        {% for category, books in book_groups.items() %}
            <h3>{{ category }}</h3>
            <ul>
            {% for book in books %}
                <li>
                    <strong>{{ book.title }}</strong> by {{ book.author }} - ₹{{ book.price }}<br>
                    Cloud Type: {{ book.cloud_type }} | Cloud Service: {{ book.cloud_service }}
                    <form method="POST" action="{{ url_for('buy', book_id=book.id) }}">
                        <button type="submit">Buy</button>
                    </form>
                </li>
            {% endfor %}
            </ul>
        {% endfor %}
    ''', book_groups=book_groups, messages=messages)

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
                <strong>{{ book.title }}</strong> by {{ book.author }} - ₹{{ book.price }}
                <br>Cloud Type: {{ book.cloud_type }} | Cloud Service: {{ book.cloud_service }}
                <form method="POST" action="{{ url_for('buy', book_id=book.id) }}?from=search&q={{ query }}">
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

@app.route('/buy/<int:book_id>', methods=['POST'])
def buy(book_id):
    book = store.buy_book(book_id)
    if book:
        flash(f"✅ Successfully bought '{book.title}' for ₹{book.price:.2f}. Hosted on {book.cloud_type} using {book.cloud_service}.")
    else:
        flash("❌ Book not found or already sold.")

    if request.args.get('from') == 'search':
        return redirect(url_for('search', q=request.args.get('q', '')))
    return redirect(url_for('home'))

if __name__ == "__main__":
    app.run(debug=True, port=5001)

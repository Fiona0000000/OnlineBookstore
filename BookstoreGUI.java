import javax.swing.*;
import javax.swing.table.DefaultTableModel;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.util.ArrayList;
import java.util.List;
import java.util.Random;

public class BookstoreGUI {
    private List<Book> books = new ArrayList<>();
    private JFrame frame;
    private JTable bookTable;
    private DefaultTableModel tableModel;
    private JTextField bookIdField;
    
    public BookstoreGUI() {
        initializeBooks();
        createGUI();
    }

    private void initializeBooks() {
        books.add(new Book(1, "The Great Gatsby", "F. Scott Fitzgerald", "Fiction", 15.99));
        books.add(new Book(2, "To Kill a Mockingbird", "Harper Lee", "Fiction", 12.99));
        books.add(new Book(3, "1984", "George Orwell", "Dystopian", 14.99));
        books.add(new Book(4, "Pride and Prejudice", "Jane Austen", "Romance", 10.99));
        books.add(new Book(5, "The Da Vinci Code", "Dan Brown", "Thriller", 19.99));
        books.add(new Book(6, "The Hobbit", "J.R.R. Tolkien", "Fantasy", 25.99));
        books.add(new Book(7, "Moby Dick", "Herman Melville", "Adventure", 18.50));
        books.add(new Book(8, "War and Peace", "Leo Tolstoy", "History", 20.99));
        books.add(new Book(9, "Dracula", "Bram Stoker", "Horror", 16.99));
        books.add(new Book(10, "Dune", "Frank Herbert", "Sci-Fi", 22.99));

        for (int i = 11; i <= 200; i++) {
            books.add(new Book(i, "Book Title " + i, "Author " + i, getRandomGenre(), 10 + (i % 10) * 2.5));
        }
    }

    private String getRandomGenre() {
        String[] genres = {"Fiction", "History", "Drama", "Thriller", "Sci-Fi", "Fantasy", "Romance", "Horror", "Adventure", "Mystery"};
        return genres[new Random().nextInt(genres.length)];
    }

    private void createGUI() {
        frame = new JFrame("Online Bookstore");
        frame.setSize(800, 500);
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        frame.setLayout(new BorderLayout());

        // Table
        String[] columnNames = {"ID", "Title", "Author", "Genre", "Price (Rs.)"};
        tableModel = new DefaultTableModel(columnNames, 0);
        bookTable = new JTable(tableModel);
        loadBooksIntoTable();
        JScrollPane scrollPane = new JScrollPane(bookTable);
        
        // Purchase Panel
        JPanel purchasePanel = new JPanel();
        purchasePanel.setLayout(new FlowLayout());

        JLabel enterIdLabel = new JLabel("Enter Book ID to Purchase: ");
        bookIdField = new JTextField(5);
        JButton buyButton = new JButton("Buy Book");

        purchasePanel.add(enterIdLabel);
        purchasePanel.add(bookIdField);
        purchasePanel.add(buyButton);

        buyButton.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                buyBook();
            }
        });

        // Add components to frame
        frame.add(scrollPane, BorderLayout.CENTER);
        frame.add(purchasePanel, BorderLayout.SOUTH);

        frame.setVisible(true);
    }

    private void loadBooksIntoTable() {
        for (Book book : books) {
            tableModel.addRow(new Object[]{book.getId(), book.getTitle(), book.getAuthor(), book.getGenre(), book.getPrice()});
        }
    }

    private void buyBook() {
        try {
            int bookId = Integer.parseInt(bookIdField.getText());
            for (Book book : books) {
                if (book.getId() == bookId) {
                    JOptionPane.showMessageDialog(frame, "✅ You purchased: " + book.getTitle(), "Purchase Successful", JOptionPane.INFORMATION_MESSAGE);
                    return;
                }
            }
            JOptionPane.showMessageDialog(frame, "❌ Book not found!", "Error", JOptionPane.ERROR_MESSAGE);
        } catch (NumberFormatException e) {
            JOptionPane.showMessageDialog(frame, "❌ Please enter a valid book ID!", "Error", JOptionPane.ERROR_MESSAGE);
        }
    }

    public static void main(String[] args) {
        SwingUtilities.invokeLater(() -> new BookstoreGUI());
    }
}

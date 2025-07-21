-- Administrator table
CREATE TABLE Administrator (
    admin_id INTEGER NOT NULL AUTO_INCREMENT,
    admin_name VARCHAR(50),
    admin_account VARCHAR(20),
    admin_password VARCHAR(255),
    gender VARCHAR(2),
    phone VARCHAR(11),
    PRIMARY KEY (admin_id)
);

-- Book table
CREATE TABLE Book (
    book_id INTEGER NOT NULL AUTO_INCREMENT,
    book_name VARCHAR(50),
    author VARCHAR(50),
    category VARCHAR(50),
    press VARCHAR(50),
    introduction TEXT,
    stars INTEGER,
    number INTEGER,
    cover VARCHAR(255),
    PRIMARY KEY (book_id)
);

-- Borrow table
CREATE TABLE Borrow (
    id INTEGER NOT NULL AUTO_INCREMENT,
    user_id INTEGER,
    user_name VARCHAR(50),
    book_id INTEGER,
    book_name VARCHAR(50),
    borrow_date DATE,
    expired_date DATE,
    is_agree INTEGER,
    is_return BOOLEAN,
    PRIMARY KEY (id)
);

-- Comment table
CREATE TABLE Comment (
    id INTEGER NOT NULL AUTO_INCREMENT,
    user_id INTEGER,
    user_name VARCHAR(50),
    book_id INTEGER,
    content TEXT,
    comment_date DATE,
    PRIMARY KEY (id)
);

-- ULibrary table
CREATE TABLE ULibrary (
    id INTEGER NOT NULL AUTO_INCREMENT,
    user_id INTEGER,
    book_name VARCHAR(50),
    author VARCHAR(50),
    category VARCHAR(50),
    press VARCHAR(50),
    introduction TEXT,
    PRIMARY KEY (id)
);

-- UBorrow table
CREATE TABLE UBorrow (
    id INTEGER NOT NULL AUTO_INCREMENT,
    borrower_id INTEGER,
    lender_id INTEGER,
    book_id INTEGER,
    book_name VARCHAR(50),
    borrow_date DATE,
    is_agree INTEGER,
    is_return BOOLEAN,
    PRIMARY KEY (id)
);

-- User table
CREATE TABLE User (
    user_id INTEGER NOT NULL AUTO_INCREMENT,
    user_account VARCHAR(20),
    user_name VARCHAR(50),
    user_password VARCHAR(255),
    gender VARCHAR(2),
    phone VARCHAR(11),
    email VARCHAR(20),
    profile TEXT,
    cover VARCHAR(255),
    PRIMARY KEY (user_id)
);

-- Announcement table
CREATE TABLE Announcement (
    id INTEGER NOT NULL AUTO_INCREMENT,
    title VARCHAR(80),
    content TEXT,
    publish_time DATETIME,
    PRIMARY KEY (id)
);

-- Consult table
CREATE TABLE Consult (
    id INTEGER NOT NULL AUTO_INCREMENT,
    user_id INTEGER,
    user_name VARCHAR(50),
    title VARCHAR(80),
    content TEXT,
    consult_time DATETIME,
    PRIMARY KEY (id)
);

-- Administrator
INSERT INTO Administrator (admin_name, admin_account, admin_password, gender, phone) VALUES
('Admin One', 'admin1', 'hashed_password_1', 'M', '13800138001'),
('Admin Two', 'admin2', 'hashed_password_2', 'F', '13800138002'),
('Admin Three', 'admin3', 'hashed_password_3', 'M', '13800138003');

-- User
INSERT INTO User (user_account, user_name, user_password, gender, phone, email, profile, cover) VALUES
('user1', 'Zhang San', 'user_pass_1', 'M', '13900139001', 'zs@example.com', 'Book lover', 'cover1.jpg'),
('user2', 'Li Si', 'user_pass_2', 'F', '13900139002', 'ls@example.com', 'Sci-fi fan', 'cover2.jpg'),
('user3', 'Wang Wu', 'user_pass_3', 'M', '13900139003', 'ww@example.com', 'History buff', 'cover3.jpg'),
('user4', 'Zhao Liu', 'user_pass_4', 'F', '13900139004', 'zl@example.com', 'Romance reader', 'cover4.jpg');

-- Book
INSERT INTO Book (book_name, author, category, press, introduction, stars, number, cover) VALUES
('The Great Gatsby', 'F. Scott Fitzgerald', 'Classic', 'Scribner', 'A story of wealth and love in the 1920s', 5, 10, 'gatsby.jpg'),
('To Kill a Mockingbird', 'Harper Lee', 'Fiction', 'J. B. Lippincott', 'A story of racial injustice in the American South', 4, 8, 'mockingbird.jpg'),
('1984', 'George Orwell', 'Dystopian', 'Secker & Warburg', 'A dystopian novel about totalitarianism', 5, 12, '1984.jpg'),
('Pride and Prejudice', 'Jane Austen', 'Romance', 'T. Egerton', 'A romantic novel of manners', 4, 15, 'pride.jpg'),
('The Hobbit', 'J.R.R. Tolkien', 'Fantasy', 'Allen & Unwin', 'A fantasy adventure novel', 5, 7, 'hobbit.jpg');

-- Borrow
INSERT INTO Borrow (user_id, user_name, book_id, book_name, borrow_date, expired_date, is_agree, is_return) VALUES
(1, 'Zhang San', 1, 'The Great Gatsby', '2023-01-10', '2023-02-10', 1, 1),
(2, 'Li Si', 3, '1984', '2023-02-15', '2023-03-15', 1, 0),
(3, 'Wang Wu', 2, 'To Kill a Mockingbird', '2023-03-01', '2023-04-01', 1, 1),
(1, 'Zhang San', 4, 'Pride and Prejudice', '2023-03-20', '2023-04-20', 0, 0);

-- Comment
INSERT INTO Comment (user_id, user_name, book_id, content, comment_date) VALUES
(1, 'Zhang San', 1, 'A timeless classic that everyone should read!', '2023-01-25'),
(2, 'Li Si', 3, 'Disturbingly relevant even today.', '2023-02-20'),
(3, 'Wang Wu', 2, 'Powerful story with important lessons.', '2023-03-10'),
(4, 'Zhao Liu', 4, 'The romance is beautifully written.', '2023-03-25');

-- ULibrary
INSERT INTO ULibrary (user_id, book_name, author, category, press, introduction) VALUES
(1, 'The Catcher in the Rye', 'J.D. Salinger', 'Fiction', 'Little, Brown', 'Story of teenage alienation'),
(2, 'Brave New World', 'Aldous Huxley', 'Dystopian', 'Chatto & Windus', 'Future society novel'),
(3, 'The Lord of the Rings', 'J.R.R. Tolkien', 'Fantasy', 'Allen & Unwin', 'Epic fantasy trilogy'),
(4, 'Jane Eyre', 'Charlotte Brontë', 'Romance', 'Smith, Elder & Co.', 'Gothic romance novel');

-- UBorrow
INSERT INTO UBorrow (borrower_id, lender_id, book_id, book_name, borrow_date, is_agree, is_return) VALUES
(1, 2, 1, 'The Catcher in the Rye', '2023-01-15', 1, 1),
(3, 4, 3, 'Jane Eyre', '2023-02-10', 1, 0),
(2, 1, 2, 'Brave New World', '2023-03-05', 0, 0),
(4, 3, 4, 'The Lord of the Rings', '2023-03-20', 1, 1);

-- Announcement
INSERT INTO Announcement (title, content, publish_time) VALUES
('Library Hours Update', 'The library will open at 9am instead of 8am next week.', '2023-01-05 10:00:00'),
('New Book Arrivals', 'Check out our new collection of science fiction books!', '2023-02-15 14:30:00'),
('Maintenance Notice', 'The library system will be down for maintenance on March 1st.', '2023-02-28 09:15:00');

-- Consult
INSERT INTO Consult (user_id, user_name, title, content, consult_time) VALUES
(1, 'Zhang San', 'Book Recommendation', 'Can you recommend books similar to The Great Gatsby?', '2023-01-12 11:20:00'),
(2, 'Li Si', 'Late Return', 'I need to extend my borrowing period for 1984.', '2023-02-18 15:45:00'),
(3, 'Wang Wu', 'Membership', 'How can I renew my library membership?', '2023-03-05 10:10:00');

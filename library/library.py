import random
import string
import datetime
import json
import os

class User:
    def __init__(self, user_id, name, email, phone, password, register_time):
        self.user_id = user_id
        self.name = name
        self.email = email
        self.phone = phone
        self.password = password
        self.register_time = register_time
        self.is_admin = False

class Book:
    def __init__(self, isbn, title, author, add_time):
        self.isbn = isbn
        self.title = title
        self.author = author
        self.add_time = add_time
        self.is_available = True
        self.issue_history = []
    
    def display(self):
        status = "✅ Available" if self.is_available else "❌ Issued"
        return f"📚 {self.title} by {self.author} | ID: {self.isbn} | {status}"

class Library:
    def __init__(self):
        self.users = self.load_users()
        self.books = []
    
    def generate_random_id(self, length=8):
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))
    
    def register_user(self):
        print("\n" + "="*60)
        print("👤 NEW USER REGISTRATION")
        print("="*60)
        name = input("👤 Full Name: ")
        email = input("📧 Email: ")
        phone = input("📱 Phone (+91): ")
        password = input("🔒 Password: ")
        
        if len(phone) != 10 or not phone.isdigit():
            print("❌ Phone must be 10 digits!")
            return None
        
        if any(u.email == email for u in self.users):
            print("❌ Email already registered!")
            return None
        
        user_id = self.generate_random_id()
        register_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        user = User(user_id, name, email, phone, password, register_time)
        self.users.append(user)
        self.save_users()
        
        print(f"\n✅ REGISTERED SUCCESSFULLY!")
        print(f"🆔 ID: {user_id}")
        print(f"📱 Phone: +91{phone}")
        return user
    
    def login_user(self):
        print("\n" + "="*60)
        print("🔐 LOGIN")
        print("="*60)
        identifier = input("📧/📱 Email or Phone: ")
        password = input("🔒 Password: ")
        
        for user in self.users:
            if (user.email == identifier or user.phone == identifier) and user.password == password:
                print(f"\n✅ Welcome {user.name}!")
                print(f"🆔 ID: {user.user_id}")
                return user
        print("❌ Wrong credentials!")
        return None
    
    def add_book(self, title, author):
        isbn = self.generate_random_id(6)
        add_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        book = Book(isbn, title, author, add_time)
        self.books.append(book)
    
    def save_users(self):
        data = [{"id": u.user_id, "name": u.name, "email": u.email, "phone": u.phone,
                "reg_time": u.register_time} for u in self.users]
        try:
            with open("users.json", "w") as f:
                json.dump(data, f, indent=2)
        except:
            pass
    
    def load_users(self):
        try:
            if os.path.exists("users.json"):
                with open("users.json", "r") as f:
                    data = json.load(f)
                    return [User(d["id"], d["name"], d["email"], d["phone"], "", d["reg_time"]) for d in data]
        except:
            pass
        return []

def main_menu():
    lib = Library()
    
    
    sample_books = [
        ("Python Crash Course", "Eric Matthes"),
        ("Clean Code", "Robert Martin"),
        ("Head First Java", "Kathy Sierra")
    ]
    for title, author in sample_books:
        lib.add_book(title, author)
    
    while True:
        print("\n" + "="*70)
        print("🏛️  LIBRARY MANAGEMENT SYSTEM")
        print("="*70)
        print("🔐 1. Login")
        print("➕ 2. Register")
        print("❌ 3. Exit")
        print("="*70)
        
        choice = input("Enter choice (1-3): ").strip()
        
        if choice == '1':
            user = lib.login_user()
            if user:
                member_menu(lib, user)
                
        elif choice == '2':
            user = lib.register_user()
            if user:
                print("\n🎉 Use your ID to login next time!")
                
        elif choice == '3':
            print("👋 Thank you!")
            break
            
        else:
            print("❌ Enter 1, 2 or 3 only!")

def member_menu(lib, user):
    while True:
        print(f"\n👋 Welcome {user.name}")
        print(f"🆔 ID: {user.user_id} | 📱 +91{user.phone}")
        print("="*70)
        print("📚 1. View All Books")
        print("🔍 2. Search Books")
        print("➕ 3. Add Book")
        print("📖 4. Issue Book")
        print("🔄 5. Return Book")
        print("👤 6. My Profile")
        print("🚪 7. Logout")
        print("="*70)
        
        choice = input("Enter choice (1-7): ").strip()
        
        if choice == '1':
            print("\n📚 ALL BOOKS:")
            print("-"*50)
            for book in lib.books:
                print(book.display())
                
        elif choice == '2':
            search_term = input("🔍 Search (title/author/ID): ")
            results = []
            for book in lib.books:
                if (search_term.lower() in book.title.lower() or 
                    search_term.lower() in book.author.lower() or
                    search_term in book.isbn):
                    results.append(book)
            
            if results:
                print("\n✅ Found:")
                for book in results:
                    print(book.display())
            else:
                print("❌ No books found!")
                
        elif choice == '3':
            title = input("📖 Book title: ")
            author = input("✍️ Author: ")
            lib.add_book(title, author)
            print("✅ Book added!")
            
        elif choice == '4':
            print("\n📚 Available Books:")
            available = [b for b in lib.books if b.is_available]
            for i, book in enumerate(available, 1):
                print(f"{i}. {book.display()}")
            
            if available:
                isbn = input("\nEnter book ID to issue: ")
     
                book = next((b for b in lib.books if b.isbn == isbn), None)
                if book and book.is_available:
                    book.is_available = False
                    print(f"✅ {book.title} issued to you!")
                else:
                    print("❌ Book not available!")
            else:
                print("No books available!")
                
        elif choice == '5':
            print("🔄 Return feature - Enter book ID")
            
        elif choice == '6':
            print(f"\n👤 {user.name}")
            print(f"📧 {user.email}")
            print(f"📱 +91{user.phone}")
            print(f"🆔 {user.user_id}")
            print(f"⏰ Registered: {user.register_time}")
            
        elif choice == '7':
            print("👋 Logged out!")
            break
            
        else:
            print("❌ Invalid choice!")

main_menu()

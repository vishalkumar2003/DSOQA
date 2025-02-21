import pymysql

class BTreeNode:
    def __init__(self, leaf=False):
        self.leaf = leaf
        self.keys = []
        self.children = []

class BTree:
    def __init__(self, t):
        self.root = BTreeNode(leaf=True)  # Start with an empty leaf node
        self.t = t  # Minimum degree (defines branching factor)

    def search(self, node, key):
        """Search for a key in the B-Tree"""
        i = 0
        while i < len(node.keys) and key > node.keys[i]:
            i += 1

        if i < len(node.keys) and node.keys[i] == key:
            return True  # Key found

        if node.leaf:
            return False  # Key not found
        
        return self.search(node.children[i], key)

    def insert(self, key):
        """Insert a key into the B-Tree"""
        root = self.root
        if len(root.keys) == (2 * self.t) - 1:  # If root is full, split
            new_root = BTreeNode(leaf=False)
            new_root.children.append(self.root)
            self.root = new_root
            self._split_child(new_root, 0)
        
        self._insert_non_full(self.root, key)

    def _insert_non_full(self, node, key):
        """Insert a key into a non-full node"""
        if node.leaf:
            node.keys.append(key)
            node.keys.sort()
        else:
            i = len(node.keys) - 1
            while i >= 0 and key < node.keys[i]:
                i -= 1
            i += 1
            if len(node.children[i].keys) == (2 * self.t) - 1:
                self._split_child(node, i)
                if key > node.keys[i]:
                    i += 1
            self._insert_non_full(node.children[i], key)

    def _split_child(self, parent, index):
        """Split a child node"""
        t = self.t
        child = parent.children[index]
        new_child = BTreeNode(leaf=child.leaf)
        mid = t - 1

        parent.keys.insert(index, child.keys[mid])
        parent.children.insert(index + 1, new_child)

        new_child.keys = child.keys[mid + 1:]
        child.keys = child.keys[:mid]

        if not child.leaf:
            new_child.children = child.children[mid + 1:]
            child.children = child.children[:mid + 1]

# Connect to MySQL
conn = pymysql.connect(
    host="localhost",
    user="root",
    password="Viskav@2003",
    database="email",
    cursorclass=pymysql.cursors.DictCursor
)

cursor = conn.cursor()

# Fetch all emails from the database
cursor.execute("SELECT email FROM users ORDER BY email")  # Ensure emails are ordered
emails = [row["email"] for row in cursor.fetchall()]

# Close the connection
cursor.close()
conn.close()

# Create a B-Tree and insert emails
btree = BTree(t=3)  # Set minimum degree (t=3 for simplicity)
for email in emails:
    btree.insert(email)

# 🔹 SEARCH FOR AN EMAIL
email_to_search = "viskav2003@gmail.com"  # Replace with the email to search
if btree.search(btree.root, email_to_search):
    print(f"{email_to_search} found in the database!")
else:
    print(f"{email_to_search} NOT found in the database.")

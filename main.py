import sys
import string
import random

# helper for book title/author generation
def randomString(size=6, chars=string.ascii_uppercase):
    return ''.join(random.choice(chars) for _ in range(size))

class Book:
    def __init__(self, author, title):
        self.title = title
        self.author = author

    def shelf(self, shelf, slot=None):
        self.slot = shelf.addBook(self, slot)
        self.shelf = shelf
        self.printMe('added')

    def unshelf(self):
        self.shelf.removeBook(self)
        self.printMe('removed')
        self.shelf = None
        self.slot = None
        return self

    def printMe(self, action):
        print 'Book: ' + self.title + ' ' + action + ' from shelf ' + \
            str(self.shelf.getShelfNum()) + ', slot ' + str(self.slot)

class Shelf:

    slots = 10

    def __init__(self, library):
        self.library = library
        self.books = {}
        self.full = False

    def addBook(self, book, slot=None):
        # add to specific slot
        if slot is not None:
            if slot in self.books and self.books[slot]:
                raise Exception('shelf ' + str(self.getShelfNum()) + ', slot ' + str(slot) + \
                    ' already has book ' + self.books[slot].title)
            self.books[slot] = book
            self.full = self.testFull()
            return slot

        # add to next available slot
        for slot in xrange(0, Shelf.slots):
            if slot not in self.books:
                self.books[slot] = book
                self.full = self.testFull()
                return slot

    def removeBook(self, book):
        if (self.full):
            self.full = False
        return self.books.pop(book.slot, None)

    def getShelfNum(self):
        count = 0
        for shelf in self.library.shelves:
            if shelf == self:
                return count
            count += 1
        return -1

    def report(self, shelfNum):
        sys.stdout.write('SHELF ' + str(shelfNum) + ': ')
        for x in xrange(0, Shelf.slots):
            if x in self.books and self.books[x]:
                sys.stdout.write( ' B ' )
            else:
                sys.stdout.write( ' _ ' )
        print ''

    def testFull(self):
        for slot in xrange(0, Shelf.slots):
            if slot not in self.books:
                return False
        return True

class Library:
    def __init__(self, name):
        self.name = name
        self.shelves = []

    def buildShelves(self, num):
        for x in xrange(0, num):
            self.shelves.append(Shelf(self))

    def getShelfWithFreeSlot(self):
        for x in xrange(0, len(self.shelves)):
            if self.shelves[x].full == False:
                return self.shelves[x]
        return None

    def addBookToNextSlot(self, book):
        if self.getShelfWithFreeSlot():
            return book.shelf(self.getShelfWithFreeSlot())
        raise Exception('no free slots')

    def addBookToSpecificSlot(self, book, shelfNum, slotNum):
        return book.shelf(self.shelves[shelfNum], slotNum)

    def report(self):
        print '## Library\n'
        sys.stdout.write('SLOTS:   ')
        for x in xrange(0, Shelf.slots):
            sys.stdout.write(' ' + str(x) + ' ')
        print ''
        for x in xrange(0, len(self.shelves)):
            self.shelves[x].report(x)
        print ''
        return None


# Create a library of books, and create some shelves to house those books
shelfCount = 8
books = []
lib = Library('Chris\'s Library')
lib.buildShelves(shelfCount)

print 'Welcome to ' + lib.name + '\n'

# add some books sequentially to shelves
for x in xrange(0, 15):
    book = Book(randomString(3), randomString(10))
    books.append(book)
    lib.addBookToNextSlot(book)

# add some books randomly to shelves
for x in xrange(0, 10):
    book = Book(randomString(3), randomString(10))
    books.append(book)
    try:
        lib.addBookToSpecificSlot(book, int(randomString(1, '0123457')), int(randomString(1, '012345789')))
    except Exception as detail:
        print detail

# show me the library!
lib.report()

# remove a book
books[12].unshelf()

# show me the library!
lib.report()

# fill the hole back in
book = Book(randomString(3), randomString(10))
lib.addBookToSpecificSlot(book, 1, 2)

# show me the library!
lib.report()
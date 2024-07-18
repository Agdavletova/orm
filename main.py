import sqlalchemy
import sqlalchemy as sq
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from models import create_tables, Book, Publisher, Sale, Stock, Shop
import datetime



password = "123aisly"
db_name = "test_orm"
db_user = "postgres"

DSN = f"postgresql://{db_user}:{password}@localhost:5432/{db_name}"

engine = sqlalchemy.create_engine(DSN)

create_tables(engine)

# сессия
Session = sessionmaker(bind=engine)
session = Session()
#
# a1 = Publisher(name="Издательство 1")
# session.add(a1)
# session.commit()
#
# b1 = Book(title="Непоседа", id_publisher=a1.id)
# b2 = Book(title="Луки", id_publisher=a1.id)
#
# session.add(b1)
# session.add(b2)
# session.commit()
#
# shop1 = Shop(name="Магазин1")
# shop2 = Shop(name="Магазин2")
# session.add_all([shop1, shop2])
# session.commit()
#
# stock1 = Stock(id_book=b1.id, id_shop=shop1.id, count=600)
# stock2 = Stock(id_book=b1.id, id_shop=shop2.id, count=300)
# stock3 = Stock(id_book=b2.id, id_shop=shop1.id, count=1000)
# session.add_all([stock1, stock2, stock3])
# session.commit()
#
# sale1 = Sale(price=150.25, date_sale=datetime.date(2024,7,10), id_stock=stock1.id, count=100)
# sale2 = Sale(price=150.25, date_sale=datetime.date(2024,5,1), id_stock=stock2.id, count=150)
# sale3 = Sale(price=200, date_sale=datetime.date(2023,2,1), id_stock=stock3.id, count=50)
# session.add_all([sale1, sale2, sale3])
# session.commit()

def get_shops(p):
    q = session.query(Book.title, Shop.name, Sale.price, Sale.date_sale,
).select_from(Shop).join(Stock).join(Book).join(Publisher).join(Sale)
    if p.isdigit():
        publisher = session.query(Publisher).filter(Publisher.id == int(p)).first()
    else:
        publisher = session.query(Publisher).filter(Publisher.name == p).first()

    if publisher:
        for book_title, shop_name, price, date_sale in q.filter(Publisher.id == publisher.id):
            print(f"{book_title: <40} | {shop_name: <10} | {price: <8} | {date_sale.strftime('%d-%m-%Y')}")
    else:
        print("Нет такого издательства")
if __name__ == '__main__':
    pub = input("Введите название или идентификатор издательства: ")
    get_shops(pub)


# session.query(Sale).delete()
# session.query(Stock).delete()
# session.query(Shop).delete()
# session.query(Book).delete()
# session.query(Publisher).delete()
# session.commit()

session.close()
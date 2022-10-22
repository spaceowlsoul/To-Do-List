from datetime import date

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

engine = create_engine('sqlite:///todo.db?check_same_thread=False')


class Task(Base):
    __tablename__ = 'task'

    id = Column(Integer, primary_key=True)
    task = Column(String())
    deadline = Column(Date, default=date.today())

    def __repr__(self):
        return self.task


Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()


def output_tasks():
    rows = session.query(Task).all()
    print('Today:')
    if len(rows) > 0:
        for i in range(len(rows)):
            if rows[i].deadline == date.today():
                print(f'{rows[i].id}. {rows[i].task}')
    else:
        print('Nothing to do!')


def add_task():
    input_task = input('Enter a task\n')
    row_1 = Task(task=input_task)
    session.add(row_1)
    session.commit()
    print('The task has been added!')


def main():
    while True:
        print('''1) Today's tasks\n2) Add a task\n0) Exit''')
        action = int(input())
        print()
        if action == 1:
            output_tasks()
        elif action == 2:
            add_task()
        elif action == 0:
            print('Bye')
            return False
        print()


if __name__ == "__main__":
    main()

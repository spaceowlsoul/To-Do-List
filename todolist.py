from datetime import datetime, timedelta

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import sessionmaker

today = datetime.today()

Base = declarative_base()
engine = create_engine('sqlite:///todo.db?check_same_thread=False')


class Task(Base):
    __tablename__ = 'task'

    id = Column(Integer, primary_key=True)
    task = Column(String())
    deadline = Column(Date, default=today)

    def __repr__(self):
        return self.task, self.id, self.deadline


Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()


def output(rows, f):
    if len(rows) > 0:
        for i in range(len(rows)):
            if f in ['day', 'week']:
                print(f'{rows[i].id}. {rows[i].task}')
            elif f in ['all', 'missed']:
                format_deadline = rows[i].deadline.strftime('%d %b')
                print(f'{rows[i].id}. {rows[i].task}. {format_deadline}')
    else:
        if f in ['day', 'week', 'all']:
            print('Nothing to do!')
        elif f in ['missed']:
            print('All tasks have been completed! ')


def today_tasks():
    output_format = today.strftime('%d %b')
    rows = session.query(Task).filter(Task.deadline == today.date()).all()
    print(f'Today {output_format}:')
    output(rows, 'day')


def week_tasks():
    for i in range(0, 7):
        day = today + timedelta(days=i)
        output_format = day.strftime('%A %d %b')
        rows = session.query(Task).filter(Task.deadline == day.date()).all()
        print(f'\n{output_format}:')
        output(rows, 'week')


def all_tasks():
    rows = session.query(Task).order_by(Task.deadline).all()
    print('All tasks:')
    output(rows, 'all')
        

def missed_tasks():
    rows = session.query(Task).filter(Task.deadline < today.date()).order_by(Task.deadline).all()
    print('Missed tasks:')
    output(rows, 'missed')


def add_task():
    input_task = input('Enter a task\n')
    input_deadline = input(f'Enter a deadline. Example format: {today.date()}\n')
    row_1 = Task(task=input_task, deadline=datetime.strptime(input_deadline, '%Y-%m-%d').date())
    session.add(row_1)
    session.commit()
    print('The task has been added!')


def delete_task():
    all_rows = session.query(Task).order_by(Task.deadline).all()
    print('Choose the number of the task you want to delete:')
    if len(all_rows) > 0:
        output(all_rows, 'all')
        input_task = int(input())
        session.query(Task).filter(Task.id == input_task).delete()
        session.commit()
        print('The task has been deleted!')
    else:
        print('Nothing to delete')


def main():
    actions = {'1': today_tasks, '2': week_tasks, '3': all_tasks, '4': missed_tasks,
               '5': add_task, '6': delete_task}
    action = ''
    while action != '0':
        print("1) Today's tasks\n2) Week's tasks\n3) All tasks")
        print("4) Missed tasks\n5) Add a task\n6) Delete a task\n0) Exit")
        action = input('Choose an option:\n')
        print()
        if action in actions:
            actions[action]()
        elif action == '0':
            print('Bye!\n\nBye!')
        else:
            print('Invalid command!')
        print()


if __name__ == "__main__":
    main()

import sqlite3 as sql
from main.src.toDoList.user import User
from main.src.game.map import GameMap
from main.src.game.map import render_gamestatus, save_gamestatus
from main.src.utils.writer import write_tasks
from main.src.utils.reader import read_tasks


class LoginException(Exception):
    """Raised when there is incorrect login or password entered"""
    pass


class RegistrationException(Exception):
    """Raised when there is incorrect data to register into database"""
    pass


class LoginHandler:
    def __init__(self):
        self.con = sql.connect("../resources/users.db")
        self.cur = self.con.cursor()
        # statement = "SELECT username, password FROM users"
        # self.cur.execute(statement)
        # print(self.cur.fetchall())

    def log(self, login: str, password: str):
        statement = f"SELECT * from users WHERE username='{login}' AND Password = '{password}';"
        self.cur.execute(statement)
        user_data = self.cur.fetchone()
        if not user_data:
            raise LoginException("wrong login or password")
        else:
            blocks = render_gamestatus(user_data[4])
            game = GameMap(theme=user_data[3], blocks=blocks)
            user = User(login, points=user_data[2], game=game)
            read_tasks(user)
            return user

    def register(self, login: str, password: str):
        if login == "":
            raise RegistrationException("try different login")
        elif password == "":
            raise RegistrationException("try different password")
        else:
            try:
                query = "INSERT INTO users (username, password, points, theme, gamestatus) VALUES (?, ?, ?, ?, ?)"
                self.cur.execute(query, (login, password, 0, GameMap().theme, save_gamestatus(GameMap().blocks)))
                self.con.commit()
            except sql.IntegrityError:
                raise RegistrationException("this login is not available")

    def save(self, user: User):
        statement = f"SELECT password from users WHERE username='{user.name}';"
        self.cur.execute(statement)
        password = self.cur.fetchone()[0]
        statement = f"DELETE FROM users WHERE username='{user.name}';"
        self.cur.execute(statement)
        statement = "INSERT INTO users (username, password, points, theme, gamestatus) VALUES (?, ?, ?, ?, ?)"
        self.cur.execute(statement,
                         (user.name, password, user.points, user.game.theme, save_gamestatus(user.game.blocks)))
        self.con.commit()
        write_tasks(user)

    def disconnect(self):
        self.con.commit()
        self.con.close()

import random

from src.models import Film, User, UserAction
from src.settings import settings


class FakeData:

    def __init__(self):
        self.users = [User() for _ in range(settings.user_num)]
        self.films = [Film() for _ in range(settings.films_num)]

    def user_actions(self) -> list:
        data = []

        for user in self.users:
            user_films = random.sample(self.films, settings.user_films)
            for film in user_films:
                data.append(
                    UserAction(
                        user_id=user.id,
                        film_id=film.id,
                        like=random.choices([0, 1], weights=[settings.dislike_prob, settings.like_prob], k=1)[0],
                    ).dict()
                )

        random.shuffle(data)

        return data

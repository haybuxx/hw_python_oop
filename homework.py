from typing import List, ClassVar, Dict


class InfoMessage:
    """Информационное сообщение о тренировке."""
    TRAINING_TYPE = str
    DURATION = float
    DISTANCE = float
    SPEED = float
    CALORIES = float

    def __init__(self, training_type: str, duration:
                 float, distance: float, speed: float, calories: float):
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        return (f'Тип тренировки: {self.training_type};'
                f' Длительность: {self.duration:.3f} ч.;'
                f' Дистанция: {self.distance:.3f} км;'
                f' Ср. скорость: {self.speed:.3f} км/ч;'
                f' Потрачено ккал: {self.calories:.3f}.')


class Training:
    """Базовый класс тренировки."""
    M_IN_KM: int = 1000
    CM_IN_M: int = 100
    MIN_IN_H: int = 60
    LEN_STEP: float = 0.65

    action: int
    duration: float
    weight: float

    def __init__(self, action: float, duration: float, weight: float):
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """Тренировка: спортивная ходьба."""
    #TRAINING_TYPE: ClassVar[str] = 'Бег'
    CALORIES_MEAN_SPEED_MULTIPLIER: ClassVar[float] = 18
    CALORIES_MEAN_SPEED_SHIFT: ClassVar[float] = 1.79

    def get_spent_calories(self) -> float:
        return ((self.CALORIES_MEAN_SPEED_MULTIPLIER
                * self.get_mean_speed()
                + self.CALORIES_MEAN_SPEED_SHIFT
                * self.weight / self.M_IN_KM
                * (self.duration * self.MIN_IN_H)))


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    CALORIES_WEIGHT_MULTIPLIER: ClassVar[float] = 0.035
    CALORIES_SPEED_HEIGHT_MULTIPLIER: ClassVar[float] = 0.029
    KMH_IN_MSEC: ClassVar[float] = 0.278

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: int) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        return (((self.CALORIES_WEIGHT_MULTIPLIER * self.weight
                  + ((self.get_mean_speed()
                      * self.KMH_IN_MSEC) ** 2
                     / (self.height / self.CM_IN_M))
                  * self.CALORIES_SPEED_HEIGHT_MULTIPLIER
                  * self.weight)
                 * self.duration * self.MIN_IN_H))


class Swimming(Training):
    """Тренировка: плавание."""
    TRAINING_TYPE: ClassVar[str] = 'Плавание'
    LEN_STEP: ClassVar[float] = 1.38
    CALORIES_MEAN_SPEED_SHIFT: ClassVar[float] = 1.1
    CALORIES_WEIGHT_MULTIPLIER: ClassVar[float] = 2.0

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 lenght_pool: float,
                 count_pool: float) -> None:
        super().__init__(action, duration, weight)
        self.lenght_pool = lenght_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        return (self.lenght_pool * self.count_pool
                / self.M_IN_KM) / self.duration

    def get_spent_calories(self) -> float:
        return ((self.get_mean_speed()
                 + self.CALORIES_MEAN_SPEED_SHIFT)
                * self.CALORIES_WEIGHT_MULTIPLIER
                * self.weight * self.duration)


def read_package(workout_type: str, data: List[int]) -> Training:
    """Прочитать данные полученные от датчиков."""
    type_of_training: Dict = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }
    if workout_type in type_of_training:
        class_type: Training = type_of_training[workout_type](*data)
        return class_type
    if workout_type not in type_of_training:
        raise ValueError('Сообщение об ошибке.')


def main(training: Training) -> None:
    """Главная функция."""
    info: InfoMessage = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = str = read_package(workout_type, data)
        main(training)

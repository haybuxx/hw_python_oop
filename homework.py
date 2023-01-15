from typing import List, ClassVar, Dict


class InfoMessage:
    """Информационное сообщение о тренировке."""

    def __init__(self, training_type: str, duration:
                 float, distance: float, speed: float, calories: float):
        """
        Инициализация тренировки
        :param training type - тип тренировки
        :param duration - длительность тренировки в часах
        :param distance - пройденное расстояние в километрах
        :param speed - средняя скорость премещения километров в час
        :param calories - потрачено каллорий во время тренировки.
        """
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        """Округление результата тренировки до трех символов после запятой."""
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

    def __init__(self, action: float, duration: float, weight: float):
        """
        Инициализация тренирокви
        :param action - количество действий(гребков или шагов)
        :param duration - длительность в секундах
        :param weight - вес пользователя в киллограммах.
        """
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получаем дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получаем среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получаем количество затраченных калорий."""
        raise NotImplementedError()

    def show_training_info(self) -> InfoMessage:
        """Возращаем информационное сообщение о выполненной тренировке."""
        return InfoMessage(self.__class__.__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """Тренировка: спортивная ходьба."""
    CALORIES_MEAN_SPEED_MULTIPLIER: ClassVar[float] = 18
    CALORIES_MEAN_SPEED_SHIFT: ClassVar[float] = 1.79

    def get_spent_calories(self) -> float:
        """Расчет каллорий ходьбы."""
        return ((self.CALORIES_MEAN_SPEED_MULTIPLIER * self.get_mean_speed()
                + self.CALORIES_MEAN_SPEED_SHIFT) * self.weight / self.M_IN_KM
                * self.duration * self.MIN_IN_H)


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    CALORIES_WEIGHT_MULTIPLIER: ClassVar[float] = 0.035
    CALORIES_SPEED_HEIGHT_MULTIPLIER: ClassVar[float] = 0.029
    KMH_IN_MSEC: ClassVar[float] = 0.278

    def __init__(self, action: int, duration: float,
                 weight: float, height: int) -> None:
        """
        Инициализация тренировки спортивная ходьба.

        :param action - количество шагов
        :param duration - длительность в секундах
        :param weight - вес пользователя в киллограммах.

        Добавлен новый параметр
        :param height - рост пользователя в сантиметрах.
        """
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        """Расчет каллорий спорт ходьбы."""
        return (((self.CALORIES_WEIGHT_MULTIPLIER * self.weight
                  + ((self.get_mean_speed()
                      * self.KMH_IN_MSEC) ** 2
                     / (self.height / self.CM_IN_M))
                  * self.CALORIES_SPEED_HEIGHT_MULTIPLIER
                  * self.weight)
                 * self.duration * self.MIN_IN_H))


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: ClassVar[float] = 1.38
    CALORIES_MEAN_SPEED_SHIFT: ClassVar[float] = 1.1
    CALORIES_WEIGHT_MULTIPLIER: ClassVar[float] = 2.0

    def __init__(self, action: int, duration: float, weight: float,
                 length_pool: float, count_pool: float) -> None:
        """
        Инициализация тренировки плавание.

        :param action - количество гребков
        :param duration - длительность в секундах
        :param weight - вес пользователя в киллограммах.

        Добавлены два новых параметра
        :param length_pool - длина бассейна в метрах
        :param count_pool - сколько раз пользователь переплыл бассейн.
        """
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        """Расчет ср скорости плавания."""
        return (self.length_pool * self.count_pool
                / self.M_IN_KM) / self.duration

    def get_spent_calories(self) -> float:
        """Расчет каллорий плавания."""
        return ((self.get_mean_speed()
                 + self.CALORIES_MEAN_SPEED_SHIFT)
                * self.CALORIES_WEIGHT_MULTIPLIER
                * self.weight * self.duration)


def read_package(workout_type: str, data: List[int]) -> Training:
    """Прочитываем данные полученные от датчиков."""
    type_of_training: Dict[str: type[Training]] = {'SWM': Swimming,
                                                   'RUN': Running,
                                                   'WLK': SportsWalking}
    if workout_type in type_of_training:
        return type_of_training[workout_type](*data)
    else:
        raise ValueError('Сообщение об ошибке.')


def main(training: Training) -> None:
    """Главная функция."""
    info: InfoMessage = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    """Данные датчиков."""
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        """"Перебор всех функций."""
        training = str = read_package(workout_type, data)
        main(training)

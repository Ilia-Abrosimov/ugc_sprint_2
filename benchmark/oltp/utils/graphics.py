import matplotlib.pyplot as plt

x = [100, 500, 1000, 5000, 8000, 10000]
kafka_writing = [585.02, 1926.82, 4009.43, 8096.79, 8425.81, 8296.34]
kafka_reading = [72.83, 397.06, 745.32, 3550.52, 6312.91, 7370.55]
kafka_writing_reading = [41.7, 411.89, 786.78, 2731.58, 2000.60, 2460.88]
es_writing = [52.43, 47.18, 47.00, 47.54, 45.42, 43.81]
es_writing_100 = [52.43 * 100, 47.18 * 100, 47.00 * 100, 47.54 * 100, 45.42 * 100, 43.81 * 100]
es_reading = [3076.11, 3096.85, 3156.32, 3880.36, 3835.96, 3784.08]
es_writing_reading = [30.55 * 10, 37.82 * 10, 37.11 * 10, 37.94 * 10, 39.09 * 10, 38.25 * 10]


def draw_plot(title: str, data1: list, data2: list, legend: list, filename: str) -> None:
    plt.subplot()
    plt.plot(x, data1)
    plt.plot(x, data2)
    plt.title(title)
    plt.xlabel('Msgs')
    plt.ylabel('Msgs/s')
    plt.legend(legend)
    plt.savefig(filename)
    plt.show()


if __name__ == '__main__':
    draw_plot(
        title='Kafka vs EventStore (writing)',
        data1=kafka_writing,
        data2=es_writing_100,
        legend=['Kafka', 'EventStore (*10^2)'],
        filename='../media/writing.png',
    )
    draw_plot(
        title='Kafka vs EventStore (reading)',
        data1=kafka_reading,
        data2=es_reading,
        legend=['Kafka', 'EventStore'],
        filename='../media/reading.png',
    )
    draw_plot(
        title='Kafka vs EventStore (writing/reading)',
        data1=kafka_writing_reading,
        data2=es_writing_reading,
        legend=['Kafka', 'EventStore (*10)'],
        filename='../media/writing_reading.png',
    )

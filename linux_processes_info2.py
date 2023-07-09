import subprocess
from datetime import datetime

# Выполнение команды 'ps aux' и получение результата
result = subprocess.run(['ps', 'aux'], capture_output=True, text=True)

# Разделение вывода на строки
lines = result.stdout.split('\n')

# Получение текущей даты и времени
current_datetime = datetime.now().strftime('%d-%m-%Y-%H:%M')

# Создание имени файла
filename = f"{current_datetime}-scan.txt"

# Открытие файла для записи отчета
with open(filename, 'w') as file:
    # Парсинг информации о процессах
    processes = []
    for line in lines:
        data = line.split()
        if len(data) >= 11 and data[3] != '%MEM':  # Учитываем только строки с полной информацией о процессе и исключаем строки с заголовками
            username = data[0]
            processes.append(username)

    # Формирование отчета
    report = "Отчёт о состоянии системы:\n"
    report += f"Пользователи системы: {', '.join(set(processes))}\n"
    report += f"Процессов запущено: {len(processes)}\n"

    # Получение информации о пользовательских процессах
    user_processes = {}
    for user in set(processes):
        user_processes[user] = processes.count(user)

    report += "Пользовательских процессов:\n"
    for user, count in user_processes.items():
        report += f"{user}: {count}\n"

    # Нахождение процесса, использующего больше всего памяти и CPU
    memory_highest = ""
    cpu_highest = ""
    highest_memory_usage = 0
    highest_cpu_usage = 0

    for line in lines:
        data = line.split()
        if len(data) >= 11 and data[3] != '%MEM':  # Учитываем только строки с полной информацией о процессе и исключаем строки с заголовками
            try:
                memory_usage = float(data[3])
                cpu_usage = float(data[2])
            except ValueError:
                continue  # Пропускаем строки, которые не могут быть преобразованы в числа

            process_name = ' '.join(data[10:])

            if memory_usage > highest_memory_usage:
                highest_memory_usage = memory_usage
                memory_highest = process_name[:20] if len(process_name) > 20 else process_name

            if cpu_usage > highest_cpu_usage:
                highest_cpu_usage = cpu_usage
                cpu_highest = process_name[:20] if len(process_name) > 20 else process_name

    report += f"Всего памяти используется: {highest_memory_usage:.1f} mb\n"
    report += f"Всего CPU используется: {highest_cpu_usage:.1f}%\n"
    report += f"Больше всего памяти использует: {memory_highest}\n"
    report += f"Больше всего CPU использует: {cpu_highest}\n"

    # Запись отчета в файл
    file.write(report)

# Вывод отчета в консоль
print(report)
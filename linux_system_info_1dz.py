import subprocess
import datetime

def parse_user_processes(processes):
    user_processes = {}
    for process in processes:
        user = process['USER']
        user_processes[user] = user_processes.get(user, 0) + 1
    return user_processes

def parse_memory_usage(processes):
    total_memory = 0
    max_memory_process = None
    max_memory = 0
    for process in processes:
        memory = float(process['%MEM'])
        total_memory += memory
        if memory > max_memory:
            max_memory = memory
            max_memory_process = process
    return total_memory, max_memory_process

def parse_cpu_usage(processes):
    total_cpu = 0
    max_cpu_process = None
    max_cpu = 0
    for process in processes:
        cpu = float(process['%CPU'])
        total_cpu += cpu
        if cpu > max_cpu:
            max_cpu = cpu
            max_cpu_process = process
    return total_cpu, max_cpu_process

# Выполнение команды 'ps aux' и получение результата
process = subprocess.Popen(['ps', 'aux'], stdout=subprocess.PIPE)
output, error = process.communicate()

# Обработка ошибки, если таковая возникла
if error:
    print(f'Ошибка выполнения команды: {error.decode()}')
    exit()

# Парсинг результата
if output:
    # Парсинг вывода команды "ps aux"
    output = output.decode()
    lines = output.split('\n')
    headers = lines[0].split()
    lines = lines[1:-1]
    processes = []

    for line in lines:
        values = line.split()
        process = {}
        for i, header in enumerate(headers):
            process[header] = values[i]
        processes.append(process)

    num_processes = len(processes)
    user_processes = parse_user_processes(processes)
    total_memory, max_memory_process = parse_memory_usage(processes)
    total_cpu, max_cpu_process = parse_cpu_usage(processes)

    # Формирование отчёта
    report = f"Отчёт о состоянии системы ({datetime.datetime.now().strftime('%d-%m-%Y-%H:%M')})\n"
    report += f"Пользователи системы: {', '.join(user_processes.keys())}\n"
    report += f"Процессов запущено: {num_processes}\n"
    report += "Пользовательских процессов:\n"
    for user, count in user_processes.items():
        report += f"{user}: {count}\n"
    report += f"Всего памяти используется: {total_memory:.1f} mb\n"
    report += f"Всего CPU используется: {total_cpu:.1f}%\n"
    report += f"Больше всего памяти использует: ({max_memory_process.get('COMMAND', '')[:20]})\n"
    report += f"Больше всего CPU использует: ({max_cpu_process.get('COMMAND', '')[:20]})\n"

    # Вывод отчёта в стандартный вывод
    print(report)

    # Сохранение отчёта в файл
    file_name = datetime.datetime.now().strftime('%d-%m-%Y-%H:%M') + '-scan.txt'
    with open(file_name, 'w') as file:
        file.write(report)

    print(f"Отчёт сохранён в файле: {file_name}")

from typing import List, Dict
from dataclasses import dataclass

@dataclass
class PrintJob:
    id: str
    volume: float
    priority: int
    print_time: int

@dataclass
class PrinterConstraints:
    max_volume: float
    max_items: int

def optimize_printing(print_jobs: List[Dict], constraints: Dict) -> Dict:
    """
    Оптимізує чергу 3D-друку згідно з пріоритетами та обмеженнями принтера

    Args:
        print_jobs: Список завдань на друк
        constraints: Обмеження принтера

    Returns:
        Dict з порядком друку та загальним часом
    """
    if not print_jobs:
        return {"print_order": [], "total_time": 0}

    jobs: List[PrintJob] = []
    for j in print_jobs:
        if j["volume"] <= 0 or j["print_time"] <= 0:
            raise ValueError("volume і print_time повинні бути > 0")
        jobs.append(PrintJob(
            id=str(j["id"]),
            volume=float(j["volume"]),
            priority=int(j["priority"]),
            print_time=int(j["print_time"])
        ))

    c = PrinterConstraints(
        max_volume=float(constraints["max_volume"]),
        max_items=int(constraints["max_items"])
    )
    if c.max_volume <= 0 or c.max_items <= 0:
        raise ValueError("max_volume і max_items повинні бути > 0")

    jobs.sort(key=lambda x: x.priority)

    print_order: List[str] = []
    total_time = 0
    batch: List[PrintJob] = []
    batch_volume = 0.0

    def flush_batch():
        nonlocal batch, batch_volume, total_time, print_order
        if not batch:
            return
        batch_time = max(x.print_time for x in batch)
        total_time += batch_time
        print_order.extend(x.id for x in batch)
        batch = []
        batch_volume = 0.0

    for job in jobs:
        fits_items = (len(batch) + 1) <= c.max_items
        fits_volume = (batch_volume + job.volume) <= c.max_volume

        if fits_items and fits_volume:
            batch.append(job)
            batch_volume += job.volume
        else:
            flush_batch()
            batch.append(job)
            batch_volume = job.volume

    flush_batch()

    return {
        "print_order": print_order,
        "total_time": total_time
    }

# Тестування
def test_printing_optimization():
    # Тест 1: Моделі однакового пріоритету
    test1_jobs = [
        {"id": "M1", "volume": 100, "priority": 1, "print_time": 120},
        {"id": "M2", "volume": 150, "priority": 1, "print_time": 90},
        {"id": "M3", "volume": 120, "priority": 1, "print_time": 150}
    ]

    # Тест 2: Моделі різних пріоритетів
    test2_jobs = [
        {"id": "M1", "volume": 100, "priority": 2, "print_time": 120},  # лабораторна
        {"id": "M2", "volume": 150, "priority": 1, "print_time": 90},   # дипломна
        {"id": "M3", "volume": 120, "priority": 3, "print_time": 150}   # особистий проєкт
    ]

    # Тест 3: Перевищення обмежень об'єму
    test3_jobs = [
        {"id": "M1", "volume": 250, "priority": 1, "print_time": 180},
        {"id": "M2", "volume": 200, "priority": 1, "print_time": 150},
        {"id": "M3", "volume": 180, "priority": 2, "print_time": 120}
    ]

    constraints = {
        "max_volume": 300,
        "max_items": 2
    }

    print("Тест 1 (однаковий пріоритет):")
    result1 = optimize_printing(test1_jobs, constraints)
    print(f"Порядок друку: {result1['print_order']}")
    print(f"Загальний час: {result1['total_time']} хвилин")

    print("\nТест 2 (різні пріоритети):")
    result2 = optimize_printing(test2_jobs, constraints)
    print(f"Порядок друку: {result2['print_order']}")
    print(f"Загальний час: {result2['total_time']} хвилин")

    print("\nТест 3 (перевищення обмежень):")
    result3 = optimize_printing(test3_jobs, constraints)
    print(f"Порядок друку: {result3['print_order']}")
    print(f"Загальний час: {result3['total_time']} хвилин")

def test_more_cases():
    jobs4 = [
        {"id": "N1", "volume": 50, "priority": 1, "print_time": 200},
        {"id": "N2", "volume": 40, "priority": 1, "print_time": 30},
        {"id": "N3", "volume": 30, "priority": 1, "print_time": 30},
    ]
    constraints4 = {"max_volume": 100, "max_items": 2}
    r4 = optimize_printing(jobs4, constraints4)
    print("\nТест 4 (межа по кількості):")
    print(f"Порядок друку: {r4['print_order']}")
    print(f"Загальний час: {r4['total_time']} хвилин")

    jobs5 = [
        {"id": "V1", "volume": 60, "priority": 1, "print_time": 100},
        {"id": "V2", "volume": 70, "priority": 1, "print_time": 90},
        {"id": "V3", "volume": 30, "priority": 1, "print_time": 80},
        {"id": "V4", "volume": 20, "priority": 1, "print_time": 10},
    ]
    constraints5 = {"max_volume": 150, "max_items": 5}
    r5 = optimize_printing(jobs5, constraints5)
    print("\nТест 5 (межа по об'єму):")
    print(f"Порядок друку: {r5['print_order']}")
    print(f"Загальний час: {r5['total_time']} хвилин")

    jobs6 = [
        {"id": "P1", "volume": 150, "priority": 1, "print_time": 60},
        {"id": "P2", "volume": 100, "priority": 1, "print_time": 50},
        {"id": "P3", "volume": 50, "priority": 2, "print_time": 10},
    ]
    constraints6 = {"max_volume": 200, "max_items": 2}
    r6 = optimize_printing(jobs6, constraints6)
    print("\nТест 6 (різні пріоритети, розбиття партій):")
    print(f"Порядок друку: {r6['print_order']}")
    print(f"Загальний час: {r6['total_time']} хвилин")

    jobs7 = [
        {"id": "E1", "volume": 300, "priority": 1, "print_time": 200},
        {"id": "E2", "volume": 10, "priority": 1, "print_time": 10},
    ]
    constraints7 = {"max_volume": 300, "max_items": 2}
    r7 = optimize_printing(jobs7, constraints7)
    print("\nТест 7 (об'єм == max_volume):")
    print(f"Порядок друку: {r7['print_order']}")
    print(f"Загальний час: {r7['total_time']} хвилин")

    jobs8 = [
        {"id": "S1", "volume": 10, "priority": 1, "print_time": 5},
        {"id": "S2", "volume": 10, "priority": 1, "print_time": 500},
        {"id": "S3", "volume": 10, "priority": 1, "print_time": 10},
    ]
    constraints8 = {"max_volume": 1000, "max_items": 1}
    r8 = optimize_printing(jobs8, constraints8)
    print("\nТест 8 (max_items = 1):")
    print(f"Порядок друку: {r8['print_order']}")
    print(f"Загальний час: {r8['total_time']} хвилин")

    jobs9 = [
        {"id": "B1", "volume": 40, "priority": 1, "print_time": 300},
        {"id": "B2", "volume": 40, "priority": 1, "print_time": 60},
        {"id": "B3", "volume": 40, "priority": 1, "print_time": 200},
    ]
    constraints9 = {"max_volume": 200, "max_items": 3}
    r9 = optimize_printing(jobs9, constraints9)
    print("\nТест 9 (максимум часу в дрібній моделі):")
    print(f"Порядок друку: {r9['print_order']}")
    print(f"Загальний час: {r9['total_time']} хвилин")

    jobs10 = [
        {"id": "T1", "volume": 120, "priority": 1, "print_time": 70},
        {"id": "T2", "volume": 190, "priority": 1, "print_time": 80},
        {"id": "T3", "volume": 100, "priority": 1, "print_time": 60},
        {"id": "T4", "volume": 180, "priority": 1, "print_time": 40},
    ]
    constraints10 = {"max_volume": 300, "max_items": 2}
    r10 = optimize_printing(jobs10, constraints10)
    print("\nТест 10 (кілька партій через об'єм):")
    print(f"Порядок друку: {r10['print_order']}")
    print(f"Загальний час: {r10['total_time']} хвилин")


if __name__ == "__main__":
    test_printing_optimization()
    # test_more_cases()


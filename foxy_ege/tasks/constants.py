from .models import ExamSubject

# Define exam-specific maximum task counts
EXAM_MAX_TASKS = {
    ExamSubject.MATH: 19,  # Профильная математика
    ExamSubject.MATHB: 20,  # Базовая математика
    ExamSubject.RUS: 26,  # Русский язык
    ExamSubject.PHYS: 32,  # Физика
    ExamSubject.CHEM: 34,  # Химия
    ExamSubject.BIO: 28,  # Биология
    ExamSubject.HIST: 25,  # История
    ExamSubject.SOC: 29,  # Обществознание
    ExamSubject.LIT: 17,  # Литература
    ExamSubject.GEO: 34,  # География
    ExamSubject.ENG: 40,  # Английский язык
    ExamSubject.INF: 27,  # Информатика
}

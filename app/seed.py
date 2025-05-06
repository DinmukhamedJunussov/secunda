from sqlalchemy.orm import Session
from app.models import Base, Building, Activity, Organization, PhoneNumber
from app.database import engine

def seed_database():
    # Создаем таблицы
    Base.metadata.create_all(bind=engine)
    
    # Создаем сессию
    session = Session(engine)
    
    try:
        # Создаем здания
        buildings = [
            Building(address="ул. Пушкина, 10", latitude=55.7558, longitude=37.6173),
            Building(address="пр. Ленина, 25", latitude=55.7517, longitude=37.6178),
            Building(address="ул. Гагарина, 15", latitude=55.7520, longitude=37.6175),
        ]
        session.add_all(buildings)
        session.flush()
        
        # Создаем виды деятельности
        activities = [
            Activity(name="Розничная торговля"),
            Activity(name="Общественное питание"),
            Activity(name="Услуги"),
        ]
        session.add_all(activities)
        session.flush()
        
        # Создаем организации
        organizations = [
            Organization(name="Магазин 'Продукты'", building_id=buildings[0].id),
            Organization(name="Кафе 'Уют'", building_id=buildings[1].id),
            Organization(name="Салон красоты 'Красота'", building_id=buildings[2].id),
        ]
        session.add_all(organizations)
        session.flush()
        
        # Добавляем телефоны
        phones = [
            PhoneNumber(phone="+7 (999) 123-45-67", organization_id=organizations[0].id),
            PhoneNumber(phone="+7 (999) 234-56-78", organization_id=organizations[1].id),
            PhoneNumber(phone="+7 (999) 345-67-89", organization_id=organizations[2].id),
        ]
        session.add_all(phones)
        
        # Связываем организации с видами деятельности
        organizations[0].activities.append(activities[0])  # Магазин - розничная торговля
        organizations[1].activities.append(activities[1])  # Кафе - общественное питание
        organizations[2].activities.append(activities[2])  # Салон красоты - услуги
        
        # Сохраняем изменения
        session.commit()
        print("База данных успешно заполнена тестовыми данными!")
        
    except Exception as e:
        session.rollback()
        print(f"Произошла ошибка при заполнении базы данных: {e}")
    finally:
        session.close()

if __name__ == "__main__":
    seed_database() 
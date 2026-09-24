from datetime import datetime, timedelta

class Time:
    @staticmethod
    def time_init_and_limit():
        now = datetime.now()
        time_frame = timedelta(days=14)
        time_limit = now + time_frame
        now = now.strftime("%d/%m/%Y %H:%M")
        time_limit = time_limit.strftime("%d/%m/%Y %H:%M")
        return now, time_limit
    
    @staticmethod
    def time_now():
        now = datetime.now()
        return now.strftime("%d/%m/%Y %H:%M")
        
    
    @staticmethod
    def time_diference(end_lending, limit_lending):
        end_lending_object = datetime.strptime(end_lending, "%d/%m/%Y %H:%M")
        limit_lending_object = datetime.strptime(limit_lending, "%d/%m/%Y %H:%M")
        
        penalty_time = end_lending_object - limit_lending_object
        if penalty_time <= timedelta(0):
            return 0
        return penalty_time
    
    def penalty(penalty_time):
        if penalty_time <= timedelta(0):
            return 0
        
        return (penalty_time.total_seconds() / 86400)
        
    
    @staticmethod
    def days_defeated(penalty_time):
        return (penalty_time.total_seconds() // 86400)
        
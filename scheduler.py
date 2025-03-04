from apscheduler.schedulers.background import BackgroundScheduler
from fetch_rates import fetch_exchange_rates
import time

def start_scheduler():
    scheduler = BackgroundScheduler()

    
    def test_fetch():
        print("FETCHING CURRENCIES...")
        fetch_exchange_rates()
        print("FETCHING DONE!!!!!!!")

    
    test_fetch()  #Initial fetch
    scheduler.add_job(test_fetch, "interval", minutes=30) #Fetch every x minutes

    scheduler.start()
    print("SCHEDULER STARTED...<>")

    try:
        while True:
            time.sleep(2)
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()
        print("!!!!SCHEDULER STOPPED!!!!")

if __name__ == "__main__":
    start_scheduler()

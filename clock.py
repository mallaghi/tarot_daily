from app import scheduler

if __name__ == '__main__':
    scheduler.start()

    try:

        while True:
            pass
    finally:
        scheduler.shutdown()

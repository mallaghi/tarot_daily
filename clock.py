from app import scheduler

if __name__ == '__main__':
    scheduler.start()

    try:
        # Keep the process alive
        while True:
            pass
    finally:
        scheduler.shutdown()

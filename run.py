from app import app, scheduler

if __name__ == '__main__':
    # scheduler.start()

    try:
        app.run(debug=True, port=8000)
    finally:
        scheduler.shutdown()

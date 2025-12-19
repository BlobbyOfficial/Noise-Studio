from ui.main_window import MainWindow

def main():
    try:
        MainWindow().run()
    except Exception:
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()

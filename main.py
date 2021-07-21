from src.context import UnitContext


def unit_code():
    unit_menu = UnitContext()
    unit_menu.start()
    
def main():
    try:
        unit_code()
    
    except Exception as e:
        input(e)

if __name__ =='__main__':
    main()

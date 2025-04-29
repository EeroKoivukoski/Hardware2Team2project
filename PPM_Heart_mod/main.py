from PPM_Heart_rate_project.menu import run_menu

def main():
    current_index = 0
    menu_items = [
    "1.Measure HR",
    "2.Basic HRV Analysis",
    "3.Kubios",
    "4.History"
]
    current_index =run_menu(current_index,menu_items)

if __name__ == "__main__":
    main()


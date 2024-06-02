import os
import random
import json
from tabulate import tabulate
import pandas as pd


intro = '''
Welcome to "What's for Dinner!" menu generator by ChefWare.
Enter how many days of menus you want generated and Whats for Dinner!
will generate them. From that starting point regenerate individual dishes 
or entire themes until you get what you want.
Then the program will export your menu to a spreadsheet where you can save it
and print it.
The program loads a .json database (if you have a previously saved one) otherwise
it will create one for you and you can begin populating it with your own dishes.

TECHNICAL NOTES: 
Breakfasts and Desserts are not themed.
The "Generic" theme houses these 2 categories as well as other normal unthemed dishes
like steak, BBQ wings, Garden salad, Steamed veg, etc.
To change entire lunch/dinner themes select Theme (indices 2).
Scroll right to see all columns of the tables.

COMMANDS:
Commands used here are mostly yes/no, theme names or the indices indicated on the table itself.
Stay tuned for updates!
'''
outro = ("Thanks for using What's for Dinner!")

file_path = os.getcwd()
filename = os.path.join(file_path, 'themes_data.json')
pd.options.display.max_columns = None


def load_from_file(filename):
    try:
        with open(filename, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}


def days_func(days_choice):
    while not days_choice.isdigit() or int(days_choice) <= 0:
        print('\n')
        print('INVALID CHOICE!')
        print('\n')
        days_choice = input('How many days of meals do you want generated? >>> ')
    else:
        return int(days_choice)


def theme_generator(themes_dict):
    themes_list = list(themes_dict)
    random.shuffle(themes_list)
    theme = random.choice(themes_list)
    return theme


def menu_generator(themes_dict, theme, meal_type):
    meat_category = random.choice(list(themes_dict[theme]['meats'].keys()))  # TODO here maybe can break the program
    meat_dish = random.choice(themes_dict[theme]['meats'][meat_category])
    seafood_dish = random.choice(list(themes_dict[theme].get('seafood', ['NOT FOUND!'])))

    carb_dish = random.choice(list(themes_dict[theme].get('carb', ['NOT FOUND!'])))
    veg_list = themes_dict[theme]['veg']
    veg_samples = random.sample(veg_list, 3)
    veg_sample_one = veg_samples[0]
    veg_sample_two = veg_samples[1]
    veg_sample_three = veg_samples[2]
    extras_dish = random.choice(list(themes_dict[theme].get('extras', ['NOT FOUND!'])))

    days_menu = {
        'Meal type': meal_type,
        '2 - Theme': theme,
        '3 - Meat dish': meat_dish,
        '4 - Seafood dish': seafood_dish,
        '5 - Carb dish': carb_dish,
        '6 - Veg dish one': veg_sample_one,
        '7 - Veg dish two': veg_sample_two,
        '8 - Veg dish three': veg_sample_three,
        '9 - Extras': extras_dish
    }
    return days_menu


def generate_breakfast_menu(themes_dict):
    meal_type = 'Breakfast'
    breakfast_dish = random.choice(themes_dict['generic']['breakfast'])
    breakfast_dict = {
        'Meal type': meal_type,
        '1 - Breakfast': breakfast_dish
    }
    return breakfast_dict


def generate_lunch_menu(themes_dict, theme):
    meal_type = 'Lunch'
    return menu_generator(themes_dict, theme, meal_type)


def generate_dinner_menu(themes_dict, theme):
    meal_type = 'Dinner'
    return menu_generator(themes_dict, theme, meal_type)


def generate_dessert_menu(themes_dict):
    meal_type = 'Dessert'
    dessert_dish = random.choice(themes_dict['generic']['dessert'])
    dessert_dict = {
        'Meal type': meal_type,
        '10 - Dessert': dessert_dish
    }
    return dessert_dict


def regenerate_dish(regen_choice, menu_df, themes_dict):
    while True:
        while regen_choice not in ['yes', 'no']:
            regen_choice = input('Would you like to regenerate THEMES or DISHES? >>> ').lower()

        if regen_choice == 'yes':
            row_choice = int(input('Which row number is the THEME/DISH on? >>> '))
            column_choice = int(input('Which column NUMBER is the THEME/DISH in? >>> '))
            dish_choice = menu_df.iloc[row_choice, column_choice]
            if not pd.isna(menu_df.iloc[row_choice, column_choice]):

                if column_choice == 1:
                    new_dish = random.choice(themes_dict['generic']['breakfast'])
                    menu_df.iloc[row_choice, column_choice] = new_dish

                elif column_choice == 2 and menu_df.iloc[row_choice, 0] == 'Lunch':
                    avail_themes = list(themes_dict.keys())
                    theme_choice = input(f"Available themes to choose are:\n{avail_themes}\nor type RANDOM for a random theme >>> ").lower()
                    while theme_choice not in avail_themes and theme_choice != 'random':
                        print('\n')
                        print(F'{theme_choice} IS INVALID!')
                        print('\n')
                        theme_choice = input(
                            f"Available themes to choose are:\n{avail_themes}\nor type RANDOM for a random theme >>> ").lower()
                    if theme_choice in avail_themes:
                        regen_theme = theme_choice
                        menu_df.iloc[row_choice] = generate_lunch_menu(themes_dict, regen_theme)
                    else:
                        regen_theme = theme_generator(themes_dict)
                        menu_df.iloc[row_choice] = generate_lunch_menu(themes_dict, regen_theme)

                elif column_choice == 2 and menu_df.iloc[row_choice, 0] == 'Dinner':
                    avail_themes = list(themes_dict.keys())
                    theme_choice = input(f"Available themes to choose are:\n{avail_themes}\nor type RANDOM for a random theme >>> ").lower()
                    while theme_choice not in avail_themes and theme_choice != 'random':
                        print('\n')
                        print(f'{theme_choice} IS INVALID!')
                        print('\n')
                        theme_choice = input(
                            f"Available themes to choose are:\n{avail_themes}\nor type RANDOM for a random theme >>> ").lower()
                    if theme_choice in avail_themes:
                        regen_theme = theme_choice
                        menu_df.iloc[row_choice] = generate_dinner_menu(themes_dict, regen_theme)
                    else:
                        regen_theme = theme_generator(themes_dict)
                        menu_df.iloc[row_choice] = generate_dinner_menu(themes_dict, regen_theme)

                elif column_choice == 3:
                    theme_name = menu_df.iloc[row_choice, 2]
                    avail_meats = list(themes_dict[theme_name]['meats'].keys())
                    meat_choice_regen = input(f'Choice of meats for {theme_name} are:\n{avail_meats}\nWhat meat are you '
                                              f'thinking? >>> ').lower()
                    while meat_choice_regen not in avail_meats:
                        print('\n')
                        print(f'{meat_choice_regen} IS INVALID!')
                        print('\n')
                        meat_choice_regen = input(
                            f'Choice of meats for {theme_name} are:\n{avail_meats}\nWhat meat are you '
                            f'thinking? >>> ').lower()
                    new_dish = random.choice(themes_dict[theme_name]['meats'][meat_choice_regen])
                    menu_df.iloc[row_choice, column_choice] = new_dish

                elif column_choice == 4:
                    theme_name = menu_df.iloc[row_choice, 2]
                    new_dish = random.choice(themes_dict[theme_name]['seafood'])
                    menu_df.iloc[row_choice, column_choice] = new_dish

                elif column_choice == 5:
                    theme_name = menu_df.iloc[row_choice, 2]
                    new_dish = random.choice(themes_dict[theme_name]['carb'])
                    menu_df.iloc[row_choice, column_choice] = new_dish

                elif column_choice == 6:
                    theme_name = menu_df.iloc[row_choice, 2]
                    new_dish = random.choice(themes_dict[theme_name]['veg'])
                    menu_df.iloc[row_choice, column_choice] = new_dish

                elif column_choice == 7:
                    theme_name = menu_df.iloc[row_choice, 2]
                    new_dish = random.choice(themes_dict[theme_name]['veg'])
                    menu_df.iloc[row_choice, column_choice] = new_dish

                elif column_choice == 8:
                    theme_name = menu_df.iloc[row_choice, 2]
                    new_dish = random.choice(themes_dict[theme_name]['veg'])
                    menu_df.iloc[row_choice, column_choice] = new_dish

                elif column_choice == 9:
                    theme_name = menu_df.iloc[row_choice, 2]
                    new_dish = random.choice(themes_dict[theme_name]['extras'])
                    menu_df.iloc[row_choice, column_choice] = new_dish

                elif column_choice == 10:
                    new_dish = random.choice(themes_dict['generic']['dessert'])
                    menu_df.iloc[row_choice, column_choice] = new_dish

                else:
                    print('\n')
                    print(f"Invalid dish type: {dish_choice}")
                    print('\n')
                    return menu_df

                print(tabulate(menu_df.fillna(value='   ---'), headers='keys', tablefmt='psql'))

            else:
                print(f"Dish type not found: {dish_choice}")
                return menu_df

        elif regen_choice == 'no':
            break

        regen_choice = input('Would you like to regenerate THEMES or DISHES? >>> ').lower()

    return menu_df


def export_to_excel(menu_df):
    menu_plan_name = 'completed_menu_plan.xlsx'
    menu_df.to_excel(menu_plan_name)
    print(f"Your menu has been saved as {menu_plan_name} in the current directory")


def main():
    print(intro)
    load_from_file(filename)
    themes_dict = load_from_file(filename)
    days_choice = input('How many days of meals do you want generated? >>> ')
    days_func(days_choice)
    days = days_func(days_choice)
    menus = []
    for _ in range(days):
        theme = theme_generator(themes_dict)
        # theme_generator(themes_dict)
        breakfast_menu = generate_breakfast_menu(themes_dict)
        lunch_menu = generate_lunch_menu(themes_dict, theme)
        theme = theme_generator(themes_dict)
        dinner_menu = generate_dinner_menu(themes_dict, theme)
        dessert_menu = generate_dessert_menu(themes_dict)
        menus.extend([breakfast_menu, lunch_menu, dinner_menu, dessert_menu])
    menu_df = pd.DataFrame(menus)
    print(tabulate(menu_df.fillna(value='   ---'), headers='keys', tablefmt='psql'))

    # Regenerate dishes if needed
    regen_choice = input('Would you like to regenerate THEMES or DISHES? >>> ').lower()
    menu_df = regenerate_dish(regen_choice, menu_df, themes_dict)
    print("FINAL COPY BELOW (scroll right to see all columns)")
    print(tabulate(menu_df.fillna(value='   ---'), headers='keys', tablefmt='psql'))
    save_choice = input('Would you like to export your work to a spreadsheet? >>> ').lower()
    if save_choice not in ['yes', 'no']:
        print('\n')
        print(f'{save_choice} IS INVALID!')
        print('\n')
        save_choice = input('Would you like to export your work to a spreadsheet? >>> ').lower()
    elif save_choice == 'yes':
        export_to_excel(menu_df)

    else:
        print('Your file was NOT saved')
    print('\n')
    print(outro)

if __name__ == "__main__":
    main()

# todo add read spreadsheet capability

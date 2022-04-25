from booking.booking import Booking

try:

    with Booking() as bot:
        bot.land_first_page()
        bot.accept_cookies()
        bot.select_place_to_go(place='Amsterdam')
        bot.select_dates(start_date='2022-04-25', end_date='2022-05-30')
        bot.rooms_and_occupancy(rooms=1, adults=1, children=0)
        bot.search()
        # bot.change_currency(currency='EUR')
        bot.apply_filtration(3)

except Exception as e:
    if 'in PATH' in str(e):
        print(
            'Please add  Selenium Driver to PATH \n'
            'Windows: \n'
            '    set PATH=%PATH%;C:\path-to-drivers \n'
            'Linux: \n'
            '    export PATH=$PATH:/path-to-drivers \n'
        )
    else:
        raise

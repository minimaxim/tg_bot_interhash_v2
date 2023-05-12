
if __name__ == '__main__':
    from loader import dp, bot
    from handlers import router
    from parser.test_par import parse_and_save

    dp.include_router(router=router)
    dp.run_polling(bot)

    parse_and_save()


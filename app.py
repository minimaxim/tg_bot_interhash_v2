
if __name__ == '__main__':
    from loader import dp, bot
    from handlers import router

    dp.include_router(router=router)
    dp.run_polling(bot)


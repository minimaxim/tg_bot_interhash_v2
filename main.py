from models import Start, Category, Currency, Discont, Power, Promo, Coin, Application, Admin


async def main():

    starts = ["Хочу купить оборудование 🔥", "Подключиться к пулу со скидкой ✅", "Связь с менеджером 📞",
              "Калькулятор 📊"]
    for s in starts:
        s = Start(
            name=s,
        )
        await s.save()

    categories = ["Калькулятор 📊", "Нужна консультация 📞", "Да, знаю ✅"]
    for c in categories:
        c = Category(
            name=c,
        )
        await c.save()

    currencies = ["RUB ₽", "USD $"]
    for cu in currencies:
        cu = Currency(
            name=cu,
        )
        await cu.save()

    disconts = ["Да ✅", "Нет ❌"]
    for d in disconts:
        d = Discont(
            name=d,
        )
        await d.save()

    powers = ["Меньше 1 ph 🔥", "Больше 1 ph 🔥"]
    for p in powers:
        p = Power(
            name=p,
        )
        await p.save()

    promocodes = ["Промокод 💥",]
    for pr in promocodes:
        pr = Promo(
            name=pr,
        )
        await pr.save()

    coins = ["bitcoin", "bitcoin-cash", "litecoin", "ethereum-classic", "zcash", "dash"]
    for co in coins:
        co = Coin(
            name=co,
        )
        await co.save()

    applications = ["Оставить заявку ✅"]
    for a in applications:
        a = Application(
            name=a,
        )
        await a.save()

    admins = ['max']
    for n in admins:
        n = Admin(
            name=n,
            id=594555381
        )
        await n.save()


if __name__ == '__main__':
    import asyncio
    asyncio.run(main())

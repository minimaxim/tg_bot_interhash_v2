from models import Start, Category, Brand, Model


async def main():
    N = ['Да, хочу скидку', 'Нет, откажусь']
    for n in N:
        n = Model(
            name=n,
            brand_id=1
        )
        await n.save()


if __name__ == '__main__':
    import asyncio
    asyncio.run(main())

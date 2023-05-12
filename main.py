from models import Start, Text, Category


async def main():
    N = ['Хочу купить оборудование', 'Хочу обсудить индивидуально', 'У меня есть вопрос', 'Калькулятор доходности']
    for n in N:
        n = Start(
            name=n,
        )
        await n.save()


if __name__ == '__main__':
    import asyncio
    asyncio.run(main())

import requests
import os
import aiohttp


async def load_excel(table: str, date: str):
    async with aiohttp.ClientSession() as session:
        async with session.get(table) as response:
            folder_path = "src/data"
            splitted_date = date.split(":")[-1]
            file_name = f"result_{splitted_date}.xlsx"

            save_path = os.path.join(folder_path, file_name)

            if not os.path.exists(folder_path):
                os.makedirs(folder_path)

            with open(save_path, "wb") as file:
                content = await response.read()
                file.write(content)
                print(f"Документ {file_name} загружен")

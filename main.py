import asyncio
from playwright.async_api import async_playwright
from random import uniform
from loguru import logger
from config import EXTENSION_PATH, MAX_RETRY, THREADS_NUM, USE_PROXY

from utils import get_accounts, get_format_proxy, switch_to_page_by_title

NEW_PASSWORD = "Password_12345"

async def run(id, private_key, proxy, semaphore):
    for _ in range(MAX_RETRY):
        try:
            async with semaphore:
                # await gas_checker(id)
                logger.info(f"START {id}")
                
                
                # Initialize the browser and context
                async with async_playwright() as p:
                    
                    if proxy is not None and USE_PROXY is True:
                        address, port, login, password = get_format_proxy(proxy)  
                        context = await p.chromium.launch_persistent_context(
                            '',
                            headless=False,
                            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
                            proxy={
                            "server": f"http://{address}:{port}",
                            "username": login,
                            "password": password
                            },
                            args=[
                                '--disable-blink-features=AutomationControlled',
                                f"--disable-extensions-except={EXTENSION_PATH}",
                                f"--load-extension={EXTENSION_PATH}"
                            ]
                        )
                    else:
                        context = await p.chromium.launch_persistent_context(
                            '',
                            headless=False,
                            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',

                            args=[
                                '--disable-blink-features=AutomationControlled',
                                f"--disable-extensions-except={EXTENSION_PATH}",
                                f"--load-extension={EXTENSION_PATH}"
                            ]
                        )
                    page = await context.new_page()
                    await page.goto('chrome-extension://aibihgfojaoplnbnecdjiioleemgfope/onboarding.html')
                    await page.close()

                    page = await switch_to_page_by_title(context, 'Magic Eden')
                    await page.goto('chrome-extension://aibihgfojaoplnbnecdjiioleemgfope/onboarding.html')
                    await asyncio.sleep(uniform(0.3, 0.7))
                    
                    await page.click(f'div:text("I Have A Wallet")')
                    await asyncio.sleep(uniform(0.3, 0.7))
                    
                    inputs = await page.query_selector_all("input")
                    seed_phrase = private_key.split(' ')
                    num_word = 0
                    for input_element in inputs:
                        await input_element.fill(seed_phrase[num_word])
                        num_word+=1
                        
                    await asyncio.sleep(uniform(0.3, 0.7))
                    await page.click(f'div:text("Continue")')
                    await asyncio.sleep(uniform(0.3, 0.7))
                    
                    # Ввод пароля
                    await page.fill('input[type="password"]', NEW_PASSWORD) 
                    await page.press('input[type="password"]', 'Enter')
                    await asyncio.sleep(uniform(0.3, 0.7))
                    
                    await page.fill('input[type="password"]', NEW_PASSWORD) 
                    await page.press('input[type="password"]', 'Enter')
                    await asyncio.sleep(uniform(0.3, 0.7))

                    await page.click(f'div:text("Restore Wallet Now")')
                    await asyncio.sleep(uniform(0.3, 0.7))
                    await page.click(f'div:text("Continue")', timeout=50000)
                    await asyncio.sleep(uniform(0.3, 0.7))
                    await page.click(f'div:text("Continue")', timeout=50000)
                    await asyncio.sleep(uniform(0.3, 0.7))
                    
                    try:
                        await page.click(f'div:text("Claim Now")', timeout=10000)
                    except:
                        try:
                            await page.click(f'div:text("Claim your collectible!")', timeout=30000)
                        except:
                            await page.click(f'div:text("Claim Now")', timeout=30000)
                    
                    await asyncio.sleep(uniform(0.3, 0.7))
                    await page.click(f'div:text("Complete Claim")', timeout=10000)
                    await asyncio.sleep(uniform(0.3, 0.7))
                    await page.click(f'div:text("Continue")', timeout=10000)
                    await asyncio.sleep(uniform(0.5, 0.9))
                    await page.click(f'xpath=/html/body/div[1]/div/div/div[2]/div/div[1]/div/div/div/div/div/div[1]/div[3]/div[2]/div[2]/div/div/div/div[1]/div[2]/div[2]/div[3]/div/div', timeout=10000)
                    await asyncio.sleep(uniform(0.5, 0.9))
                    try:
                        await page.wait_for_selector('div:text("Item Minted")', timeout=20000)
                        logger.info(f'{id} Success Mint MonkeDao')
                        return
                    except:
                        logger.error(f"{id} Error tx Mint MonkeDao")
                    
                    
        except Exception as ex:
            logger.error(f"{id} | {ex}")
            await asyncio.sleep(30)
        finally:
            try:
                await context.close()
            except:
                pass


async def main(accounts):
    semaphore = asyncio.Semaphore(THREADS_NUM)
    tasks = [run(id, private_key, proxy, semaphore) for id, private_key, proxy in accounts]
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    accounts = get_accounts()
    logger.info(f"Loaded {len(accounts)} accounts")
    asyncio.run(main(accounts))
    
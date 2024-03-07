import asyncio
import random
import traceback
from playwright.async_api import async_playwright
from random import uniform
from loguru import logger
from config import EXTENSION_PATH, MAX_RETRY, MODE, THREADS_NUM, USE_PROXY

from utils import get_accounts, get_format_proxy, switch_to_page_by_title

NEW_PASSWORD = "Password_12345"

async def run(id, private_key, proxy, semaphore):
    for _ in range(MAX_RETRY):
        try:
            async with semaphore:
                # await gas_checker(id)
                logger.info(f"{id} | START")
                
                
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
                    # page = await context.new_page()
                    # await page.goto('chrome-extension://aibihgfojaoplnbnecdjiioleemgfope/onboarding.html')
                    # await page.close()

                    page = await switch_to_page_by_title(context, 'Magic Eden')
                    url_extension = page.url
                    await page.goto(url_extension)
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
                    await asyncio.sleep(uniform(4, 5))
                    
                    if MODE == "MINT":
                        await mint_monkeDAO(id, context, page)
                    elif MODE == "SWAP":
                        await swap(id, context, page)
                    
                    logger.info(f"{id} | START")
        except Exception as ex:
            logger.error(f"{id} Retry... | {traceback.format_exc()}, {ex} ")
            await asyncio.sleep(10)
        finally:
            try:
                await context.close()
            except:
                pass

async def mint_monkeDAO(id, context, page):
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
    

# async def swap(id, context, page):
#     rand_self_count = random.randint(SWAP_COUNT[0], SWAP_COUNT[1])
#     logger.info(f"{id} | START {rand_self_count} swaps..")
#     for i in range(1, rand_self_count+1):
#         try:
#             p = await page.click('xpath=//*[@id="root"]/div/div/div[2]/div/div[1]/div/div/div/div/div/div[1]/div/div[2]/div[2]/div/div/div/div[1]/div/div/div[2]/div/div[3]', timeout=5000)
#             await asyncio.sleep(0.5)

#             await page.click(f'xpath=//div/div[5]/div[1]/div/div/div[1]/div[1]/div/div/div/button/div/div/div[text()="{SOL}"]', timeout=5000)
            
#             await asyncio.sleep(random.uniform(0.5, 1))
#             await page.click('xpath=//div[1]/div[4]/div/div[3]/div/div/div[5]/div[1]/div/div/div[1]/div[2]/label[1]/fieldset/div/div[2]/div[1]/button', timeout=10000)

#             await asyncio.sleep(random.uniform(0.5, 1))
#             from_asset = random.choice(FROM_ASSET_LIST)
#             await page.click(f'xpath=//span[text()="{from_asset}"]', timeout=10000)

#             await asyncio.sleep(random.uniform(0.5, 1))
#             await page.click('xpath=//div[1]/div[4]/div/div[3]/div/div/div[5]/div[1]/div/div/div[1]/div[2]/label[2]/fieldset/div/div[2]/div[1]/button', timeout=10000)

#             await asyncio.sleep(random.uniform(0.5, 1))
#             p = await page.wait_for_selector('xpath=//div[1]/div[2]/input', timeout=10000)
#             to_asset = random.choice(TO_ASSET_LIST)
#             await p.fill(to_asset)

#             await asyncio.sleep(random.uniform(1, 2))
#             elements = await page.query_selector_all('xpath=//div')
            
#             for el in elements:
#                 text_el = await el.text_content()
#                 if text_el.strip() == to_asset:
#                     # print("Элемент найден:", el)
#                     await el.click()
#                     break

#             await asyncio.sleep(random.uniform(1, 1.5))
#             rand_sum_tx = random.uniform(float(SWAP_SELF_AMOUNT[0]), float(SWAP_SELF_AMOUNT[1]))
#             p = await page.wait_for_selector('#sell-value', timeout=10000)
#             await p.fill(f"{rand_sum_tx:.10f}") 
#             #/html/body/div[1]/div[4]/div/div[3]/div/div/div[5]/div[1]/div/div/div[3]/button
#             await page.click('xpath=//div/div/div[3]/button', timeout=10000)

#             zerion_popup_window = await switch_to_page_by_title(context, 'Zerion · Send Transaction')
#             await zerion_popup_window.click('text="Confirm"', timeout=10000)

#             for t in range(15):
#                 await asyncio.sleep(1)
#                 if len(context.pages) < 2:
#                     logger.success(f"{id} | Swap {i} | {SWAP_CHAIN} {rand_sum_tx} {from_asset} -> {to_asset}")
#                     break
#                 if t > 12:
#                     logger.error(f"{id} | Transaction execution error")
#                     break
#             await asyncio.sleep(random.randrange(NEXT_TX_MIN_WAIT_TIME, NEXT_TX_MAX_WAIT_TIME))
#         except Exception as ex:
#             logger.error(traceback.format_exc(), ex)

async def main(accounts):
    semaphore = asyncio.Semaphore(THREADS_NUM)
    tasks = [run(id, private_key, proxy, semaphore) for id, private_key, proxy in accounts]
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    accounts = get_accounts()
    logger.info(f"Loaded {len(accounts)} accounts")
    asyncio.run(main(accounts))
    
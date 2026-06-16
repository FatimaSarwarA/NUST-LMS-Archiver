import asyncio
from playwright.async_api import async_playwright
import os
import random
from dotenv import load_dotenv

# ==========================igi================
# --- SECURITY & CONFIGURATION ---
# ==========================================
load_dotenv()

USERNAME = os.getenv("NUST_USERNAME")
PASSWORD = os.getenv("NUST_PASSWORD")
DOWNLOAD_DIR = "./NUST_Submissions"

if not os.path.exists(DOWNLOAD_DIR):
    os.makedirs(DOWNLOAD_DIR)


# ==========================================
# --- THE AUTOMATION BOT ---
# ==========================================
async def run():
    if not USERNAME or not PASSWORD:
        print("[ERROR] Could not find NUST_USERNAME or NUST_PASSWORD in your .env file.")
        return

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()

        # ------------------------------------------
        # 1. LOGIN
        # ------------------------------------------
        print("Logging in...")
        await page.goto("https://lms.nust.edu.pk/portal/login/index.php")
        await page.fill('input[name="username"]', USERNAME)
        await page.fill('input[name="password"]', PASSWORD)
        await page.click('button[id="loginbtn"]')

        # ------------------------------------------
        # 2. NAVIGATE TO DASHBOARD & AUTO-SCROLL
        # ------------------------------------------
        print("Navigating to dashboard...")
        await page.goto("https://lms.nust.edu.pk/portal/my/")

        print("Scrolling to the bottom to trigger lazy-loading...")
        last_course_count = 0
        retries = 0

        # Keep scrolling until we hit the bottom
        while retries < 3:
            await page.keyboard.press("End")
            await asyncio.sleep(2.5)

            current_count = await page.locator('a.coursename').count()

            if current_count > last_course_count:
                print(f"  ... loaded {current_count} courses so far.")
                last_course_count = current_count
                retries = 0
            else:
                retries += 1

        print(f"\n[SUCCESS] Hit the bottom! Found {current_count} total courses.")

        course_links = page.locator('a.coursename')
        course_urls = [await course_links.nth(i).get_attribute("href") for i in range(current_count)]

        # ------------------------------------------
        # 3. PROCESS EVERY COURSE
        # ------------------------------------------
        for c_url in course_urls:
            await page.goto(c_url)
            raw_course_name = await page.title()

            # Clean up the course name so Windows/Mac allows it as a folder name
            clean_course_name = "".join([c for c in raw_course_name if c.isalnum() or c in (' ', '_', '-')]).strip()
            print(f"\n=== Entering Course: {clean_course_name} ===")

            # ---> CREATE THE COURSE FOLDER <---
            course_dir = os.path.join(DOWNLOAD_DIR, clean_course_name)
            if not os.path.exists(course_dir):
                os.makedirs(course_dir)

            await page.wait_for_load_state("networkidle")

            # Find all assignment dropboxes
            assign_links = page.locator("a[href*='/mod/assign/view.php']")
            assign_urls = [await assign_links.nth(i).get_attribute("href") for i in range(await assign_links.count())]

            print(f"Found {len(assign_urls)} assignment dropboxes here.")

            # ------------------------------------------
            # 4. VISIT ASSIGNMENTS & DOWNLOAD FILES
            # ------------------------------------------
            for a_url in assign_urls:
                await page.goto(a_url)
                await asyncio.sleep(1.5)

                file_links = page.locator("a[href*='forcedownload=1']")
                file_count = await file_links.count()

                for j in range(file_count):
                    try:
                        async with page.expect_download(timeout=15000) as download_info:
                            await file_links.nth(j).click()

                        download = await download_info.value

                        # ---> SAVE IT IN THE COURSE FOLDER <---
                        # We don't need to add the course name to the file itself anymore,
                        # since it's going inside the course's dedicated folder!
                        final_path = os.path.join(course_dir, download.suggested_filename)
                        await download.save_as(final_path)

                        print(f"  [SUCCESS] Saved: {download.suggested_filename} in /{clean_course_name}")

                    except Exception as e:
                        print(f"  [ERROR] Failed to download a file: {e}")

                await asyncio.sleep(random.uniform(1.5, 3.0))

        print("\nProcess Complete! Check your NUST_Submissions folder.")
        await browser.close()


if __name__ == "__main__":
    asyncio.run(run())
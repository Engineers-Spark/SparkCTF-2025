const puppeteer = require("puppeteer")

const browser_options = {
    pipe: true,
    dumpio: true,
    headless: true,
    executablePath: "/opt/google/chrome/google-chrome",
    args: [
                "--no-sandbox",
                "--disable-setuid-sandbox",
                "--js-flags=--noexpose_wasm,--jitless",
    ],
};



module.exports.visit = async function (url) {
    const browser = await puppeteer.launch(browser_options);

    try {
        const page = await browser.newPage();

        // 1 min is all you get!
        await page.goto(url, { waitUntil: "networkidle2" });
        await page.waitForTimeout(60000);
	    await browser.close();
        
    } catch (err) {
        console.log(err);
    } finally {
        if (browser) await browser.close();
    }

}

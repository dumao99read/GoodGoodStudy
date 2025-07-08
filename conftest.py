import pytest
from playwright.sync_api import sync_playwright

ui_keywords = ['ui_baidu', 'ui_douban']
api_keywords = ['api_baidu', 'api_douban']

@pytest.fixture(autouse=True)
def browser(request):
    if any(keyword in request.node.keywords for keyword in ui_keywords):
        with sync_playwright() as pw:
            browser = pw.chromium.launch(headless=False)
            yield browser
            browser.close()
    elif any(keyword in request.node.keywords for keyword in api_keywords):
        yield None
    else:
        yield None

@pytest.fixture(autouse=True)
def page(browser, request):
    if any(keyword in request.node.keywords for keyword in ui_keywords):
        context = browser.new_context()
        page = context.new_page()
        yield page
        context.close()
    elif any(keyword in request.node.keywords for keyword in api_keywords):
        yield None
    else:
        yield None

@pytest.fixture(autouse=True)
def before_each_after_each(page, request):
    if 'ui_baidu' in request.node.keywords:
        page.goto("http://www.baidu.com")
        yield page

    elif 'ui_douban' in request.node.keywords:
        page.goto("http://www.douban.com")
        yield page

    elif any(keyword in request.node.keywords for keyword in api_keywords):
        yield None

    else:
        yield None

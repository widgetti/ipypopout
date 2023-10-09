import playwright.sync_api
from IPython.display import display
import ipypopout
import queue

def test_popout(
    ipywidgets_runner, page_session: playwright.sync_api.Page, context_session: playwright.sync_api.BrowserContext,assert_solara_snapshot
):
    def kernel_code():
        import ipyvuetify as v
        import ipypopout

        container = v.Container(
            children=[],
        )

        button = ipypopout.PopoutButton(
            target=container,
        )
        text = v.Html(tag="div", children=["Test ipypopout"])
        container.children = [button, text]
        display(container)

    ipywidgets_runner(kernel_code)
    with context_session.expect_page() as new_page_info:
        page_session.locator("_vue=v-btn[icon]").click()
    new_page = new_page_info.value
    new_page.locator("text=Test ipypopout").wait_for()
    # the button should not be on the page
    new_page.locator("_vue=v-btn").wait_for(state="detached")
    new_page.close()

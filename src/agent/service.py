from src.agent.views import AgentActionResult, AgentActions, AgentPageState
from src.browser.service import BrowserService


class AgentService:
	"""
	Agent service that interacts with the browser.

	Right now this is just a LLM friendly wrapper around the browser service.
	In the future we can add the functionality that this is a self-contained agent that can plan and act single steps.

	TODO: easy hanging fruit: pass in a list of actions, compare html that changed and self assess if goal is done -> makes clicking MUCH MUCH faster and cheaper.

	TODO#2: from the state generate functions that can be passed directly into the LLM as function calls. Then it could actually in the same call request for example multiple actions and new state.
	"""

	def __init__(self):
		self.browser = BrowserService()

	def get_current_state(self, screenshot: bool = False) -> AgentPageState:
		browser_state = self.browser.get_updated_state()
		screenshot_b64 = None
		if screenshot:
			screenshot_b64 = self.browser.take_screenshot()

		return AgentPageState(
			items=browser_state.items,
			url=browser_state.url,
			title=browser_state.title,
			selector_map=browser_state.selector_map,
			screenshot=screenshot_b64,
		)

	def act(self, action: AgentActions) -> AgentActionResult:
		try:
			if action.search_google:
				self.browser.search_google(action.search_google.query)
			elif action.go_to_url:
				self.browser.go_to_url(action.go_to_url.url)
			elif action.nothing:
				# self.browser.nothing()
				# TODO: implement
				pass
			elif action.go_back:
				self.browser.go_back()
			elif action.done:
				return AgentActionResult(done=True)
			elif action.click_element:
				self.browser.click_element_by_index(action.click_element.id)
			elif action.input_text:
				self.browser.input_text_by_index(action.input_text.id, action.input_text.text)
			elif action.extract_page_content:
				content = self.browser.extract_page_content()
				return AgentActionResult(done=False, extracted_content=content)
			else:
				return AgentActionResult(done=False)

		except Exception as e:
			return AgentActionResult(done=False, error=str(e))

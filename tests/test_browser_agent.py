import pytest
from unittest.mock import patch, AsyncMock, MagicMock
from ai_agents.browser_agent import BrowserAgent

@pytest.mark.asyncio
@patch('ai_agents.browser_agent.async_playwright')
@patch('ai_agents.browser_agent.BeautifulSoup')
async def test_fetch_text_happy_path(mock_bs, mock_playwright):
    # Arrange
    mock_browser = AsyncMock()
    mock_page = AsyncMock()
    mock_page.content.return_value = '<html><body><p>Hello</p></body></html>'
    mock_browser.new_page.return_value = mock_page
    mock_playwright.return_value.__aenter__.return_value.chromium.launch.return_value = mock_browser
    mock_bs.return_value.get_text.return_value = 'Hello'
    agent = BrowserAgent()
    # Act
    result = await agent.fetch_text('http://example.com')
    # Assert
    assert result == 'Hello'

@pytest.mark.asyncio
@patch('ai_agents.browser_agent.async_playwright')
async def test_fetch_text_failure(mock_playwright):
    # Arrange
    mock_playwright.side_effect = Exception('Browser error')
    agent = BrowserAgent()
    # Act
    result = await agent.fetch_text('http://example.com')
    # Assert
    assert result is None 
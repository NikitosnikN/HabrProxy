import httpx
from sanic import Sanic, response

from proceed_page import proceed_page

app = Sanic(
    'habr_proxy',
)


async def get_page(url: str) -> str:
    async with httpx.AsyncClient() as session:
        resp = await session.get(url)
    return proceed_page(resp.text)


@app.get('<path:[^/].*?>')
async def main(request, path):
    html_page = await get_page(f'https://habr.com/{path}/')
    return response.html(html_page)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)

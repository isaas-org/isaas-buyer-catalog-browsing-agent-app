import httpx
from mcp.server.mcpserver import MCPServer

from isaas_buyer_catalog_agent.backend import BackendClient
from isaas_buyer_catalog_agent.config import load_settings


def build_server(backend: BackendClient) -> MCPServer:
    server = MCPServer(
        name="isaas-buyer-catalog",
        instructions="Tools for browsing the iSaaS SaaS catalog on behalf of a buyer company.",
    )

    @server.tool()
    async def backend_health() -> dict[str, str]:
        """Report whether the iSaaS buyer catalog backend is reachable."""
        try:
            body = await backend.health()
        except httpx.HTTPError as err:
            return {"status": "UNREACHABLE", "detail": str(err)}
        return {"status": str(body.get("status", "UNKNOWN"))}

    return server


def main() -> None:
    settings = load_settings()
    server = build_server(BackendClient(settings.backend_api_url, settings.backend_api_key))
    if settings.transport == "stdio":
        server.run("stdio")
    else:
        server.run("streamable-http", host=settings.host, port=settings.port)


if __name__ == "__main__":
    main()

from mcp.server.mcpserver import MCPServer

from isaas_buyer_catalog_agent.backend import BackendClient
from isaas_buyer_catalog_agent.config import load_settings
from isaas_buyer_catalog_agent.tools.mcp_health_check import HealthCheckTools


def build_server(backend: BackendClient) -> MCPServer:
    server = MCPServer(
        name="isaas-buyer-catalog",
        instructions="Tools for browsing the iSaaS SaaS catalog on behalf of a buyer company.",
    )
    HealthCheckTools(backend).register(server)
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
